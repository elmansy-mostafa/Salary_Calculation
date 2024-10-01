import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock, MagicMock
from src.main import app
from src.modules.auth.authentication import create_access_token

client = TestClient(app)

@pytest.mark.asyncio
@patch("src.services.exportPdf.generate_salary_pdf", return_value=b"%PDF-1.4 mock content")  # Mock PDF generation
@patch("src.modules.employees.employees_crud.get_employee", new_callable=AsyncMock)
@patch("src.config.database.database.daily_report_collection.find", new_callable=AsyncMock)
@patch("src.services.exportPdf.get_static_values", new_callable=AsyncMock)
async def test_generate_salary_pdf_endpoint(mock_get_static_values, mock_daily_report_find, mock_get_employee, mock_generate_salary_pdf):
    # Mock employee data
    mock_employee = MagicMock()
    mock_employee.name = 'John Doe'
    mock_employee.position = 'Developer'
    mock_get_employee.return_value = mock_employee

    # Mock static values
    mock_static_values = MagicMock()
    mock_static_values.hour_price = {'A': 10}
    mock_static_values.no_of_qulified_appt_tier_setter = {'A': 5}
    mock_static_values.kpis = 100
    mock_static_values.allowance = {"travel": 50}
    mock_static_values.tier_base_salary = {'A': 5000}
    mock_static_values.cad = 1.5
    mock_static_values.butter_up = 10
    mock_get_static_values.return_value = mock_static_values

    # Mock daily reports
    mock_daily_reports = [
        {
            "employee_id": 1,
            "date": "2024-09-01",
            "adherence_status": True,
            "working_hours": 9,
            "is_saturday": False,
            "appointment": {"no_of_qualified_appointment": 3},
            "compensation": {"kpis": 100, "spiffs": 50, "butter_up": 5},
            "deductions": {"deductions": 0, "reason": ""}
        }
    ]
    mock_daily_report_find.return_value.to_list.return_value = mock_daily_reports
    
    with patch('src.modules.auth.authorizations.get_admin', return_value={"email": "admin@example.com", "role": "admin"}):      
        token = create_access_token({"sub": "admin@example.com", "role": "admin"})
        # Make the request to the endpoint
        response = client.get(
                "/generate_salary_pdf/1/1",
                headers={"Authorization": f"Bearer {token}"}
            )

        # Assertions
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"
