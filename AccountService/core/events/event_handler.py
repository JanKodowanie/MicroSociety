from common.events.models import *
from settings import logger


class EventHandler:
    
    @classmethod
    async def handle_events(cls, event: dict, message_id: int, sender: str):
        if not await ReceivedEvent.exists(message_id=message_id, domain=sender):
            type = event.pop('event', None)
            await ReceivedEvent.create(message_id=message_id, domain=sender, name=type)    
        else:
            logger.info('To zdarzenie zostało już obsłużone.')