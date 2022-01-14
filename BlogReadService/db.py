import settings
import asyncio
import sys
from motor.motor_asyncio import AsyncIOMotorClient


db_client: AsyncIOMotorClient = None


try:
    db_client = AsyncIOMotorClient(settings.DATABASE_URL)
    db_client.get_io_loop = asyncio.get_running_loop
except Exception as e:
    settings.logger.error("Couldn't connect to db")
    settings.logger.error(e)
    sys.exit(-1)
    
database = db_client.BlogReadDB