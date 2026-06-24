from django.contrib import admin

from .models import PolicyChallenge, PolicyFramework


@admin.register(PolicyFramework)
class PolicyFrameworkAdmin(admin.ModelAdmin):
    list_display = ("name", "authority", "year")
    list_filter = ("authority", "year")


@admin.register(PolicyChallenge)
class PolicyChallengeAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "severity")
    list_filter = ("category", "severity")
