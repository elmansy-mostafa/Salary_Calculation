from typing import Optional, List
from datetime import datetime
from Salary_Calculation.models import DailyReport, Employee, SalaryCalculator
from Salary_Calculation.database import employee_collection, daily_report_collection

# CRUD operations for employee

async def create_employee(employee : Employee) -> Employee:
    employee_dict = employee.dict()
    await employee_collection.insert_one(employee_dict)
    return employee

async def get_employee(employee_id : int) -> Optional[Employee]:
    employee_data = await employee_collection.find_one({"id":employee_id})
    if employee_data:
        return Employee(**employee_data)
    return None

async def update_employee(employee_id:int, update_data:dict) -> Optional[Employee]:
    updated_employee = await employee_collection.find_one_and_update(
        {"id" : employee_id},
        {"$set" : update_data},
        return_document = True
    )
    if updated_employee:
        return Employee(**updated_employee)
    return None

async def delete_employee(employee_id : int) -> bool:
    result = await employee_collection.delete_one({"id":employee_id})
    return result.deleted_count == 1


async def get_all_employee() -> List[Employee]:
    employee_sursor = employee_collection.find({})
    employees = await employee_sursor.to_list(length=None)
    return [Employee(**employee_data) for employee_data in employees]

# CRUD operations for daily_report        

async def create_daily_report(report:DailyReport) -> DailyReport:
    report_dict = report.dict()
    await daily_report_collection.insert_one(report_dict)
    return report

async def get_daily_report(employee_id:int, report_date:datetime) -> Optional[DailyReport]:
    report_data =await daily_report_collection.find_one({"employee_id":employee_id, "date":report_date})
    if report_data:
        return DailyReport(**report_data)
    return None

async def update_daily_report(employee_id:int, report_date:datetime, update_data:dict) -> Optional[DailyReport]:
    updated_report = await daily_report_collection.find_one_and_update(
        {"employee_id" : employee_id, "date" : report_date},
        {"$set" : update_data},
        return_document = True
    )
    if updated_report:
        return DailyReport(**updated_report)
    return None

async def delete_daily_report(employee_id:int, report_date:datetime) -> bool:
    result = await daily_report_collection.delete_one({"employee_id":employee_id, "date":report_date})
    return result.deleted_count == 1

async def get_all_daily_reports() -> List[DailyReport]:
    report_cursor = daily_report_collection.find({})
    reports = await report_cursor.to_list(length=None)
    return [DailyReport(**report_data) for report_data in reports]

# get dailyreport by specific employee and range date
async def get_daily_reports_by_employee_and_range_date(employee_id:int, start_date:Optional[datetime], end_date:Optional[datetime]) -> list[DailyReport]:
    query = {"employee_id" : employee_id}
    if start_date and end_date:
        query["date"] = {"$gte":start_date, "$lte":end_date}
    elif start_date:
        query["date"] = {"$gte":start_date}
    elif end_date:
        query["date"] = {"$lte":end_date}
    cursor = daily_report_collection.find(query)
    reports = await cursor.to_list(length=None)
    return [DailyReport(**report) for report in reports]


async def calculate_daily_report_salary(employee_id:int, report_date:datetime) -> float:
    query = {
        "employee_id" : employee_id,
        "date" : report_date
    }
    report_data = await daily_report_collection.find_one(query)
    if not report_data:
        return None
    report = DailyReport(**report_data)
    total_salary = SalaryCalculator.calculate_salary(report)
    return total_salary
    