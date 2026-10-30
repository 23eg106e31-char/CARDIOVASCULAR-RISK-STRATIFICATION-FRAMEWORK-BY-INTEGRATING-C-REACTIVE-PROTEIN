#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/ml-service"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
if [ ! -f models/preprocessor.joblib ]; then
  python3 src/train.py --data_path data/nhanes_cvd_crp_combined_harmonized.csv
fi
uvicorn app:app --host 0.0.0.0 --port 8000
