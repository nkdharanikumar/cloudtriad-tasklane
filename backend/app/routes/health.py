from flask import Blueprint, jsonify

from app.database.db import is_database_available

health_bp = Blueprint("health", __name__, url_prefix="/health")


@health_bp.get("")
def health():
    """
    Simple liveness/readiness check.

    Returns 200 with status "healthy" when the app + database are reachable,
    and 200 with status "degraded" if the app is up but the database isn't
    (useful for k8s liveness vs readiness probes later on).
    """
    db_ok = is_database_available()
    payload = {
        "status": "healthy" if db_ok else "degraded",
        "database": "connected" if db_ok else "unavailable",
    }
    return jsonify(payload), 200
