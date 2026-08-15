from flask import Blueprint, jsonify

from app.models import task as task_model

stats_bp = Blueprint("stats", __name__, url_prefix="/api/stats")


@stats_bp.get("")
def get_stats():
    try:
        stats = task_model.get_stats()
    except RuntimeError as exc:
        return jsonify({"error": f"Database unavailable: {exc}"}), 500
    except Exception as exc:  # noqa: BLE001
        return jsonify({"error": f"Database error: {exc}"}), 500

    return jsonify(stats), 200
