from pydantic import ValidationError
from settings import logger
from core.users.schemas import *
from core.posts.schemas import *
from core.users.managers import *
from core.posts.managers import *


class EventHandler:
    
    @classmethod
    async def handle_events(cls, event: dict, message_id: int, sender: str):
        type = event.pop('event', None)
        
        if type == "blog_user.created":
            await cls._handle_blog_user_created(event)
        if type == "blog_user.updated":
            await cls._handle_blog_user_updated(event)
        if type == "blog_user.deleted":
            await cls._handle_blog_user_deleted(event)
        if type == "blog_post.created":
            await cls._handle_blog_post_created(event)
        if type == "blog_post.updated":
            await cls._handle_blog_post_updated(event)
        if type == "blog_post.deleted":
            await cls._handle_blog_post_deleted(event)
        
    @classmethod
    async def _handle_blog_user_created(cls, event: dict):
        try:
            event = BlogUserCreatedEvent(**event)
        except ValidationError as e:
            logger.error(e)
            
        await BlogUserCollectionManager().create(event)
        
    @classmethod
    async def _handle_blog_user_updated(cls, event: dict):
        try:
            event = BlogUserUpdatedEvent(**event)
        except ValidationError as e:
            logger.error(e)
            
        await BlogUserCollectionManager().update(event)
        await BlogPostCollectionManager().update_creator_data(event)
        
    @classmethod
    async def _handle_blog_user_deleted(cls, event: dict):
        try:
            event = BlogUserDeletedEvent(**event)
        except ValidationError as e:
            logger.error(e)
            
        await BlogUserCollectionManager().delete(event)
        await BlogPostCollectionManager().delete_posts_on_user_delete(event)
        
    @classmethod
    async def _handle_blog_post_created(cls, event: dict):
        try:
            event = BlogPostCreatedEvent(**event)
        except ValidationError as e:
            logger.error(e)
            
        await BlogPostCollectionManager().create(event)
        
    @classmethod
    async def _handle_blog_post_updated(cls, event: dict):
        try:
            event = BlogPostUpdatedEvent(**event)
        except ValidationError as e:
            logger.error(e)
            
        await BlogPostCollectionManager().update_post(event)
        
    @classmethod
    async def _handle_blog_post_deleted(cls, event: dict):
        try:
            event = BlogPostDeletedEvent(**event)
        except ValidationError as e:
            logger.error(e)
            
        await BlogPostCollectionManager().delete(event)