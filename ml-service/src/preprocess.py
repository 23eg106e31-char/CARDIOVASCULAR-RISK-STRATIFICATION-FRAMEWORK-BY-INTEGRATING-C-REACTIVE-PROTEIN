"""Preprocessing for the supplied NHANES CVD/CRP dataset."""
import os
import joblib
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

CONTINUOUS_COLS = [
    "age", "bmi", "systolic_bp", "diastolic_bp", "total_cholesterol",
    "hdl", "ldl", "triglycerides", "glucose", "hba1c", "hs_crp",
]
BINARY_COLS = ["sex", "smoker", "diabetes"]
TARGET_COL = "major_cvd_target"

class CVRiskPreprocessor:
    def __init__(self):
        self.scaler = StandardScaler()
        self.imputer = SimpleImputer(strategy="median")
        self.feature_names_ = CONTINUOUS_COLS + BINARY_COLS
        self.fitted = False

    def _engineer(self, df):
        df = df.copy()
        # Harmonize categorical fields from the supplied NHANES file.
        if "sex" in df:
            if df["sex"].dtype == object:
                df["sex"] = df["sex"].map({"Female": 0, "Male": 1}).fillna(pd.to_numeric(df["sex"], errors="coerce"))
        if "smoking_status" in df:
            df["smoker"] = df["smoking_status"].map({"Never": 0, "Former": 0, "Current": 1})
        if "smoker" not in df:
            df["smoker"] = np.nan
        if "diabetes_status" in df:
            df["diabetes"] = df["diabetes_status"].map({"No": 0, "Yes": 1})
        if "diabetes" not in df:
            df["diabetes"] = np.nan
        for col in CONTINUOUS_COLS:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        for col in BINARY_COLS:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        return df

    def fit_transform(self, df):
        df = self._engineer(df)
        X_cont = self.scaler.fit_transform(self.imputer.fit_transform(df[CONTINUOUS_COLS]))
        X_bin = df[BINARY_COLS].fillna(0).values.astype(float)
        X = np.hstack([X_cont, X_bin]).astype(np.float32)
        self.fitted = True
        y = df[TARGET_COL].astype(int).values if TARGET_COL in df.columns else None
        return X, y

    def transform(self, df):
        if not self.fitted:
            raise RuntimeError("Preprocessor must be fit before transform().")
        df = self._engineer(df)
        X_cont = self.scaler.transform(self.imputer.transform(df[CONTINUOUS_COLS]))
        X_bin = df[BINARY_COLS].fillna(0).values.astype(float)
        return np.hstack([X_cont, X_bin]).astype(np.float32)

    def save(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        joblib.dump(self, path)

    @staticmethod
    def load(path):
        return joblib.load(path)
