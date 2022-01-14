from fastapi import Request
from uuid import UUID
from .published import *
from common.events.models import *
from common.events.broker_client import BrokerClient
from common.enums import *
from core.blog_users.models import *
from core.employees.models import *


class EventPublisher:
    
    def __init__(self, request: Request):
        self.broker: BrokerClient = request.app.broker_client
        
    async def _publish_event(self, body: str, routing_key: str, message_id: str):
        await self.broker.send_message(body, routing_key, 'accounts', message_id)
        
    async def publish_blog_user_deleted(self, id: UUID, username: str, email: str):
        message_schema = BlogUserDeleted(id=str(id), username=username, email=email)
        body = message_schema.json()
        event = await PublishedEvent.create(name=message_schema.event, body=body)
        
        await self._publish_event(body, event.name, event.id)
        
    async def publish_blog_user_updated(self, instance: BlogUser):
        message_schema = BlogUserUpdated(
            id = str(instance.account.id),
            username = instance.account.username,
            email = instance.account.email,
            role = instance.account.role,
            gender = instance.account.gender,
            rank = instance.rank,
            picture_url = instance.picture_url
        )
        body = message_schema.json()
        event = await PublishedEvent.create(name=message_schema.event, body=body)
        
        await self._publish_event(body, event.name, event.id)
        
    async def publish_blog_user_created(self, instance: BlogUser):
        message_schema = BlogUserCreated(
            id = str(instance.account.id),
            username = instance.account.username,
            email = instance.account.email,
            role = instance.account.role,
            gender = instance.account.gender,
            rank = instance.rank,
            picture_url = instance.picture_url
        )
        body = message_schema.json()
        event = await PublishedEvent.create(name=message_schema.event, body=body)
        
        await self._publish_event(body, event.name, event.id)
        
    async def publish_employee_created(self, instance: Employee, password: str):
        message_schema = EmployeeCreated(
            firstname = instance.firstname,
            lastname = instance.lastname,
            password = password,
            email = instance.account.email,
            role = instance.account.role
        )
        body = message_schema.json()
        event = await PublishedEvent.create(name=message_schema.event, body=body)
        
        await self._publish_event(body, event.name, event.id)
              
    async def publish_password_reset_code_created(self, code: UUID, username: str, 
                                      email: str):
        
        message_schema = PasswordResetCodeCreated(code=str(code), username=username, email=email)
        body = message_schema.json()
        event = await PublishedEvent.create(name=message_schema.event, body=body)
        
        await self._publish_event(body, event.name, event.id)