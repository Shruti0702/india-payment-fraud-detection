from django.core.management.base import BaseCommand

from policy.models import PolicyChallenge, PolicyFramework


FRAMEWORKS = [
    {
        "name": "Master Direction on Digital Payment Security Controls",
        "authority": "RBI",
        "year": 2021,
        "summary": "Mandates multi-factor authentication, transaction limits, and fraud monitoring for payment system participants.",
        "relevance_to_ai": "Provides regulatory basis for deploying ML-based real-time fraud scoring and step-up authentication triggers.",
        "source_url": "https://www.rbi.org.in/",
    },
    {
        "name": "Digital Personal Data Protection Act",
        "authority": "MeitY",
        "year": 2023,
        "summary": "Governs processing of personal data including transaction metadata, device fingerprints, and behavioural signals.",
        "relevance_to_ai": "Requires purpose limitation, consent, and explainability when AI models process payer data for fraud detection.",
        "source_url": "https://www.meity.gov.in/",
    },
    {
        "name": "NPCI UPI Risk Management Framework",
        "authority": "NPCI",
        "year": 2022,
        "summary": "Defines risk tiers, velocity checks, and dispute resolution for UPI — India's dominant real-time payment rail.",
        "relevance_to_ai": "AI models must align with NPCI velocity limits and mule-account typologies without blocking legitimate P2P flows.",
        "source_url": "https://www.npci.org.in/",
    },
    {
        "name": "Reserve Bank Guidelines on IT Governance",
        "authority": "RBI",
        "year": 2023,
        "summary": "Requires banks and NBFCs to maintain model risk management, audit trails, and incident reporting.",
        "relevance_to_ai": "Establishes governance expectations for ML model validation, drift monitoring, and human-in-the-loop review.",
        "source_url": "https://www.rbi.org.in/",
    },
]

CHALLENGES = [
    {
        "category": "Data",
        "title": "Limited labelled fraud data",
        "description": "Indian banks rarely share fraud labels across institutions, constraining supervised learning.",
        "india_context": "UPI's interoperable architecture means fraud patterns span multiple PSPs, but data silos persist.",
        "mitigation": "Federated learning pilots and synthetic data augmentation (as demonstrated in this project).",
        "severity": "HIGH",
    },
    {
        "category": "Infrastructure",
        "title": "Real-time scoring at UPI scale",
        "description": "UPI processes billions of monthly transactions; sub-100ms inference is required at peak.",
        "india_context": "Tier-2/3 banks and smaller PSPs lack GPU infrastructure for complex deep learning models.",
        "mitigation": "Lightweight ensemble models (GBM + Isolation Forest) with horizontal scaling.",
        "severity": "HIGH",
    },
    {
        "category": "Fairness",
        "title": "Bias against new-to-credit users",
        "description": "ML models may over-flag young accounts and rural first-time digital payers.",
        "india_context": "India's Jan Dhan expansion brought millions of new accounts — false positives erode trust.",
        "mitigation": "Fairness constraints, regional calibration, and graduated friction instead of hard blocks.",
        "severity": "MEDIUM",
    },
    {
        "category": "Explainability",
        "title": "Black-box models vs. regulatory audit",
        "description": "RBI expects banks to explain why a transaction was blocked or flagged.",
        "india_context": "Ombudsman complaints rise when customers cannot understand AI-driven declines.",
        "mitigation": "Rule-augmented explanations mapping risk factors to NPCI/RBI fraud typologies.",
        "severity": "HIGH",
    },
    {
        "category": "Adversarial",
        "title": "Social engineering bypasses technical controls",
        "description": "Vishing and OTP-sharing scams coerce users to authorise fraudulent UPI payments.",
        "india_context": "India's CERT-In and NPCI report social engineering as the top fraud vector, not technical exploits.",
        "mitigation": "Behavioural biometrics, cooling-off periods for new beneficiaries, and customer education.",
        "severity": "HIGH",
    },
    {
        "category": "Policy",
        "title": "Cross-border data localisation",
        "description": "Cloud-hosted ML pipelines may process transaction data outside India.",
        "india_context": "RBI's data localisation norms require payment data to remain onshore.",
        "mitigation": "Deploy models on Indian cloud regions; avoid sending PII to foreign LLM APIs.",
        "severity": "MEDIUM",
    },
]


class Command(BaseCommand):
    help = "Load Indian policy frameworks and AI fraud challenges for the policy module."

    def handle(self, *args, **options):
        PolicyFramework.objects.all().delete()
        PolicyChallenge.objects.all().delete()

        for item in FRAMEWORKS:
            PolicyFramework.objects.create(**item)
        for item in CHALLENGES:
            PolicyChallenge.objects.create(**item)

        self.stdout.write(self.style.SUCCESS(
            f"Loaded {len(FRAMEWORKS)} frameworks and {len(CHALLENGES)} challenges."
        ))
