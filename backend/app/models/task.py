"""
Task model.

This is a lightweight data-access layer (not an ORM) that talks to the
`tasks` table directly with SQL via psycopg2. Keeping it simple on purpose.
"""
from app.database.db import get_cursor

VALID_STATUSES = ("TODO", "IN_PROGRESS", "COMPLETED")
VALID_PRIORITIES = ("LOW", "MEDIUM", "HIGH")

_ALLOWED_SORT_COLUMNS = {"created_at", "updated_at", "due_date", "priority", "title"}


class TaskValidationError(ValueError):
    """Raised when task input data fails validation."""


def validate_task_payload(data, partial=False):
    """
    Validate incoming task data.

    partial=True allows a subset of fields (used for PUT/patch-style updates).
    Raises TaskValidationError with a human-readable message on failure.
    Returns a cleaned dict of only the recognized fields that were provided.
    """
    if not isinstance(data, dict) or (not partial and not data):
        raise TaskValidationError("Request body must be a non-empty JSON object.")

    cleaned = {}

    if "title" in data or not partial:
        title = data.get("title")
        if not title or not isinstance(title, str) or not title.strip():
            raise TaskValidationError("Field 'title' is required and cannot be empty.")
        cleaned["title"] = title.strip()

    if "description" in data:
        description = data.get("description") or ""
        if not isinstance(description, str):
            raise TaskValidationError("Field 'description' must be a string.")
        cleaned["description"] = description.strip()
    elif not partial:
        cleaned["description"] = ""

    if "status" in data:
        status = data.get("status")
        if status not in VALID_STATUSES:
            raise TaskValidationError(
                f"Field 'status' must be one of {VALID_STATUSES}."
            )
        cleaned["status"] = status
    elif not partial:
        cleaned["status"] = "TODO"

    if "priority" in data:
        priority = data.get("priority")
        if priority not in VALID_PRIORITIES:
            raise TaskValidationError(
                f"Field 'priority' must be one of {VALID_PRIORITIES}."
            )
        cleaned["priority"] = priority
    elif not partial:
        cleaned["priority"] = "MEDIUM"

    if "due_date" in data:
        due_date = data.get("due_date")
        if due_date is not None and not isinstance(due_date, str):
            raise TaskValidationError("Field 'due_date' must be an ISO date string.")
        cleaned["due_date"] = due_date
    elif not partial:
        cleaned["due_date"] = None

    return cleaned


def list_tasks(status=None, priority=None, search=None, sort_by="created_at", order="desc"):
    """Return all tasks, optionally filtered by status/priority/search text."""
    query = "SELECT * FROM tasks WHERE 1=1"
    params = []

    if status:
        query += " AND status = %s"
        params.append(status)

    if priority:
        query += " AND priority = %s"
        params.append(priority)

    if search:
        query += " AND (title ILIKE %s OR description ILIKE %s)"
        like = f"%{search}%"
        params.extend([like, like])

    sort_column = sort_by if sort_by in _ALLOWED_SORT_COLUMNS else "created_at"
    sort_order = "ASC" if str(order).lower() == "asc" else "DESC"
    query += f" ORDER BY {sort_column} {sort_order}"

    with get_cursor() as cur:
        cur.execute(query, params)
        return cur.fetchall()


def get_task(task_id):
    with get_cursor() as cur:
        cur.execute("SELECT * FROM tasks WHERE id = %s;", (task_id,))
        return cur.fetchone()


def create_task(data):
    with get_cursor(commit=True) as cur:
        cur.execute(
            """
            INSERT INTO tasks (title, description, status, priority, due_date)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING *;
            """,
            (
                data["title"],
                data.get("description", ""),
                data.get("status", "TODO"),
                data.get("priority", "MEDIUM"),
                data.get("due_date"),
            ),
        )
        return cur.fetchone()


def update_task(task_id, data):
    """Partial update - only fields present in `data` are changed."""
    if not data:
        return get_task(task_id)

    set_clauses = []
    params = []
    for field in ("title", "description", "status", "priority", "due_date"):
        if field in data:
            set_clauses.append(f"{field} = %s")
            params.append(data[field])

    if not set_clauses:
        return get_task(task_id)

    set_clauses.append("updated_at = NOW()")
    params.append(task_id)

    query = f"UPDATE tasks SET {', '.join(set_clauses)} WHERE id = %s RETURNING *;"

    with get_cursor(commit=True) as cur:
        cur.execute(query, params)
        return cur.fetchone()


def delete_task(task_id):
    with get_cursor(commit=True) as cur:
        cur.execute("DELETE FROM tasks WHERE id = %s RETURNING id;", (task_id,))
        return cur.fetchone()


def get_stats():
    with get_cursor() as cur:
        cur.execute(
            """
            SELECT
                COUNT(*) AS total,
                COUNT(*) FILTER (WHERE status = 'TODO') AS todo,
                COUNT(*) FILTER (WHERE status = 'IN_PROGRESS') AS in_progress,
                COUNT(*) FILTER (WHERE status = 'COMPLETED') AS completed
            FROM tasks;
            """
        )
        row = cur.fetchone()

    total = row["total"] or 0
    completed = row["completed"] or 0
    completion_rate = round((completed / total) * 100, 1) if total else 0.0

    return {
        "total_tasks": total,
        "pending_tasks": row["todo"] or 0,
        "in_progress_tasks": row["in_progress"] or 0,
        "completed_tasks": completed,
        "completion_rate": completion_rate,
    }
