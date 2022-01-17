from pydantic import BaseModel
from datetime import datetime
from pydantic.types import UUID4
from common.enums import AccountStatus, AccountRole

    
class AccessTokenSchema(BaseModel):
    sub: UUID4
    role: AccountRole
    status: AccountStatus
    iat: datetime
    exp: datetime
    
    
class RefreshTokenSchema(BaseModel):
    sub: UUID4
    jti: UUID4
    iat: datetime