from flask import Blueprint, jsonify, request

from app.models import task as task_model
from app.models.task import TaskValidationError

tasks_bp = Blueprint("tasks", __name__, url_prefix="/api/tasks")


def _error(message, status_code):
    return jsonify({"error": message}), status_code


def _handle_db_error(exc):
    return _error(f"Database error: {exc}", 500)


@tasks_bp.get("")
def get_tasks():
    status = request.args.get("status") or None
    priority = request.args.get("priority") or None
    search = request.args.get("search") or None
    sort_by = request.args.get("sort_by", "created_at")
    order = request.args.get("order", "desc")

    if status and status not in task_model.VALID_STATUSES:
        return _error(f"Invalid status filter. Must be one of {task_model.VALID_STATUSES}.", 400)
    if priority and priority not in task_model.VALID_PRIORITIES:
        return _error(f"Invalid priority filter. Must be one of {task_model.VALID_PRIORITIES}.", 400)

    try:
        tasks = task_model.list_tasks(
            status=status, priority=priority, search=search, sort_by=sort_by, order=order
        )
    except RuntimeError as exc:
        return _error(f"Database unavailable: {exc}", 500)
    except Exception as exc:  # noqa: BLE001
        return _handle_db_error(exc)

    return jsonify(tasks), 200


@tasks_bp.get("/<int:task_id>")
def get_task(task_id):
    try:
        task = task_model.get_task(task_id)
    except RuntimeError as exc:
        return _error(f"Database unavailable: {exc}", 500)
    except Exception as exc:  # noqa: BLE001
        return _handle_db_error(exc)

    if task is None:
        return _error(f"Task with id {task_id} not found.", 404)
    return jsonify(task), 200


@tasks_bp.post("")
def create_task():
    data = request.get_json(silent=True)
    if data is None:
        return _error("Request body must be valid JSON.", 400)

    try:
        cleaned = task_model.validate_task_payload(data, partial=False)
    except TaskValidationError as exc:
        return _error(str(exc), 400)

    try:
        task = task_model.create_task(cleaned)
    except RuntimeError as exc:
        return _error(f"Database unavailable: {exc}", 500)
    except Exception as exc:  # noqa: BLE001
        return _handle_db_error(exc)

    return jsonify(task), 201


@tasks_bp.put("/<int:task_id>")
def update_task(task_id):
    data = request.get_json(silent=True)
    if data is None:
        return _error("Request body must be valid JSON.", 400)

    try:
        cleaned = task_model.validate_task_payload(data, partial=True)
    except TaskValidationError as exc:
        return _error(str(exc), 400)

    try:
        existing = task_model.get_task(task_id)
        if existing is None:
            return _error(f"Task with id {task_id} not found.", 404)
        task = task_model.update_task(task_id, cleaned)
    except RuntimeError as exc:
        return _error(f"Database unavailable: {exc}", 500)
    except Exception as exc:  # noqa: BLE001
        return _handle_db_error(exc)

    return jsonify(task), 200


@tasks_bp.delete("/<int:task_id>")
def delete_task(task_id):
    try:
        deleted = task_model.delete_task(task_id)
    except RuntimeError as exc:
        return _error(f"Database unavailable: {exc}", 500)
    except Exception as exc:  # noqa: BLE001
        return _handle_db_error(exc)

    if deleted is None:
        return _error(f"Task with id {task_id} not found.", 404)
    return jsonify({"message": f"Task {task_id} deleted successfully."}), 200
