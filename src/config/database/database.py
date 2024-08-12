from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from shared.models_schemas.models import DailyReport, Employee, User
import os
from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__), '..', 'env', '.env')
load_dotenv(dotenv_path)

# creating a client instance to interact with mongodb
DATABASE_URL = os.getenv("DATABASE_URL")
client = AsyncIOMotorClient(DATABASE_URL)

# specifying database within mongodb
DATABASE_NAME = os.getenv("DATABASE_NAME")
database = client.DATABASE_NAME

# defining collections within database
employee_collection = database.get_collection("employees")
daily_report_collection = database.get_collection("daily_reports")
user_collection = database.get_collection("users")

#function to initialize beanie with the database and models
async def init_db():
    await init_beanie(database=database, document_models=[DailyReport, Employee, User])

