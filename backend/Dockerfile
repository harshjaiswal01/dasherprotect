# Multi-stage: build deps then run
FROM python:3.12-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5001
# Using Gunicorn for prod-like run; Flask-SocketIO via eventlet
CMD ["gunicorn", "-c", "gunicorn.conf.py", "wsgi:app"]
