from settings import logger
from .received import AccountDeleted
from pydantic import ValidationError
from core.posts.managers import *


class EventHandler:
    
    post_manager: BlogPostManager = BlogPostManager()
    tag_manager: TagManager = TagManager()
    
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
         
        await cls.post_manager.delete_posts({'creator_id': data.id})
        await cls.tag_manager.set_creator_to_null(data.id)