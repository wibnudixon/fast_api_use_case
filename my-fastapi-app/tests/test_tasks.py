from fastapi.testclient import TestClient
from datetime import UTC, datetime
from uuid import UUID, uuid4
from app.api.dependencies import task_service
from app.main import app

client = TestClient(app)
# functions setup functions, create test tasl

def setup_function() -> None:
    """Start every test with empty in-memory storage."""
    task_service.clear_tasks()


def create_test_task() -> dict[str, object]:
    response = client.post(
        "/api/v1/tasks",
        json={
            "title": "Original task",
            "description": "Keep this description during a partial update.",
            "priority": "medium",
        },
    )

    assert response.status_code == 201
    return response.json()


def test_create_task_returns_created_task() -> None:
    response = client.post(
        "/api/v1/tasks",
        json={
            "title": "Build task endpoints",
            "description": "Implement create and list routes.",
            "status": "in_progress",
            "priority": "high",
            "due_date": "2026-08-20",
        },
    )

    assert response.status_code == 201

    body = response.json()
    assert body["title"] == "Build task endpoints"
    assert body["description"] == "Implement create and list routes."
    assert body["status"] == "in_progress"
    assert body["priority"] == "high"
    assert body["due_date"] == "2026-08-20"
    assert body["id"]
    assert body["created_at"]
    assert body["updated_at"]


def test_list_tasks_returns_previously_created_task() -> None:
    client.post("/api/v1/tasks", json={"title": "First task"})

    response = client.get("/api/v1/tasks")

    assert response.status_code == 200

    body = response.json()
    assert len(body) == 1
    assert body[0]["title"] == "First task"
    assert body[0]["status"] == "todo"
    assert body[0]["priority"] == "medium"


def test_create_task_rejects_invalid_payload() -> None:
    response = client.post(
        "/api/v1/tasks",
        json={"title": "", "status": "blocked"},
    )

    assert response.status_code == 422


def test_get_task_returns_created_task() -> None:
    task = create_test_task()

    response = client.get(f"/api/v1/tasks/{task['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == task["id"]
    assert response.json()["title"] == "Original task"


def test_get_task_returns_not_found_for_unknown_id() -> None:
    response = client.get("/api/v1/tasks/00000000-0000-0000-0000-000000000000")

    assert response.status_code == 404
    assert response.json() == {
        "error": {
            "code": "resource_not_found",
            "message": "Task not found",
            
        }}


def test_update_task_changes_only_sent_fields() -> None:
    task = create_test_task()

    response = client.patch(
        f"/api/v1/tasks/{task['id']}",
        json={"priority": "high"},
    )

    assert response.status_code == 200

    body = response.json()
    assert body["title"] == "Original task"
    assert body["description"] == "Keep this description during a partial update."
    assert body["priority"] == "high"
    assert body["updated_at"] != task["updated_at"]


def test_update_task_returns_not_found_for_unknown_id() -> None:
    response = client.patch(
        "/api/v1/tasks/00000000-0000-0000-0000-000000000000",
        json={"title": "Does not exist"},
    )

    assert response.status_code == 404


def test_delete_task_removes_task() -> None:
    task = create_test_task()

    delete_response = client.delete(f"/api/v1/tasks/{task['id']}")

    assert delete_response.status_code == 204
    assert delete_response.content == b""

    get_response = client.get(f"/api/v1/tasks/{task['id']}")
    assert get_response.status_code == 404


def test_delete_task_returns_not_found_for_unknown_id() -> None:
    response = client.delete("/api/v1/tasks/00000000-0000-0000-0000-000000000000")

    assert response.status_code == 404