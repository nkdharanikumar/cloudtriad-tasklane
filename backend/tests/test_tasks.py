"""
Basic tests.

Validation tests run without a database. The health-check test spins up the
Flask app and hits /health - it will report "degraded" if no DB is running,
which is expected in isolated test environments.
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest  # noqa: E402

from app.models.task import TaskValidationError, validate_task_payload  # noqa: E402


def test_validate_task_payload_requires_title():
    with pytest.raises(TaskValidationError):
        validate_task_payload({})


def test_validate_task_payload_rejects_bad_status():
    with pytest.raises(TaskValidationError):
        validate_task_payload({"title": "Test", "status": "NOT_A_STATUS"})


def test_validate_task_payload_rejects_bad_priority():
    with pytest.raises(TaskValidationError):
        validate_task_payload({"title": "Test", "priority": "URGENT"})


def test_validate_task_payload_applies_defaults():
    cleaned = validate_task_payload({"title": "Test task"})
    assert cleaned["title"] == "Test task"
    assert cleaned["status"] == "TODO"
    assert cleaned["priority"] == "MEDIUM"
    assert cleaned["description"] == ""


def test_validate_task_payload_partial_update_allows_missing_title():
    cleaned = validate_task_payload({"status": "COMPLETED"}, partial=True)
    assert cleaned == {"status": "COMPLETED"}


def test_health_endpoint_returns_200():
    from app import create_app

    app = create_app()
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] in ("healthy", "degraded")
