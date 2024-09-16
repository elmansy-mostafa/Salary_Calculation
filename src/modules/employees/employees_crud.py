from typing import Optional, List
from shared.models_schemas.models import Employee
from config.database.database import employee_collection
import os
from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'env', '.env')
load_dotenv(dotenv_path)

# CRUD operations for employee

async def create_employee(employee : Employee) -> Employee:
    employee_dict = employee.model_dump()
    if os.getenv("TESTING") == "True":
        employee_collection.insert_one(employee_dict)
    else:
        await employee_collection.insert_one(employee_dict)        
    return employee

async def get_employee(employee_id: int) -> Optional[Employee]:
    if os.getenv("TESTING") == "True":
        # Use synchronous find_one for tests
        employee_data = employee_collection.find_one({"id": employee_id})
    else:
        # Use asynchronous find_one for production
        employee_data = await employee_collection.find_one({"id": employee_id})

    if employee_data:
        return Employee(**employee_data)
    return None


async def update_employee(employee_id:int, update_data:dict) -> Optional[Employee]:
    if os.getenv("TESTING") == "True":
        updated_employee = employee_collection.find_one_and_update(
            {"id" : employee_id},
            {"$set" : update_data},
            return_document = True
        )
    else:
        updated_employee = await employee_collection.find_one_and_update(
            {"id" : employee_id},
            {"$set" : update_data},
            return_document = True
        )
    if updated_employee:
        return Employee(**updated_employee)
    return None

async def delete_employee(employee_id : int) -> bool:
    if os.getenv("TESTING") == "True":
        result = employee_collection.delete_one({"id":employee_id})
    else:
        result = await employee_collection.delete_one({"id":employee_id})
    if result:
        return True
    return False



async def get_all_employee() -> List[Employee]:
    if os.getenv("TESTING") == "True":
        employees = list(employee_collection.find({})) 
        return [Employee(**employee) for employee in employees]
    else:
        employee_cursor = employee_collection.find({})
        employees = await employee_cursor.to_list(length=None)
        return [Employee(**employee_data) for employee_data in employees]