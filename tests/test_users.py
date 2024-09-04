from datetime import timedelta
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.testclient import TestClient
from pymongo.results import DeleteResult
import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from mongomock import MongoClient
from src.main import app
from src.modules.auth.authentication import create_access_token
from src.modules.users.users_controller import delete_user, get_all_users, login, signup
from src.modules.users.users_crud import create_user, get_all_user, get_user_by_email
from src.modules.users.users_router import get_all_users_endpoints, login_endpoint
from src.shared.models_schemas.models import Login, User
from src.shared.models_schemas.schemas import UserCreate


client = TestClient(app)

# Helper function to create a mock MongoDB client and collection
def get_mock_collection():
    mock_client = MongoClient()
    mock_db = mock_client['test_db']
    return mock_db['users']

# Helper function to prepare test user data
def get_test_user_data():
    return {
        "email" : "test@example.com",
        "password" : "testpassword123",
        "role" : "user"
    }

# test for create user
@pytest.mark.asyncio
async def test_create_user():
    # Prepare test data
    test_user_data = get_test_user_data()
    test_user = UserCreate(**test_user_data)

    # Create the expected data that will be passed to insert_one
    expected_data = test_user.model_dump()
    expected_data.pop('password')
    expected_data['hashed_password'] = "mock_hashed_password"
    expected_data['is_verified'] = False

    # Create a mock MongoDB collection
    mock_collection = MagicMock()

    # Patch the correct import path for user_collection in users_crud
    with patch('src.modules.users.users_crud.user_collection', mock_collection):
        # Mock the password hashing function
        with patch('src.modules.users.users_crud.get_password_hash') as mock_get_password_hash:
            mock_get_password_hash.return_value = "mock_hashed_password"

            # Mock the insert_one method to return an async result
            mock_collection.insert_one.return_value = test_user_data

            # Call the function
            result = await create_user(test_user)

            # Assertions
            assert result.email == test_user.email
            assert result.role == test_user.role
            assert result.hashed_password == "mock_hashed_password"
            assert result.is_verified == False

        # Verify that the user was inserted into the collection with the expected data
        mock_collection.insert_one.assert_called_once_with(expected_data)
        

#  test for get user by email 
@pytest.mark.asyncio
async def test_get_user_by_email():
    # Prepare test data
    test_email = "test@example.com"
    test_user = get_test_user_data()

    # Create the expected data that will be passed to insert_one
    expected_data = test_user
    expected_data['hashed_password'] = "mock_hashed_password"
    expected_data['is_verified'] = False
    expected_data = User(**test_user)

# Create a mock MongoDB collection
    mock_collection = MagicMock()

    # Patch the correct import path for user_collection in users_crud
    with patch('src.modules.users.users_crud.user_collection', mock_collection):
        # Mock the find_one method to return an async result
        mock_collection.find_one.return_value = test_user
        
        # call the function
        result = await get_user_by_email(test_email)

        # Assertions
        assert result.email == expected_data.email
        assert result.role == expected_data.role
        assert result.hashed_password == expected_data.hashed_password
        assert result.is_verified == expected_data.is_verified
        
## get user by email not found ......
    # Patch the correct import path for user_collection in users_crud
    with patch('src.modules.users.users_crud.user_collection', mock_collection):
        # Mock the find_one method to return an async result
        mock_collection.find_one.return_value = None
        
        # call the function
        result = await get_user_by_email(test_email)

        # Assertions
        assert result is None
        

    
# test for signup of existing user
@pytest.mark.asyncio
async def test_signup_existing_user():
    # Prepare test data
    test_user_data = get_test_user_data()
    test_user_create = UserCreate(**test_user_data)
    test_user = test_user_data
    test_user['hashed_password'] = "mock_hashed_password"
    test_user['is_verified'] = False
    test_user = User(**test_user_data)

    # Create a mock for get_user_by_email to return an existing user
    mock_get_user_by_email = AsyncMock(return_value=test_user)

    with patch('src.modules.users.users_controller.get_user_by_email', mock_get_user_by_email):
        with pytest.raises(HTTPException) as exc_info:
            await signup(test_user_create)
        
        # Assertions
        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == "Email already registerd"

    # Verify that get_user_by_email was called
    mock_get_user_by_email.assert_called_once_with(test_user_create.email)


@pytest.mark.asyncio
async def test_signup_success():
    # Prepare test data
    test_user_data = get_test_user_data()
    test_user = UserCreate(**test_user_data)

    # Mocks
    mock_get_user_by_email = AsyncMock(return_value=None)
    mock_create_user = AsyncMock()
    mock_send_verification_email = AsyncMock()

    with patch('src.modules.users.users_controller.get_user_by_email', mock_get_user_by_email):
        with patch('src.modules.users.users_controller.create_user', mock_create_user):
            with patch('src.modules.users.users_controller.create_verification_token', return_value="mock_token" ) as mock_create_verification_token:
                with patch('src.modules.users.users_controller.send_verification_email', mock_send_verification_email):
                    # Call the function
                    result = await signup(test_user)

                    # Assertions
                    assert result["msg"] == "Please check your email to verify your account"
                    mock_create_user.assert_called_once_with(test_user)
                    mock_create_verification_token.assert_called_once_with(test_user.email)
                    mock_send_verification_email.assert_called_once_with(test_user.email, "mock_token")

    # Verify that get_user_by_email was called
    mock_get_user_by_email.assert_called_once_with(test_user.email)
    
    
# test for signup
@pytest.mark.asyncio
async def test_signup_endpoint_success():
    # Prepare test data
    test_user_data = get_test_user_data()

    # Mock dependencies
    mock_get_user_by_email = AsyncMock(return_value=None)
    mock_create_user = AsyncMock()
    mock_send_verification_email = AsyncMock()

    with patch('src.modules.users.users_controller.get_user_by_email', mock_get_user_by_email):
        with patch('src.modules.users.users_controller.create_user', mock_create_user):
            with patch('src.modules.users.users_controller.create_verification_token', return_value="mock_token" ) as mock_create_verification_token:
                with patch('src.modules.users.users_controller.send_verification_email', mock_send_verification_email):
                    
                    # Make a POST request to the /signup endpoint
                    response = client.post("/signup", json=test_user_data)
                    
                    # Assert the response status code and message
                    assert response.status_code == 200
                    assert response.json() == {"msg": "Please check your email to verify your account"}
                    
                    
@pytest.mark.asyncio
async def test_signup_endpoint_existing_user():
    # Prepare test data
    test_user_data = get_test_user_data()

    # Mock an existing user
    existing_user = UserCreate(**test_user_data)
    mock_get_user_by_email = AsyncMock(return_value=existing_user)

    with patch('src.modules.users.users_controller.get_user_by_email', mock_get_user_by_email):
        with patch('src.modules.users.users_controller.create_user') as mock_create_user:
            # Make a POST request to the /signup endpoint
            response = client.post("/signup", json=test_user_data)
            
            # Assert the response status code and detail for HTTPException
            assert response.status_code == 400
            assert response.json() == {"detail": "Email already registerd"}
            
            # Ensure create_user was not called
            mock_create_user.assert_not_called()
            

# Assuming constants defined somewhere in your project
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_ECPIRE_DAYS = 7

def get_test_login_data():
    return {
        "username": "test@example.com",
        "password": "testpassword123"
    }

def get_test_user():
    return {
        "email": "test@example.com",
        "hashed_password": "mock_hashed_password",
        "role": "user",
        "is_verified": True  
    }
@pytest.mark.asyncio
async def test_login_success():
    # Prepare test data
    test_user_data = get_test_user()
    test_user = User(**test_user_data)
    
    test_login_data = get_test_login_data()
    test_login = Login(**test_login_data)

    # Mock dependencies
    mock_get_user_by_email = AsyncMock(return_value=test_user)

    with patch('src.modules.users.users_controller.get_user_by_email', mock_get_user_by_email):
        with patch('src.modules.users.users_controller.verify_password',return_value=True) as mock_verify_password:
            with patch('src.modules.users.users_controller.create_access_token',return_value="mock_access_token") as mock_create_access_token:
                with patch('src.modules.users.users_controller.create_refresh_token', return_value="mock_refresh_token") as mock_create_refresh_token:

                    # Call the login function
                    result = await login(test_login)
                    
                    # Assertions
                    assert result["access_token"] == "mock_access_token"
                    assert result["refresh_token"] == "mock_refresh_token"
                    assert result["token_type"] == "bearer"
                    
                    mock_get_user_by_email.assert_called_once_with(test_login.username)
                    mock_verify_password.assert_called_once_with(test_login.password, test_user.hashed_password)
                    mock_create_access_token.assert_called_once_with(
                        data={"sub": test_user.email, "role": test_user.role},
                        expire_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
                    )
                    mock_create_refresh_token.assert_called_once_with(
                        data={"sub": test_user.email, "role": test_user.role},
                        expire_delta=timedelta(minutes=REFRESH_TOKEN_ECPIRE_DAYS)
                    )
                    
                    
@pytest.mark.asyncio
async def test_login_invalid_credentials():
    # Prepare test data    
    test_login_data = get_test_login_data()
    test_login = Login(**test_login_data)

    # Mock get_user_by_email to return None (user does not exist)
    mock_get_user_by_email = AsyncMock(return_value=None)

    with patch('src.modules.users.users_controller.get_user_by_email', mock_get_user_by_email):
        with patch('src.modules.users.users_controller.verify_password',return_value=False) as mock_verify_password:
            with pytest.raises(HTTPException) as exc_info:
                await login(test_login)
                
            # Assertions
            assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
            assert exc_info.value.detail == "incorrect email or password"

@pytest.mark.asyncio
async def test_login_email_not_verified():
    # Prepare test data
    test_user_data = get_test_user()
    test_user_data['is_verified'] = False
    test_user = User(**test_user_data)
    
    test_login_data = get_test_login_data()
    test_login = Login(**test_login_data)
    
    # Mock get_user_by_email to return the unverified user
    mock_get_user_by_email = AsyncMock(return_value=test_user)

    with patch('src.modules.users.users_controller.get_user_by_email', mock_get_user_by_email):
        with patch('src.modules.users.users_controller.verify_password',return_value=True) as mock_verify_password:
            with pytest.raises(HTTPException) as exc_info:
                await login(test_login)
                
            # Assertions
            assert exc_info.value.status_code == 400
            assert exc_info.value.detail == "Email is not verified"

# test for login endpoint
@pytest.mark.asyncio
async def test_login_endpoint_success():
    # Prepare test data
    test_user_data = get_test_user()
    test_user_data["is_verified"] = True
    test_user = User(**test_user_data)
    test_login_data = get_test_login_data()

    # Mock dependencies
    mock_get_user_by_email = AsyncMock(return_value=test_user)

    with patch('src.modules.users.users_controller.get_user_by_email', mock_get_user_by_email):
        with patch('src.modules.users.users_controller.verify_password', return_value=True) as mock_verify_password:
            with patch('src.modules.users.users_controller.create_access_token', return_value="mock_access_token") as mock_create_access_token:
                with patch('src.modules.users.users_controller.create_refresh_token', return_value="mock_refresh_token") as mock_create_refresh_token:
                    # Create OAuth2PasswordRequestForm
                    form_data = OAuth2PasswordRequestForm(username=test_login_data['username'], password=test_login_data['password'])

                    # Call the function directly
                    response = await login_endpoint(form_data)

                    # Verify mock calls
                    mock_get_user_by_email.assert_called_once_with(test_login_data['username'])
                    returned_user = await mock_get_user_by_email(test_login_data['username'])
                    assert returned_user.is_verified == True

                    # Check the response
                    assert isinstance(response, dict), f"Expected dict, got {type(response)}"
                    assert "access_token" in response, f"Expected access_token in response, got {response}"
                    assert response["access_token"] == "mock_access_token"
                    assert response["refresh_token"] == "mock_refresh_token"
                    assert response["token_type"] == "bearer"

                    # Verify that other mocks were called correctly
                    mock_verify_password.assert_called_once()
                    mock_create_access_token.assert_called_once()
                    mock_create_refresh_token.assert_called_once()
                    
                    
                    
# test for delete user 
@pytest.mark.asyncio
async def test_delete_user():
    # Prepare test data
    email = "test@example.com"

    # Create a mock MongoDB collection
    mock_collection = MagicMock()

    # Patch the user_collection used in delete_user
    with patch('src.modules.users.users_controller.user_collection', mock_collection):
        
        # Mock the DeleteResult with deleted_count = 1 for successful deletion
        mock_result = MagicMock(spec=DeleteResult)
        mock_result.deleted_count = 1
        mock_collection.delete_one.return_value = mock_result
        
        # Call the function
        result = await delete_user(email)
        
        # Assertion check that the result is true for successful deletion
        assert result["message"] == "User deleted successfully"

    # Patch the user_collection used in delete_user
    with patch('src.modules.users.users_controller.user_collection', mock_collection):
        
        # Mock the DeleteResult with deleted_count = 0 for failed deletion
        mock_result = MagicMock(spec=DeleteResult)
        mock_result.deleted_count = 0
        mock_collection.delete_one.return_value = mock_result

        # Check for the exception
        with pytest.raises(HTTPException) as exc_info:
            await delete_user(email)
        
        # Assertions
        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == "User not found"
        



@pytest.mark.asyncio
async def test_delete_user_endpoint_success():
    # Prepare test data
    email = "test@example.com"

    # Mock the delete_user function to simulate successful deletion
    with patch('src.modules.users.users_controller.delete_user', return_value={"message": "User deleted successfully"}) as mock_delete_user:
        with patch('src.modules.auth.authorizations.get_superadmin', return_value={"email": "admin@example.com", "role": "admin"}):      
            token = create_access_token({"sub": "admin@example.com", "role": "superadmin"})

            response = client.delete(
                    f"/users/{email}",
                    headers={"Authorization": f"Bearer {token}"}
                    )
            # Check the response
            assert response.status_code == 200
            json_response = response.json()
            assert json_response["message"] == "User deleted successfully"


@pytest.mark.asyncio
async def test_delete_user_endpoint_user_not_found():
    # Prepare test data
    email = "nonexistent@example.com"

    # Mock the delete_user function to raise an HTTPException for a non-existent user
    with patch('src.modules.users.users_controller.delete_user', side_effect=HTTPException(status_code=400, detail="User not found")) as mock_delete_user:
        with patch('src.modules.auth.authorizations.get_superadmin', return_value={"email": "admin@example.com", "role": "admin"}):      
            token = create_access_token({"sub": "admin@example.com", "role": "superadmin"})

            response = client.delete(
                    f"/users/{email}",
                    headers={"Authorization": f"Bearer {token}"}
                    )

            # Check the response
            assert response.status_code == 400
            json_response = response.json()
            assert json_response["detail"] == "User not found"


def get_test_data():
    return [
        {
        "email": "test@example.com",
        "hashed_password": "mock_hashed_password",
        "role": "user",
        "is_verified": True  
    },
        {
        "email": "test2@example.com",
        "hashed_password": "mock_hashed_password",
        "role": "amin",
        "is_verified": True  
    }
        ]

# test for get all users
@pytest.mark.asyncio
async def test_get_all_user():
    test_user_data = get_test_data()

    # Convert the test data into user instances
    mock_user_data = [User(**data) for data in test_user_data]

    # Mock the collection's find method to return the test data
    mock_collection = MagicMock()
    mock_collection.find.return_value = test_user_data

    # Patch the user_collection to use the mock collection
    with patch('src.modules.users.users_crud.user_collection', mock_collection):
        result = await get_all_user()

        # Convert results to dictionaries for easy comparison
        assert [user.model_dump() for user in result] == [user.model_dump() for user in mock_user_data]

    # Check if the find method was called once with no arguments
    mock_collection.find.assert_called_once_with({})

@pytest.mark.asyncio
async def test_get_all_users_control():
    test_user_data = get_test_data()

    # Convert the test data into user instances
    mock_user_data = [User(**data) for data in test_user_data]
    
    # Mock the collection's find method to return the test data
    mock_collection = MagicMock()
    mock_collection.find.return_value = test_user_data

    # Patch the user_collection to use the mock collection
    with patch('src.modules.users.users_crud.user_collection', mock_collection):
        # Mock the get_all_user function to return the test data
        with patch('src.modules.users.users_crud.get_all_user', return_value=mock_user_data):
            # Call the function under test
            result = await get_all_users()

            # Ensure results match the expected data structure
            assert [user.model_dump() for user in result] == [user.model_dump() for user in mock_user_data]

@pytest.mark.asyncio
async def test_get_all_users_endpoint():
    test_user_data = get_test_data()
    mock_user_data = [User(**data) for data in test_user_data]

    mock_collection = MagicMock()
    mock_collection.find.return_value = test_user_data

    with patch('src.modules.users.users_crud.user_collection', mock_collection):
        # Patch get_all_user instead of get_all_users_control
        with patch('src.modules.users.users_crud.get_all_user', return_value=mock_user_data) as mock_get_all:
            with patch('src.modules.users.users_router.get_all_users_endpoints', return_value=mock_user_data) as mock_get_all:
                result = await get_all_users_endpoints()
                with patch('src.modules.auth.authorizations.get_admin', return_value={"email": "admin@example.com", "role": "admin"}):      
                    token = create_access_token({"sub": "admin@example.com", "role": "admin"})

                    response = client.get(
                        "/users",
                        headers={"Authorization": f"Bearer {token}"}
                        )
                        
                    assert response.status_code == 200
                    assert [user.model_dump() for user in result] ==[user.model_dump() for user in mock_user_data]
