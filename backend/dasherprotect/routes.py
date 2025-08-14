"""
API blueprint placeholder. M1 will add:
- POST /v1/persons
- POST /v1/persons/{id}/faces
- POST /v1/identify
- GET  /v1/sightings

For M0 we just expose a small "hello" to verify prefix.
"""

from flask import Blueprint, jsonify

bp = Blueprint("api", __name__)

@bp.get("/hello")
def hello():
    return jsonify(service="dasher-protect-api", version="m0")
