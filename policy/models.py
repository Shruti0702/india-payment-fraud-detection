from django.db import models


class PolicyFramework(models.Model):
    """Indian regulatory frameworks relevant to AI fraud detection."""

    name = models.CharField(max_length=128)
    authority = models.CharField(max_length=64, help_text="e.g. RBI, MeitY, NPCI")
    year = models.PositiveSmallIntegerField()
    summary = models.TextField()
    relevance_to_ai = models.TextField()
    source_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-year", "name"]

    def __str__(self) -> str:
        return f"{self.name} ({self.authority}, {self.year})"


class PolicyChallenge(models.Model):
    category = models.CharField(max_length=64)
    title = models.CharField(max_length=200)
    description = models.TextField()
    india_context = models.TextField(help_text="Why this matters specifically for India")
    mitigation = models.TextField(blank=True)
    severity = models.CharField(
        max_length=16,
        choices=[("LOW", "Low"), ("MEDIUM", "Medium"), ("HIGH", "High")],
        default="MEDIUM",
    )

    class Meta:
        ordering = ["category", "title"]

    def __str__(self) -> str:
        return self.title
