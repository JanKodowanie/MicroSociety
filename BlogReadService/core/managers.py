import pymongo
from .schemas import *
from db import database
from core.users.managers import BlogUserCollectionManager
from core.users.schemas import BlogUserDeletedEvent, BlogUserUpdatedEvent


class PostCollectionManager:
    
    def __init__(self):
        self.collection = database.blog_posts
        self.blog_users = BlogUserCollectionManager()
        
    async def create(self, event: PostCreatedEvent):
        data = event.dict()
        creator_id = data.pop('creator_id')
        creator_data = await self.blog_users.get(creator_id)
        data['creator'] = creator_data
        
        model = PostBasicModel(**data)
        
        await self.collection.insert_one(model.dict())
        
    async def get(self, id: int):
        return await self.collection.find_one({"id": id})
    
    async def get_list(self):
        cursor = self.collection.find().sort([("date_created", pymongo.DESCENDING)])
        return await cursor.to_list(None)
    
    async def update_post(self, event: PostUpdatedEvent):
        new_data = event.dict()
        update_model = PostUpdateModel(**new_data)
        await self.collection.update_one({"id": event.id}, {"$set": update_model.dict()})
        
    async def update_creator_data(self, event: BlogUserUpdatedEvent):
        new_data = event.dict()
        update_model = PostCreatorUpdateModel(**new_data)
        await self.collection.update_many({"creator.id": event.id}, {"$set": update_model.dict()})
        
    async def delete(self, event: PostDeletedEvent):
        return await self.collection.delete_one({"id": event.post_id})
    
    async def delete_posts_on_user_delete(self, event: BlogUserDeletedEvent):
        return await self.collection.delete_many({"creator.id": event.id})