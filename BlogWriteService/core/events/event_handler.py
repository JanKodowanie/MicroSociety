from settings import logger
from .received import *
from common.events.models import *
from pydantic import ValidationError
from core.managers import PostManager
from core.comments.managers import CommentManager
from common.auth.models import FullLogoutEvent


class EventHandler:
    
    post_manager: PostManager = PostManager()
    comment_manager: CommentManager = CommentManager()
    
    @classmethod
    async def handle_events(cls, event: dict, message_id: int, sender: str):
        if not await ReceivedEvent.exists(message_id=message_id, domain=sender):
            type = event.pop('event', None)
            await ReceivedEvent.create(message_id=message_id, domain=sender, name=type)
            
            if type == "blog_user.deleted":
                await cls._handle_blog_user_deleted(event)
            if type == "account.full_logout":
                await cls._handle_full_logout(event)
        else:
            logger.info('To zdarzenie zostało już obsłużone.')
        
    @classmethod
    async def _handle_blog_user_deleted(cls, event: dict):
        try:
            data = BlogUserDeleted(**event)
        except ValidationError as e:
            logger.error(e)
         
        await cls.post_manager.bulk_delete({'creator_id': data.id})
        await cls.comment_manager.bulk_delete({'creator_id': data.id})
        
    @classmethod
    async def _handle_full_logout(cls, event: dict):
        try:
            data = FullLogout(**event)
        except ValidationError as e:
            logger.error(e)
        await FullLogoutEvent.create(user_id=data.user_id, logout_date=data.logout_date)