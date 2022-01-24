import pymongo
from .schemas import *
from db import database
from core.users.managers import BlogUserCollectionManager
from core.events.received import *
from typing import List, Optional


class TagCollectionManager:
    def __init__(self):
        self.collection = database.tags
        
    async def create_or_increase_popularity(self, post: PostUpdateModel):
        for tag in post.tag_list:
            await self.collection.update_one({"name": tag}, {"$inc": {"popularity": 1}}, upsert=True)
            
    async def decrease_popularity(self, post: PostUpdateModel):
        for tag in post.tag_list:
            await self.collection.update_one({"name": tag}, {"$inc": {"popularity": -1}})
            
    async def get_tags(self, name_contains: Optional[str] = None) -> List[dict]:
        filters = {
            "popularity": {"$gt": 0}
        }
        if name_contains:
            filters["name"] = {"$regex": name_contains}
            
        cursor = self.collection.find(filters).sort([("popularity", pymongo.DESCENDING)])
        return await cursor.to_list(None)
    
        
class PostCollectionManager:
    
    def __init__(self):
        self.collection = database.posts
        self.blog_users = BlogUserCollectionManager()
        self.tags = TagCollectionManager()
        
    async def create(self, event: PostCreated):
        data = event.dict()
        creator_id = data.pop('creator_id')
        creator_data = await self.blog_users.get(creator_id)
        data['creator'] = creator_data
        
        model = PostModel(**data)
        await self.collection.insert_one(model.dict())
        await self.tags.create_or_increase_popularity(model)
        
    async def get(self, id: int) -> dict:
        return await self.collection.find_one({"id": id})
    
    async def get_list(self, filters: PostListQueryParams) -> Optional[List[dict]]:
        filters_dict = filters.dict()
        ordering = filters_dict.pop('ordering')
    
        if filters_dict:
            cursor = self.collection.find(filters_dict).sort([ordering])
        else: 
            cursor = self.collection.find().sort([ordering])
        return await cursor.to_list(None)
    
    async def update_post(self, event: PostUpdated):
        old_model = PostModel(**(await self.get(event.id)))
        await self.tags.decrease_popularity(old_model)
        
        new_data = event.dict()
        update_model = PostUpdateModel(**new_data)
        await self.collection.update_one({"id": event.id}, {"$set": update_model.dict()})
        await self.tags.create_or_increase_popularity(update_model)
        
    async def update_creator_data(self, event: BlogUserUpdated):
        new_data = event.dict()
        update_model = CreatorUpdateModel(**new_data)
        await self.collection.update_many({"creator.id": event.id}, {"$set": update_model.dict()})
        
    async def delete(self, event: PostDeleted):
        post = await self.collection.find_one({"id": event.id})
        await self.tags.decrease_popularity(PostModel(**post))
        return await self.collection.delete_one({"id": event.id})
    
    async def delete_posts_on_user_delete(self, event: BlogUserDeleted):
        cursor = self.collection.find({"creator.id": event.id})
        posts = await cursor.to_list(None)
        for post in posts:
            await self.tags.decrease_popularity(PostModel(**post))
        return await self.collection.delete_many({"creator.id": event.id})

    async def create_post_like(self, event: LikeCreated):
        await self.collection.update_one({"id": event.post_id}, 
                                        {"$push": {"like_list": event.creator_id},
                                         "$inc": {"like_count": 1}})

    async def delete_post_like(self, event: LikeDeleted):
        await self.collection.update_one({"id": event.post_id}, 
                                        {"$pull": {"like_list": event.creator_id},
                                         "$inc": {"like_count": -1}})
        
    async def delete_likes_on_user_delete(self, event: BlogUserDeleted):
        await self.collection.update_many({"like_list": event.id}, 
                                        {"$pull": {"like_list": event.id},
                                         "$inc": {"like_count": -1}})
    
    
class CommentCollectionManager:
    
    def __init__(self):
        self.collection = database.comments
        self.blog_users = BlogUserCollectionManager()
        
    async def create(self, event: PostCreated):
        data = event.dict()
        creator_id = data.pop('creator_id')
        creator_data = await self.blog_users.get(creator_id)
        data['creator'] = creator_data
        model = CommentModel(**data)
        await self.collection.insert_one(model.dict())
        
    async def get(self, id: int) -> dict:
        return await self.collection.find_one({"id": id})
        
    async def get_comments_for_post(self, post_id: int) -> Optional[List[dict]]:
        cursor = self.collection.find({"post_id": post_id}).sort([("date_created", pymongo.DESCENDING)])
        return await cursor.to_list(None)
    
    async def update_comment(self, event: CommentUpdated):
        new_data = event.dict()
        update_model = CommentUpdateModel(**new_data)
        await self.collection.update_one({"id": event.id}, {"$set": update_model.dict()})
        
    async def update_creator_data(self, event: BlogUserUpdated):
        new_data = event.dict()
        update_model = CreatorUpdateModel(**new_data)
        await self.collection.update_many({"creator.id": event.id}, {"$set": update_model.dict()})
        
    async def delete(self, event: CommentDeleted):
        return await self.collection.delete_one({"id": event.id})
    
    async def delete_comments_on_post_delete(self, event: PostDeleted):
        return await self.collection.delete_many({"post_id": event.id})
    
    async def delete_comments_on_user_delete(self, event: BlogUserDeleted):
        return await self.collection.delete_many({"creator.id": event.id})