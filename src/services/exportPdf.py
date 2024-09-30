from datetime import datetime, timezone
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from fastapi import HTTPException
from fastapi import Response, APIRouter
from modules.employees.employees_crud import get_employee
from config.database.database import daily_report_collection
from modules.static_values.static_values_crud import get_static_values

import os

def generate_salary_pdf(salary_data: dict) -> bytes:
    
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
    # Get the current month and year
    now = datetime.now(timezone.utc)
    start_of_month = datetime(now.year, now.month, 1)  # First day of the current month
    next_month = datetime(now.year, now.month + 1, 1) if now.month < 12 else datetime(now.year + 1, 1, 1)  # First day of the next month

    # Query to get only reports for the current month
    if os.getenv("TESTING") == "True":
        daily_reports = await daily_report_collection.find({
            "employee_id": employee_id,
            "date": {
                "$gte": start_of_month,   
                "$lt": next_month         
            }
        })
    else:
        daily_reports = await daily_report_collection.find({
            "employee_id": employee_id,
            "date": {
                "$gte": start_of_month,   # Greater than or equal to the first day of the current month
                "$lt": next_month         # Less than the first day of the next month
            }
        }).to_list(length=None)
    
    if daily_reports is None:
        return{"error":"daily report not found for employee"}
    
    employee = await get_employee(employee_id)
    if employee is None:
        return {"error": "Employee not found"}
    
    static_values = await get_static_values(values_id)
    
    # Prepare list of absent with dates
    absent_info = []
    absent_count = 0
    for report in daily_reports:
        if report.get("adherence_status", 0) == False:
            date_str = report["date"].strftime("%Y-%m-%d")
            date_name = report["date"].strftime("%A")
            absent_info.append(f"In {date_name} {date_str} : absent ")
            absent_count += 1 

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
            date_name = report["date"].strftime("%A")
            missing_hours_info.append(f"In {date_name} {date_str} : {missing_hours} hrs missing")
            
        if report.get("working_hours", 0) > 9 :
            additional_hours = report["working_hours"] - 9
            additional_hours_value = additional_hours_value + (additional_hours * static_values.hour_price[employee.tier_type])
            date_str = report["date"].strftime("%Y-%m-%d")
            date_name = report["date"].strftime("%A")
            additional_hours_info.append(f"In {date_name} {date_str} : {additional_hours} hrs over : (double paid)")
    
    # Prepare list of working in saturdays
    saturdays = []
    saturdays_value = 0
    for report in daily_reports:
        if report.get("is_saturday", 0) == True:
            date_str = report["date"].strftime("%Y-%m-%d")
            hours = report["working_hours"]
            saturdays_value = saturdays_value + (hours * static_values.hour_price[employee.tier_type])
            saturdays.append(f"working on saturday {date_str} for {hours} hours : (double paid)")

    # Prepare list of kpis in compensation
    kpis = []
    kpis_values = 0
    kpis_amount = 0  

    for report in daily_reports:
        no_of_qulified_app = report.get("appointment", {}).get("no_of_qualified_appointment", 0)
        kpis_values += no_of_qulified_app
        kpis_amount += report.get("compensation", {}).get("kpis", 0)
        date_str = report["date"].strftime("%Y-%m-%d")
        date_name = report["date"].strftime("%A")
        kpis.append(f"Making {no_of_qulified_app} qualified appointments on {date_name} {date_str}")
        
        # Ensure that compensation and kpi information exist in each report before accessing them
    if employee.employee_type.is_appointment_serrer == True:
        if kpis_values >= static_values.no_of_qulified_appt_tier_setter[employee.tier_type] * 30:
            kpis_total = kpis_amount * static_values.kpis
    else:
        if kpis_values >= static_values.no_of_qulified_appt_tier_fronter[employee.tier_type] * 30:
            kpis_total = kpis_amount * static_values.kpis
            
    # Prepare list of spiffs in compensation
    spiffs_list = []
    spiffs_values = 0
    for report in daily_reports:
        spiffs = report.get("compensation", {}).get("spiffs", 0)
        spiffs_values += spiffs
        date_str = report["date"].strftime("%Y-%m-%d")
        date_name = report["date"].strftime("%A")
        spiffs_list.append(f"In {date_name} {date_str} has {spiffs} spiffs")
    

    # Prepare list of transportation allowance data 
    count = 0
    for report in daily_reports:
        if report.get("adherence_status", 0) == True:
            count += 1 
    if count == 0:
        transportation_allowance = 0
    else:
        allowance_sum = count * static_values.allowance["travel"]
        transportation_allowance = f"{count} Days * {static_values.allowance["travel"]} EGP = {allowance_sum}"
            
    
    # Prepare list of deductions
    deductions_info = []
    deductions_values = 0
    for report in daily_reports:
        if report.get("deductions", {}).get("deductions", 0) !=0:
            deduction = report.get("deductions", {}).get("deductions", 0)
            reason = report.get("deductions", {}).get("reason", 0)
            deductions_values += deduction
            date_str = report["date"].strftime("%Y-%m-%d")
            date_name = report["date"].strftime("%A")
            deductions_info.append(f"In {date_name} {date_str} has {deduction} deduction for the reason of: {reason}")
        else:
            deductions_values = 0
            
    # Prepare list of butterup in compensation
    butter_up_values = 0
    for report in daily_reports:
        butter_up = report.get("compensation", {}).get("butter_up", 0)
        butter_up_values += butter_up
    butter_up_total = butter_up_values * static_values.butter_up
            
    # basic salary
    basic_salary = static_values.tier_base_salary[employee.tier_type]
    basic_salary_deduction_absent = absent_count * (static_values.tier_base_salary[employee.tier_type] / 30)
    basic_salary_deduction_missing_hours =  static_values.hour_price[employee.tier_type] * sum
    final_salary = basic_salary - basic_salary_deduction_absent - basic_salary_deduction_missing_hours
    
    # overpay
    overpay_summary =  saturdays_value * 2 
    additional_hours = additional_hours_value * 2
    total_spiffs = spiffs_values * 2 * static_values.cad
        

    # total salary
    total_salary = final_salary + overpay_summary + additional_hours + kpis_total + total_spiffs + allowance_sum + deductions_values + butter_up_total
    

    
    # Prepare salary data dictionary
    salary_data = {
        "name": employee.name,
        "position":employee.position,
        "tier_type":employee.tier_type,
        "is_onsite":employee.is_onsite,
        "has_insurance":employee.has_insurance,
        "is_appointment_serrer":employee.employee_type.is_appointment_serrer,
        "is_full_time":employee.employee_type.is_full_time,
        "name": employee.name,
        "month": now.strftime("%m"),
        "month_name": now.strftime("%B"),
        "year": now.strftime("%Y"),
        "basic_salary" :basic_salary, 
        "basic_salary_deduction_absent":basic_salary_deduction_absent,
        "basic_salary_deduction_missing_hours": basic_salary_deduction_missing_hours ,
        "final_salary": final_salary,
        "no_show_days": "<br>".join(absent_info), 
        "missing_hours": "<br>".join(missing_hours_info),
        "saturdays": "<br>".join(saturdays),
        "overpay_summary": overpay_summary,
        "additional_hours": "<br>".join(additional_hours_info),
        "additional_hours_value": additional_hours,
        "kpis_score": "<br>".join(kpis),
        "kpis_total": kpis_total,
        "spiffs_logs": "<br>".join(spiffs_list),
        "spiffs_total": total_spiffs,
        "transportation_allowance": transportation_allowance,
        "deductions_info": "<br>".join(deductions_info),
        "deductions": deductions_values,
        "butter_up": butter_up_total,
        "total_salary": total_salary,
        

    }

    # Generate PDF using the service function
    pdf = generate_salary_pdf(salary_data)

    # Return the PDF as a response
    headers = {'Content-Disposition': 'inline; filename="salary_breakdown.pdf"'}
    return Response(content=pdf, media_type="application/pdf", headers=headers)