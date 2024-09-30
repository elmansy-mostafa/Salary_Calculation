from datetime import datetime
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock, MagicMock
import pytest
from src.main import app

client = TestClient(app)

@pytest.mark.asyncio
@patch("src.modules.employees.employees_crud.get_employee", new_callable=AsyncMock)
@patch("src.config.database.database.daily_report_collection.find", new_callable=AsyncMock)
@patch("src.services.exportPdf.generate_salary_pdf", new_callable=AsyncMock)
async def test_generate_salary_pdf_endpoint(mock_generate_salary_pdf, mock_daily_report_find, mock_get_employee):
    # Mock employee data
    mock_employee = MagicMock()
    mock_employee.name = 'John Doe'
    mock_employee.position = 'Developer'
    mock_get_employee.return_value = mock_employee

    # Mock daily reports
    mock_daily_reports = [MagicMock(date=datetime(2024, 9, 1)), MagicMock(date=datetime(2024, 9, 2))]
    mock_daily_report_find.return_value.to_list.return_value = mock_daily_reports

    # Mock the PDF content returned from generate_salary_pdf
    mock_pdf_content = b"%PDF-1.4 mock content"
    mock_generate_salary_pdf.return_value = mock_pdf_content

    # Make the request to the endpoint
    response = client.get("/generate_salary_pdf/1/1")

    # Assertions
    assert response.status_code == 200
    assert response.headers["Content-Disposition"] == 'inline; filename="salary_breakdown.pdf"'
    assert response.content == mock_pdf_content  # Check if the PDF content is as expected