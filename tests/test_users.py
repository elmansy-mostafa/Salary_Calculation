import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

@pytest.mark.asyncio
async def test_signup():
    user_data = {"email": "test@example.com", "password": "password", "role": "user"}
    response = client.post("/signup", json=user_data)
    assert response.status_code == 200
    assert response.json() == {"msg": "Please check your email to verify your account"}

@pytest.mark.asyncio
async def test_login():
    user_data = {"username": "test@example.com", "password": "password"}
    response = client.post("/signin", data=user_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()

@pytest.mark.asyncio
async def test_get_users():
    response = client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)