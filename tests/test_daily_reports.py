import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch, AsyncMock
from mongomock import MongoClient
from datetime import datetime
from src.main import app
from src.modules.auth.authentication import create_access_token
from src.modules.daily_reports.daily_reports_controller import create_daily_report_control, delete_daily_report_control, get_all_daily_reports_control, get_daily_report_control, get_daily_reports_by_employee_and_renage_date_control, update_daily_report_control
from src.modules.daily_reports.daily_reports_router import get_all_daily_reports_endpoints, get_daily_reports_by_employee_and_renage_date_endpoint
from src.shared.models_schemas.models import  Deduction, DailyReport
from src.modules.daily_reports.daily_reports_crud import create_daily_report, delete_daily_report, get_all_daily_reports, get_daily_report, get_daily_reports_by_employee_and_range_date, update_daily_report
from src.shared.models_schemas.schemas import DailyReportCreate, DailyReportResponse

client = TestClient(app)

# Helper function to create a mock MongoDB client and collection
def get_mock_collection():
    mock_client = MongoClient()
    mock_db = mock_client['test_db']
    return mock_db['daily_report']

# drop the collection
def drop_mock_collection():
    collection = get_mock_collection()
    collection.drop()


# Helper function to prepare test daily_report data
def get_test_daily_report_data():
    return  {
        "date": datetime(2023, 1, 1).isoformat(),
        "employee_id": 1,
        "appointment": {
            "no_of_qualified_appointment": 5,
            "no_of_not_qualified_appointment": 2
        },
        "compensation": {
            "spiffs": 150,
            "kpis": 500,
            "butter_up": 5
        },
        "deductions": {
            "deductions": 50,
            "reason": "looser"
        },
        "allowance": {
            "allowance_type": "test",
            "allowance_value": 100
        },
        "adherence_status": True,
        "total_salary": 1550,
        "is_saturday": True,
        "working_hours": 7
    }

# test for create daily_report
@pytest.mark.asyncio
async def test_create_daily_report():
    # Prepare test data
    test_daily_report_data = get_test_daily_report_data()
    test_daily_report = DailyReport(**test_daily_report_data)

    # Create a mock MongoDB collection
    mock_collection = MagicMock()

    # Patch the employee_collection used in create_employee
    with patch('src.modules.daily_reports.daily_reports_crud.daily_report_collection', mock_collection):
        # Mock the insert_one method to be an async method
        mock_collection.insert_one.return_value = test_daily_report_data

        # Call the function
        result = await create_daily_report(test_daily_report)

        # Assertions: Check all attributes and type
        assert result== test_daily_report
        # Verify that the employee was inserted into the collection
        mock_collection.insert_one.assert_called_once_with(test_daily_report.model_dump())
        
        
@pytest.mark.asyncio
async def test_create_daily_report():
    # Prepare test data
    test_daily_report_data = get_test_daily_report_data()
    test_daily_report = DailyReport(**test_daily_report_data)
    values_id = 1  # Mock value for values_id
    employee_id = 1  # Mock value for employee_id

    # Create a mock MongoDB collection
    mock_collection = MagicMock()

    # Mock the get_static_values and get_employee functions
    with patch('src.modules.daily_reports.daily_reports_crud.daily_report_collection', mock_collection), \
        patch('src.modules.static_values.static_values_crud.get_static_values') as mock_get_static_values, \
        patch('src.modules.employees.employees_crud.get_employee') as mock_get_employee:

        # Mock return values for get_static_values and get_employee
        mock_get_static_values.return_value = {"hour_price": {"tier_A": 33.33}}  # Mock static values
        mock_get_employee.return_value = {"tier_type": "tier_A"}  # Mock employee data

        # Mock the insert_one method to simulate insertion
        mock_collection.insert_one.return_value = test_daily_report_data

        # Call the function with all required arguments
        result = await create_daily_report(test_daily_report, values_id, employee_id)

        # Assertions: Check if the returned report matches the input
        assert result == test_daily_report

        # Verify that the report was inserted into the collection
        mock_collection.insert_one.assert_called_once_with(test_daily_report.model_dump())

# Test for create_daily_report_control
@pytest.mark.asyncio
async def test_create_daily_report_control():
    # Prepare test data
    test_daily_report_data = get_test_daily_report_data()
    test_report_create_data = DailyReportCreate(**test_daily_report_data)
    test_daily_report = DailyReport(**test_daily_report_data)
    values_id = 1  # Mock value for values_id
    employee_id = 1  # Mock value for employee_id

    # Patch create_daily_report
    with patch('src.modules.daily_reports.daily_reports_controller.create_daily_report', AsyncMock(return_value=test_daily_report)):
        result = await create_daily_report_control(test_report_create_data, values_id, employee_id)

        # Assertions: Check all attributes and type
        assert result== test_daily_report


# Test for create_daily_report_endpoint
@pytest.mark.asyncio
async def test_create_daily_report_endpoint():
    # Prepare test data
    test_daily_report_data = get_test_daily_report_data()
    test_daily_report = DailyReportResponse(**test_daily_report_data)
    values_id = 1  # Mock value for values_id
    employee_id = 1  # Mock value for employee_id
    
    # Mock the create_daily_report_control function to return a test employee
    with patch('src.modules.daily_reports.daily_reports_controller.create_daily_report_control', AsyncMock(return_value=test_daily_report)):
        # Patch the authorization dependency to always return a valid user
        with patch('src.modules.auth.authorizations.get_admin', return_value={"email": "admin@example.com", "role": "admin"}):
            # Create a mock token for the authenticated user
            token = create_access_token({"sub": "admin@example.com", "role": "admin"})

            # Call the create_employee_endpoint using FastAPI's TestClient with authentication
            response = client.post(
                f"/daily_reports/static_values/{values_id}/employee/{employee_id}",
                json=test_daily_report_data,
                headers={"Authorization": f"Bearer {token}"}
            )

            # Assertions
            assert response.status_code == 200
            response_json = response.json()
            assert response_json['date'] == test_daily_report.date.isoformat()
            assert response_json['employee_id'] == test_daily_report.employee_id
            assert response_json['adherence_status'] == test_daily_report.adherence_status
            assert response_json['appointment'] == test_daily_report.appointment.model_dump()
            assert response_json['compensation'] == test_daily_report.compensation.model_dump()
            assert response_json['allowance'] == test_daily_report.allowance.model_dump()
            assert response_json['deductions'] == test_daily_report.deductions.model_dump()
            assert response_json['total_salary'] == test_daily_report.total_salary
            assert response_json['is_saturday'] == test_daily_report.is_saturday
            assert response_json['working_hours'] == test_daily_report.working_hours


# test for get daily_report
@pytest.mark.asyncio
async def test_get_daily_report():
    # Prepare test data
    test_daily_report_data = get_test_daily_report_data()
    test_daily_report = DailyReport(**test_daily_report_data)

    # Create a mock MongoDB collection
    mock_collection = MagicMock()

    # Patch the employee_collection used in create_employee
    with patch('src.modules.daily_reports.daily_reports_crud.daily_report_collection', mock_collection):
        # Mock the find_one method to be an async method
        mock_collection.find_one.return_value = test_daily_report.model_dump()

        # Call the function
        result = await get_daily_report(test_daily_report.employee_id, test_daily_report.date)

        # Assertions: Check all attributes and type
        assert result is not None, "Expected result to be an Employee instance, but got None"
        assert result.model_dump() == test_daily_report.model_dump()

    # Test for a non-existent employee
    with patch('src.modules.daily_reports.daily_reports_crud.daily_report_collection', mock_collection):
        # Mock the find_one method to return None for a non-existent employee
        mock_collection.find_one.return_value = None

        result = await get_daily_report(999, datetime(2024, 11, 16))  # ID that does not exist
        assert result is None, "Expected result to be None for a non-existent employee"
        



# Test for get_daily_report_control
@pytest.mark.asyncio
async def test_get_daily_report_control():
    # Prepare test data
    test_daily_report_data = get_test_daily_report_data()
    test_daily_report = DailyReport(**test_daily_report_data)

    # Patch get_daily_report
    with patch('src.modules.daily_reports.daily_reports_controller.get_daily_report', AsyncMock(return_value=test_daily_report)):
        result = await get_daily_report_control(test_daily_report.employee_id, test_daily_report.date)

        # Assertions: Check all attributes and type
        assert result== test_daily_report


# Test for get_daily_report_endpoint
@pytest.mark.asyncio
async def test_get_daily_report_endpoint():
    # Prepare test data
    test_daily_report_data = get_test_daily_report_data()
    test_daily_report = DailyReportResponse(**test_daily_report_data)

    # Mock the get_daily_report_control function to return a test employee
    with patch('src.modules.daily_reports.daily_reports_controller.get_daily_report_control', AsyncMock(return_value=test_daily_report)):
        # Patch the authorization dependency to always return a valid user
        with patch('src.modules.auth.authorizations.get_admin', return_value={"email": "admin@example.com", "role": "admin"}):
            # Create a mock token for the authenticated user
            token = create_access_token({"sub": "admin@example.com", "role": "admin"})

            # Call the create_employee_endpoint using FastAPI's TestClient with authentication
            response = client.get(
                f"/daily_reports/{test_daily_report.employee_id}/daily_reports/{test_daily_report.date}",
                headers={"Authorization": f"Bearer {token}"}
            )

            # Assertions
            assert response.status_code == 200
            response_json = response.json()
            assert response_json['date'] == test_daily_report.date.isoformat()
            assert response_json['employee_id'] == test_daily_report.employee_id
            assert response_json['adherence_status'] == test_daily_report.adherence_status
            assert response_json['appointment'] == test_daily_report.appointment.model_dump()
            assert response_json['compensation'] == test_daily_report.compensation.model_dump()
            assert response_json['allowance'] == test_daily_report.allowance.model_dump()
            assert response_json['deductions'] == test_daily_report.deductions.model_dump()
            assert response_json['total_salary'] == test_daily_report.total_salary
            assert response_json['is_saturday'] == test_daily_report.is_saturday
            assert response_json['working_hours'] == test_daily_report.working_hours

# test for update daily_report
@pytest.mark.asyncio
async def test_update_daily_report():
    # drop mock_collection
    drop_mock_collection()
    
    # Prepare test data
    test_daily_report_data = get_test_daily_report_data()
    test_daily_report = DailyReport(**test_daily_report_data)
    updated_data = {"total_salary": 2000}

    # Create a mock MongoDB collection
    mock_collection = MagicMock()
    
    # Patch the daily_report_collection used in update_daily_report
    with patch('src.modules.daily_reports.daily_reports_crud.daily_report_collection', mock_collection):
        # Mock the find_one_and_update method to return the updated daily_report data
        updated_report = test_daily_report.model_dump()
        updated_report.update(updated_data)
        mock_collection.find_one_and_update.return_value = updated_report

        # Call the function
        result = await update_daily_report(test_daily_report.employee_id, test_daily_report.date, updated_data)

        # Assertions: Check that the result is as expected
        assert result is not None, "Expected an daily_report instance, but got None"
        assert result.employee_id == test_daily_report.employee_id
        assert result.date == test_daily_report.date
        assert result.total_salary == 2000  # Updated attribute


    # Patch the daily_report_collection used in update_daily_report
    with patch('src.modules.daily_reports.daily_reports_crud.daily_report_collection', mock_collection):
        # Mock the find_one_and_update method to return None for a non-existent daily_report
        mock_collection.find_one_and_update.return_value = None

        # Call the function
        result = await update_daily_report(999, datetime(2024, 11, 2), updated_data)  # ID that does not exist

        # Assertions: Check that the result is None
        assert result is None, "Expected result to be None for a non-existent daily_report"


# Test for update_daily_report_control
@pytest.mark.asyncio
async def test_update_daily_report_control():
    # drop mock_collection
    drop_mock_collection()
    
    # Prepare test data
    test_daily_report_data = get_test_daily_report_data()
    test_daily_report_data['total_salary'] = 2000
    test_daily_report = DailyReport(**test_daily_report_data)
    updated_data = {"total_salary": 2000}


    # Patch update_daily_report
    with patch('src.modules.daily_reports.daily_reports_controller.update_daily_report', AsyncMock(return_value=test_daily_report)):
        result = await update_daily_report_control(test_daily_report.employee_id, test_daily_report.date, updated_data)

        # Assertions: Check all attributes and type
        assert result is not None, "Expected an daily_report instance, but got None"
        assert result.employee_id == test_daily_report.employee_id
        assert result.date == test_daily_report.date
        assert result.total_salary == 2000


# Test for update_daily_report_endpoint
@pytest.mark.asyncio
async def test_update_daily_report_endpoint():
    # drop mock_collection
    drop_mock_collection()
    
    # Prepare test data
    test_daily_report_data = get_test_daily_report_data()
    test_daily_report_data['total_salary'] = 2000
    test_daily_report = DailyReportResponse(**test_daily_report_data)
    updated_data = {"total_salary": 2000}

    # Mock the update_daily_report_control function to return a test employee
    with patch('src.modules.daily_reports.daily_reports_controller.update_daily_report_control', AsyncMock(return_value=test_daily_report)):
        # Patch the authorization dependency to always return a valid user
        with patch('src.modules.auth.authorizations.get_admin', return_value={"email": "admin@example.com", "role": "admin"}):
            # Create a mock token for the authenticated user
            token = create_access_token({"sub": "admin@example.com", "role": "admin"})

            # Call the update_employee_endpoint using FastAPI's TestClient with authentication
            response = client.put(
                f"/daily_reports/{test_daily_report.employee_id}/daily_reports/{test_daily_report.date}",
                json=test_daily_report_data,
                headers={"Authorization": f"Bearer {token}"}
            )

            # Assertions
            assert response.status_code == 200
            response_json = response.json()
            assert response_json['employee_id'] == test_daily_report.employee_id
            assert response_json['total_salary'] == updated_data["total_salary"]
    
        
# test foe delete daily_report
@pytest.mark.asyncio
async def test_delete_daily_report():
    # Prepare test data
    test_daily_report_data = get_test_daily_report_data()
    test_daily_report = DailyReport(**test_daily_report_data)
    test_daily_report.employee_id = 1
    test_daily_report.date = datetime(2024, 10, 10)
    
    # Create a mock MongoDB collection    
    mock_collection = MagicMock()
    
    # Patch the daily_report_collection used in get_daily_report
    with patch('src.modules.daily_reports.daily_reports_crud.daily_report_collection', mock_collection):
        
        # Mock the delete_one method to return result including successful deletion
        mock_collection.delete_one.return_value = True
        
        # Call the function
        result = await delete_daily_report(test_daily_report.employee_id, test_daily_report.date)
        
        #assertion check that the result is true for successful deletion
        assert result is True

    # Patch the daily_report_collection used in get_daily_report
    with patch('src.modules.daily_reports.daily_reports_crud.daily_report_collection', mock_collection):
        
        # Mock the delete_one method to return result including successful deletion
        mock_collection.delete_one.return_value = False
        
        # Call the function
        result = await delete_daily_report(test_daily_report.employee_id, test_daily_report.date)
        
        #assertion check that the result is true for successful deletion
        assert result is False


# Test for delete_daily_report_control
@pytest.mark.asyncio
async def test_delete_daily_report_control():
    # Prepare test data
    test_daily_report_data = get_test_daily_report_data()
    test_daily_report = DailyReport(**test_daily_report_data)
    test_daily_report.employee_id = 1
    test_daily_report.date = datetime(2024, 10, 10)

    # Patch delete_daily_report
    with patch('src.modules.daily_reports.daily_reports_controller.delete_daily_report', AsyncMock(return_value=True)):
        result = await delete_daily_report_control(test_daily_report.employee_id, test_daily_report.date)

        # Assertions
        assert result is True


# Test for delete_daily_report_endpoint
@pytest.mark.asyncio
async def test_delete_daily_report_endpoint():
    # Prepare test data
    test_daily_report_data = get_test_daily_report_data()
    test_daily_report = DailyReport(**test_daily_report_data)
    test_daily_report.employee_id = 1
    test_daily_report.date = datetime(2024, 10, 10)

    # Mock the delete_daily_report_control function to return a test employee
    with patch('src.modules.daily_reports.daily_reports_controller.delete_daily_report_control', AsyncMock(return_value=True)):
        # Patch the authorization dependency to always return a valid user
        with patch('src.modules.auth.authorizations.get_admin', return_value={"email": "admin@example.com", "role": "admin"}):
            # Create a mock token for the authenticated user
            token = create_access_token({"sub": "admin@example.com", "role": "admin"})

            # Call the update_employee_endpoint using FastAPI's TestClient with authentication
            response = client.delete(
                f"/daily_reports/{test_daily_report.employee_id}/daily_reports/{test_daily_report.date}",
                headers={"Authorization": f"Bearer {token}"}
            )

            # Assertions
            assert response.status_code == 200
            assert response.json() is True


def get_test_data():
    return [
        {
        "date": datetime(2023, 1, 1).isoformat(),
        "employee_id": 1,
        "appointment": {
            "no_of_qualified_appointment": 5,
            "no_of_not_qualified_appointment": 2
        },
        "compensation": {
            "spiffs": 150,
            "kpis": 500,
            "butter_up": 5
        },
        "deductions": {
            "deductions": 50,
            "reason": "looser"
        },
        "allowance": {
            "allowance_type": "test",
            "allowance_value": 100
        },
        "adherence_status": True,
        "total_salary": 1550,
        "is_saturday": True,
        "working_hours": 7
    },
        {
        "date": datetime(2024, 5, 1).isoformat(),
        "employee_id": 2,
        "appointment": {
            "no_of_qualified_appointment": 6,
            "no_of_not_qualified_appointment": 2
        },
        "compensation": {
            "spiffs": 200,
            "kpis": 500,
            "butter_up": 5
        },
        "deductions": {
            "deductions": 50,
            "reason": "looser"
        },
        "allowance": {
            "allowance_type": "test",
            "allowance_value": 100
        },
        "adherence_status": True,
        "total_salary": 1550,
        "is_saturday": True,
        "working_hours": 7
    }
    ]
    
    
# test for get all daily_reports    
@pytest.mark.asyncio
async def test_get_all_daily_reports():
    test_daily_report_data = get_test_data()

    # Convert the test data into daily_report instances
    mock_daily_report_data = [DailyReport(**data) for data in test_daily_report_data]

    # Mock the collection's find method to return the test data
    mock_collection = MagicMock()
    mock_collection.find.return_value = test_daily_report_data

    # Patch the daily_report_collection to use the mock collection
    with patch('src.modules.daily_reports.daily_reports_crud.daily_report_collection', mock_collection):
        result = await get_all_daily_reports()
        # Convert results to dictionaries for easy comparison
        assert [daily_report.model_dump() for daily_report in result] == [daily_report.model_dump() for daily_report in mock_daily_report_data]

    # Check if the find method was called once with no arguments
    mock_collection.find.assert_called_once_with({})

@pytest.mark.asyncio
async def test_get_all_daily_reports_control():
    test_daily_report_data = get_test_data()

    # Convert the test data into daily_report instances
    mock_daily_report_data = [DailyReport(**data) for data in test_daily_report_data]
    
    # Mock the collection's find method to return the test data
    mock_collection = MagicMock()
    mock_collection.find.return_value = test_daily_report_data

    # Patch the daily_report_collection to use the mock collection
    with patch('src.modules.daily_reports.daily_reports_crud.daily_report_collection', mock_collection):
        # Mock the get_all_daily_report function to return the test data
        with patch('src.modules.daily_reports.daily_reports_crud.get_all_daily_reports', return_value=mock_daily_report_data):
            # Call the function under test
            result = await get_all_daily_reports_control()

            # Ensure results match the expected data structure
            assert [daily_report.model_dump() for daily_report in result] == [daily_report.model_dump() for daily_report in mock_daily_report_data]

@pytest.mark.asyncio
async def test_get_all_daily_reports_endpoint():
    test_daily_report_data = get_test_data()
    
    mock_daily_report_data = [DailyReport(**data) for data in test_daily_report_data]

    mock_collection = MagicMock()
    mock_collection.find.return_value = test_daily_report_data

    with patch('src.modules.daily_reports.daily_reports_crud.daily_report_collection', mock_collection):
        # Patch get_all_daily_report instead of get_all_daily_reports_control
        with patch('src.modules.daily_reports.daily_reports_crud.get_all_daily_reports', return_value=mock_daily_report_data) as mock_get_all:
            with patch('src.modules.daily_reports.daily_reports_router.get_all_daily_reports_endpoints', return_value=mock_daily_report_data) as mock_get_all:
                result = await get_all_daily_reports_endpoints()
                with patch('src.modules.auth.authorizations.get_admin', return_value={"email": "admin@example.com", "role": "admin"}):      
                    token = create_access_token({"sub": "admin@example.com", "role": "admin"})

                    response = client.get(
                        "/daily_reports",
                        headers={"Authorization": f"Bearer {token}"}
                        )
                        
                    assert response.status_code == 200
                    # assert response.json() == [daily_report.model_dump() for daily_report in mock_daily_report_data]
                    assert [daily_report.model_dump() for daily_report in result] ==[daily_report.model_dump() for daily_report in mock_daily_report_data]

    
def get_test_data():
    return [
        {
        "date": datetime(2023, 8, 16).isoformat(),
        "employee_id": 1,
        "appointment": {
            "no_of_qualified_appointment": 5,
            "no_of_not_qualified_appointment": 2
        },
        "compensation": {
            "spiffs": 150,
            "kpis": 500,
            "butter_up": 5
        },
        "deductions": {
            "deductions": 50,
            "reason": "looser"
        },
        "allowance": {
            "allowance_type": "test",
            "allowance_value": 100
        },
        "adherence_status": True,
        "total_salary": 1550,
        "is_saturday": True,
        "working_hours": 7
    },
        {
        "date": datetime(2024, 8, 17).isoformat(),
        "employee_id": 1,
        "appointment": {
            "no_of_qualified_appointment": 6,
            "no_of_not_qualified_appointment": 2
        },
        "compensation": {
            "spiffs": 200,
            "kpis": 500,
            "butter_up": 5
        },
        "deductions": {
            "deductions": 50,
            "reason": "looser"
        },
        "allowance": {
            "allowance_type": "test",
            "allowance_value": 100
        },
        "adherence_status": True,
        "total_salary": 2020,
        "is_saturday": True,
        "working_hours": 7
    },
        {
        "date": datetime(2024, 8, 18).isoformat(),
        "employee_id": 2,
        "appointment": {
            "no_of_qualified_appointment": 6,
            "no_of_not_qualified_appointment": 6
        },
        "compensation": {
            "spiffs": 300,
            "kpis": 500,
            "butter_up": 5
        },
        "deductions": {
            "deductions": 100,
            "reason": "looser"
        },
        "allowance": {
            "allowance_type": "test",
            "allowance_value": 200
        },
        "adherence_status": True,
        "total_salary": 1566,
        "is_saturday": True,
        "working_hours": 7
    }
    ]
    
# test for get dailyreport by specific employee and range date
@pytest.mark.asyncio
async def test_get_daily_reports_by_employee_and_range_date():
    test_daily_report_data = get_test_data()

    # Convert the test data into daily_report instances
    mock_daily_report_data = [DailyReport(**data) for data in test_daily_report_data]

    # Mock the collection's find method to return the test data
    mock_collection = MagicMock()
    mock_collection.find.return_value = test_daily_report_data

    # Patch the daily_report_collection to use the mock collection
    with patch('src.modules.daily_reports.daily_reports_crud.daily_report_collection', mock_collection):
        # Call the function with a specific employee_id and date range
        start_date = datetime(2024, 8, 16)
        end_date = datetime(2024, 8, 17)
        result = await get_daily_reports_by_employee_and_range_date(employee_id=1, start_date=start_date, end_date=end_date)

        # Convert results to dictionaries for easy comparison
        assert [daily_report.model_dump() for daily_report in result] == [daily_report.model_dump() for daily_report in mock_daily_report_data]

    # Verify that the find method was called with the correct query
    expected_query = {"employee_id": 1, "date": {"$gte": start_date, "$lte": end_date}}
    mock_collection.find.assert_called_once_with(expected_query)

@pytest.mark.asyncio
async def test_get_daily_reports_by_employee_and_range_date_control():
    test_daily_report_data = get_test_data()

    # Convert the test data into daily_report instances
    mock_daily_report_data = [DailyReport(**data) for data in test_daily_report_data]
    
    # Mock the collection's find method to return the test data
    mock_collection = MagicMock()
    mock_collection.find.return_value = test_daily_report_data

    # Patch the daily_report_collection to use the mock collection
    with patch('src.modules.daily_reports.daily_reports_crud.daily_report_collection', mock_collection):
        # Mock the get_all_daily_report function to return the test data
        with patch('src.modules.daily_reports.daily_reports_crud.get_all_daily_reports', return_value=mock_daily_report_data):
            # Call the function with a specific employee_id and date range
            start_date = datetime(2024, 8, 16)
            end_date = datetime(2024, 8, 17)
            result = await get_daily_reports_by_employee_and_renage_date_control(employee_id=1, start_date=start_date, end_date=end_date)

            # Ensure results match the expected data structure
            assert [daily_report.model_dump() for daily_report in result] == [daily_report.model_dump() for daily_report in mock_daily_report_data]

@pytest.mark.asyncio
async def test_get_all_daily_reports_endpoint():
    test_daily_report_data = get_test_data()
    
    mock_daily_report_data = [DailyReport(**data) for data in test_daily_report_data]

    mock_collection = MagicMock()
    mock_collection.find.return_value = test_daily_report_data

    with patch('src.modules.daily_reports.daily_reports_crud.daily_report_collection', mock_collection):
        # Patch get_all_daily_report instead of get_all_daily_reports_control
        with patch('src.modules.daily_reports.daily_reports_crud.get_all_daily_reports', return_value=mock_daily_report_data) as mock_get_all:
            with patch('src.modules.daily_reports.daily_reports_router.get_all_daily_reports_endpoints', return_value=mock_daily_report_data) as mock_get_all:
                # Call the function with a specific employee_id and date range
                employee_id=1
                start_date = datetime(2024, 8, 16)
                end_date = datetime(2024, 8, 17)
                result = await get_daily_reports_by_employee_and_renage_date_endpoint(employee_id, start_date=start_date, end_date=end_date)

                with patch('src.modules.auth.authorizations.get_admin', return_value={"email": "admin@example.com", "role": "admin"}):      
                    token = create_access_token({"sub": "admin@example.com", "role": "admin"})

                    response = client.get(
                        f"/daily_reports/{employee_id}/daily_reports/{start_date}/{end_date}",
                        headers={"Authorization": f"Bearer {token}"}
                        )
                        
                    assert response.status_code == 200
                    # assert response.json() == [daily_report.model_dump() for daily_report in mock_daily_report_data]
                    assert [daily_report.model_dump() for daily_report in result] ==[daily_report.model_dump() for daily_report in mock_daily_report_data]

