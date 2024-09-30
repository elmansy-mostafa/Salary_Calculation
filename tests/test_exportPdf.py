import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from weasyprint import HTML
from src.main import app  # Replace with your actual app import
from src.services.exportPdf import generate_salary_pdf

client = TestClient(app)

# Mock data for employee and static values
mock_employee = {
    "employee_id": 1,
    "name": "John Doe",
    "position": "Developer",
    "tier_type": "A",
    "is_onsite": True,
    "has_insurance": True,
    "employee_type": {"is_appointment_serrer": True, "is_full_time": True}
}

mock_static_values = {
    "hour_price": {"A": 50},
    "no_of_qulified_appt_tier_setter": {"A": 5},
    "allowance": {"travel": 20},
    "kpis": 100,
    "tier_base_salary": {"A": 3000},
    "butter_up": 10
}

mock_daily_reports = [
    {"date": "2024-09-01", "adherence_status": True, "working_hours": 9, "is_saturday": False},
    {"date": "2024-09-02", "adherence_status": False, "working_hours": 7, "is_saturday": True},
]

@pytest.mark.asyncio
@patch("modules.salary.get_employee", return_value=mock_employee)
@patch("modules.salary.get_static_values", return_value=mock_static_values)
@patch("config.database.database.daily_report_collection.find")
@patch("weasyprint.HTML.write_pdf")
async def test_generate_salary_pdf_endpoint(mock_write_pdf, mock_find, mock_get_employee, mock_get_static_values):
    # Mock the daily report collection find query
    mock_find.return_value.to_list = MagicMock(return_value=mock_daily_reports)

    # Mock the PDF generation
    mock_write_pdf.return_value = b"%PDF-1.4 mock content"

    # Make the request to the endpoint
    response = client.get("/generate_salary_pdf/1/1")

    # Assertions

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/pdf"
    assert "Content-Disposition" in response.headers
    assert response.headers["Content-Disposition"] == 'inline; filename="salary_breakdown.pdf"'
    assert response.content == b"%PDF-1.4 mock content"

@patch("weasyprint.HTML.write_pdf")
def test_generate_salary_pdf(mock_write_pdf):
    # Mock the PDF generation
    mock_write_pdf.return_value = b"%PDF-1.4 mock content"

    # Example salary data
    salary_data = {
        "name": "John Doe",
        "position": "Developer",
        "tier_type": "A",
        "is_onsite": True,
        "has_insurance": True,
        "is_appointment_serrer": True,
        "is_full_time": True,
        "basic_salary": 3000,
        "final_salary": 2800,
        "total_salary": 3200
    }

    # Generate the PDF
    pdf = generate_salary_pdf(salary_data)

    # Assertions
    assert pdf == b"%PDF-1.4 mock content"

    