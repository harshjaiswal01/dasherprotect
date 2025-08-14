"""
Centralized extension objects so imports are tidy.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from prometheus_client import CollectorRegistry, generate_latest, CONTENT_TYPE_LATEST

db = SQLAlchemy()
socketio = SocketIO(async_mode="eventlet")

# Simple Prometheus hook (we'll add counters/histograms in M4)
class _Prom:
    def __init__(self):
        self.registry = CollectorRegistry()

    def generate_latest(self):
        return generate_latest(self.registry)

    @property
    def CONTENT_TYPE_LATEST(self):
        return CONTENT_TYPE_LATEST

prometheus_metrics = _Prom()

# Swagger UI stub — we mount a static Swagger UI that reads our openapi.yaml
from flask import Blueprint, send_from_directory
import os

swagger_ui_blueprint = Blueprint("swagger_ui", __name__)

@swagger_ui_blueprint.route("/", methods=["GET"])
def swagger_index():
    # Simple redirect to the raw YAML (you can replace with full Swagger UI later)
    return send_from_directory(os.path.dirname(__file__), "openapi.yaml", mimetype="text/yaml")
