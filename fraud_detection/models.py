from django.db import models


class PaymentChannel(models.TextChoices):
    UPI = "UPI", "UPI"
    IMPS = "IMPS", "IMPS"
    NEFT = "NEFT", "NEFT"
    RTGS = "RTGS", "RTGS"
    CARD = "CARD", "Card"
    WALLET = "WALLET", "Wallet"


class RiskLevel(models.TextChoices):
    MINIMAL = "MINIMAL", "Minimal"
    LOW = "LOW", "Low"
    MEDIUM = "MEDIUM", "Medium"
    HIGH = "HIGH", "High"
    CRITICAL = "CRITICAL", "Critical"


class Transaction(models.Model):
    transaction_id = models.CharField(max_length=32, unique=True, db_index=True)
    amount_inr = models.DecimalField(max_digits=12, decimal_places=2)
    payment_channel = models.CharField(max_length=10, choices=PaymentChannel.choices, default=PaymentChannel.UPI)
    device_type = models.CharField(max_length=10, default="ANDROID")
    payer_state = models.CharField(max_length=64)
    beneficiary_state = models.CharField(max_length=64)
    merchant_category = models.CharField(max_length=32, default="P2P")
    merchant_risk_score = models.FloatField(default=0.2)
    account_age_days = models.PositiveIntegerField(default=365)
    beneficiary_age_days = models.PositiveIntegerField(default=30)
    txn_velocity_1h = models.PositiveSmallIntegerField(default=1)
    distance_km = models.FloatField(default=5.0)
    hour_of_day = models.PositiveSmallIntegerField(default=12)
    day_of_week = models.PositiveSmallIntegerField(default=2)

    new_beneficiary = models.BooleanField(default=False)
    high_velocity = models.BooleanField(default=False)
    odd_hour = models.BooleanField(default=False)
    geo_mismatch = models.BooleanField(default=False)
    vpn_detected = models.BooleanField(default=False)
    first_large_txn = models.BooleanField(default=False)

    fraud_probability = models.FloatField(null=True, blank=True)
    risk_level = models.CharField(max_length=12, choices=RiskLevel.choices, blank=True)
    is_flagged = models.BooleanField(default=False)
    ground_truth_fraud = models.BooleanField(null=True, blank=True, help_text="Known label for evaluation")

    risk_factors = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.transaction_id} — ₹{self.amount_inr}"


class FraudAlert(models.Model):
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, related_name="alert")
    title = models.CharField(max_length=128)
    description = models.TextField()
    recommended_action = models.CharField(max_length=64, default="REVIEW")
    resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.title


class ModelMetrics(models.Model):
    """Snapshot of ML model performance for dashboard and paper citations."""

    precision = models.FloatField()
    recall = models.FloatField()
    f1_score = models.FloatField()
    roc_auc = models.FloatField()
    train_samples = models.PositiveIntegerField()
    test_samples = models.PositiveIntegerField()
    confusion_matrix = models.JSONField(default=list)
    classification_report = models.TextField()
    trained_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-trained_at"]
        verbose_name_plural = "Model metrics"

    def __str__(self) -> str:
        return f"Model run — F1 {self.f1_score:.3f} @ {self.trained_at:%Y-%m-%d}"
