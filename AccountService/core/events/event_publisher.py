from fastapi import Request
from uuid import UUID
from .published import *
from common.broker.client import BrokerClient
from common.enums import AccountRole


class EventPublisher:
    
    def __init__(self, request: Request):
        self.broker: BrokerClient = request.app.broker_client
        
    async def publish_account_deleted(self, user_id: UUID):
        event = AccountDeleted(id=str(user_id))
        await self.broker.send_message(event.json(), event.event)
        
    async def publish_account_created(self, user_id: UUID, username: str, 
                                      email: str, role: AccountRole):
        
        event = AccountCreated(id=str(user_id), username=username, email=email, role=role)
        await self.broker.send_message(event.json(), event.event)
        
    async def publish_password_reset_code_created(self, code: UUID, username: str, 
                                      email: str):
        
        event = PasswordResetCodeCreated(code=str(code), username=username, email=email)
        await self.broker.send_message(event.json(), event.event)