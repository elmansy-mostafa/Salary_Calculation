import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch, AsyncMock
from mongomock import MongoClient
from datetime import datetime
from src.main import app
from src.modules.employees.employees_controller import create_employee_control, delete_employee_control, get_all_employees_control, get_employee_control, update_employee_control
from src.modules.employees.employees_router import get_all_employees_endpoint
from src.shared.models_schemas.models import Employee
from src.modules.employees.employees_crud import create_employee, get_all_employee, get_employee, update_employee, delete_employee
from src.shared.models_schemas.schemas import EmployeeCreate, EmployeeResponse
from src.modules.auth.authentication import create_access_token

client = TestClient(app)

# Helper function to create a mock MongoDB client and collection
def get_mock_collection():
    mock_client = MongoClient()
    mock_db = mock_client['test_db']
    return mock_db['employees']

# Helper function to prepare test employee data
def get_test_employee_data():
    return {
        "id": 1,
        "name": "John Doe",
        "national_id": 1234567890,
        "company_id": 1001,
        "start_date": datetime(2023, 1, 1).isoformat(),
        "end_date": None,
        "position": "Sales Representative",
        "tier_type": "B",
        "is_onsite": True,
        "has_insurance": True,
        "employee_type": {
            "is_appointment_serrer": True,
            "is_full_time": True
        }
    }

# Test for create_employee
@pytest.mark.asyncio
async def test_create_employee():
    # Prepare test data
    test_employee_data = get_test_employee_data()
    test_employee = Employee(**test_employee_data)

    # Create a mock MongoDB collection
    mock_collection = MagicMock()

    # Patch the employee_collection used in create_employee
    with patch('src.modules.employees.employees_crud.employee_collection', mock_collection):
        # Mock the insert_one method to be an async method
        mock_collection.insert_one.return_value = test_employee_data

        # Call the create_employee function
        result = await create_employee(test_employee)

        # Assertions: Check all attributes and type
        assert result.id == test_employee.id
        assert result.name == test_employee.name
        assert result.national_id == test_employee.national_id
        assert result.company_id == test_employee.company_id
        assert result.start_date == test_employee.start_date.isoformat()
        assert result.end_date == test_employee.end_date
        assert result.position == test_employee.position
        assert result.tier_type == test_employee.tier_type
        assert result.is_onsite == test_employee.is_onsite
        assert result.has_insurance == test_employee.has_insurance
        assert result.employee_type.is_appointment_serrer == test_employee.employee_type.is_appointment_serrer
        assert result.employee_type.is_full_time == test_employee.employee_type.is_full_time

        # Verify that the employee was inserted into the collection
        mock_collection.insert_one.assert_called_once_with(test_employee.model_dump())

# Test for create_employee_control
@pytest.mark.asyncio
async def test_create_employee_control():
    # Prepare test data
    test_employee_data = get_test_employee_data()
    test_employee_create_data = EmployeeCreate(**test_employee_data)
    test_employee = Employee(**test_employee_data)

    # Patch create_employee
    with patch('src.modules.employees.employees_controller.create_employee', AsyncMock(return_value=test_employee)):
        result = await create_employee_control(test_employee_create_data)

        # Assertions
        assert result.id == test_employee.id
        assert result.name == test_employee.name
        assert result.national_id == test_employee.national_id
        assert result.company_id == test_employee.company_id
        assert result.start_date == test_employee.start_date.isoformat()
        assert result.end_date == test_employee.end_date
        assert result.position == test_employee.position
        assert result.tier_type == test_employee.tier_type
        assert result.is_onsite == test_employee.is_onsite
        assert result.has_insurance == test_employee.has_insurance
        assert result.employee_type.is_appointment_serrer == test_employee.employee_type.is_appointment_serrer
        assert result.employee_type.is_full_time == test_employee.employee_type.is_full_time

# Test for create_employee_endpoint
@pytest.mark.asyncio
async def test_create_employee_endpoint():
    # Prepare test data
    test_employee_data = get_test_employee_data()
    test_employee = EmployeeResponse(**test_employee_data)

    # Mock the create_employee_control function to return a test employee
    with patch('src.modules.employees.employees_controller.create_employee_control', AsyncMock(return_value=test_employee)):
        # Patch the authorization dependency to always return a valid user
        with patch('src.modules.auth.authorizations.get_admin', return_value={"email": "admin@example.com", "role": "admin"}):
            # Create a mock token for the authenticated user
            token = create_access_token({"sub": "admin@example.com", "role": "admin"})

            # Call the create_employee_endpoint using FastAPI's TestClient with authentication
            response = client.post(
                "/employees",
                json=test_employee_data,
                headers={"Authorization": f"Bearer {token}"}
            )

            # Assertions
            assert response.status_code == 200
            response_json = response.json()
            assert response_json["id"] == test_employee.id
            assert response_json["name"] == test_employee.name
            assert response_json["national_id"] == test_employee.national_id
            assert response_json['company_id'] == test_employee.company_id
            assert response_json["start_date"] == test_employee.start_date.isoformat()
            assert response_json["end_date"] == test_employee.end_date
            assert response_json["position"] == test_employee.position
            assert response_json["tier_type"] == test_employee.tier_type
            assert response_json["is_onsite"] == test_employee.is_onsite
            assert response_json["has_insurance"] == test_employee.has_insurance
            assert response_json["employee_type"] == test_employee.employee_type.model_dump()
            assert response_json["employee_type"] == test_employee.employee_type.model_dump()


# test for get employee
@pytest.mark.asyncio
async def test_get_employee():
    # Prepare test data
    test_employee_data = get_test_employee_data()
    test_employee = Employee(**test_employee_data)

    # Create a mock MongoDB collection
    mock_collection = MagicMock()
    
    # Patch the employee_collection used in get_employee
    with patch('src.modules.employees.employees_crud.employee_collection', mock_collection):
        # Mock the find_one method to return the test_employee_data
        mock_collection.find_one.return_value = test_employee_data

        # Call the function
        result = await get_employee(test_employee_data["id"])

        # Validate the result
        assert result is not None, "Expected result to be an Employee instance, but got None"
        assert result.id == test_employee.id
        assert result.name == test_employee.name
        assert result.national_id == test_employee.national_id
        assert result.company_id == test_employee.company_id
        assert result.start_date == test_employee.start_date.isoformat()
        assert result.end_date == test_employee.end_date
        assert result.position == test_employee.position
        assert result.tier_type == test_employee.tier_type
        assert result.is_onsite == test_employee.is_onsite
        assert result.has_insurance == test_employee.has_insurance
        assert result.employee_type.is_appointment_serrer == test_employee.employee_type.is_appointment_serrer
        assert result.employee_type.is_full_time == test_employee.employee_type.is_full_time
        
    # Test for a non-existent employee
    with patch('src.modules.employees.employees_crud.employee_collection', mock_collection):
        # Mock the find_one method to return None for a non-existent employee
        mock_collection.find_one.return_value = None

        result = await get_employee(999)  # ID that does not exist
        assert result is None, "Expected result to be None for a non-existent employee"
        

# Test for get_employee_control
@pytest.mark.asyncio
async def test_get_employee_control():
    # Prepare test data
    test_employee_data = get_test_employee_data()
    test_employee = Employee(**test_employee_data)

    # Patch get_employee
    with patch('src.modules.employees.employees_controller.get_employee', AsyncMock(return_value=test_employee)):
        result = await get_employee_control(test_employee.id)

        # Assertions
        assert result.id == test_employee.id
        assert result.name == test_employee.name
        assert result.national_id == test_employee.national_id
        assert result.company_id == test_employee.company_id
        assert result.start_date == test_employee.start_date.isoformat()
        assert result.end_date == test_employee.end_date
        assert result.position == test_employee.position
        assert result.tier_type == test_employee.tier_type
        assert result.is_onsite == test_employee.is_onsite
        assert result.has_insurance == test_employee.has_insurance
        assert result.employee_type.is_appointment_serrer == test_employee.employee_type.is_appointment_serrer
        assert result.employee_type.is_full_time == test_employee.employee_type.is_full_time

# Test for get_employee_endpoint
@pytest.mark.asyncio
async def test_get_employee_endpoint():
    # Prepare test data
    test_employee_data = get_test_employee_data()
    test_employee = EmployeeResponse(**test_employee_data)

    # Mock the get_employee_control function to return a test employee
    with patch('src.modules.employees.employees_controller.get_employee_control', AsyncMock(return_value=test_employee)):
        # Patch the authorization dependency to always return a valid user
        with patch('src.modules.auth.authorizations.get_admin', return_value={"email": "admin@example.com", "role": "admin"}):
            # Create a mock token for the authenticated user
            token = create_access_token({"sub": "admin@example.com", "role": "admin"})

            # Call the get_employee_endpoint using FastAPI's TestClient with authentication
            response = client.get(
                f"/employees/{test_employee.id}",
                headers={"Authorization": f"Bearer {token}"}
            )

            # Assertions
            assert response.status_code == 200
            response_json = response.json()
            assert response_json["id"] == test_employee.id
            assert response_json["name"] == test_employee.name
            assert response_json["national_id"] == test_employee.national_id
            assert response_json['company_id'] == test_employee.company_id
            assert response_json["start_date"] == test_employee.start_date.isoformat()
            assert response_json["end_date"] == test_employee.end_date
            assert response_json["position"] == test_employee.position
            assert response_json["tier_type"] == test_employee.tier_type
            assert response_json["is_onsite"] == test_employee.is_onsite
            assert response_json["has_insurance"] == test_employee.has_insurance
            assert response_json["employee_type"] == test_employee.employee_type.model_dump()
            assert response_json["employee_type"] == test_employee.employee_type.model_dump()


        
        
# test for update employee
@pytest.mark.asyncio
async def test_update_employee():
    # Prepare test data
    test_employee_data = get_test_employee_data()
    test_employee = Employee(**test_employee_data)
    update_data = {"position": "Senior Sales Representative"}
    
    # Create a mock MongoDB collection
    mock_collection = MagicMock()
    
    # Patch the employee_collection used in update_employee
    with patch('src.modules.employees.employees_crud.employee_collection', mock_collection):
        # Mock the find_one_and_update method to return the updated employee data
        mock_collection.find_one_and_update.return_value = {
            **test_employee_data,
            **update_data
        }

        # Call the function
        result = await update_employee(test_employee.id, update_data)

        # Assertions: Check that the result is as expected
        assert result is not None, "Expected an Employee instance, but got None"
        assert result.id == test_employee.id
        assert result.position == "Senior Sales Representative"  # Updated attribute

    # Patch the employee_collection used in update_employee
    with patch('src.modules.employees.employees_crud.employee_collection', mock_collection):
        # Mock the find_one_and_update method to return None for a non-existent employee
        mock_collection.find_one_and_update.return_value = None

        # Call the function
        result = await update_employee(999, update_data)  # ID that does not exist

        # Assertions: Check that the result is None
        assert result is None, "Expected result to be None for a non-existent employee"

# Test for update_employee_control
@pytest.mark.asyncio
async def test_update_employee_control():
    # Prepare test data
    test_employee_data = get_test_employee_data()
    test_employee_data['position'] = "Senior Sales Representative"
    test_employee = Employee(**test_employee_data)
    update_data = {"position" : "Senior Sales Representative"}

    # Patch update_employee
    with patch('src.modules.employees.employees_controller.update_employee', AsyncMock(return_value=test_employee)):
        result = await update_employee_control(test_employee.id, update_data)

        # Assertions
        assert result is not None, "Expected an Employee instance, but got None"
        assert result.id == test_employee.id
        assert result.position == "Senior Sales Representative"  # Updated attribute

# Test for update_employee_endpoint
@pytest.mark.asyncio
async def test_update_employee_endpoint():
    # Prepare test data
    test_employee_data = get_test_employee_data()
    test_employee_data['position'] = "Senior Sales Representative"
    test_employee = EmployeeResponse(**test_employee_data)
    update_data = {"position": "Senior Sales Representative"}

    # Mock the update_employee_control function to return a test employee
    with patch('src.modules.employees.employees_controller.update_employee_control', AsyncMock(return_value=test_employee)):
        # Patch the authorization dependency to always return a valid user
        with patch('src.modules.auth.authorizations.get_admin', return_value={"email": "admin@example.com", "role": "admin"}):
            # Create a mock token for the authenticated user
            token = create_access_token({"sub": "admin@example.com", "role": "admin"})

            # Call the update_employee_endpoint using FastAPI's TestClient with authentication
            response = client.put(
                f"/employees/{test_employee.id}",
                json=test_employee_data,
                headers={"Authorization": f"Bearer {token}"}
            )

            # Assertions
            assert response.status_code == 200
            response_json = response.json()
            assert response_json['id'] == test_employee.id
            assert response_json['position'] == update_data['position']  # Updated attribute



# test for delete employee 
@pytest.mark.asyncio
async def test_delete_employee():
    # Prepare test data
    employee_id = 1

    # Create a mock MongoDB collection    
    mock_collection = MagicMock()

    
    # Patch the employee_collection used in delete_employee
    with patch('src.modules.employees.employees_crud.employee_collection', mock_collection):
        
        # Mock the delete_one method to return result including successful deletion
        mock_collection.delete_one.return_value = True
        
        # Call the function
        result = await delete_employee(employee_id)
        #assertion check that the result is true for successful deletion
        assert result is True
    
    # Patch the employee_collection used in delete_employee
    with patch('src.modules.employees.employees_crud.employee_collection', mock_collection):
        
        # Mock the delete_one method to return result including successful deletion
        mock_collection.delete_one.return_value = False
        
        # Call the function
        result = await delete_employee(99)
        #assertion check that the result is true for successful deletion
        assert result is False


# Test for delete_employee_control
@pytest.mark.asyncio
async def test_delete_employee_control():
    # Prepare test data
    employee_id = 1

    # Patch delete_employee method
    with patch('src.modules.employees.employees_crud.delete_employee', return_value=True):
        result = await delete_employee_control(employee_id)
        # Assertions
        assert result is True
        
        

# Test for delete_employee_endpoint
@pytest.mark.asyncio
async def test_delete_employee_endpoint():
    # Prepare test data
    employee_id = 1
    
    # Patch delete_employee_control
    with patch('src.modules.employees.employees_controller.delete_employee_control', return_value=True):
        # Patch the authorization dependency to always return a valid user
        
        with patch('src.modules.auth.authorizations.get_admin', return_value={"email": "admin@example.com", "role": "admin"}):
            # Create a mock token for the authenticated user
            token = create_access_token({"sub": "admin@example.com", "role": "admin"})
            
            # Call the delete_employee_endpoint using FastAPI's TestClient with authentication
            response = client.delete(
                f"/employees/{employee_id}",
                headers={"Authorization": f"Bearer {token}"}
            )
            # Assertions
            assert response.status_code == 200
            assert response.json() is True


def get_test_data():
    return [
        {
        "id": 1,
        "name": "John Doe",
        "national_id": 1234567890,
        "company_id": 1001,
        "start_date": datetime(2023, 1, 1).isoformat(),
        "end_date": None,
        "position": "Sales Representative",
        "tier_type": "B",
        "is_onsite": True,
        "has_insurance": True,
        "employee_type": {
            "is_appointment_serrer": True,
            "is_full_time": True
        }
    },
        {
        "id": 1,
        "name": " Doe",
        "national_id": 123456,
        "company_id": 1021,
        "start_date": datetime(2023, 1, 1).isoformat(),
        "end_date": None,
        "position": "Sales agent",
        "tier_type": "A",
        "is_onsite": True,
        "has_insurance": True,
        "employee_type": {
            "is_appointment_serrer": True,
            "is_full_time": True
        }
    }
    ]

@pytest.mark.asyncio
async def test_get_all_employee():
    test_employee_data = get_test_data()

    # Convert the test data into Employee instances
    mock_employee_data = [Employee(**data) for data in test_employee_data]

    # Mock the collection's find method to return the test data
    mock_collection = MagicMock()
    mock_collection.find.return_value = test_employee_data

    # Patch the employee_collection to use the mock collection
    with patch('src.modules.employees.employees_crud.employee_collection', mock_collection):
        result = await get_all_employee()

        # Convert results to dictionaries for easy comparison
        assert [employee.model_dump() for employee in result] == [employee.model_dump() for employee in mock_employee_data]

    # Check if the find method was called once with no arguments
    mock_collection.find.assert_called_once_with({})

@pytest.mark.asyncio
async def test_get_all_employees_control():
    test_employee_data = get_test_data()

    # Convert the test data into Employee instances
    mock_employee_data = [Employee(**data) for data in test_employee_data]
    
    # Mock the collection's find method to return the test data
    mock_collection = MagicMock()
    mock_collection.find.return_value = test_employee_data

    # Patch the employee_collection to use the mock collection
    with patch('src.modules.employees.employees_crud.employee_collection', mock_collection):
        # Mock the get_all_employee function to return the test data
        with patch('src.modules.employees.employees_crud.get_all_employee', return_value=mock_employee_data):
            # Call the function under test
            result = await get_all_employees_control()

            # Ensure results match the expected data structure
            assert [employee.model_dump() for employee in result] == [employee.model_dump() for employee in mock_employee_data]

@pytest.mark.asyncio
async def test_get_all_employees_endpoint():
    test_employee_data = get_test_data()
    mock_employee_data = [Employee(**data) for data in test_employee_data]

    mock_collection = MagicMock()
    mock_collection.find.return_value = test_employee_data

    with patch('src.modules.employees.employees_crud.employee_collection', mock_collection):
        # Patch get_all_employee instead of get_all_employees_control
        with patch('src.modules.employees.employees_crud.get_all_employee', return_value=mock_employee_data) as mock_get_all:
            with patch('src.modules.employees.employees_router.get_all_employees_endpoint', return_value=mock_employee_data) as mock_get_all:
                result = await get_all_employees_endpoint()
                with patch('src.modules.auth.authorizations.get_admin', return_value={"email": "admin@example.com", "role": "admin"}):      
                    token = create_access_token({"sub": "admin@example.com", "role": "admin"})

                    response = client.get(
                        "/employees",
                        headers={"Authorization": f"Bearer {token}"}
                        )
                        
                    assert response.status_code == 200
                    assert [employee.model_dump() for employee in result] ==[employee.model_dump() for employee in mock_employee_data]
