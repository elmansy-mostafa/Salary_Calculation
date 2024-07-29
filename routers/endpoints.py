from fastapi import APIRouter, HTTPException
from typing import Optional, List
from datetime import date
from Salary_Calculation.crud import get_employee, update_employee, delete_employee, get_all_employee, create_daily_report, update_daily_report, get_daily_report, delete_daily_report, get_all_daily_reports, get_daily_report_by_employee_and_date, get_daily_reports_by_employee_and_range_date
from Salary_Calculation.schemas import EmployeeCreate, EmployeeUpdate, EmployeeResponse, DailyReportCreate, DailyReportUpdate, DailyReportResponse


router = APIRouter()

# Employee endpoints

@router.post("/employees", response_model=EmployeeResponse)
async def create_employee_endpoint(employee:EmployeeCreate):
    create_employee = await create_employee(employee)
    return create_employee

@router.get("/employees/{employee_id}", response_model=EmployeeResponse)
async def get_employee_endpoint(employee_id:int):
    employee  = await get_employee(employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@router.put("/employees/{employee_id}", response_model=EmployeeResponse)
async def update_employee_endpoint(employee_id:int, employee_update:EmployeeUpdate):
    updated_employee = await update_employee(employee_id, employee_update.dict(exclude_unset=True))
    if not updated_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return updated_employee

@router.delete("/employees/{employee_id}", response_model=bool)
async def delete_employee_endpoint(employee_id:int):
    deleted = await delete_employee(employee_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Employee not found")
    return deleted

@router.get("/employees", response_model=list[EmployeeResponse])
async def get_all_employees_endpoint():
    employees = await get_all_employee()
    return employees

# daily_reports endpoints

@router.post("/daily_reports", response_model=DailyReportResponse)
async def create_daily_report_endpoint(report:DailyReportCreate):
    create_report = await create_daily_report(report)
    return create_report

@router.get("/daily_reports/{report_id}", response_model=DailyReportResponse)
async def get_daily_report_endpoint(report_id:int):
    report = await get_daily_report(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Daily report not found")
    return report
        
@router.put("/daily_reports/{report_id}", response_model=DailyReportResponse)
async def update_daily_report_endpoint(report_id:int, update_report:DailyReportUpdate):
    updated_report = await update_daily_report(report_id, update_report.dict(exclude_unset=True))
    if not updated_report:
        raise HTTPException(status_code=404, detail="Daily report not found")
    return updated_report

@router.delete("/daily_reports/{report_id}", response_model=bool)
async def delete_daily_report_endpoint(report_id):
    deleted = await delete_daily_report(report_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Daily report not found")
    return deleted

@router.get("/daily_reports", response_model=list[DailyReportResponse])
async def get_all_daily_reports_endpoints():
    reports = await get_all_daily_reports()
    return reports

@router.get("/daily_reports/{report_id}/daily_reports", response_model=list[DailyReportResponse])
async def get_daily_reports_by_employee_and_renage_date_endpoint(employee_id:int, start_date:Optional[date], end_date:Optional[date]):
    reports = await get_daily_reports_by_employee_and_range_date(employee_id, start_date, end_date)
    return reports


@router.get("/daily_reports/{report_id}/daily_reports/{report_date}", response_model=DailyReportResponse)
async def get_daily_report_for_employee_endpoint(employee_id:int, report_date:date):
    report = await get_daily_report_by_employee_and_date(employee_id, report_date)
    if not report:
        raise HTTPException(status_code=404, detail="Daily report not found for this employee on the specific date")
    return report