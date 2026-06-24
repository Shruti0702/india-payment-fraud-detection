from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("fraud_detection.urls")),
    path("", include("fraud_detection.urls")),
    path("policy/", include("policy.urls")),
]
