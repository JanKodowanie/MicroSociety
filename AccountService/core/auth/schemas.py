from pydantic import BaseModel
from datetime import datetime
from pydantic.types import UUID4
from core.accounts.enums import AccountStatus, AccountRole


class TokenSchema(BaseModel):
    access_token: str
    token_type: str
    
    
class TokenDataSchema(BaseModel):
    sub: UUID4
    username: str
    role: AccountRole
    status: AccountStatus
    exp: datetime