#!/usr/bin/env bash
set -euo pipefail

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate --noinput
python manage.py train_model
python manage.py seed_policy
python manage.py seed_data --count 150
