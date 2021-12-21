from pydantic import BaseModel
from datetime import datetime
from pydantic.types import UUID4
from common.enums import AccountStatus, AccountRole

    
class UserDataSchema(BaseModel):
    sub: UUID4
    username: str
    role: AccountRole
    status: AccountStatus
    iat: datetime
    exp: datetime