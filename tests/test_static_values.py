import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch, AsyncMock
from mongomock import MongoClient
from src.main import app
from src.modules.static_values.static_values_controller import create_static_values_control, delete_static_values_control, get_static_values_control, update_static_values_control
from src.shared.models_schemas.models import StaticValues
from src.modules.static_values.static_values_crud import create_static_values, delete_static_values, get_static_values, update_static_values
from src.shared.models_schemas.schemas import StaticValuesCreate, StaticValuesResponse
from src.modules.auth.authentication import create_access_token

client = TestClient(app)

# Helper function to create a mock MongoDB client and collection
def get_mock_collection():
    mock_client = MongoClient()
    mock_db = mock_client['test_db']
    return mock_db['static_values']

# Helper function to prepare test static_values data
def get_test_static_values_data():
    return {
        "id":1,
        "tier_base_salary": {
            "A": 15000,
            "B": 12000,
            "C": 9000
        },
        "cad": 35.66,
        "kpis": 2000.0,
        "butter_up": 500.0,
        "allowance": {
            "travel": 300.0,
            "food": 150.0
        },
        "hour_price": {
            "A": 55.55,
            "B": 44.44,
            "C": 33.33
        },
        "no_of_qulified_appt_tier_setter": {
            "A": 6,
            "B": 4,
            "C": 3
        },
        "no_of_qulified_appt_tier_fronter": {
            "A": 9,
            "B": 8,
            "C": 7
    }
}

# Test for static_values
@pytest.mark.asyncio
async def test_create_static_values():
    # Prepare test data
    test_static_values_data = get_test_static_values_data()
    test_static_values = StaticValues(**test_static_values_data)

    # Create a mock MongoDB collection
    mock_collection = MagicMock()

    # Patch the static_values_collection used in create_static_values
    with patch('src.modules.static_values.static_values_crud.static_values_collection', mock_collection):
        # Mock the insert_one method to be an async method
        mock_collection.insert_one.return_value = test_static_values_data

        # Call the create_static_values function
        result = await create_static_values(test_static_values)

        # Assertions: Check all attributes and type
        assert result == test_static_values


        # Verify that the static_values was inserted into the collection
        mock_collection.insert_one.assert_called_once_with(test_static_values.model_dump())

# Test for create_static_values_control
@pytest.mark.asyncio
async def test_create_static_values_control():
    # Prepare test data
    test_static_values_data = get_test_static_values_data()
    test_static_values_create_data = StaticValuesCreate(**test_static_values_data)
    test_static_values = StaticValues(**test_static_values_data)

    # Patch create_static_values
    with patch('src.modules.static_values.static_values_controller.create_static_values', AsyncMock(return_value=test_static_values)):
        result = await create_static_values_control(test_static_values_create_data)

        # Assertions
        assert result == test_static_values

# Test for create_static_values_endpoint
@pytest.mark.asyncio
async def test_create_static_values_endpoint():
    # Prepare test data
    test_static_values_data = get_test_static_values_data()
    test_static_values = StaticValuesResponse(**test_static_values_data)

    # Mock the create_static_values_control function to return a test static_values
    with patch('src.modules.static_values.static_values_controller.create_static_values_control', AsyncMock(return_value=test_static_values)):
        # Patch the authorization dependency to always return a valid user
        with patch('src.modules.auth.authorizations.get_superadmin', return_value={"email": "admin@example.com", "role": "superadmin"}):
            # Create a mock token for the authenticated user
            token = create_access_token({"sub": "admin@example.com", "role": "superadmin"})

            # Call the create_static_values_endpoint using FastAPI's TestClient with authentication
            response = client.post(
                "/static_values",
                json=test_static_values_data,
                headers={"Authorization": f"Bearer {token}"}
            )

            # Assertions
            assert response.status_code == 200
            response_json = response.json()
            assert response_json == test_static_values
            
            


# test for get static_values
@pytest.mark.asyncio
async def test_get_static_values():
    # Prepare test data
    test_static_values_data = get_test_static_values_data()
    test_static_values = StaticValues(**test_static_values_data)

    # Create a mock MongoDB collection
    mock_collection = MagicMock()
    
    # Patch the static_values_collection used in get_static_values
    with patch('src.modules.static_values.static_values_crud.static_values_collection', mock_collection):
        # Mock the find_one method to return the test_static_values_data
        mock_collection.find_one.return_value = test_static_values_data

        # Call the function
        result = await get_static_values(test_static_values_data["id"])

        # Validate the result
        assert result is not None, "Expected result to be an static_values instance, but got None"
        assert result == test_static_values
        
    # Test for a non-existent static_values
    with patch('src.modules.static_values.static_values_crud.static_values_collection', mock_collection):
        # Mock the find_one method to return None for a non-existent static_values
        mock_collection.find_one.return_value = None

        result = await get_static_values(999)  # ID that does not exist
        assert result is None, "Expected result to be None for a non-existent static_values"
        

# Test for get_static_values_control
@pytest.mark.asyncio
async def test_get_static_values_control():
    # Prepare test data
    test_static_values_data = get_test_static_values_data()
    test_static_values = StaticValues(**test_static_values_data)

    # Patch get_static_values
    with patch('src.modules.static_values.static_values_controller.get_static_values', AsyncMock(return_value=test_static_values)):
        result = await get_static_values_control(test_static_values.id)

        # Assertions
        assert result == test_static_values

# Test for get_static_values_endpoint
@pytest.mark.asyncio
async def test_get_static_values_endpoint():
    # Prepare test data
    test_static_values_data = get_test_static_values_data()
    test_static_values = StaticValuesResponse(**test_static_values_data)

    # Mock the get_static_values_control function to return a test static_values
    with patch('src.modules.static_values.static_values_controller.get_static_values_control', AsyncMock(return_value=test_static_values)):
        # Patch the authorization dependency to always return a valid user
        with patch('src.modules.auth.authorizations.get_superadmin', return_value={"email": "admin@example.com", "role": "superadmin"}):
            # Create a mock token for the authenticated user
            token = create_access_token({"sub": "admin@example.com", "role": "superadmin"})

            # Call the get_static_values_endpoint using FastAPI's TestClient with authentication
            response = client.get(
                f"/static_values/{test_static_values.id}",
                headers={"Authorization": f"Bearer {token}"}
            )

            # Assertions
            assert response.status_code == 200
            response_json = response.json()
            assert response_json == test_static_values



        
# test for update static_values
@pytest.mark.asyncio
async def test_update_static_values():
    # Prepare test data
    test_static_values_data = get_test_static_values_data()
    test_static_values = StaticValues(**test_static_values_data)
    update_data = {"cad": 40}
    
    # Create a mock MongoDB collection
    mock_collection = MagicMock()
    
    # Patch the static_values_collection used in update_static_values
    with patch('src.modules.static_values.static_values_crud.static_values_collection', mock_collection):
        # Mock the find_one_and_update method to return the updated static_values data
        mock_collection.find_one_and_update.return_value = {
            **test_static_values_data,
            **update_data
        }

        # Call the function
        result = await update_static_values(test_static_values.id, update_data)

        # Assertions: Check that the result is as expected
        assert result is not None, "Expected an static_values instance, but got None"
        assert result.id == test_static_values.id
        assert result.cad == 40  # Updated attribute

    # Patch the static_values_collection used in update_static_values
    with patch('src.modules.static_values.static_values_crud.static_values_collection', mock_collection):
        # Mock the find_one_and_update method to return None for a non-existent static_values
        mock_collection.find_one_and_update.return_value = None

        # Call the function
        result = await update_static_values(999, update_data)  # ID that does not exist

        # Assertions: Check that the result is None
        assert result is None, "Expected result to be None for a non-existent static_values"

# Test for update_static_values_control
@pytest.mark.asyncio
async def test_update_static_values_control():
    # Prepare test data
    test_static_values_data = get_test_static_values_data()
    test_static_values_data['cad'] = 40
    test_static_values = StaticValues(**test_static_values_data)
    update_data = {"cad" : 40}

    # Patch update_static_values
    with patch('src.modules.static_values.static_values_controller.update_static_values', AsyncMock(return_value=test_static_values)):
        result = await update_static_values_control(test_static_values.id, update_data)

        # Assertions
        assert result is not None, "Expected an static_values instance, but got None"
        assert result.id == test_static_values.id
        assert result.cad == 40  # Updated attribute

# Test for update_static_values_endpoint
@pytest.mark.asyncio
async def test_update_static_values_endpoint():
    # Prepare test data
    test_static_values_data = get_test_static_values_data()
    test_static_values_data['cad'] = 40
    test_static_values = StaticValuesResponse(**test_static_values_data)
    update_data = {"cad": 40}

    # Mock the update_static_values_control function to return a test static_values
    with patch('src.modules.static_values.static_values_controller.update_static_values_control', AsyncMock(return_value=test_static_values)):
        # Patch the authorization dependency to always return a valid user
        with patch('src.modules.auth.authorizations.get_superadmin', return_value={"email": "admin@example.com", "role": "superadmin"}):
            # Create a mock token for the authenticated user
            token = create_access_token({"sub": "admin@example.com", "role": "superadmin"})

            # Call the update_static_values_endpoint using FastAPI's TestClient with authentication
            response = client.put(
                f"/static_values/{test_static_values.id}",
                json=test_static_values_data,
                headers={"Authorization": f"Bearer {token}"}
            )

            # Assertions
            assert response.status_code == 200
            response_json = response.json()
            assert response_json['id'] == test_static_values.id
            assert response_json['cad'] == update_data['cad']  # Updated attribute



# test for delete static_values 
@pytest.mark.asyncio
async def test_delete_static_values():
    # Prepare test data
    static_values_id = 1

    # Create a mock MongoDB collection    
    mock_collection = MagicMock()

    
    # Patch the static_values_collection used in delete_static_values
    with patch('src.modules.static_values.static_values_crud.static_values_collection', mock_collection):
        
        # Mock the delete_one method to return result including successful deletion
        mock_collection.delete_one.return_value = True
        
        # Call the function
        result = await delete_static_values(static_values_id)
        #assertion check that the result is true for successful deletion
        assert result is True
    
    # Patch the static_values_collection used in delete_static_values
    with patch('src.modules.static_values.static_values_crud.static_values_collection', mock_collection):
        
        # Mock the delete_one method to return result including successful deletion
        mock_collection.delete_one.return_value = False
        
        # Call the function
        result = await delete_static_values(99)
        #assertion check that the result is true for successful deletion
        assert result is False


# Test for delete_static_values_control
@pytest.mark.asyncio
async def test_delete_static_values_control():
    # Prepare test data
    static_values_id = 1

    # Patch delete_static_values method
    with patch('src.modules.static_values.static_values_crud.delete_static_values', return_value=True):
        result = await delete_static_values_control(static_values_id)
        # Assertions
        assert result is True
        
        

# Test for delete_static_values_endpoint
@pytest.mark.asyncio
async def test_delete_static_values_endpoint():
    # Prepare test data
    static_values_id = 1
    
    # Patch delete_static_values_control
    with patch('src.modules.static_values.static_values_controller.delete_static_values_control', return_value=True):
        # Patch the authorization dependency to always return a valid user
        
        with patch('src.modules.auth.authorizations.get_superadmin', return_value={"email": "admin@example.com", "role": "superadmin"}):
            # Create a mock token for the authenticated user
            token = create_access_token({"sub": "admin@example.com", "role": "superadmin"})
            
            # Call the delete_static_values_endpoint using FastAPI's TestClient with authentication
            response = client.delete(
                f"/static_values/{static_values_id}",
                headers={"Authorization": f"Bearer {token}"}
            )
            # Assertions
            assert response.status_code == 200
            assert response.json() is True