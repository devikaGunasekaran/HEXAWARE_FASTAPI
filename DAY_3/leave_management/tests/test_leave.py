from fastapi.testclient import TestClient
from app.main import app
from datetime import date, timedelta

client = TestClient(app)

def get_token(email, password, role="EMPLOYEE"):
    # Register if not exists
    client.post(
        "/auth/register",
        json={"name": "User", "email": email, "password": password, "role": role}
    )
    # Login
    response = client.post(
        "/auth/login",
        data={"username": email, "password": password}
    )
    return response.json()["access_token"]

def test_employee_apply_leave():
    token = get_token("emp@example.com", "password123", "EMPLOYEE")
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.post(
        "/employee/apply-leave",
        json={
            "start_date": str(date.today() + timedelta(days=1)),
            "end_date": str(date.today() + timedelta(days=2)),
            "reason": "Sick Leave"
        },
        headers=headers
    )
    assert response.status_code == 200
    assert response.json()["status"] == "PENDING"

def test_unauthorized_access():
    token = get_token("emp2@example.com", "password123", "EMPLOYEE")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Try to access admin route
    response = client.get("/admin/leaves", headers=headers)
    assert response.status_code == 403
