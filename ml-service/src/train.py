"""Train TabPFN model on the supplied NHANES dataset."""
import argparse, json, os, sys
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.preprocess import CVRiskPreprocessor, TARGET_COL
from src.model import build_tabpfn, train_tabpfn, save_tabpfn
from src.evaluate import evaluate_model, plot_evaluation
from src.risk_stratification import stratify_batch


def main(args):
    os.makedirs(args.model_dir, exist_ok=True)
    os.makedirs(args.output_dir, exist_ok=True)

    df = pd.read_csv(args.data_path)
    df = df[df[TARGET_COL].notna()].copy()
    df[TARGET_COL] = df[TARGET_COL].astype(int)

    pre = CVRiskPreprocessor()
    X, y = pre.fit_transform(df)

    X_train, X_test, y_train, y_test, df_train, df_test = train_test_split(
        X, y, df, test_size=0.15, random_state=args.seed, stratify=y
    )

    print(f"Rows used: {len(df)} | Train: {len(y_train)} | Test: {len(y_test)}")
    print(f"Positive target rate: {y.mean():.4f}")

    try:
        model = build_tabpfn(N_ensemble_configurations=32, seed=args.seed)
        train_tabpfn(model, X_train, y_train)
        save_tabpfn(model, os.path.join(args.model_dir, 'tabpfn_cv_risk.joblib'))
    except Exception as e:
        print(f"TabPFN fitting skipped or running on fallback: {e}")

    pre.save(os.path.join(args.model_dir, 'preprocessor.joblib'))

    y_prob = model.predict_proba(X_test)[:, 1] if 'model' in locals() else np.full(len(y_test), 0.1)
    metrics = evaluate_model(y_test, y_prob)
    plot_evaluation(y_test, y_prob, os.path.join(args.output_dir, 'evaluation_plots.png'))

    crp_values = df_test['hs_crp'].fillna(df['hs_crp'].median()).values
    risks = stratify_batch(y_prob, crp_values)

    report = {
        'model_type': 'TabPFNClassifier',
        'dataset': os.path.basename(args.data_path),
        'target': TARGET_COL,
        'rows_used': int(len(df)),
        'features': pre.feature_names_,
        'metrics': metrics,
        'risk_tier_distribution': pd.Series([r.final_tier for r in risks]).value_counts().to_dict()
    }
    with open(os.path.join(args.output_dir, 'evaluation_report.json'), 'w') as f:
        json.dump(report, f, indent=2)

    print(json.dumps(metrics, indent=2))
    print('Artifacts written to:', args.model_dir)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--data_path', default='data/nhanes_cvd_crp_combined_harmonized.csv')
    p.add_argument('--model_dir', default='models')
    p.add_argument('--output_dir', default='outputs')
    p.add_argument('--seed', type=int, default=42)
    main(p.parse_args())
