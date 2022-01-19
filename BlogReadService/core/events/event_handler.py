from pydantic import ValidationError
from settings import logger
from .received import *
from core.users.schemas import *
from core.schemas import *
from core.users.managers import *
from core.managers import *
from db import database


class EventHandler:
    
    collection = database.received_events
    
    @classmethod
    async def handle_events(cls, event: dict, message_id: int, sender: str):
        if not await cls.collection.find_one({"message_id": message_id}):
            type = event.pop('event', None)
            model = ReceivedEventModel(message_id=message_id, domain=sender, name=type)
            await cls.collection.insert_one(model.dict())
            
            if type == "blog_user.created":
                await cls._handle_blog_user_created(event)
            if type == "blog_user.updated":
                await cls._handle_blog_user_updated(event)
            if type == "blog_user.deleted":
                await cls._handle_blog_user_deleted(event)
            if type == "post.created":
                await cls._handle_post_created(event)
            if type == "post.updated":
                await cls._handle_post_updated(event)
            if type == "post.deleted":
                await cls._handle_post_deleted(event)
            if type == "comment.created":
                await cls._handle_comment_created(event)
            if type == "comment.updated":
                await cls._handle_comment_updated(event)
            if type == "comment.deleted":
                await cls._handle_comment_deleted(event)
            if type == "like.created":
                await cls._handle_like_created(event)
            if type == "like.deleted":
                await cls._handle_like_deleted(event)
        else:
            logger.info('To zdarzenie zostało już obsłużone.')
        
        
    @classmethod
    async def _handle_blog_user_created(cls, event: dict):
        try:
            event = BlogUserCreated(**event)
        except ValidationError as e:
            logger.error(e)
            
        await BlogUserCollectionManager().create(event)
        
    @classmethod
    async def _handle_blog_user_updated(cls, event: dict):
        try:
            event = BlogUserUpdated(**event)
        except ValidationError as e:
            logger.error(e)
            
        await BlogUserCollectionManager().update(event)
        await PostCollectionManager().update_creator_data(event)
        await CommentCollectionManager().update_creator_data(event)
        
    @classmethod
    async def _handle_blog_user_deleted(cls, event: dict):
        try:
            event = BlogUserDeleted(**event)
        except ValidationError as e:
            logger.error(e)
            
        await BlogUserCollectionManager().delete(event)
        await PostCollectionManager().delete_posts_on_user_delete(event)
        await PostCollectionManager().delete_likes_on_user_delete(event)
        await CommentCollectionManager().delete_comments_on_user_delete(event)
        
    @classmethod
    async def _handle_post_created(cls, event: dict):
        try:
            event = PostCreated(**event)
        except ValidationError as e:
            logger.error(e)
            
        await PostCollectionManager().create(event)
        
    @classmethod
    async def _handle_post_updated(cls, event: dict):
        try:
            event = PostUpdated(**event)
        except ValidationError as e:
            logger.error(e)
            
        await PostCollectionManager().update_post(event)
        
    @classmethod
    async def _handle_post_deleted(cls, event: dict):
        try:
            event = PostDeleted(**event)
        except ValidationError as e:
            logger.error(e)
            
        await PostCollectionManager().delete(event)
        await CommentCollectionManager().delete_comments_on_post_delete(event)
        
    @classmethod
    async def _handle_comment_created(cls, event: dict):
        try:
            event = CommentCreated(**event)
        except ValidationError as e:
            logger.error(e)
            
        await CommentCollectionManager().create(event)
        
    @classmethod
    async def _handle_comment_updated(cls, event: dict):
        try:
            event = CommentUpdated(**event)
        except ValidationError as e:
            logger.error(e)
            
        await CommentCollectionManager().update_comment(event)
        
    @classmethod
    async def _handle_comment_deleted(cls, event: dict):
        try:
            event = CommentDeleted(**event)
        except ValidationError as e:
            logger.error(e)
            
        await CommentCollectionManager().delete(event)
        
        
    @classmethod
    async def _handle_like_created(cls, event: dict):
        try:
            event = LikeCreated(**event)
        except ValidationError as e:
            logger.error(e)
            
        await PostCollectionManager().create_post_like(event)
        
    @classmethod
    async def _handle_like_deleted(cls, event: dict):
        try:
            event = LikeDeleted(**event)
        except ValidationError as e:
            logger.error(e)
            
        await PostCollectionManager().delete_post_like(event)