"""CLI prediction helper for the NHANES-trained TabPFN model."""
import argparse, json, sys, os, pandas as pd
import joblib

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.preprocess import CVRiskPreprocessor

p = argparse.ArgumentParser()
p.add_argument('--input_csv', required=True)
p.add_argument('--model_dir', default='models')
a = p.parse_args()

pre = CVRiskPreprocessor.load(os.path.join(a.model_dir, 'preprocessor.joblib'))
model_path = os.path.join(a.model_dir, 'tabpfn_cv_risk.joblib')
if not os.path.exists(model_path):
    model_path = os.path.join(a.model_dir, 'fallback_model.joblib')

model = joblib.load(model_path)
df = pd.read_csv(a.input_csv)
X = pre.transform(df)
probs = model.predict_proba(X)[:, 1]
print(json.dumps({'predicted_probability': probs.tolist()}))
