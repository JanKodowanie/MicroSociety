from fastapi import Depends
from .models import *
from .schemas import *
from .exceptions import *
from core.posts.models import BlogPost
from core.posts.managers import BlogPostManager
from core.posts.exceptions import BlogPostNotFound
from tortoise.exceptions import DoesNotExist


class CommentManager:
    
    def __init__(self, blog_post_manager: BlogPostManager = Depends()):
        self.blog_post_manager = blog_post_manager
    
    async def create(self, creator_id: UUID, content: CommentCreateSchema, post_id: int) -> Comment:
        try:
            post = await self.blog_post_manager.get(post_id)
        except BlogPostNotFound as e:
            raise e
        
        instance = await Comment.create(creator_id=creator_id, post=post, **content.dict())
        return instance
    
    async def edit(self, instance: Comment, new_content: CommentUpdateSchema) -> Comment:
        instance.content = new_content.content
        await instance.save()
        
    async def get(self, id: int) -> Comment:
        try:
            instance = await Comment.get(id=id)
        except DoesNotExist:
            raise CommentNotFound()
        
        return instance
    
    async def delete(self, instance: Comment):
        await instance.delete()
        
    async def bulk_delete(self, filters: dict = None):
        comments = await Comment.filter(**filters)
        for comment in comments:
            self.delete(comment)