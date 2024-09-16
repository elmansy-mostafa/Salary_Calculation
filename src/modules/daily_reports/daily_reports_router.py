from datetime import datetime
from fastapi import APIRouter
from typing import List, Optional
from shared.models_schemas.schemas import DailyReportCreate, DailyReportResponse
from .daily_reports_controller import create_daily_report_control, get_daily_report_control, update_daily_report_control, delete_daily_report_control, get_all_daily_reports_control, get_daily_reports_by_employee_and_renage_date_control


router = APIRouter()


# daily_reports endpoints

@router.post("/daily_reports/static_values/{values_id}/employee/{employee_id}", response_model=DailyReportResponse)
async def create_daily_report_endpoint(report:DailyReportCreate, values_id:int, employee_id:int):
    return await create_daily_report_control(report, values_id, employee_id)



@router.get("/daily_reports/{employee_id}/daily_reports/{report_date}", response_model=DailyReportResponse)
async def get_daily_report_endpoint(employee_id:int, report_date:datetime):
    return await get_daily_report_control(employee_id, report_date)

        
@router.put("/daily_reports/{employee_id}/daily_reports/{report_date}", response_model=DailyReportResponse)
async def update_daily_report_endpoint(employee_id:int, report_date:datetime, update_report:dict):
    return await update_daily_report_control(employee_id, report_date,update_report) 

@router.delete("/daily_reports/{employee_id}/daily_reports/{report_date}", response_model=bool)
async def delete_daily_report_endpoint(employee_id:int, report_date:datetime):
    return await delete_daily_report_control(employee_id, report_date)

@router.get("/daily_reports", response_model=List[DailyReportResponse])
async def get_all_daily_reports_endpoints():
    return await get_all_daily_reports_control()


@router.get("/daily_reports/{employee_id}/daily_reports/{start_date}/{end_date}", response_model=list[DailyReportResponse])
async def get_daily_reports_by_employee_and_renage_date_endpoint(employee_id:int, start_date:Optional[datetime], end_date:Optional[datetime]):
    return await get_daily_reports_by_employee_and_renage_date_control(employee_id, start_date, end_date)

# @router.get("/employees/{employee_id}/daily_reports/{report_date}/salary", response_model=float)
# async def get_daily_report_salary_endpoint(employee_id:int, report_date:datetime):
#     return await get_daily_report_salary_control(employee_id, report_date)