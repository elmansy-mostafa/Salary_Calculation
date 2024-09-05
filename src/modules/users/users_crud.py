from typing import List
from shared.models_schemas.models import User
from config.database.database import user_collection
from shared.models_schemas.schemas import UserCreate, UserInDB
from modules.auth.authentication import get_password_hash
import os
from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'env', '.env')
load_dotenv(dotenv_path)


# CRUD operations for User

async def create_user(user:UserCreate) -> UserInDB:
    hashed_password = get_password_hash(user.password)
    user_data = user.model_dump()
    user_data['hashed_password'] = hashed_password
    user_data['is_verified'] = False
    db_user = UserInDB(**user_data)
    if os.getenv("TESTING") == "True":
        user_collection.insert_one(db_user.model_dump())
    else:
        await user_collection.insert_one(db_user.model_dump())
    return db_user

async def get_user_by_email(email:str) -> User:
    if os.getenv("TESTING") == "True":
        user_data = user_collection.find_one({"email":email}) 
    else:
        user_data = await user_collection.find_one({"email":email}) 
    if user_data:
        return User(**user_data)
    return None


async def get_all_user() -> List[User]:
    if os.getenv("TESTING") == "True":
        users = list(user_collection.find({})) 
        return [User(**user) for user in users]
    else:
        users = await user_collection.find({}).to_list(length=None)
        return [User(**user) for user in users]

