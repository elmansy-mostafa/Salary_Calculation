from fastapi import APIRouter
from shared.models_schemas.schemas import StaticValuesCreate, StaticValuesResponse 
from .static_values_controller import create_static_values_control, get_static_values_control, update_static_values_control, delete_static_values_control


router = APIRouter()

# static values endpoints
@router.post("/static_values", response_model=StaticValuesResponse)
async def create_static_values_endpoint(values:StaticValuesCreate):
    return await create_static_values_control(values)


@router.get("/static_values/{values_id}", response_model=StaticValuesResponse)
async def get_employee_endpoint(values_id:int):
    return await get_static_values_control(values_id)


@router.put("/static_values/{values_id}", response_model=StaticValuesResponse)
async def update_static_values_endpoint(values_id:int, values_update:dict):
    return await update_static_values_control(values_id, values_update)


@router.delete("/static_values/{values_id}", response_model=bool)
async def delete_static_values_endpoint(values_id:int):
    return await delete_static_values_control(values_id)