"""Synthetic Indian payment dataset generator for training and demos."""

from __future__ import annotations

import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

from .features import DEVICE_TYPES, INDIAN_STATES, PAYMENT_CHANNELS, RISK_FLAGS

RNG = np.random.default_rng(42)


def _random_timestamp() -> datetime:
    start = datetime(2024, 1, 1)
    offset = timedelta(days=int(RNG.integers(0, 400)), hours=int(RNG.integers(0, 24)))
    return start + offset


def generate_transaction(is_fraud: bool) -> dict:
    channel = RNG.choice(PAYMENT_CHANNELS, p=[0.45, 0.2, 0.1, 0.05, 0.15, 0.05])
    device = RNG.choice(DEVICE_TYPES, p=[0.55, 0.25, 0.15, 0.05])
    ts = _random_timestamp()

    if is_fraud:
        amount = float(RNG.choice([49999, 99999, 199999, 250000], p=[0.3, 0.3, 0.25, 0.15]))
        if RNG.random() < 0.4:
            amount = float(RNG.uniform(500, 5000))
        account_age = int(RNG.integers(1, 90))
        beneficiary_age = int(RNG.integers(0, 3))
        velocity = int(RNG.integers(5, 25))
        merchant_risk = float(RNG.uniform(0.6, 0.95))
        distance = float(RNG.uniform(200, 2500))
        flags = {flag: bool(RNG.random() < 0.55) for flag in RISK_FLAGS}
        if channel == "UPI":
            flags["new_beneficiary"] = True
    else:
        amount = float(RNG.lognormal(mean=7.5, sigma=1.0))
        amount = min(amount, 150000)
        account_age = int(RNG.integers(180, 2500))
        beneficiary_age = int(RNG.integers(30, 800))
        velocity = int(RNG.integers(0, 3))
        merchant_risk = float(RNG.uniform(0.05, 0.35))
        distance = float(RNG.uniform(0, 50))
        flags = {flag: bool(RNG.random() < 0.03) for flag in RISK_FLAGS}

    hour = ts.hour
    flags["odd_hour"] = flags.get("odd_hour", False) or hour < 5 or hour > 23
    flags["high_velocity"] = flags.get("high_velocity", False) or velocity >= 5
    flags["first_large_txn"] = flags.get("first_large_txn", False) or (
        amount > 50000 and account_age < 120
    )

    return {
        "transaction_id": f"TXN{RNG.integers(100000000, 999999999)}",
        "amount_inr": round(amount, 2),
        "payment_channel": channel,
        "device_type": device,
        "payer_state": RNG.choice(INDIAN_STATES),
        "beneficiary_state": RNG.choice(INDIAN_STATES),
        "merchant_category": RNG.choice(
            ["GROCERY", "FUEL", "ECOMMERCE", "UTILITY", "P2P", "GAMING", "CRYPTO"]
        ),
        "merchant_risk_score": round(merchant_risk, 3),
        "account_age_days": account_age,
        "beneficiary_age_days": beneficiary_age,
        "txn_velocity_1h": velocity,
        "distance_km": round(distance, 1),
        "hour_of_day": hour,
        "day_of_week": ts.weekday(),
        "timestamp": ts.isoformat(),
        "is_fraud": int(is_fraud),
        **flags,
    }


def generate_dataset(n_samples: int = 10000, fraud_rate: float = 0.08) -> pd.DataFrame:
    n_fraud = int(n_samples * fraud_rate)
    n_legit = n_samples - n_fraud
    records = [generate_transaction(False) for _ in range(n_legit)]
    records += [generate_transaction(True) for _ in range(n_fraud)]
    random.shuffle(records)
    return pd.DataFrame(records)
