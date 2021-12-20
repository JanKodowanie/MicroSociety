from core.emails.managers import EmailManager
from common.enums import AccountRole
from pydantic import ValidationError
from .received import *
from settings import logger


class EventHandler:
    
    email_manager: EmailManager = EmailManager()
    
    @classmethod
    async def handle_events(cls, event: dict, message_id: int, sender: str):
        type = event.pop('event', None)
        
        if type == 'blog_user.created':
            await cls._handle_blog_user_created(event)
            
        if type == 'blog_user.deleted':
            await cls._handle_blog_user_deleted(event)
            
        if type == 'employee.created':
            await cls._handle_employee_created(event)
            
        if type == 'account.password_reset':
            await cls._handle_password_reset(event)
        
    @classmethod
    async def _handle_blog_user_created(cls, event: dict):
        try:
            data = BlogUserCreated(**event)
        except ValidationError as e:
            logger.error(e)
        
        if data.role == AccountRole.STANDARD: 
            await cls.email_manager.send_blog_user_greetings_email(data.username, data.email)
            
    @classmethod
    async def _handle_blog_user_deleted(cls, event: dict):
        try:
            data = BlogUserDeleted(**event)
        except ValidationError as e:
            logger.error(e)
        
        await cls.email_manager.send_blog_user_farewell_email(data.username, data.email)
        
    @classmethod
    async def _handle_employee_created(cls, event: dict):
        try:
            data = EmployeeCreated(**event)
        except ValidationError as e:
            logger.error(e)
        
        if data.role == AccountRole.MODERATOR: 
            await cls.email_manager.send_moderator_greetings_email(data.firstname, 
                                data.password, data.email)
        if data.role == AccountRole.ADMINISTRATOR: 
            await cls.email_manager.send_admin_greetings_email(data.firstname, 
                                data.password, data.email)
    
    @classmethod
    async def _handle_password_reset(cls, event: dict):
        try:
            data = PasswordResetCodeCreated(**event)
        except ValidationError as e:
            logger.error(e)
         
        await cls.email_manager.send_password_reset_email(data.username, data.email, data.code)