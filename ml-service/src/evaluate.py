"""
Evaluation utilities: discrimination (AUROC, AUPRC), calibration,
and confusion-matrix-style summaries at a chosen operating threshold.
"""

import numpy as np
from sklearn.metrics import (
    roc_auc_score, average_precision_score, brier_score_loss,
    roc_curve, precision_recall_curve, confusion_matrix,
    accuracy_score, precision_score, recall_score, f1_score
)
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def evaluate_model(y_true, y_prob, threshold: float = 0.5) -> dict:
    y_pred = (y_prob >= threshold).astype(int)
    metrics = {
        "auroc": float(roc_auc_score(y_true, y_prob)),
        "auprc": float(average_precision_score(y_true, y_prob)),
        "brier_score": float(brier_score_loss(y_true, y_prob)),
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(precision_score(y_true, y_pred, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, zero_division=0)),
        "f1": float(f1_score(y_true, y_pred, zero_division=0)),
        "confusion_matrix": confusion_matrix(y_true, y_pred).tolist(),
        "operating_threshold": threshold,
    }
    return metrics


def plot_evaluation(y_true, y_prob, out_path: str):
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    # ROC curve
    fpr, tpr, _ = roc_curve(y_true, y_prob)
    auc = roc_auc_score(y_true, y_prob)
    axes[0].plot(fpr, tpr, label=f"AUROC = {auc:.3f}")
    axes[0].plot([0, 1], [0, 1], linestyle="--", color="gray")
    axes[0].set_xlabel("False Positive Rate")
    axes[0].set_ylabel("True Positive Rate")
    axes[0].set_title("ROC Curve")
    axes[0].legend()

    # Precision-Recall curve
    prec, rec, _ = precision_recall_curve(y_true, y_prob)
    auprc = average_precision_score(y_true, y_prob)
    axes[1].plot(rec, prec, label=f"AUPRC = {auprc:.3f}")
    axes[1].set_xlabel("Recall")
    axes[1].set_ylabel("Precision")
    axes[1].set_title("Precision-Recall Curve")
    axes[1].legend()

    # Predicted probability distribution by class (calibration proxy)
    axes[2].hist(y_prob[y_true == 0], bins=30, alpha=0.6, label="No event", density=True)
    axes[2].hist(y_prob[y_true == 1], bins=30, alpha=0.6, label="Event", density=True)
    axes[2].set_xlabel("Predicted probability")
    axes[2].set_ylabel("Density")
    axes[2].set_title("Predicted Probability Distribution")
    axes[2].legend()

    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close(fig)
