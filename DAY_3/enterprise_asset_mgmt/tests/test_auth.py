import pytest
from fastapi.testclient import TestClient
from app.main import app
from database.session import get_db, SessionLocal
from database.base import Base
from database.session import engine

client = TestClient(app)

@pytest.fixture(scope="module")
def db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

def test_login_invalid_credentials():
    response = client.post("/auth/login", data={"username": "wrong@email.com", "password": "wrongpassword"})
    assert response.status_code == 401
