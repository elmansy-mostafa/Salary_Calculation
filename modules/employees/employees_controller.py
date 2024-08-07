from fastapi import HTTPException
from .employees_crud import  create_employee, get_employee, update_employee, delete_employee, get_all_employee
from shared.models_schemas.schemas import EmployeeCreate, EmployeeUpdate

exception_error = HTTPException(status_code=404, detail="Employee not found")

async def create_employee_control(employee:EmployeeCreate):
    create_employe = await create_employee(employee)
    return create_employe


async def get_employee_control(employee_id:int):
    employee  = await get_employee(employee_id)
    if not employee:
        raise exception_error
    return employee


async def update_employee_control(employee_id:int, employee_update:EmployeeUpdate):
    updated_employee = await update_employee(employee_id, employee_update.dict(exclude_unset=True))
    if not updated_employee:
        raise exception_error
    return updated_employee


async def delete_employee_control(employee_id:int):
    deleted = await delete_employee(employee_id)
    if not deleted:
        raise exception_error
    return deleted


async def get_all_employees_control():
    employees = await get_all_employee()
    return employees