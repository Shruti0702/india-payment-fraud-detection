from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("transactions", views.TransactionViewSet, basename="transaction")
router.register("alerts", views.FraudAlertViewSet, basename="alert")
router.register("metrics", views.ModelMetricsViewSet, basename="metrics")

urlpatterns = [
    path("", views.home, name="home"),
    path("analyze/", views.analyze, name="analyze"),
    path("api/dashboard/", views.dashboard_stats, name="dashboard-stats"),
    path("api/", include(router.urls)),
]
