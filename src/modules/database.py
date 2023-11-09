from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

client= AsyncIOMotorClient(os.getenv("URI"))

collection= client["Game_Cache"]["Games"]