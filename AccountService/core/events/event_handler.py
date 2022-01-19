from core.blog_users.managers import BlogUserManager
from common.events.models import *
from .received import *
from pydantic import ValidationError
from settings import logger


class EventHandler:
    
    blog_user_manager: BlogUserManager = BlogUserManager()
    
    @classmethod
    async def handle_events(cls, event: dict, message_id: int, sender: str):
        if not await ReceivedEvent.exists(message_id=message_id, domain=sender):
            type = event.pop('event', None)
            await ReceivedEvent.create(message_id=message_id, domain=sender, name=type)    
            
            if type == "like.created":
                await cls._handle_like_created(event)
            if type == "like.deleted":
                await cls._handle_like_deleted(event)
        else:
            logger.info('To zdarzenie zostało już obsłużone.')
            
    @classmethod
    async def _handle_like_created(cls, event: dict):
        try:
            event = LikeCreated(**event)
        except ValidationError as e:
            logger.error(e)
            
        await cls.blog_user_manager.increase_users_points(event.post_creator_id)
        
    @classmethod
    async def _handle_like_deleted(cls, event: dict):
        try:
            event = LikeDeleted(**event)
        except ValidationError as e:
            logger.error(e)
            
        await cls.blog_user_manager.decrease_users_points(event.post_creator_id)