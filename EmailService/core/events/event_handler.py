from core.emails.managers import EmailManager
from pydantic import ValidationError
from .received import *
from settings import logger


class EventHandler:
    
    email_manager: EmailManager = EmailManager()
    
    @classmethod
    async def handle_events(cls, event: dict):
        type = event.pop('event', None)
        
        if type == 'account.created':
            await cls._handle_account_created(event)
            
        if type == 'account.password_reset':
            await cls._handle_password_reset(event)
        
    @classmethod
    async def _handle_account_created(cls, event: dict):
        try:
            data = AccountCreated(**event)
        except ValidationError as e:
            logger.error(e)
         
        await cls.email_manager.send_greetings_email(data.username, data.email)
        
    @classmethod
    async def _handle_password_reset(cls, event: dict):
        try:
            data = PasswordResetCodeCreated(**event)
        except ValidationError as e:
            logger.error(e)
         
        await cls.email_manager.send_password_reset_email(data.username, data.email, data.code)