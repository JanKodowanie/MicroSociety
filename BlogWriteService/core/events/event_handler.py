from fastapi import Depends
from settings import logger
from .received import BlogUserDeleted
from .models import *
from pydantic import ValidationError
from core.posts.managers import BlogPostManager
from core.comments.managers import CommentManager


class EventHandler:
    
    post_manager: BlogPostManager = BlogPostManager()
    comment_manager: CommentManager = CommentManager()
    
    @classmethod
    async def handle_events(cls, event: dict, message_id: int, sender: str):
        if not await ReceivedEvent.exists(message_id=message_id, domain=sender):
            await ReceivedEvent.create(message_id=message_id, domain=sender)
            type = event.pop('event', None)
            
            if type == "blog_user.deleted":
                await cls._handle_blog_user_deleted(event)
        else:
            logger.info('Event already processed')
        
        
    @classmethod
    async def _handle_blog_user_deleted(cls, event: dict):
        try:
            data = BlogUserDeleted(**event)
        except ValidationError as e:
            logger.error(e)
         
        await cls.post_manager.bulk_delete({'creator_id': data.id})
        await cls.comment_manager.bulk_delete({'creator_id': data.id})