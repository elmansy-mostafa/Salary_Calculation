from typing import List
from shared.models_schemas.models import User
from config.database.database import user_collection
from shared.models_schemas.schemas import UserCreate, USerInDB
from modules.auth.authentication import get_password_hash


# CRUD operations for User


async def create_user(user:UserCreate) -> User:
    hashed_password = get_password_hash(user.password)
    user_data = user.dict()
    user_data['hashed_password'] = hashed_password
    user_data['is_verified'] = False
    db_user = USerInDB(**user_data)
    await user_collection.insert_one(db_user.dict())
    return db_user

async def get_user_by_email(email:str) -> User:
    user_data = await user_collection.find_one({"email":email}) 
    if user_data:
        return User(**user_data)
    return None


async def get_all_user() -> List[User]:
    users = await user_collection.find({}).to_list(length=None)
    return [User(**user) for user in users]

