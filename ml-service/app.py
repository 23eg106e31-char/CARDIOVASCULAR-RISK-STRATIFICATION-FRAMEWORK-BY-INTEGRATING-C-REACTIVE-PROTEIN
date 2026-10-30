from pathlib import Path
from typing import List
import sys, numpy as np, pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

try:
    from tabpfn import TabPFNClassifier
except Exception:
    TabPFNClassifier = None

from src.preprocess import CVRiskPreprocessor
from src.risk_stratification import stratify

TABPFN_MODEL_PATH = ROOT / "models" / "tabpfn_cv_risk.joblib"
FALLBACK_MODEL_PATH = ROOT / "models" / "fallback_model.joblib"
PREPROCESSOR_PATH = ROOT / "models" / "preprocessor.joblib"

app = FastAPI(title="CV Risk TabPFN ML Service", version="3.0.0")


class Patient(BaseModel):
    age: float = Field(..., ge=18, le=120)
    sex: int = Field(..., ge=0, le=1)
    bmi: float = Field(..., ge=10, le=80)
    systolicBp: float = Field(..., ge=70, le=260)
    diastolicBp: float = Field(..., ge=40, le=160)
    totalCholesterol: float = Field(..., ge=50, le=500)
    hdlCholesterol: float = Field(..., ge=10, le=150)
    ldlCholesterol: float = Field(..., ge=10, le=400)
    triglycerides: float = Field(..., ge=20, le=1000)
    fastingGlucose: float = Field(..., ge=40, le=500)
    hba1c: float = Field(..., ge=2, le=20)
    crp: float = Field(..., ge=0, le=100)
    smoker: int = Field(..., ge=0, le=1)
    diabetes: int = Field(..., ge=0, le=1)

    hypertensionTreated: int = Field(0, ge=0, le=1)
    familyHistoryCvd: int = Field(0, ge=0, le=1)
    physicalActivityScore: float = Field(0, ge=0, le=100)


class TopFeature(BaseModel):
    feature: str
    weight: float


class PredictionResponse(BaseModel):
    predictedProbability: float
    baseTier: str
    crpCategory: str
    crpModifierApplied: bool
    finalTier: str
    topFeatures: List[TopFeature]


_model = None
_pre = None
_model_type = None


def load_artifacts():
    global _model, _pre, _model_type

    if not PREPROCESSOR_PATH.exists():
        raise RuntimeError("Preprocessor artifact is missing. Expected ml-service/models/preprocessor.joblib.")

    _pre = CVRiskPreprocessor.load(str(PREPROCESSOR_PATH))

    if TABPFN_MODEL_PATH.exists():
        _model = joblib.load(str(TABPFN_MODEL_PATH))
        _model_type = "tabpfn"
    elif FALLBACK_MODEL_PATH.exists():
        _model = joblib.load(str(FALLBACK_MODEL_PATH))
        _model_type = "sklearn-fallback"
    else:
        raise RuntimeError("No trained ML model artifact found. Expected tabpfn_cv_risk.joblib or fallback_model.joblib.")


@app.on_event("startup")
def startup():
    try:
        load_artifacts()
        print(f"Model loaded: {_model_type}")
    except Exception as e:
        print("WARNING:", e)


@app.get("/health")
def health():
    return {
        "status": "up",
        "modelLoaded": _model is not None,
        "modelType": _model_type,
        "dataset": "NHANES CVD/CRP Harmonized",
        "target": "major_cvd_target",
    }


def _calculate_top_features(patient_dict, prob):
    """Generates feature weights based on clinical variable deviations."""
    features = [
        ("C-Reactive Protein (CRP)", min(0.35, max(0.05, patient_dict["crp"] / 10.0))),
        ("Systolic BP", min(0.30, max(0.05, (patient_dict["systolicBp"] - 110) / 100.0))),
        ("Age", min(0.25, max(0.05, patient_dict["age"] / 100.0))),
        ("HbA1c", min(0.20, max(0.05, (patient_dict["hba1c"] - 4.5) / 10.0))),
        ("Total Cholesterol", min(0.18, max(0.05, patient_dict["totalCholesterol"] / 300.0)))
    ]
    total = sum(w for _, w in features)
    return [TopFeature(feature=name, weight=round(w / total, 3)) for name, w in features]


@app.post("/predict", response_model=PredictionResponse)
def predict(patient: Patient):
    global _model, _pre

    if _model is None or _pre is None:
        try:
            load_artifacts()
        except Exception as e:
            raise HTTPException(status_code=503, detail=str(e))

    raw = patient.model_dump()
    row = {
        "age": raw["age"],
        "sex": raw["sex"],
        "bmi": raw["bmi"],
        "systolic_bp": raw["systolicBp"],
        "diastolic_bp": raw["diastolicBp"],
        "total_cholesterol": raw["totalCholesterol"],
        "hdl": raw["hdlCholesterol"],
        "ldl": raw["ldlCholesterol"],
        "triglycerides": raw["triglycerides"],
        "glucose": raw["fastingGlucose"],
        "hba1c": raw["hba1c"],
        "hs_crp": raw["crp"],
        "smoker": raw["smoker"],
        "diabetes": raw["diabetes"],
    }

    try:
        X = _pre.transform(pd.DataFrame([row]))
        probability = float(_model.predict_proba(X)[0, 1])
        probability = float(np.clip(probability, 0.0, 1.0))
        
        top = _calculate_top_features(raw, probability)

        result = stratify(
            probability,
            patient.crp,
            [(x.feature, x.weight) for x in top],
        )

        return PredictionResponse(
            predictedProbability=result.predicted_probability,
            baseTier=result.base_tier,
            crpCategory=result.crp_category,
            crpModifierApplied=result.crp_modifier_applied,
            finalTier=result.final_tier,
            topFeatures=top,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {type(e).__name__}: {e}")
