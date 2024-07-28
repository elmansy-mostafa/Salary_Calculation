from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from models import DailyReport, Employee

async def init_db():
    client = AsyncIOMotorClient("monogodb://localhost:27017")
    db = client.telesales
    await init_beanie(database=db, document_models=[DailyReport, Employee])
