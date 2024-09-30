from typing import Optional, List
from datetime import datetime
from shared.models_schemas.models import DailyReport
from config.database.database import daily_report_collection
import os
from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'env', '.env')
load_dotenv(dotenv_path)


# CRUD operations for daily_report        

async def create_daily_report(report:DailyReport ) -> DailyReport:    
    report_dict = report.model_dump()
    if os.getenv("TESTING") == "True":
        daily_report_collection.insert_one(report_dict)
    else:
        await daily_report_collection.insert_one(report_dict)
    return report


async def get_daily_report(employee_id:int, report_date:datetime) -> Optional[DailyReport]:
    if os.getenv("TESTING") == "True":
        report_data = daily_report_collection.find_one({"employee_id":employee_id, "date":report_date})
    else:
        report_data =await daily_report_collection.find_one({"employee_id":employee_id, "date":report_date})
    if report_data:
        return DailyReport(**report_data)
    return None

async def update_daily_report(employee_id:int, report_date:datetime, update_data:dict) -> Optional[DailyReport]:
    if os.getenv("TESTING") == "True":
        updated_report = daily_report_collection.find_one_and_update(
            {"employee_id" : employee_id, "date" : report_date},
            {"$set" : update_data},
            return_document = True
        )
    else:
        updated_report = await daily_report_collection.find_one_and_update(
            {"employee_id" : employee_id, "date" : report_date},
            {"$set" : update_data},
            return_document = True
        )
    if updated_report:
        return DailyReport(**updated_report)
    return None

async def delete_daily_report(employee_id:int, report_date:datetime) -> bool:
    if os.getenv("TESTING") == "True":
        result = daily_report_collection.delete_one({"employee_id":employee_id, "date":report_date})
    else:
        result = await daily_report_collection.delete_one({"employee_id":employee_id, "date":report_date})
    if result:
        return True
    return False

async def get_all_daily_reports() -> List[DailyReport]:
    if os.getenv("TESTING") == "True":
        reports = list(daily_report_collection.find({}))
        return [DailyReport(**report_data) for report_data in reports]
    else:
        report_cursor = daily_report_collection.find({})
        reports = await report_cursor.to_list(length=None)
        return [DailyReport(**report_data) for report_data in reports]

# get dailyreport by specific employee and range date
async def get_daily_reports_by_employee_and_range_date(employee_id:int, start_date:Optional[datetime], end_date:Optional[datetime]) -> List[DailyReport]:
    query = {"employee_id" : employee_id}
    if start_date and end_date:
        query["date"] = {"$gte":start_date, "$lte":end_date}
    elif start_date:
        query["date"] = {"$gte":start_date}
    elif end_date:
        query["date"] = {"$lte":end_date}
        
    if os.getenv("TESTING") == "True":
        reports = list(daily_report_collection.find(query))
        return [DailyReport(**report_data) for report_data in reports]
    else:
        cursor = daily_report_collection.find(query)
        reports = await cursor.to_list(length=None)
        return [DailyReport(**report) for report in reports]

