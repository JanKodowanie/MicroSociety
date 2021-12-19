from fastapi import Request
from uuid import UUID
from .published import *
from common.broker.client import BrokerClient
from common.enums import *
from core.blog_users.models import *
from core.employees.models import *


class EventPublisher:
    
    def __init__(self, request: Request):
        self.broker: BrokerClient = request.app.broker_client
        
    async def publish_blog_user_deleted(self, id: UUID):
        event = BlogUserDeleted(id=str(id))
        await self.broker.send_message(event.json(), event.event)
        
    async def publish_blog_user_updated(self, instance: BlogUser):
        event = BlogUserUpdated(
            id = str(instance.account.id),
            username = instance.account.username,
            email = instance.account.email,
            role = instance.account.role,
            gender = instance.account.gender,
            rank = instance.rank,
            picture_url = instance.picture_url
        )
        await self.broker.send_message(event.json(), event.event)
        
    async def publish_blog_user_created(self, instance: BlogUser):
        event = BlogUserCreated(
            id = str(instance.account.id),
            username = instance.account.username,
            email = instance.account.email,
            role = instance.account.role,
            gender = instance.account.gender,
            rank = instance.rank,
            picture_url = instance.picture_url
        )
        await self.broker.send_message(event.json(), event.event)
        
    async def publish_employee_created(self, instance: Employee, password: str):
        event = EmployeeCreated(
            firstname = instance.firstname,
            lastname = instance.lastname,
            password = password,
            email = instance.account.email,
            role = instance.account.role
        )
        await self.broker.send_message(event.json(), event.event)
              
    async def publish_password_reset_code_created(self, code: UUID, username: str, 
                                      email: str):
        
        event = PasswordResetCodeCreated(code=str(code), username=username, email=email)
        await self.broker.send_message(event.json(), event.event)