import pytest
from fastapi.testclient import TestClient
from src.main import app
from datetime import datetime

client = TestClient(app)

@pytest.mark.asyncio
async def test_create_daily_report():
    report_data = {"employee_id": 1, "date": datetime.utcnow().isoformat(), "hours_worked": 8, "compensation": 100}
    response = client.post("/daily_reports", json=report_data)
    assert response.status_code == 200
    assert response.json()["employee_id"] == 1

@pytest.mark.asyncio
async def test_get_daily_report():
    today = datetime.utcnow().isoformat()
    response = client.get(f"/daily_reports/1/daily_reports/{today}")
    assert response.status_code == 200
    assert response.json()["employee_id"] == 1

@pytest.mark.asyncio
async def test_update_daily_report():
    today = datetime.utcnow().isoformat()
    update_data = {"hours_worked": 10}
    response = client.put(f"/daily_reports/1/daily_reports/{today}", json=update_data)
    assert response.status_code == 200
    assert response.json()["hours_worked"] == 10

@pytest.mark.asyncio
async def test_delete_daily_report():
    today = datetime.utcnow().isoformat()
    response = client.delete(f"/daily_reports/1/daily_reports/{today}")
    assert response.status_code == 200
    assert response.json() == True