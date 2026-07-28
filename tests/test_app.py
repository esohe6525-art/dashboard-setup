import os
from pathlib import Path

import pytest

TEST_DB = Path("tests/test_app.db")
if TEST_DB.exists():
    TEST_DB.unlink()
os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DB}"

from app import app
from models import SessionLocal, User


@pytest.fixture
def client():
    app.config.update(TESTING=True)
    with app.test_client() as client:
        yield client


def test_index_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Welcome to john.com" in response.data


def test_register_page(client):
    response = client.get("/auth/register")
    assert response.status_code == 200


def test_login_page(client):
    response = client.get("/auth/login")
    assert response.status_code == 200


def test_register_and_login_store_user(client):
    response = client.post(
        "/auth/register",
        data={"username": "alice", "password": "secret123"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Account created successfully" in response.data

    session = SessionLocal()
    user = session.query(User).filter(User.username == "alice").first()
    session.close()

    assert user is not None
    assert user.username == "alice"

    login_response = client.post(
        "/auth/login",
        data={"username": "alice", "password": "secret123"},
        follow_redirects=True,
    )
    assert login_response.status_code == 200
    assert b"Login successful" in login_response.data
