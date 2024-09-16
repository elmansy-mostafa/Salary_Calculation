from fastapi import HTTPException
from .static_values_crud import  create_static_values, get_static_values, update_static_values, delete_static_values
from shared.models_schemas.schemas import StaticValuesCreate

exception_error = HTTPException(status_code=404, detail="static_values not found")


async def create_static_values_control(values:StaticValuesCreate):
    create_static_value = await create_static_values(values)
    return create_static_value


async def get_static_values_control(values_id:int):
    values  = await get_static_values(values_id)
    return values


async def update_static_values_control(values_id:int, values_update:dict):
    updated_static_values = await update_static_values(values_id, values_update)
    if not updated_static_values:
        raise exception_error
    return updated_static_values


async def delete_static_values_control(values_id:int):
    deleted = await delete_static_values(values_id)
    if not deleted:
        raise exception_error
    return deleted