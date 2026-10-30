# Cardiovascular Risk Stratification with TabNet + CRP

**Objective 2:** Develop a clinically interpretable cardiovascular risk
stratification system categorizing individuals into **Low / Moderate /
High** risk groups, based on AI/ML model outputs that integrate
**C-reactive protein (CRP)** with standard clinical risk factors.

## Why TabNet

TabNet (Arik & Pfister, 2019) is an attention-based deep learning model
built for tabular data that produces **instance-wise feature masks** —
i.e., for every single patient, it exposes *which features drove that
specific prediction*. This gives built-in local interpretability
(clinician can see "this patient's risk was driven by CRP + systolic BP
+ smoking") without bolting on a separate explainer, plus global feature
importance for the whole model. That directly serves the "clinically
interpretable" part of the objective.

## Project structure

```
cv-risk-tabnet/
├── data/
│   └── generate_synthetic_data.py   # synthetic dataset generator (swap for real data)
├── src/
│   ├── preprocess.py                # imputation, scaling, CRP log-transform
│   ├── model.py                     # TabNet build/train/explain wrappers
│   ├── evaluate.py                  # AUROC/AUPRC/Brier/confusion-matrix + plots
│   ├── risk_stratification.py       # probability -> Low/Moderate/High + CRP modifier
│   ├── train.py                     # end-to-end training pipeline
│   └── predict.py                   # score new patients -> risk tiers + explanations
├── models/                          # saved model + preprocessor (created after training)
├── outputs/                         # metrics, plots, prediction CSVs
├── requirements.txt
└── README.md
```

## Setup

```bash
pip install -r requirements.txt
```

## Step 1 — Generate (or supply) data

If you don't yet have a real clinical dataset, generate a synthetic one
that mimics realistic distributions of age, blood pressure, lipid panel,
glucose/HbA1c, CRP, and standard binary risk factors, with a simulated
10-year cardiovascular event outcome:

```bash
python data/generate_synthetic_data.py --n_samples 5000 --out data/cv_risk_synthetic.csv
```

To use **your own dataset**, produce a CSV with these columns and skip
this step:

```
age, sex, bmi, systolic_bp, diastolic_bp, total_cholesterol,
hdl_cholesterol, ldl_cholesterol, triglycerides, fasting_glucose,
hba1c, crp, smoker, diabetes, hypertension_treated,
family_history_cvd, physical_activity_score, event_10yr
```
(`sex`: 0=female/1=male; binary columns: 0/1; `event_10yr` is the label —
1 if the patient had a cardiovascular event within the follow-up window.)

## Step 2 — Train

```bash
python src/train.py --data_path data/cv_risk_synthetic.csv
```

This will:
1. Preprocess features (median imputation, standard scaling, log-transform CRP)
2. Split into train/validation/test (70/15/15, stratified)
3. Train TabNet with early stopping on validation AUC
4. Evaluate on the held-out test set (AUROC, AUPRC, Brier score, confusion matrix)
5. Apply the risk stratification layer and report the Low/Moderate/High
   distribution on the test set
6. Save `models/tabnet_cv_risk.zip`, `models/preprocessor.joblib`,
   `outputs/evaluation_report.json`, `outputs/evaluation_plots.png`

## Step 3 — Score new patients

```bash
python src/predict.py --input data/new_patients.csv --output outputs/predictions.csv
```

Output columns include `predicted_probability`, `base_tier`,
`crp_category`, `crp_modifier_applied`, `final_tier`, and `top_features`
(the top 5 features driving that individual's prediction, from TabNet's
local attention mask).

## Risk stratification logic

1. **Base tier** from TabNet's predicted 10-year event probability,
   using ACC/AHA-style pooled-cohort bands:
   - Low: probability < 7.5%
   - Moderate: 7.5% – 20%
   - High: probability > 20%
2. **CRP modifier** (AHA/CDC CRP categories: Low <1 mg/L, Average
   1–3 mg/L, High >3 mg/L) refines patients who land in the *Moderate*
   band only — a high CRP nudges them to High, a low CRP nudges them to
   Low. This mirrors how CRP is used clinically as a refinement marker
   for borderline-risk patients, rather than overriding a clearly
   low- or high-probability model output.
3. Every classification is returned with the probability, both tiers,
   the CRP category, whether the modifier fired, and the top
   contributing features — so the output is auditable, not a black box.

## Notes / next steps for your report

- The bundled dataset generator is **synthetic** (for pipeline testing
  only) — swap in your real clinical cohort data before drawing
  conclusions. The synthetic event probability model is a simplified
  logistic function and not a validated clinical risk equation.
- Suggested extensions: calibration curves + Platt/ isotonic
  recalibration, external validation cohort, SHAP as a secondary
  interpretability cross-check against TabNet's native masks,
  sensitivity analysis on the probability-band thresholds.
- This tool is for research/educational purposes and is **not** a
  validated clinical decision-support device.
