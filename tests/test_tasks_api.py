import os
from pathlib import Path

import pytest

from app import create_app
from config import Config
from extensions import db
from models import Task

BASE_DIR = Path(__file__).resolve().parent
TEST_DB = BASE_DIR / "test_tasks.db"


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{TEST_DB.resolve().as_posix()}"
    SECRET_KEY = "test-secret"


@pytest.fixture(autouse=True)
def clean_database():
    if TEST_DB.exists():
        TEST_DB.unlink()
    yield
    if TEST_DB.exists():
        TEST_DB.unlink()


@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.engine.dispose()


@pytest.fixture
def client(app):
    return app.test_client()


def test_get_empty_tasks(client):
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.get_json() == []


def test_create_task(client):
    payload = {"title": "Buy groceries", "description": "Eggs, milk, bread"}
    response = client.post("/tasks", json=payload)

    assert response.status_code == 201
    data = response.get_json()
    assert data["title"] == "Buy groceries"
    assert data["description"] == "Eggs, milk, bread"
    assert data["completed"] is False
    assert "created_at" in data


def test_get_task_by_id(client):
    create = client.post("/tasks", json={"title": "Read book"})
    task_id = create.get_json()["id"]

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.get_json()["title"] == "Read book"


def test_update_task(client):
    create = client.post("/tasks", json={"title": "Write tests"})
    task_id = create.get_json()["id"]

    response = client.put(
        f"/tasks/{task_id}",
        json={"description": "Add API coverage", "completed": True},
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["completed"] is True
    assert data["description"] == "Add API coverage"


def test_delete_task(client):
    create = client.post("/tasks", json={"title": "Clean room"})
    task_id = create.get_json()["id"]

    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.get_json()["message"] == "Task deleted successfully."

    missing = client.get(f"/tasks/{task_id}")
    assert missing.status_code == 404


def test_create_task_validation(client):
    response = client.post("/tasks", json={"description": "No title"})
    assert response.status_code == 400
    assert response.get_json()["error"] == "Task title is required."
