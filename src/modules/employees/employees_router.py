from fastapi import APIRouter
from typing import List
from shared.models_schemas.schemas import EmployeeCreate, EmployeeUpdate, EmployeeResponse, DailyReportCreate, DailyReportUpdate, DailyReportResponse
from .employees_controller import create_employee_control, get_employee_control, update_employee_control, delete_employee_control, get_all_employees_control



router = APIRouter()

# Employee endpoints

@router.post("/employees", response_model=EmployeeResponse)
async def create_employee_endpoint(employee:EmployeeCreate):
    return await create_employee_control(employee)

@router.get("/employees/{employee_id}", response_model=EmployeeResponse)
async def get_employee_endpoint(employee_id:int):
    return await get_employee_control(employee_id)


@router.put("/employees/{employee_id}", response_model=EmployeeResponse)
async def update_employee_endpoint(employee_id:int, employee_update:EmployeeUpdate):
    return await update_employee_control(employee_id, employee_update)


@router.delete("/employees/{employee_id}", response_model=bool)
async def delete_employee_endpoint(employee_id:int):
    return await delete_employee_control(employee_id)


@router.get("/employees", response_model=List[EmployeeResponse])
async def get_all_employees_endpoint():
    return await get_all_employees_control()