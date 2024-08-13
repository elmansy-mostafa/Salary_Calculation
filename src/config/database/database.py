from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from beanie import init_beanie
from shared.models_schemas.models import DailyReport, Employee, User
import os
from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__), '..', 'env', '.env')
load_dotenv(dotenv_path)

# creating a client instance to interact with mongodb
mongo_uri = os.getenv("MONGO_URI")
client = AsyncIOMotorClient(mongo_uri)

# specifying database within mongodb
DATABASE_NAME = os.getenv("DATABASE_NAME")
database = client["DATABASE_NAME"]

# defining collections within database
employee_collection = database["employees"]
daily_report_collection = database["daily_reports"]
user_collection = database["users"]

print("Mongo URI:", mongo_uri)
print("User collection:", user_collection)

#function to initialize beanie with the database and models
async def init_db():
    await init_beanie(database=database, document_models=[DailyReport, Employee, User])

