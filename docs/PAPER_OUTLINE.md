# Paper Outline: AI for Fraud Detection in Indian Digital Payments

Use this outline as a starting structure for your research paper. Metrics and numbers can be pulled from the live system (`/api/metrics/`).

---

## Abstract (150–250 words)

- India's digital payment revolution (UPI: 10B+ monthly transactions)
- Rising fraud losses and social engineering (vishing, mule accounts)
- AI/ML as a technical response vs. policy and governance constraints
- This paper presents PayGuard AI as a case study and analyses opportunities, challenges, and policy implications

---

## 1. Introduction

### 1.1 Background
- Growth of UPI, IMPS, wallets since demonetisation and COVID
- NPCI as infrastructure backbone; RBI as regulator

### 1.2 Problem Statement
- Fraud typologies in India: authorised push payment fraud, mule networks, SIM swap, QR tampering
- Limitations of rule-based systems at scale

### 1.3 Research Objectives
1. Evaluate ML approaches suitable for Indian payment fraud
2. Identify technical and regulatory challenges
3. Propose policy-aligned deployment framework

### 1.4 Contribution
- Hybrid ML prototype (GBM + Isolation Forest)
- Explainability layer for regulatory compliance
- Policy analysis mapped to RBI, NPCI, DPDP Act

---

## 2. Literature Review

- Global card fraud ML (FICO Falcon, feedzai)
- UPI-specific fraud reports (RBI annual report, NPCI circulars)
- Fairness and explainability in financial AI (EU AI Act parallels)
- Federated learning for cross-bank fraud detection

---

## 3. Indian Digital Payment Landscape

### 3.1 Payment Rails
| Rail | Volume share | Fraud characteristics |
|------|-------------|----------------------|
| UPI | ~60%+ | P2P mule, social engineering |
| IMPS | Moderate | Account takeover |
| NEFT/RTGS | Corporate | Business email compromise |
| Cards | Declining share | Skimming, CNP fraud |

### 3.2 Regulatory Environment
- RBI Master Direction on Digital Payment Security Controls (2021)
- DPDP Act 2023 — consent, purpose limitation, data localisation
- NPCI UPI Risk Management Framework

---

## 4. Methodology — PayGuard AI System

### 4.1 Architecture
- Django REST backend, SQLite/PostgreSQL
- Real-time scoring API (`POST /api/transactions/score/`)
- Dashboard for analyst review

### 4.2 Feature Engineering
- Transaction amount, channel (one-hot), device type
- Behavioural: velocity, beneficiary age, account age
- Geographic: payer/beneficiary state distance
- Risk flags: new beneficiary, odd hour, VPN, geo mismatch

### 4.3 Model Design
- **Supervised:** Gradient Boosting Classifier (200 estimators)
- **Unsupervised:** Isolation Forest (contamination = 8%)
- **Ensemble:** 0.7 × supervised + 0.3 × anomaly score

### 4.4 Evaluation Metrics
- Precision, Recall, F1, ROC-AUC (report from `python manage.py train_model`)
- Confusion matrix analysis — trade-off between false positives and fraud capture

### 4.5 Explainability
- Rule-based risk factor extraction post-scoring
- Mapping to NPCI fraud categories for ombudsman-ready audit trails

---

## 5. Opportunities

1. **Real-time intervention** — Block or step-up auth before settlement
2. **Cross-channel intelligence** — Unified scoring across UPI + card + wallet
3. **Network effects** — Consortium models across PSPs (with privacy tech)
4. **Cost reduction** — Automate L1 fraud review; human analysts for edge cases
5. **Inclusion-safe fraud prevention** — Graduated friction vs. hard blocks for new users

---

## 6. Challenges

| Challenge | India-specific impact | Mitigation |
|-----------|----------------------|------------|
| Data silos | Banks don't share labels | Federated learning, synthetic data |
| Latency | UPI expects <1s end-to-end | Lightweight models, edge deployment |
| Social engineering | User authorises fraud | Behavioural signals, cooling-off periods |
| Bias | Rural/new accounts over-flagged | Fairness constraints, regional calibration |
| Explainability | RBI audit requirements | Rule-augmented explanations (implemented) |
| Adversarial ML | Fraudsters adapt to models | Continuous retraining, drift monitoring |

---

## 7. Policy Implications

### 7.1 For RBI
- Mandate model risk management for AI-based fraud systems
- Standardise fraud label sharing via secure enclaves
- Require explainability in customer communication for blocked transactions

### 7.2 For NPCI
- Integrate AI risk scores into UPI switch with velocity caps
- Publish anonymised fraud typology datasets for research

### 7.3 For MeitY / DPDP
- Clarify lawful basis for fraud detection under "legitimate interest"
- Data localisation compliance for cloud-hosted ML

### 7.4 For Banks & PSPs
- Human-in-the-loop for HIGH/CRITICAL alerts
- Customer education on vishing — technology alone is insufficient

---

## 8. Results & Discussion

- Insert metrics from your trained model
- Channel-wise fraud distribution from seeded dashboard data
- Case study: walk through a high-risk UPI transaction on `/analyze/`
- Limitations: synthetic data, no production bank integration

---

## 9. Conclusion

- AI is necessary but not sufficient for Indian payment fraud
- Policy, education, and technology must align
- PayGuard AI demonstrates a deployable, explainable, regulation-aware approach

---

## 10. References (starter list)

1. Reserve Bank of India. (2021). *Master Direction on Digital Payment Security Controls*.
2. Ministry of Electronics and IT. (2023). *Digital Personal Data Protection Act*.
3. NPCI. (2022). *UPI Risk Management Framework*.
4. Bhaskar, et al. — fraud detection surveys (add from Google Scholar)
5. RBI Annual Report — digital fraud statistics

---

## Appendix A: API Specification

Document endpoints from README.

## Appendix B: Model Hyperparameters

From `fraud_detection/ml/train.py`.

## Appendix C: Screenshots

- Dashboard, Analyze page, Policy page for paper figures
