from .schemas import *
from core.events.received import BlogUserCreated, \
        BlogUserUpdated, BlogUserDeleted
from db import database
from uuid import UUID


class BlogUserCollectionManager:
    
    def __init__(self):
        self.collection = database.blog_users
        
    async def create(self, event: BlogUserCreated):
        data = BlogUserModel(**event.dict())
        await self.collection.insert_one(data.dict())
        
    async def get(self, id: UUID):
        return await self.collection.find_one({"id": id})
    
    async def update(self, event: BlogUserUpdated):
        new_data = BlogUserModel(**event.dict())
        await self.collection.update_one({"id": new_data.id}, {"$set": new_data.dict()})
        
    async def delete(self, event: BlogUserDeleted):
        return await self.collection.delete_one({"id": event.id})