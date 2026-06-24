FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libgomp1 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD python manage.py migrate && \
    python manage.py train_model && \
    python manage.py seed_policy && \
    python manage.py seed_data --count 100 && \
    gunicorn config.wsgi --bind 0.0.0.0:8000 --workers 2
