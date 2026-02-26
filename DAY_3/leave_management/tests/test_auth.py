from fastapi.testclient import TestClient
from app.main import app
import pytest

client = TestClient(app)

def test_register_user():
    response = client.post(
        "/auth/register",
        json={"name": "Test User", "email": "test@example.com", "password": "password123", "role": "EMPLOYEE"}
    )
    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"

def test_login_user():
    # Login with the registered user
    response = client.post(
        "/auth/login",
        data={"username": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_invalid_login():
    response = client.post(
        "/auth/login",
        data={"username": "test@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401
