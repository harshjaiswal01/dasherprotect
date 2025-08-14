"""
Dasher Protect — Flask application factory.

This is the minimal API surface for M0:
- /healthz   : liveness probe
- /readyz    : readiness probe (DB/Redis ping)
- /docs      : serves Swagger UI based on openapi.yaml
- /metrics   : Prometheus metrics (basic counter/histogram hooks ready)
- Socket.IO  : configured and ready to emit events (e.g., 'hit_detected' later)
"""

from flask import Flask, jsonify, Response
from flask_cors import CORS
from .extensions import db, socketio, prometheus_metrics, swagger_ui_blueprint
from .config import load_config
from .routes import bp as api_bp

def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)  # allow all origins for now (dev only)
    app.config.from_mapping(load_config())

    # Init extensions
    db.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")  # PWA connects from localhost:5173

    # Blueprints
    app.register_blueprint(api_bp, url_prefix="/v1")
    app.register_blueprint(swagger_ui_blueprint, url_prefix="/docs")

    # Health endpoints
    @app.get("/healthz")
    def healthz():
        return jsonify(status="ok", name="dasher-protect")

    @app.get("/readyz")
    def readyz():
        # In M0 we just return ok; in M1 we'll ping DB/Redis here.
        return jsonify(ready=True)

    # Prometheus metrics exposition
    @app.get("/metrics")
    def metrics():
        return Response(prometheus_metrics.generate_latest(), mimetype=prometheus_metrics.CONTENT_TYPE_LATEST)

    return app
