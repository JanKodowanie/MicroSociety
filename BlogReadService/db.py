from turtle import mode
import settings
import asyncio
import sys
from uuid import UUID
from motor.motor_asyncio import AsyncIOMotorClient
from core.users.schemas import BlogUserModel
from common.enums import *


db_client: AsyncIOMotorClient = None


try:
    db_client = AsyncIOMotorClient(settings.DATABASE_URL)
    db_client.get_io_loop = asyncio.get_running_loop
except Exception as e:
    settings.logger.error("Couldn't connect to db")
    settings.logger.error(e)
    sys.exit(-1)
    
database = db_client.BlogReadDB


async def insert_test_data():
    standard_id = UUID("346707ee-e153-4598-a469-4883dc9ccfca")
    standard = BlogUserModel(id=standard_id,
                        username='standard', rank=AccountRank.RANK_1, 
                        role=AccountRole.STANDARD, gender=AccountGender.MALE, picture_url=None)  
    if not await database.blog_users.find_one({"id": standard_id}):
        database.blog_users.insert_one(standard.dict())
    
    moderator_id = UUID("bd6539c5-fcbd-4177-b764-26eb6c51ccf8")
    moderator = BlogUserModel(id=moderator_id,
                        username='moderator', rank=AccountRank.RANK_1, 
                        role=AccountRole.MODERATOR, gender=AccountGender.MALE, picture_url=None)  
    if not await database.blog_users.find_one({"id": moderator_id}):
        database.blog_users.insert_one(moderator.dict())