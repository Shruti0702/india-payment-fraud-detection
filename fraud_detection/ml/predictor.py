"""Runtime fraud prediction service."""

from __future__ import annotations

from pathlib import Path

import joblib
import numpy as np
from django.conf import settings

from .features import features_dict_to_vector, row_to_features
from .train import FraudDetectionModel


class FraudPredictor:
    def __init__(self, model_path: Path | None = None) -> None:
        self.model_path = model_path or settings.ML_MODEL_PATH
        self._model: FraudDetectionModel | None = None

    @property
    def model(self) -> FraudDetectionModel:
        if self._model is None:
            if not self.model_path.exists():
                raise FileNotFoundError(
                    f"Model not found at {self.model_path}. Run: python manage.py train_model"
                )
            self._model = joblib.load(self.model_path)
        return self._model

    def score_transaction(self, transaction: dict, threshold: float = 0.5) -> dict:
        features = row_to_features(transaction)
        vector = features_dict_to_vector(features).reshape(1, -1)
        fraud_probability = float(self.model.predict_proba(vector)[0])
        is_fraud = fraud_probability >= threshold
        risk_level = self._risk_level(fraud_probability)
        explanations = self.model.explain_risk_factors(features)

        return {
            "fraud_probability": round(fraud_probability, 4),
            "is_fraud": bool(is_fraud),
            "risk_level": risk_level,
            "risk_factors": explanations,
            "features_used": len(features),
            "model_metrics": self.model.metrics,
        }

    @staticmethod
    def _risk_level(probability: float) -> str:
        if probability >= 0.8:
            return "CRITICAL"
        if probability >= 0.6:
            return "HIGH"
        if probability >= 0.4:
            return "MEDIUM"
        if probability >= 0.2:
            return "LOW"
        return "MINIMAL"


_predictor: FraudPredictor | None = None


def get_predictor() -> FraudPredictor:
    global _predictor
    if _predictor is None:
        _predictor = FraudPredictor()
    return _predictor
