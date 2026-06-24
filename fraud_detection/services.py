import uuid

from fraud_detection.models import FraudAlert, Transaction


def recommended_action(risk_level: str) -> str:
    return {
        "CRITICAL": "BLOCK",
        "HIGH": "STEP_UP_AUTH",
        "MEDIUM": "REVIEW",
        "LOW": "MONITOR",
        "MINIMAL": "ALLOW",
    }.get(risk_level, "REVIEW")


def persist_scored_transaction(data: dict, score: dict) -> Transaction:
    txn_id = data.get("transaction_id") or f"TXN{uuid.uuid4().hex[:12].upper()}"
    txn, _ = Transaction.objects.update_or_create(
        transaction_id=txn_id,
        defaults={
            "amount_inr": data["amount_inr"],
            "payment_channel": data.get("payment_channel", "UPI"),
            "device_type": data.get("device_type", "ANDROID"),
            "payer_state": data["payer_state"],
            "beneficiary_state": data["beneficiary_state"],
            "merchant_category": data.get("merchant_category", "P2P"),
            "merchant_risk_score": data.get("merchant_risk_score", 0.2),
            "account_age_days": data.get("account_age_days", 365),
            "beneficiary_age_days": data.get("beneficiary_age_days", 30),
            "txn_velocity_1h": data.get("txn_velocity_1h", 1),
            "distance_km": data.get("distance_km", 5.0),
            "hour_of_day": data.get("hour_of_day", 12),
            "day_of_week": data.get("day_of_week", 2),
            "new_beneficiary": data.get("new_beneficiary", False),
            "high_velocity": data.get("high_velocity", False),
            "odd_hour": data.get("odd_hour", False),
            "geo_mismatch": data.get("geo_mismatch", False),
            "vpn_detected": data.get("vpn_detected", False),
            "first_large_txn": data.get("first_large_txn", False),
            "fraud_probability": score["fraud_probability"],
            "risk_level": score["risk_level"],
            "is_flagged": score["is_fraud"],
            "risk_factors": score["risk_factors"],
            "ground_truth_fraud": data.get("ground_truth_fraud"),
        },
    )

    if score["is_fraud"]:
        FraudAlert.objects.update_or_create(
            transaction=txn,
            defaults={
                "title": f"{score['risk_level']} risk — {txn.payment_channel} ₹{txn.amount_inr}",
                "description": "; ".join(f["factor"] for f in score["risk_factors"]) or "Elevated ML fraud score",
                "recommended_action": recommended_action(score["risk_level"]),
            },
        )
    return txn
