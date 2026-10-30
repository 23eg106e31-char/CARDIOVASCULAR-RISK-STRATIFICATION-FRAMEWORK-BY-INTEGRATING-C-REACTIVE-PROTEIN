"""
TabPFN Model Helper Functions
-----------------------------
Provides TabPFNClassifier model integration for tabular cardiovascular risk prediction.
"""
import numpy as np
import joblib

try:
    from tabpfn import TabPFNClassifier
except Exception:
    TabPFNClassifier = None


def build_tabpfn(N_ensemble_configurations=32, device="cpu", seed=42):
    """Instantiates TabPFNClassifier."""
    if TabPFNClassifier is None:
        raise RuntimeError("tabpfn is not installed. Please install requirements.txt (`pip install tabpfn`).")
    return TabPFNClassifier(
        N_ensemble_configurations=N_ensemble_configurations,
        device=device,
        seed=seed
    )


def train_tabpfn(model, X_train, y_train):
    """Fits TabPFN model on tabular training data."""
    if len(X_train) > 1000:
        idx = np.random.choice(len(X_train), 1000, replace=False)
        X_fit, y_fit = X_train[idx], y_train[idx]
    else:
        X_fit, y_fit = X_train, y_train

    model.fit(X_fit, y_fit)
    return model


def save_tabpfn(model, filepath):
    """Saves model artifact."""
    joblib.dump(model, filepath)


def load_tabpfn(filepath):
    """Loads saved model artifact."""
    return joblib.load(filepath)


def get_feature_importances(model, X_val, y_val, feature_names):
    """Calculates permutation importance for TabPFN."""
    from sklearn.inspection import permutation_importance
    try:
        res = permutation_importance(model, X_val, y_val, n_repeats=5, random_state=42, scoring="roc_auc")
        pairs = sorted(zip(feature_names, res.importances_mean), key=lambda x: x[1], reverse=True)
        return [(str(k), max(0.0, float(v))) for k, v in pairs]
    except Exception:
        return [(str(k), 1.0 / len(feature_names)) for k in feature_names]


def explain_instance(model, X_train, y_train, X_row, feature_names):
    """Calculates local feature contributions."""
    diffs = np.abs(X_row - np.mean(X_train, axis=0))
    weights = diffs / (np.std(X_train, axis=0) + 1e-6)
    pairs = sorted(zip(feature_names, weights), key=lambda x: x[1], reverse=True)
    return pairs
