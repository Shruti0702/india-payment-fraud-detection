from rest_framework import serializers

from .models import FraudAlert, ModelMetrics, Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"
        read_only_fields = (
            "fraud_probability",
            "risk_level",
            "is_flagged",
            "risk_factors",
            "created_at",
        )


class TransactionScoreSerializer(serializers.Serializer):
    transaction_id = serializers.CharField(required=False)
    amount_inr = serializers.DecimalField(max_digits=12, decimal_places=2)
    payment_channel = serializers.ChoiceField(
        choices=["UPI", "IMPS", "NEFT", "RTGS", "CARD", "WALLET"], default="UPI"
    )
    device_type = serializers.ChoiceField(
        choices=["ANDROID", "IOS", "WEB", "USSD"], default="ANDROID"
    )
    payer_state = serializers.CharField(max_length=64)
    beneficiary_state = serializers.CharField(max_length=64)
    merchant_category = serializers.CharField(max_length=32, default="P2P")
    merchant_risk_score = serializers.FloatField(default=0.2, min_value=0, max_value=1)
    account_age_days = serializers.IntegerField(default=365, min_value=0)
    beneficiary_age_days = serializers.IntegerField(default=30, min_value=0)
    txn_velocity_1h = serializers.IntegerField(default=1, min_value=0)
    distance_km = serializers.FloatField(default=5.0, min_value=0)
    hour_of_day = serializers.IntegerField(default=12, min_value=0, max_value=23)
    day_of_week = serializers.IntegerField(default=2, min_value=0, max_value=6)
    new_beneficiary = serializers.BooleanField(default=False)
    high_velocity = serializers.BooleanField(default=False)
    odd_hour = serializers.BooleanField(default=False)
    geo_mismatch = serializers.BooleanField(default=False)
    vpn_detected = serializers.BooleanField(default=False)
    first_large_txn = serializers.BooleanField(default=False)
    ground_truth_fraud = serializers.BooleanField(required=False, allow_null=True)


class FraudAlertSerializer(serializers.ModelSerializer):
    transaction_id = serializers.CharField(source="transaction.transaction_id", read_only=True)

    class Meta:
        model = FraudAlert
        fields = "__all__"


class ModelMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelMetrics
        fields = "__all__"
