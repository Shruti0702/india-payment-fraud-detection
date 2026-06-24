from django.db.models import Avg, Count, Q, Sum
from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response

from .ml.predictor import get_predictor
from .models import FraudAlert, ModelMetrics, PaymentChannel, Transaction
from .serializers import (
    FraudAlertSerializer,
    ModelMetricsSerializer,
    TransactionScoreSerializer,
    TransactionSerializer,
)
from .services import persist_scored_transaction


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    @action(detail=False, methods=["post"])
    def score(self, request):
        serializer = TransactionScoreSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            score = get_predictor().score_transaction(dict(data))
        except FileNotFoundError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        txn = persist_scored_transaction(dict(data), score)
        return Response(
            {
                "transaction_id": txn.transaction_id,
                **score,
            },
            status=status.HTTP_201_CREATED,
        )


class FraudAlertViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FraudAlert.objects.select_related("transaction")
    serializer_class = FraudAlertSerializer


class ModelMetricsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ModelMetrics.objects.all()
    serializer_class = ModelMetricsSerializer


def build_dashboard_stats() -> dict:
    latest_metrics = ModelMetrics.objects.first()
    totals = Transaction.objects.aggregate(
        total=Count("id"),
        flagged=Count("id", filter=Q(is_flagged=True)),
        volume=Sum("amount_inr"),
        avg_risk=Avg("fraud_probability"),
    )
    by_channel = list(
        Transaction.objects.values("payment_channel")
        .annotate(count=Count("id"), flagged=Count("id", filter=Q(is_flagged=True)))
        .order_by("-count")
    )
    by_risk = list(
        Transaction.objects.values("risk_level")
        .annotate(count=Count("id"))
        .order_by("risk_level")
    )
    recent_alerts = FraudAlert.objects.select_related("transaction")[:8]

    return {
        "totals": totals,
        "by_channel": by_channel,
        "by_risk": by_risk,
        "latest_model_metrics": ModelMetricsSerializer(latest_metrics).data if latest_metrics else None,
        "recent_alerts": FraudAlertSerializer(recent_alerts, many=True).data,
    }


@api_view(["GET"])
def dashboard_stats(request):
    return Response(build_dashboard_stats())


def home(request):
    return render(request, "fraud_detection/home.html", {"stats": build_dashboard_stats()})


def analyze(request):
    result = None
    error = None
    if request.method == "POST":
        post_data = request.POST.copy()
        for flag in (
            "new_beneficiary", "high_velocity", "odd_hour",
            "geo_mismatch", "vpn_detected", "first_large_txn",
        ):
            post_data[flag] = flag in request.POST
        serializer = TransactionScoreSerializer(data=post_data)
        if serializer.is_valid():
            try:
                score = get_predictor().score_transaction(dict(serializer.validated_data))
                txn = persist_scored_transaction(dict(serializer.validated_data), score)
                result = {"transaction": txn, **score}
            except FileNotFoundError as exc:
                error = str(exc)
        else:
            error = serializer.errors
    return render(
        request,
        "fraud_detection/analyze.html",
        {
            "result": result,
            "error": error,
            "channels": [c.value for c in PaymentChannel],
        },
    )
