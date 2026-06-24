"""Feature engineering for Indian digital payment fraud detection."""

from __future__ import annotations

import numpy as np
import pandas as pd

PAYMENT_CHANNELS = ["UPI", "IMPS", "NEFT", "RTGS", "CARD", "WALLET"]
INDIAN_STATES = [
    "Maharashtra", "Karnataka", "Delhi", "Tamil Nadu", "Gujarat",
    "Uttar Pradesh", "West Bengal", "Telangana", "Rajasthan", "Kerala",
]
DEVICE_TYPES = ["ANDROID", "IOS", "WEB", "USSD"]
RISK_FLAGS = [
    "new_beneficiary",
    "high_velocity",
    "odd_hour",
    "geo_mismatch",
    "vpn_detected",
    "first_large_txn",
]

FEATURE_COLUMNS = [
    "amount_inr",
    "hour_of_day",
    "day_of_week",
    "is_weekend",
    "channel_upi",
    "channel_imps",
    "channel_neft",
    "channel_rtgs",
    "channel_card",
    "channel_wallet",
    "device_android",
    "device_ios",
    "device_web",
    "device_ussd",
    "merchant_risk_score",
    "account_age_days",
    "txn_velocity_1h",
    "beneficiary_age_days",
    "distance_km",
    "new_beneficiary",
    "high_velocity",
    "odd_hour",
    "geo_mismatch",
    "vpn_detected",
    "first_large_txn",
]


def _one_hot(value: str, categories: list[str], prefix: str) -> dict[str, float]:
    return {f"{prefix}_{cat.lower()}": float(value == cat) for cat in categories}


def row_to_features(row: dict) -> dict[str, float]:
    """Convert a transaction dict into model-ready numeric features."""
    channel = row.get("payment_channel", "UPI").upper()
    device = row.get("device_type", "ANDROID").upper()
    amount = float(row.get("amount_inr", 0))
    hour = int(row.get("hour_of_day", 12))
    day = int(row.get("day_of_week", 2))

    features = {
        "amount_inr": amount,
        "hour_of_day": hour,
        "day_of_week": day,
        "is_weekend": float(day >= 5),
        "merchant_risk_score": float(row.get("merchant_risk_score", 0.2)),
        "account_age_days": float(row.get("account_age_days", 365)),
        "txn_velocity_1h": float(row.get("txn_velocity_1h", 1)),
        "beneficiary_age_days": float(row.get("beneficiary_age_days", 30)),
        "distance_km": float(row.get("distance_km", 5)),
    }
    features.update(_one_hot(channel, PAYMENT_CHANNELS, "channel"))
    features.update(_one_hot(device, DEVICE_TYPES, "device"))

    for flag in RISK_FLAGS:
        features[flag] = float(bool(row.get(flag, False)))

    return features


def dataframe_to_matrix(df: pd.DataFrame) -> np.ndarray:
    rows = [row_to_features(record) for record in df.to_dict(orient="records")]
    matrix = pd.DataFrame(rows, columns=FEATURE_COLUMNS)
    return matrix.values.astype(np.float64)


def features_dict_to_vector(features: dict[str, float]) -> np.ndarray:
    return np.array([features[col] for col in FEATURE_COLUMNS], dtype=np.float64)
