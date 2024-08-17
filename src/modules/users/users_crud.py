from typing import List
from shared.models_schemas.models import User
from config.database.database import user_collection
from src.shared.models_schemas.schemas import UserCreate, UserInDB
from modules.auth.authentication import get_password_hash


# CRUD operations for User

async def create_user(user: UserCreate) -> UserInDB:
    # Hash the provided password
    hashed_password = get_password_hash(user.password)
    
    # Create a UserInDB instance with the necessary data
    user_in_db = UserInDB(
        email=user.email,
        hashed_password=hashed_password,
        role=user.role,
        is_verified=False
    )
    
    # Convert the UserInDB instance to a dictionary for insertion
    user_data = user_in_db.model_dump()
    
    # Insert the user data into the database
    await user_collection.insert_one(user_data)
    
    return user_in_db

# async def create_user(user:UserCreate) -> UserInDB:
#     hashed_password = get_password_hash(user.password)
#     user_data = UserInDB.model_dump()
#     user_data['hashed_password'] = hashed_password
#     user_data['is_verified'] = False
#     db_user = UserInDB(**user_data)
#     await user_collection.insert_one(db_user.model_dump())
#     return db_user

async def get_user_by_email(email:str) -> User:
    user_data = await user_collection.find_one({"email":email}) 
    if user_data:
        return User(**user_data)
    return None


async def get_all_user() -> List[User]:
    users = await user_collection.find({}).to_list(length=None)
    return [User(**user) for user in users]

