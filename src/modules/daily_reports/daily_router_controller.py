from fastapi import HTTPException
from typing import Optional
from datetime import datetime
from .daily_reports_crud import create_daily_report, update_daily_report, get_daily_report, delete_daily_report, get_all_daily_reports, get_daily_reports_by_employee_and_range_date, calculate_daily_report_salary
from shared.models_schemas.schemas import DailyReportCreate, DailyReportUpdate


exception_error = HTTPException(status_code=404, detail="Daily report not found")

async def create_daily_report_control(report:DailyReportCreate):
    create_report = await create_daily_report(report)
    return create_report


async def get_daily_report_control(employee_id:int, report_date:datetime):
    report = await get_daily_report(employee_id, report_date)
    if not report:
        raise exception_error
    return report


async def update_daily_report_control(employee_id:int, report_date:datetime, update_report:DailyReportUpdate):
    updated_report = await update_daily_report(employee_id, report_date, update_report.dict(exclude_unset=True))
    if not updated_report:
        raise exception_error
    return updated_report



async def delete_daily_report_control(employee_id:int, report_date:datetime):
    deleted = await delete_daily_report(employee_id, report_date)
    if not deleted:
        raise exception_error
    return deleted


async def get_all_daily_reports_control():
    reports = await get_all_daily_reports()
    return reports


async def get_daily_reports_by_employee_and_renage_date_control(employee_id:int, start_date:Optional[datetime], end_date:Optional[datetime]):
    reports = await get_daily_reports_by_employee_and_range_date(employee_id, start_date, end_date)
    return reports


async def get_daily_report_salary_control(employee_id:int, report_date:datetime):
    total_salary = await calculate_daily_report_salary(employee_id, report_date)
    if not total_salary:
        raise exception_error
    return total_salary
