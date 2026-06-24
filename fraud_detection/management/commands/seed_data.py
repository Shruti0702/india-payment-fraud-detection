import uuid

from django.core.management.base import BaseCommand

from fraud_detection.ml.data_generator import generate_dataset
from fraud_detection.ml.predictor import get_predictor
from fraud_detection.services import persist_scored_transaction


class Command(BaseCommand):
    help = "Seed demo transactions with AI fraud scores for dashboard showcase."

    def add_arguments(self, parser):
        parser.add_argument("--count", type=int, default=200, help="Number of transactions to seed")

    def handle(self, *args, **options):
        try:
            predictor = get_predictor()
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR("Train model first: python manage.py train_model"))
            return

        df = generate_dataset(n_samples=options["count"], fraud_rate=0.1)
        flagged = 0
        for record in df.to_dict(orient="records"):
            record["transaction_id"] = record.get("transaction_id") or f"TXN{uuid.uuid4().hex[:10].upper()}"
            record["ground_truth_fraud"] = bool(record.pop("is_fraud"))
            score = predictor.score_transaction(record)
            persist_scored_transaction(record, score)
            if score["is_fraud"]:
                flagged += 1

        self.stdout.write(self.style.SUCCESS(
            f"Seeded {options['count']} transactions ({flagged} flagged as fraud)."
        ))
