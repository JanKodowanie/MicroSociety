import settings
from motor.motor_asyncio import AsyncIOMotorClient
import sys


db_client: AsyncIOMotorClient = None


async def get_db() -> AsyncIOMotorClient:
    """Return database client instance."""
    return db_client.BlogReadDB


async def connect_db():
    try:
        db_client = AsyncIOMotorClient(settings.DATABASE_URL)
    except Exception as e:
        settings.logger.error("Couldn't connect to db")
        settings.logger.error(e)
        sys.exit(-1)
    
    
async def close_db():
    """Close database connection."""
    db_client.close()