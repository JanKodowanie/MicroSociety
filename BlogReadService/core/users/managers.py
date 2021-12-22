from .schemas import *
from db import database
from uuid import UUID
from settings import logger


class BlogUserCollectionManager:
    
    def __init__(self):
        self.collection = database.blog_users
        
    async def create(self, event: BlogUserCreatedEvent):
        data = BlogUserModel(**event.dict())
        await self.collection.insert_one(data.dict())
        
    async def get(self, id: UUID):
        return await self.collection.find_one({"id": id})
    
    async def update(self, event: BlogUserUpdatedEvent):
        new_data = BlogUserModel(**event.dict())
        await self.collection.update_one({"id": new_data.id}, {"$set": new_data.dict()})
        
    async def delete(self, event: BlogUserDeletedEvent):
        return await self.collection.delete_one({"id": event.id})