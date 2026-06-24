"""Train and persist the fraud detection model."""

from __future__ import annotations

from pathlib import Path

import joblib
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier, IsolationForest
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from .data_generator import generate_dataset
from .features import FEATURE_COLUMNS, dataframe_to_matrix


class FraudDetectionModel:
    """Hybrid ensemble: supervised GBM + unsupervised anomaly scoring."""

    def __init__(self) -> None:
        self.supervised = Pipeline(
            [
                ("scaler", StandardScaler()),
                (
                    "classifier",
                    GradientBoostingClassifier(
                        n_estimators=200,
                        learning_rate=0.08,
                        max_depth=4,
                        random_state=42,
                    ),
                ),
            ]
        )
        self.anomaly = IsolationForest(
            n_estimators=150,
            contamination=0.08,
            random_state=42,
        )
        self.feature_columns = FEATURE_COLUMNS
        self.metrics: dict[str, float] = {}

    def fit(self, X: np.ndarray, y: np.ndarray) -> dict[str, float]:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        self.supervised.fit(X_train, y_train)
        self.anomaly.fit(X_train)

        proba = self.supervised.predict_proba(X_test)[:, 1]
        preds = (proba >= 0.5).astype(int)
        anomaly_scores = -self.anomaly.decision_function(X_test)
        anomaly_norm = (anomaly_scores - anomaly_scores.min()) / (
            anomaly_scores.max() - anomaly_scores.min() + 1e-9
        )
        hybrid_proba = 0.7 * proba + 0.3 * anomaly_norm
        hybrid_preds = (hybrid_proba >= 0.5).astype(int)

        self.metrics = {
            "precision": float(precision_score(y_test, hybrid_preds, zero_division=0)),
            "recall": float(recall_score(y_test, hybrid_preds, zero_division=0)),
            "f1": float(f1_score(y_test, hybrid_preds, zero_division=0)),
            "roc_auc": float(roc_auc_score(y_test, hybrid_proba)),
            "confusion_matrix": confusion_matrix(y_test, hybrid_preds).tolist(),
            "classification_report": classification_report(y_test, hybrid_preds, zero_division=0),
            "train_samples": int(len(X_train)),
            "test_samples": int(len(X_test)),
        }
        return self.metrics

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        proba = self.supervised.predict_proba(X)[:, 1]
        anomaly_scores = -self.anomaly.decision_function(X)
        anomaly_norm = (anomaly_scores - anomaly_scores.min()) / (
            anomaly_scores.max() - anomaly_scores.min() + 1e-9
        )
        return 0.7 * proba + 0.3 * anomaly_norm

    def predict(self, X: np.ndarray, threshold: float = 0.5) -> np.ndarray:
        return (self.predict_proba(X) >= threshold).astype(int)

    def explain_risk_factors(self, features: dict[str, float]) -> list[dict]:
        """Rule-based explanations aligned with RBI fraud typologies."""
        explanations = []
        if features.get("new_beneficiary"):
            explanations.append(
                {"factor": "New beneficiary", "severity": "high", "detail": "First-time payee — common in UPI mule accounts"}
            )
        if features.get("high_velocity"):
            explanations.append(
                {"factor": "Transaction velocity", "severity": "high", "detail": "Multiple transactions within 1 hour"}
            )
        if features.get("odd_hour"):
            explanations.append(
                {"factor": "Odd-hour activity", "severity": "medium", "detail": "Transaction outside typical banking hours (IST)"}
            )
        if features.get("amount_inr", 0) > 50000:
            explanations.append(
                {"factor": "High value", "severity": "medium", "detail": "Amount exceeds ₹50,000 threshold"}
            )
        if features.get("geo_mismatch") or features.get("distance_km", 0) > 300:
            explanations.append(
                {"factor": "Geographic anomaly", "severity": "high", "detail": "Payer-beneficiary distance inconsistent with history"}
            )
        if features.get("vpn_detected"):
            explanations.append(
                {"factor": "VPN / proxy", "severity": "high", "detail": "Device routed through anonymising network"}
            )
        if features.get("merchant_risk_score", 0) > 0.6:
            explanations.append(
                {"factor": "High-risk merchant", "severity": "medium", "detail": "Merchant category flagged under NPCI risk taxonomy"}
            )
        if features.get("account_age_days", 999) < 90:
            explanations.append(
                {"factor": "Young account", "severity": "medium", "detail": "Account age under 90 days"}
            )
        return explanations


def train_and_save(model_path: Path, n_samples: int = 12000) -> dict:
    df = generate_dataset(n_samples=n_samples)
    X = dataframe_to_matrix(df)
    y = df["is_fraud"].values

    model = FraudDetectionModel()
    metrics = model.fit(X, y)

    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, model_path)
    return metrics
