from django.contrib import admin

from .models import FraudAlert, ModelMetrics, Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "transaction_id",
        "amount_inr",
        "payment_channel",
        "risk_level",
        "is_flagged",
        "created_at",
    )
    list_filter = ("payment_channel", "risk_level", "is_flagged", "payer_state")
    search_fields = ("transaction_id", "payer_state", "beneficiary_state")


@admin.register(FraudAlert)
class FraudAlertAdmin(admin.ModelAdmin):
    list_display = ("title", "transaction", "recommended_action", "resolved", "created_at")
    list_filter = ("recommended_action", "resolved")


@admin.register(ModelMetrics)
class ModelMetricsAdmin(admin.ModelAdmin):
    list_display = ("trained_at", "precision", "recall", "f1_score", "roc_auc")
