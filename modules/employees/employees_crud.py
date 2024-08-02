from typing import Optional, List
from Salary_Calculation.shared.models_schemas.models import Employee
from Salary_Calculation.config.database.database import employee_collection



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