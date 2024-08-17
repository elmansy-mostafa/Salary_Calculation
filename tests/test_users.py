# import pytest
# from unittest.mock import patch, AsyncMock
# from mongomock import MongoClient
# from src.modules.users.users_crud import create_user
# from src.shared.models_schemas.schemas import UserCreate, UserInDB

# import re

# @pytest.mark.asyncio
# async def test_create_user():
#     # Prepare test data
#     test_user = UserCreate(
#         email="test@example.com",
#         password="testpassword123",
#         role="user"
#     )

#     # Create a mock MongoDB client
#     mock_client = MongoClient()
#     mock_db = mock_client['test_db']
#     mock_collection = mock_db['users']

#     # Patch the correct import path for user_collection in users_crud
#     with patch('src.modules.users.users_crud.user_collection', mock_collection):
#         # Mock the password hashing function
#         with patch('src.modules.auth.authentication.get_password_hash') as mock_get_password_hash:
#             mock_get_password_hash.return_value = "mock_hashed_password"

#             # Mock the insert_one method to return an async result
#             mock_collection.insert_one = AsyncMock(return_value=None)

#             # Call the function
#             result = await create_user(test_user)

#             # Debugging output
#             import src.shared.models_schemas.schemas
#             print(f"UserInDB from schemas: {src.shared.models_schemas.schemas.UserInDB}")
#             print(f"UserInDB in test: {UserInDB}")
#             print(f"Type of result: {type(result)}")
#             print(f"Type of UserInDB: {type(UserInDB)}")
#             print(f"Hashed password: {result.hashed_password}")

#             # Assertions
#             assert isinstance(result, UserInDB), f"Expected UserInDB but got {type(result)}"
#             assert result.email == test_user.email
#             assert re.match(r'^mock_hashed_password$', result.hashed_password)