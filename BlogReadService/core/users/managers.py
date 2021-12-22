from .schemas import *
from db import get_db


class BlogUserCollectionManager:
        
    async def create(self, event: BlogUserCreatedEvent):
        collection = await get_db().blog_users
        data = BlogUserModel(**event.dict())
        await collection.insert_one(data.dict())