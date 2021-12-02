from pydantic import BaseModel
from datetime import datetime
from pydantic.types import UUID4
from common.enums import AccountStatus, AccountRole


class TokenSchema(BaseModel):
    access_token: str
    token_type: str