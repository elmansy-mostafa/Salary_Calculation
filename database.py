from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from Salary_Calculation.models import DailyReport, Employee, UserInDB

# creating a client instance to interact with mongodb
client = AsyncIOMotorClient("mongodb://localhost:27017")

# specifying database within mongodb
database = client.Salary_Calculation

# defining collections within database
employee_collection = database.get_collection("employees")
daily_report_collection = database.get_collection("daily_reports")
user_collection = database.get_collection("users")

#function to initialize beanie with the database and models
async def init_db():
    await init_beanie(database, document_models=[DailyReport, Employee, UserInDB])
