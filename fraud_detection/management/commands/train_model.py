from django.core.management.base import BaseCommand

from fraud_detection.ml.train import train_and_save
from fraud_detection.models import ModelMetrics
from django.conf import settings


class Command(BaseCommand):
    help = "Train the hybrid fraud detection model and persist metrics."

    def add_arguments(self, parser):
        parser.add_argument("--samples", type=int, default=12000, help="Training sample size")

    def handle(self, *args, **options):
        self.stdout.write("Training fraud detection model...")
        metrics = train_and_save(settings.ML_MODEL_PATH, n_samples=options["samples"])

        ModelMetrics.objects.create(
            precision=metrics["precision"],
            recall=metrics["recall"],
            f1_score=metrics["f1"],
            roc_auc=metrics["roc_auc"],
            train_samples=metrics["train_samples"],
            test_samples=metrics["test_samples"],
            confusion_matrix=metrics["confusion_matrix"],
            classification_report=metrics["classification_report"],
        )

        self.stdout.write(self.style.SUCCESS(
            f"Model saved. F1={metrics['f1']:.3f} | Precision={metrics['precision']:.3f} | "
            f"Recall={metrics['recall']:.3f} | ROC-AUC={metrics['roc_auc']:.3f}"
        ))
