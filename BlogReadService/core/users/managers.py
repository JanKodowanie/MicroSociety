from .schemas import *
from db import database


class BlogUserCollectionManager:
    
    def __init__(self):
        self.collection = database.blog_users
        
    async def create(self, event: BlogUserCreatedEvent):
        data = BlogUserModel(**event.dict())
        await self.collection.insert_one(data.dict())