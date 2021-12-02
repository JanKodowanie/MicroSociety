from fastapi import Request
from uuid import UUID
from .published import AccountDeleted
from common.broker.client import BrokerClient


class EventPublisher:
    
    def __init__(self, request: Request):
        self.broker: BrokerClient = request.app.broker_client
        
    async def publish_account_deleted(self, user_id: UUID):
        event = AccountDeleted(id=str(user_id))
        await self.broker.send_message(event.json(), event.event)