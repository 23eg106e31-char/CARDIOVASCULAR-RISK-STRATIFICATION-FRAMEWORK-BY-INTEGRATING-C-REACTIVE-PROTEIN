<<<<<<< HEAD
=======
# CARDIOVASCULAR-RISK-STRATIFICATION-FRAMEWORK-BY-INTEGRATING-C-REACTIVE-PROTEIN
>>>>>>> 0c2399fd834c6f7849bdb5157d7848408452662f
# Cardiovascular Risk Stratification Framework — NHANES + TabPFN

A full-stack research/educational application for cardiovascular risk stratification using **NHANES data**, a **TabPFN** tabular model, a FastAPI ML service, a Spring Boot API, and a React + Vite interface.

> **Important medical notice:** This project is a research and educational prototype, not a validated clinical decision-support device. Its probability estimates and Low/Moderate/High labels must not be used to diagnose, treat, or make care decisions. The risk thresholds and hs-CRP modifier are simplified project rules and are not a substitute for a clinician's assessment or a validated clinical risk calculator.

## Project goals

- Accept patient risk-factor inputs through a web interface.
- Estimate the model's probability for the dataset target (`major_cvd_target`).
- Map that probability to Low, Moderate, or High base risk.
- Apply the project's hs-CRP modifier to Moderate-risk cases.
- Show the result and store assessment history through the backend.

## Architecture

```text
React + Vite (localhost:5173)
        |
        | /api (Vite proxy)
        v
Spring Boot REST API + H2 (localhost:8080)
        |
        | ML service URL: http://localhost:8000
        v
FastAPI + TabPFN / sklearn fallback (localhost:8000)
        |
        v
NHANES harmonized dataset + model/preprocessor artifacts
```

### Main folders

| Path | Purpose |
|---|---|
| `frontend/` | React UI, patient form, risk result, assessment history |
| `backend/` | Spring Boot API, H2 persistence, ML-service client |
| `ml-service/` | FastAPI prediction endpoint, preprocessing, training, stratification |
| `ml-service/data/` | NHANES CVD/CRP harmonized CSV and data-generation helper |
| `ml-service/models/` | Model and preprocessing artifacts, model metadata |
| `ml-service/src/` | Training, model, preprocessing, evaluation, risk-tier logic |

## Requirements

Install these before running:

- **Python 3.10+** (use a Python version supported by the installed TabPFN release)
- **Java 17**
- **Maven 3.8+**
- **Node.js 18+ and npm**
- Internet access for the first dependency installation

Check versions:

```bash
python --version
java -version
mvn -version
node --version
npm --version
```

## Run locally (Windows PowerShell)

Open **three separate terminals** from the extracted project folder.

### 1. ML service

```powershell
cd ml-service
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If the pre-trained artifacts are not present, train the model:

```powershell
python src/train.py --data_path data/nhanes_cvd_crp_combined_harmonized.csv
```

Start the API:

```powershell
python -m uvicorn app:app --host 127.0.0.1 --port 8000
```

Keep this terminal running. API docs: http://localhost:8000/docs  
Health check: http://localhost:8000/health

### 2. Spring Boot backend

In a second terminal, from the project root:

```powershell
cd backend
mvn spring-boot:run
```

Backend: http://localhost:8080  
H2 console (if enabled): http://localhost:8080/h2-console

The backend is configured to call the ML service at `http://localhost:8000`. If your ML service uses a different address, update `ml.service.base-url` in `backend/src/main/resources/application.properties`.

### 3. React frontend

In a third terminal, from the project root:

```powershell
cd frontend
npm install
npm run dev
```

Open the Vite URL printed in the terminal, normally http://localhost:5173.

## Run locally (Linux / macOS)

### ML service

```bash
cd ml-service
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt

# Train only if the model/preprocessor artifacts are missing:
python src/train.py --data_path data/nhanes_cvd_crp_combined_harmonized.csv

python -m uvicorn app:app --host 127.0.0.1 --port 8000
```

The repository also includes `run-ml-linux.sh` as a convenience script for Linux. It creates a virtual environment, installs requirements, trains if the preprocessor is missing, and starts Uvicorn.

### Backend and frontend

In separate terminals:

```bash
cd backend
mvn spring-boot:run
```

```bash
cd frontend
npm install
npm run dev
```

## Model and data

- **Model:** TabPFN (`TabPFNClassifier`) when the trained TabPFN artifact is available.
- **Fallback:** bundled scikit-learn model when TabPFN artifact is unavailable. Check `/health` for `modelType` and `modelLoaded`; the fallback is not TabPFN.
- **Dataset:** `ml-service/data/nhanes_cvd_crp_combined_harmonized.csv`.
- **Target:** `major_cvd_target`.
- **Input features:** age, sex, BMI, systolic/diastolic blood pressure, total/HDL/LDL cholesterol, triglycerides, glucose, HbA1c, hs-CRP, smoking, and diabetes.
- Additional compatibility fields (`hypertensionTreated`, `familyHistoryCvd`, and `physicalActivityScore`) are accepted by the ML request but are not part of the current selected model feature set.

Training writes model/preprocessor artifacts under `ml-service/models/` and evaluation outputs under `ml-service/outputs/` (including metrics/report/plots, depending on training completion). The training script uses a stratified train/test split and currently limits TabPFN fitting to at most 1,000 training rows for runtime practicality.

### Risk tier rules implemented

| Base tier | Model probability |
|---|---|
| Low | `< 7.5%` |
| Moderate | `7.5%–20%` inclusive |
| High | `> 20%` |

For **Moderate** base-risk cases only, the current code applies the following hs-CRP adjustment:

- hs-CRP `< 1 mg/L` → final Low
- hs-CRP `1–3 mg/L` → stays Moderate
- hs-CRP `> 3 mg/L` → final High

These are project-defined rules. They should be reviewed and clinically validated before any real-world use.

## API endpoints

### ML service (FastAPI)

- `GET /health` — service/model status and model type
- `POST /predict` — predict from patient risk-factor inputs

OpenAPI/Swagger UI: http://localhost:8000/docs

### Backend (Spring Boot)

The React app calls the backend through its `/api` base path. The backend exposes risk assessment and history routes used by the frontend:

- `POST /api/risk/assess` — create a risk assessment
- `GET /api/risk/history` — retrieve saved assessment history

Backend base URL: http://localhost:8080

## Troubleshooting

### `uvicorn` is not recognized / `No module named uvicorn`

Activate the ML virtual environment and install requirements:

```powershell
cd ml-service
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn app:app --host 127.0.0.1 --port 8000
```

Using `python -m uvicorn` avoids relying on the executable being on PATH.

### Port 8000 or 8080 is already in use

Stop the process already using the port, or change the port and update the backend's `ml.service.base-url` accordingly. Do not start duplicate ML/backend instances.

### Frontend cannot reach the backend

Confirm all three services are running. Check the Vite proxy configuration and backend URL. The frontend API helper uses `/api` by default.

### ML health says model is not loaded

Open http://localhost:8000/health. Confirm `ml-service/models/preprocessor.joblib` and either `tabpfn_cv_risk.joblib` or `fallback_model.joblib` exist. If artifacts are absent, activate the ML environment and run the training command. Training may take time and TabPFN may require compatible Python/package versions and sufficient memory.

### TabPFN installation or training errors

Use a clean virtual environment and a Python version supported by the installed TabPFN version. Install from `requirements.txt`, then review the complete terminal error. If TabPFN cannot train but fallback artifacts exist, the service may load the sklearn fallback; verify `modelType` on `/health`.

## Reproducibility and responsible use

- Keep the original dataset and its source/usage terms with the project.
- Record Python and package versions when reporting model metrics.
- Do not interpret training metrics as clinical validation.
- Protect patient data; use synthetic or de-identified inputs for demonstrations.
- Do not expose the local services publicly without authentication, access controls, secure transport, and a privacy review.

## License and attribution

No license is specified in this project package. Add an appropriate license and dataset attribution before redistributing the repository publicly. NHANES data have their own terms and documentation; consult the source dataset documentation.

## Authors / project

**Project:** Cardiovascular Risk Stratification Framework  
**Dataset:** NHANES CVD/CRP harmonized dataset  
**Primary model:** TabPFN  
**Application stack:** React, Vite, Spring Boot, H2, FastAPI, Python
