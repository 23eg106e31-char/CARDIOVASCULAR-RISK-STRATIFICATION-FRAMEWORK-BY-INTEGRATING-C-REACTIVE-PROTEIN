"""
Synthetic Cardiovascular Risk Dataset Generator
------------------------------------------------
Generates a realistic synthetic patient dataset combining CRP (C-reactive
protein) with standard clinical cardiovascular risk factors (roughly
following Framingham / ASCVD style variables), plus a simulated 10-year
cardiovascular event outcome used to derive risk labels.

Replace this with your real clinical dataset by producing a CSV with the
same column names (see COLUMNS below) and pointing train.py at it via
--data_path.
"""

import numpy as np
import pandas as pd
import argparse
import os

COLUMNS = [
    "age", "sex", "bmi", "systolic_bp", "diastolic_bp",
    "total_cholesterol", "hdl_cholesterol", "ldl_cholesterol",
    "triglycerides", "fasting_glucose", "hba1c", "crp",
    "smoker", "diabetes", "hypertension_treated", "family_history_cvd",
    "physical_activity_score", "event_10yr"
]


def generate_synthetic_dataset(n_samples: int = 5000, random_state: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(random_state)

    age = rng.normal(55, 12, n_samples).clip(25, 90)
    sex = rng.integers(0, 2, n_samples)  # 0=female, 1=male
    bmi = rng.normal(27, 5, n_samples).clip(15, 55)

    systolic_bp = (110 + 0.45 * (age - 40) + rng.normal(0, 12, n_samples)).clip(90, 210)
    diastolic_bp = (70 + 0.15 * (age - 40) + rng.normal(0, 8, n_samples)).clip(50, 130)

    total_cholesterol = rng.normal(200, 35, n_samples).clip(100, 350)
    hdl_cholesterol = (55 - 8 * sex + rng.normal(0, 12, n_samples)).clip(20, 100)
    ldl_cholesterol = (total_cholesterol - hdl_cholesterol - rng.normal(30, 10, n_samples)).clip(40, 250)
    triglycerides = rng.normal(140, 60, n_samples).clip(40, 500)

    fasting_glucose = rng.normal(95, 20, n_samples).clip(60, 300)
    hba1c = (5.0 + (fasting_glucose - 90) * 0.02 + rng.normal(0, 0.4, n_samples)).clip(4.0, 13.0)

    # CRP: log-normal, elevated with age, BMI, smoking (added after smoker is defined)
    smoker = rng.binomial(1, 0.20, n_samples)
    diabetes = (fasting_glucose > 126).astype(int)
    hypertension_treated = ((systolic_bp > 140) & (rng.random(n_samples) < 0.6)).astype(int)
    family_history_cvd = rng.binomial(1, 0.25, n_samples)
    physical_activity_score = rng.integers(0, 11, n_samples)  # 0 = sedentary, 10 = very active

    crp_base = np.exp(rng.normal(0.3, 0.7, n_samples))  # baseline log-normal ~1-3 mg/L
    crp = (crp_base
           + 0.02 * (bmi - 25).clip(min=0)
           + 0.8 * smoker
           + 0.01 * (age - 50).clip(min=0)
           + 0.5 * diabetes).clip(0.1, 30)

    # Latent 10-year CV risk score (log-odds), loosely inspired by ASCVD-style weighting
    logit = (
        -6.5
        + 0.065 * age
        + 0.45 * sex
        + 0.018 * (systolic_bp - 120).clip(min=0)
        + 0.30 * hypertension_treated
        + 0.010 * (total_cholesterol - 180)
        - 0.015 * (hdl_cholesterol - 50)
        + 0.55 * smoker
        + 0.60 * diabetes
        + 0.35 * family_history_cvd
        + 0.30 * np.log1p(crp)          # CRP contribution (inflammation pathway)
        - 0.04 * physical_activity_score
        + 0.02 * (bmi - 25).clip(min=0)
    )
    prob_event = 1 / (1 + np.exp(-logit))
    event_10yr = rng.binomial(1, prob_event)

    df = pd.DataFrame({
        "age": age.round(1),
        "sex": sex,
        "bmi": bmi.round(1),
        "systolic_bp": systolic_bp.round(0),
        "diastolic_bp": diastolic_bp.round(0),
        "total_cholesterol": total_cholesterol.round(0),
        "hdl_cholesterol": hdl_cholesterol.round(0),
        "ldl_cholesterol": ldl_cholesterol.round(0),
        "triglycerides": triglycerides.round(0),
        "fasting_glucose": fasting_glucose.round(0),
        "hba1c": hba1c.round(2),
        "crp": crp.round(2),
        "smoker": smoker,
        "diabetes": diabetes,
        "hypertension_treated": hypertension_treated,
        "family_history_cvd": family_history_cvd,
        "physical_activity_score": physical_activity_score,
        "event_10yr": event_10yr,
    })
    return df[COLUMNS]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate synthetic CV risk dataset")
    parser.add_argument("--n_samples", type=int, default=5000)
    parser.add_argument("--random_state", type=int, default=42)
    parser.add_argument("--out", type=str, default=os.path.join(os.path.dirname(__file__), "cv_risk_synthetic.csv"))
    args = parser.parse_args()

    df = generate_synthetic_dataset(args.n_samples, args.random_state)
    df.to_csv(args.out, index=False)
    print(f"Generated {len(df)} synthetic patient records -> {args.out}")
    print(f"Event rate: {df['event_10yr'].mean():.3f}")
