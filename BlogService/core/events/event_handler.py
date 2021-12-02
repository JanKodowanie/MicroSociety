from settings import logger
from .received import AccountDeleted
from pydantic import ValidationError
from core.posts.managers import BlogPostManager


class EventHandler:
    
    manager: BlogPostManager = BlogPostManager()
    
    @classmethod
    async def handle_events(cls, event: dict):
        type = event.pop('event', None)
        
        if type == 'account.deleted':
            await cls._handle_account_deleted(event)
        
        
    @classmethod
    async def _handle_account_deleted(cls, event: dict):
        try:
            data = AccountDeleted(**event)
        except ValidationError as e:
            logger.error(e)
         
        await cls.manager.delete_posts({'creator_id': data.id})