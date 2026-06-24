# PayGuard AI — India Payment Fraud Detection

Research prototype for **Artificial Intelligence for Fraud Detection in Digital Payments: Opportunities, Challenges and Policy Implications for India**.

## Quick Start

```bash
cd india-payment-fraud-detection
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py train_model
python manage.py seed_policy
python manage.py seed_data --count 200
python manage.py runserver
```

Open http://127.0.0.1:8000

## API

`POST /api/transactions/score/` — score a transaction  
`GET /api/dashboard/` — stats  
`GET /policy/` — regulatory frameworks and challenges

See `docs/PAPER_OUTLINE.md` for your paper structure.

## Deploy

Push to GitHub and deploy on Render using `render.yaml`, or run `docker build -t payguard-ai .`
