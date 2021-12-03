from pydantic import BaseModel
from uuid import UUID
from common.enums import AccountRole


class PasswordResetCodeCreated(BaseModel):
    event: str = 'account.password_reset'
    username: str
    email: str
    code: UUID
    
    
class AccountCreated(BaseModel):
    event: str = 'account.created'
    id: UUID
    username: str
    email: str
    role: AccountRole