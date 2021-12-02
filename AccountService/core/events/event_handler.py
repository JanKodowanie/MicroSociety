from settings import logger
from pydantic import ValidationError


class EventHandler:
    
    @classmethod
    async def handle_events(cls, event: dict):
        type = event.pop('event', None)