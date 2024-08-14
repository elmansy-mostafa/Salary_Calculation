import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

@pytest.mark.asyncio
async def test_create_employee():
    employee_data = {"id": 1, "name": "John Doe", "position": "Developer", "salary": 50000}
    response = client.post("/employees", json=employee_data)
    assert response.status_code == 200
    assert response.json()["id"] == 1

@pytest.mark.asyncio
async def test_get_employee():
    response = client.get("/employees/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

@pytest.mark.asyncio
async def test_update_employee():
    employee_update = {"name": "John Doe Updated", "salary": 60000}
    response = client.put("/employees/1", json=employee_update)
    assert response.status_code == 200
    assert response.json()["name"] == "John Doe Updated"

@pytest.mark.asyncio
async def test_delete_employee():
    response = client.delete("/employees/1")
    assert response.status_code == 200
    assert response.json() == True