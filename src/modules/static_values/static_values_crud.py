from shared.models_schemas.models import StaticValues
from config.database.database import static_values_collection
import os
from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'env', '.env')
load_dotenv(dotenv_path)


# CRUD operations for static_values

async def create_static_values(values : StaticValues):
    values_dict = values.model_dump()
    if os.getenv("TESTING") == "True":
        static_values_collection.insert_one(values_dict)
    else:
        await static_values_collection.insert_one(values_dict)        
    return values

async def get_static_values(values_id: int):
    if os.getenv("TESTING") == "True":
        # Use synchronous find_one for tests
        values = static_values_collection.find_one({"id": values_id})
    else:
        # Use asynchronous find_one for production
        values = await static_values_collection.find_one({"id": values_id})

    if values:
        return StaticValues(**values)
    return None


async def update_static_values(values_id:int, update_data:dict):
    if os.getenv("TESTING") == "True":
        updated_static_values = static_values_collection.find_one_and_update(
            {"id" : values_id},
            {"$set" : update_data},
            return_document = True
        )
    else:
        updated_static_values = await static_values_collection.find_one_and_update(
            {"id" : values_id},
            {"$set" : update_data},
            return_document = True
        )
    if updated_static_values:
        return StaticValues(**updated_static_values)
    return None

async def delete_static_values(values_id : int) -> bool:
    if os.getenv("TESTING") == "True":
        result = static_values_collection.delete_one({"id":values_id})
    else:
        result = await static_values_collection.delete_one({"id":values_id})
    if result:
        return True
    return False