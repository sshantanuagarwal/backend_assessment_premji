import pytest
from fastapi.testclient import TestClient
from assessment_app.main import app

client = TestClient(app)

@pytest.fixture
def test_user():
    return {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword"
    }

def test_register_user(test_user):
    response = client.post("/register", json=test_user)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == test_user["username"]
    assert data["email"] == test_user["email"]
    assert "id" in data
    assert "created_at" in data

def test_login_user(test_user):
    # First register the user
    client.post("/register", json=test_user)
    
    # Then try to login
    response = client.post("/login", data={
        "username": test_user["email"],
        "password": test_user["password"]
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
