import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from mongomock import MongoClient
from datetime import datetime
from src.shared.models_schemas.models import Employee
from src.modules.employees.employees_crud import create_employee, get_all_employee, get_employee, update_employee, delete_employee


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
        "start_date": datetime(2023, 1, 1),
        "end_date": None,
        "position": "Sales Representative"
    }


@pytest.mark.asyncio
async def test_create_employee():
    # Prepare test data
    test_employee_data = get_test_employee_data()
    test_employee = Employee(**test_employee_data)

    # Create a mock MongoDB collection
    mock_collection = get_mock_collection()

    # Patch the employee_collection used in create_employee
    with patch('src.modules.employees.employees_crud.employee_collection', mock_collection):
        # Mock the insert_one method to be an async method
        mock_collection.insert_one = AsyncMock(return_value=None)

        # Call the function
        result = await create_employee(test_employee)

        # Assertions: Check all attributes and type
        assert isinstance(result, Employee)
        assert result.id == test_employee.id
        assert result.name == test_employee.name
        assert result.national_id == test_employee.national_id
        assert result.company_id == test_employee.company_id
        assert result.start_date == test_employee.start_date
        assert result.end_date == test_employee.end_date
        assert result.position == test_employee.position

        # Verify that the employee was inserted into the collection
        mock_collection.insert_one.assert_called_once_with(test_employee.model_dump())


@pytest.mark.asyncio
async def test_get_employee():
    # Prepare test data
    test_employee_data = get_test_employee_data()
    test_employee = Employee(**test_employee_data)

    # Create a mock MongoDB collection
    mock_collection = get_mock_collection()

    # Patch the employee_collection used in get_employee
    with patch('src.modules.employees.employees_crud.employee_collection', mock_collection):
        # Mock the find_one method to be an async method
        mock_collection.find_one = AsyncMock(return_value=test_employee_data)

        # Call the function
        result = await get_employee(test_employee.id)

        # Assertions: Check all attributes and type
        assert result is not None, "Expected result to be an Employee instance, but got None"
        assert result.id == test_employee.id
        assert result.name == test_employee.name
        assert result.national_id == test_employee.national_id
        assert result.company_id == test_employee.company_id
        assert result.start_date == test_employee.start_date
        assert result.end_date == test_employee.end_date
        assert result.position == test_employee.position

    # Test for a non-existent employee
    with patch('src.modules.employees.employees_crud.employee_collection', mock_collection):
        # Mock the find_one method to return None for a non-existent employee
        mock_collection.find_one = AsyncMock(return_value=None)

        result = await get_employee(999)  # ID that does not exist
        assert result is None, "Expected result to be None for a non-existent employee"
        
        

@pytest.mark.asyncio
async def test_update_employee():
    # Prepare test data
    test_employee_data = get_test_employee_data()
    test_employee = Employee(**test_employee_data)
    update_data = {"position": "Senior Sales Representative"}
    
    # Create a mock MongoDB collection
    mock_collection = get_mock_collection()
    
    # Patch the employee_collection used in update_employee
    with patch('src.modules.employees.employees_crud.employee_collection', mock_collection):
        # Mock the find_one_and_update method to return the updated employee data
        mock_collection.find_one_and_update = AsyncMock(return_value={
            **test_employee_data,
            **update_data
        })

        # Call the function
        result = await update_employee(test_employee.id, update_data)

        # Assertions: Check that the result is as expected
        assert result is not None, "Expected an Employee instance, but got None"
        assert result.id == test_employee.id
        assert result.position == "Senior Sales Representative"  # Updated attribute

@pytest.mark.asyncio
async def test_update_employee_not_found():
    # Prepare test data
    update_data = {"position": "Senior Sales Representative"}
    
    # Create a mock MongoDB collection
    mock_collection = get_mock_collection()

    # Patch the employee_collection used in update_employee
    with patch('src.modules.employees.employees_crud.employee_collection', mock_collection):
        # Mock the find_one_and_update method to return None for a non-existent employee
        mock_collection.find_one_and_update = AsyncMock(return_value=None)

        # Call the function
        result = await update_employee(999, update_data)  # ID that does not exist

        # Assertions: Check that the result is None
        assert result is None, "Expected result to be None for a non-existent employee"
        

@pytest.mark.asyncio
async def test_delete_employee():
    # Prepare test data
    employee_id = 1

    # Create a mock MongoDB collection    
    mock_collection = get_mock_collection()
    
    # Patch the employee_collection used in get_employee
    with patch('src.modules.employees.employees_crud.employee_collection', mock_collection):
        
        # Mock the delete_one method to return result including successful deletion
        mock_collection.delete_one = AsyncMock(return_value=AsyncMock(deleted_count=1))
        
        # Call the function
        result = await delete_employee(employee_id)
        
        #assertion check that the result is true for successful deletion
        assert result is True


@pytest.mark.asyncio
async def test_delete_employee_failuer():
    # Prepare test data
    employee_id = 999  # no exitence employee_id

    # Create a mock MongoDB collection    
    mock_collection = get_mock_collection()
    
    # Patch the employee_collection used in get_employee
    with patch('src.modules.employees.employees_crud.employee_collection', mock_collection):
        
        # Mock the delete_one method to return result including successful deletion
        mock_collection.delete_one = AsyncMock(return_value=AsyncMock(deleted_count=0))
        
        # Call the function
        result = await delete_employee(employee_id)
        
        #assertion check that the result is true for successful deletion
        assert result is False

    


class AsyncCursorMock:
    def __init__(self, data):
        self.data = data

    async def to_list(self, length=None):
        return self.data

@pytest.mark.asyncio
async def test_get_all_employee():
    test_employee_data = [
        {
            "id": 1,
            "name": "John Doe",
            "national_id": 1234567890,
            "company_id": 1001,
            "start_date": "2023-01-01T00:00:00",
            "end_date": None,
            "position": "Sales Representative"
        },
        {
            "id": 2,
            "name": "Jane Smith",
            "national_id": 9876543210,
            "company_id": 1002,
            "start_date": "2023-02-01T00:00:00",
            "end_date": None,
            "position": "Marketing Manager"
        }
    ]

    # Create a mock MongoDB collection
    mock_collection = MagicMock()

    # Create a mock cursor object
    mock_cursor = AsyncCursorMock(test_employee_data)

    # Set up the find method to return the mock cursor
    mock_collection.find.return_value = mock_cursor

    with patch('src.modules.employees.employees_crud.employee_collection', mock_collection):
        result = await get_all_employee()

        # Convert test data to Employee instances
        expected_result = [Employee(**data) for data in test_employee_data]

        # Assertions by comparing dictionaries
        assert [employee.model_dump() for employee in result] == [employee.model_dump() for employee in expected_result], \
            f"Expected {[employee.model_dump() for employee in expected_result]} but got {[employee.model_dump() for employee in result]}"

    # Verify that the methods were called as expected
    mock_collection.find.assert_called_once_with({})