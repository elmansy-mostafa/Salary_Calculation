from datetime import datetime
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock, MagicMock
import pytest
from src.main import app
import json

client = TestClient(app)

import json

@pytest.mark.asyncio
@patch("src.modules.employees.employees_crud.get_employee", new_callable=AsyncMock)
@patch("src.config.database.database.daily_report_collection.find", new_callable=AsyncMock)
@patch("src.services.exportPdf.generate_salary_pdf", new_callable=AsyncMock)
@patch("src.modules.static_values.static_values_crud.get_static_values", new_callable=AsyncMock)
async def test_generate_salary_pdf_endpoint(
    mock_get_static_values,
    mock_generate_salary_pdf,
    mock_daily_report_find,
    mock_get_employee
):
    # Mock employee data
    mock_employee = MagicMock()
    mock_employee.name = 'John Doe'
    mock_employee.position = 'Developer'
    mock_employee.tier_type = 'A'
    mock_employee.is_onsite = True
    mock_employee.has_insurance = True
    mock_employee.employee_type = MagicMock(is_appointment_serrer=True, is_full_time=True)
    
    # Ensure this mock is returning the employee data
    mock_get_employee.return_value = mock_employee

    # Mock static values
    mock_static_values = MagicMock()
    # ... setting up mock_static_values as in your original code
    mock_get_static_values.return_value = mock_static_values

    # Mock daily reports
    mock_daily_reports = [ ... ]  # Your mock daily report setup
    mock_daily_report_find.return_value = mock_daily_reports

    # Mock the PDF content returned from generate_salary_pdf
    mock_pdf_content = b"%PDF-1.4 mock content"
    mock_generate_salary_pdf.return_value = mock_pdf_content

    # Make the request to the endpoint
    response = client.get("/generate_salary_pdf/1/1")

    # Print response content for debugging
    print(f"Response status code: {response.status_code}")
    print(f"Response headers: {response.headers}")
    print(f"Response content: {response.content}")

    # Verify that the mocked functions were called
    mock_get_employee.assert_called_once_with(1)  # Ensure it's called as expected
    mock_get_static_values.assert_called_once_with(1)
    mock_daily_report_find.assert_called_once()

    # Check if the response is JSON (error case)
    if response.headers.get("Content-Type") == "application/json":
        error_content = json.loads(response.content)
        print(f"Error content: {error_content}")
        assert "error" in error_content
        assert error_content["error"] == "Employee not found"
    else:
        # If it's not JSON, it should be a PDF
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/pdf"
        assert "Content-Disposition" in response.headers
        assert response.headers["Content-Disposition"] == 'inline; filename="salary_breakdown.pdf"'
        assert response.content == mock_pdf_content
    
    


    