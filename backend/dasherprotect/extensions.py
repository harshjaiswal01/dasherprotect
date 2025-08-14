"""
Centralized extension objects so imports are tidy.
Also exposes a tiny helper to mount Swagger UI.
"""

from __future__ import annotations

from pathlib import Path

from flask import Blueprint, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_swagger_ui import get_swaggerui_blueprint
from prometheus_client import CollectorRegistry, generate_latest, CONTENT_TYPE_LATEST

# --- Core extensions ---------------------------------------------------------

db = SQLAlchemy()
socketio = SocketIO(async_mode="eventlet", cors_allowed_origins="*")


# --- Minimal Prometheus shim (we'll add counters/histograms later) -----------

class _Prom:
    def __init__(self) -> None:
        self.registry = CollectorRegistry()

    def generate_latest(self) -> bytes:
        return generate_latest(self.registry)

    @property
    def CONTENT_TYPE_LATEST(self) -> str:
        return CONTENT_TYPE_LATEST


prometheus_metrics = _Prom()


# --- Swagger UI helper -------------------------------------------------------

def init_swagger_ui(app, spec_dir: Path) -> None:
    """
    Mounts:
      • /openapi.yaml  -> serves the raw OpenAPI file from spec_dir
      • /docs          -> Swagger UI that renders /openapi.yaml

    NOTE: spec_dir should contain a file named 'openapi.yaml'.
          In our repo layout that's backend/openapi.yaml.
    """
    # Normalize to absolute path inside the container
    spec_dir = Path(spec_dir).resolve()

    # 1) Serve the spec via a tiny blueprint (Flask 3 requires 'path=' kwarg)
    spec_bp = Blueprint("swagger_spec", __name__)

    @spec_bp.get("/openapi.yaml")
    def openapi_yaml():
        # max_age=0 disables caching while you iterate
        return send_from_directory(
            directory=str(spec_dir),
            path="openapi.yaml",
            mimetype="text/yaml",
            as_attachment=False,
            max_age=0,
        )

    app.register_blueprint(spec_bp)

    # 2) Mount Swagger UI at /docs and point it to our /openapi.yaml route
    swagger_ui_bp = get_swaggerui_blueprint(
        base_url="/docs",            # where the UI is served
        api_url="/openapi.yaml",     # the spec endpoint we just mounted
        config={
            "app_name": "Dasher Protect API",
            # Hide model schemas by default; keeps things tidy for MVP
            "defaultModelsExpandDepth": -1,
        },
    )
    app.register_blueprint(swagger_ui_bp, url_prefix="/docs")
