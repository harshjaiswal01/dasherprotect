# backend/dasherprotect/app.py
"""
Dasher Protect — Flask application factory (M0)

Exposes:
- GET /healthz      : liveness probe
- GET /readyz       : readiness probe (DB/Redis ping TBD in M1)
- GET /v1/hello     : simple API smoke check
- GET /metrics      : Prometheus metrics (stub)
- GET /openapi.yaml : raw OpenAPI spec
- GET /docs         : Swagger UI backed by openapi.yaml
"""
from __future__ import annotations

from pathlib import Path
from flask import Flask, jsonify, Response
from flask_cors import CORS

from .config import load_config
from .extensions import (
    db,
    socketio,
    prometheus_metrics,   # simple shim we added for M0
    init_swagger_ui,      # mounts /docs and serves /openapi.yaml
)

# repository /backend path (where openapi.yaml lives)
BACKEND_ROOT = Path(__file__).resolve().parents[1]


def create_app() -> Flask:
    app = Flask(__name__)

    # ---- Config (reads DATABASE_URL / SECRET_KEY / REDIS_URL from env/.env) ----
    # IMPORTANT: must be loaded before initializing extensions like SQLAlchemy.
    app.config.from_mapping(load_config())

    # ---- CORS (dev only; we’ll tighten later) ----
    CORS(app)

    # ---- Init extensions ----
    db.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")

    # ---- Health / readiness ----
    @app.get("/healthz")
    def healthz():
        return jsonify({"status": "ok"})

    @app.get("/readyz")
    def readyz():
        # M1: add real checks (e.g., db.connect(), redis.ping())
        return jsonify({"status": "ready"})

    # ---- Simple hello for quick smoke checks ----
    @app.get("/v1/hello")
    def hello():
        return jsonify({"service": "dasher-protect-api", "version": "m0"})

    # ---- Prometheus metrics (stub) ----
    @app.get("/metrics")
    def metrics():
        # prometheus_client generate_latest + correct content-type
        data = prometheus_metrics.generate_latest()
        return Response(data, mimetype=prometheus_metrics.CONTENT_TYPE_LATEST)

    # ---- Swagger UI + raw spec ----
    # Serves /openapi.yaml and a Swagger UI at /docs
    init_swagger_ui(app, spec_dir=BACKEND_ROOT)

    # ---- Future M1: register API blueprints here ----
    # from .routes import bp as api_bp
    # app.register_blueprint(api_bp, url_prefix="/v1")

    return app
