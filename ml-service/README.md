# NHANES Cardiovascular Risk ML Service (TabPFN)

FastAPI prediction and training service for the cardiovascular risk stratification project. The primary model is **TabPFN** (`TabPFNClassifier`); an optional bundled scikit-learn fallback can be loaded when the TabPFN artifact is unavailable.

> Research/educational prototype only. Not a validated medical device or a substitute for clinician assessment.

## Install (Windows PowerShell)

```powershell
cd ml-service
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Train

From the `ml-service` directory:

```powershell
python src/train.py --data_path data/nhanes_cvd_crp_combined_harmonized.csv
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/train.py --data_path data/nhanes_cvd_crp_combined_harmonized.csv
```

Training creates the TabPFN model and preprocessor under `models/` and evaluation artifacts under `outputs/`. The script limits TabPFN fitting to up to 1,000 training rows for runtime practicality.

## Start API

```powershell
python -m uvicorn app:app --host 127.0.0.1 --port 8000
```

Or Linux/macOS:

```bash
python -m uvicorn app:app --host 127.0.0.1 --port 8000
```

- Health: http://localhost:8000/health
- Swagger docs: http://localhost:8000/docs
- Prediction: `POST /predict`

## Input features

The API expects age, sex, BMI, systolic/diastolic BP, total/HDL/LDL cholesterol, triglycerides, fasting glucose, HbA1c, CRP, smoker, and diabetes. The optional compatibility fields `hypertensionTreated`, `familyHistoryCvd`, and `physicalActivityScore` are accepted but not used by the current training feature set.

## Risk tiers

The project's probability bands are Low `<7.5%`, Moderate `7.5%–20%`, and High `>20%`. For Moderate base-tier cases only, hs-CRP below 1 mg/L shifts the tier to Low, and above 3 mg/L shifts it to High. These are simplified project rules and require clinical validation.

Check `/health` to confirm whether `modelType` is `tabpfn` or `sklearn-fallback`.

