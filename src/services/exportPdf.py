from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from fastapi import HTTPException
from fastapi import Response, APIRouter
from modules.employees.employees_crud import get_employee
from config.database.database import daily_report_collection
from modules.static_values.static_values_crud import get_static_values
from modules.daily_reports.daily_reports_crud import get_daily_report

import os

def generate_salary_pdf(salary_data: dict) -> bytes:
    """
    Generates a PDF for salary breakdown using the provided salary data.
    
    :param salary_data: A dictionary containing the employee salary information
    :return: The generated PDF as bytes
    """
    try:
        # Set the path to the templates directory
        templates_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')

        # Initialize Jinja2 environment
        env = Environment(loader=FileSystemLoader(templates_dir))

        # Load the template
        template = env.get_template("salary_template.html")

        # Render the template with salary data
        html_content = template.render(**salary_data)

        # Convert HTML content to PDF
        pdf = HTML(string=html_content).write_pdf()

        return pdf
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating PDF: {str(e)}")
    
    
router = APIRouter()

@router.get("/generate_salary_pdf/{employee_id}/{values_id}")
async def generate_salary_pdf_endpoint(employee_id: int, values_id:int):
    # Fetch all daily reports for the specific employee
    daily_reports = await daily_report_collection.find({"employee_id": employee_id}).to_list(None)
    
    if daily_reports is None:
        return{"error":"daily report not found for employee"}
    
    employee = await get_employee(employee_id)
    if employee is None:
        return {"error": "Employee not found"}
    
    static_values = await get_static_values(values_id)
    
    # Prepare list of missing dates with dates
    missing_date_info = []
    count = 0
    for report in daily_reports:
        if report.get("adherence_status", 0) == False:
            date_str = report["date"].strftime("%Y-%m-%d")
            missing_date_info.append(f"In day {date_str} : absent ")
            count += 1 

    # Prepare list of missing hours with dates
    missing_hours_info = []
    additional_hours_info = []
    sum = 0
    additional_hours_value = 0
    for report in daily_reports:
        if report.get("working_hours", 0) < 9 and report.get("working_hours", 0) != 0:
            missing_hours = 9 - report["working_hours"]
            sum = sum + missing_hours
            date_str = report["date"].strftime("%Y-%m-%d")
            missing_hours_info.append(f"In day {date_str} : {missing_hours} hrs missing")
            
        if report.get("working_hours", 0) > 9 :
            additional_hours = report["working_hours"] - 9
            additional_hours_value = additional_hours_value + (additional_hours * static_values.hour_price[employee.tier_type])
            date_str = report["date"].strftime("%Y-%m-%d")
            additional_hours_info.append(f"In day {date_str} : {additional_hours} hrs over : (double paid)")
    
    # Prepare list of working in saturdays
    saturdays = []
    saturdays_value = 0
    for report in daily_reports:
        if report.get("is_saturday", 0) == True:
            date_str = report["date"].strftime("%Y-%m-%d")
            hours = report["working_hours"]
            saturdays_value = saturdays_value + (hours * static_values.hour_price[employee.tier_type])
            saturdays.append(f"working in: {date_str}, saturday for {hours} hours : (double paid)")
            
            
    # basic salary
    basic_salary = static_values.tier_base_salary[employee.tier_type]
    basic_salary_deduction_absent = count * (static_values.tier_base_salary[employee.tier_type] / 30)
    basic_salary_deduction_missing_hours =  static_values.hour_price[employee.tier_type] * sum
    final_salary = basic_salary - basic_salary_deduction_absent - basic_salary_deduction_missing_hours
    
    # overpay
    overpay_summary =  saturdays_value * 2 
    additional_hours = additional_hours_value * 2
    # Prepare salary data dictionary
    salary_data = {
        "name": employee.name,
        "basic_salary" :basic_salary, 
        "basic_salary_deduction_absent":basic_salary_deduction_absent,
        "basic_salary_deduction_missing_hours": basic_salary_deduction_missing_hours ,
        "final_salary": final_salary,
        "no_show_days": ", ".join(missing_date_info), 
        "missing_hours": ", ".join(missing_hours_info),
        "saturdays": ", ".join(saturdays),
        "overpay_summary": overpay_summary,
        "additional_hours": ", ".join(additional_hours_info),
        "additional_hours_value": additional_hours,
        "kpi_score": "63/91 and quality",
        "kpi_amount": "2000 EGP",
        "spiffs_summary": "47 CAD = 1648 EGP (4/1, One CAD equals 35.07)",
        "ramadan_allowance_summary": "13 days * 150 EGP = 1650 EGP",
        "transportation_allowance_summary": "45.45 EGP * 22 days = 1000 EGP",
        "deductions": "N/A",
        "butter_up": 500,
        "tier_type": "A",
        "appointment_target": 3
    }

    # Generate PDF using the service function
    pdf = generate_salary_pdf(salary_data)

    # Return the PDF as a response
    headers = {'Content-Disposition': 'inline; filename="salary_breakdown.pdf"'}
    return Response(content=pdf, media_type="application/pdf", headers=headers)