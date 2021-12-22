from pydantic import ValidationError
from settings import logger
from core.users.schemas import *
# from core.users.managers import *


class EventHandler:
    
    
    @classmethod
    async def handle_events(cls, event: dict, message_id: int, sender: str):
        type = event.pop('event', None)
        
        if type == "blog_user.created":
            await cls._handle_blog_user_created(event)
        
    @classmethod
    async def _handle_blog_user_created(cls, event: dict):
        print("HELLO")
        # try:
        #     event = BlogUserCreatedEvent(**event)
        # except ValidationError as e:
        #     logger.error(e)
            
        # await BlogUserCollectionManager().create(event)