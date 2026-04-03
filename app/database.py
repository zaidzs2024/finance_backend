import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()   # ✅ ADD THIS

MONGO_URL = os.getenv("MONGO_URL")

if not MONGO_URL:
    raise Exception("MONGO_URL is not set in environment variables")

client = AsyncIOMotorClient(MONGO_URL)

db = client.finance_db

users_collection = db["users"]
records_collection = db["records"]