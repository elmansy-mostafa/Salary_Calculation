from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from shared.models_schemas.models import DailyReport, Employee, User
import os
from dotenv import load_dotenv
from mongomock import MongoClient


dotenv_path = os.path.join(os.path.dirname(__file__), '..', 'env', '.env')
load_dotenv(dotenv_path)

# Check if the TESTING environment variable is set to "True"
if os.getenv("TESTING") == "True":
    # Create a mock MongoDB client
    mock_client = MongoClient()
    database = mock_client['test_db']  # Use a test database
    
else:
    # Use the real MongoDB client
    mongo_uri = os.getenv("MONGO_URI")
    client = AsyncIOMotorClient(mongo_uri)
    
    # specifying database within mongodb
    DATABASE_NAME = os.getenv("DATABASE_NAME")
    database = client[DATABASE_NAME]

# defining collections within the database
employee_collection = database["employees"]
daily_report_collection = database["daily_reports"]
user_collection = database["users"]

# Function to initialize beanie with the database and models
async def init_db():
    await init_beanie(database=database, document_models=[DailyReport, Employee, User])