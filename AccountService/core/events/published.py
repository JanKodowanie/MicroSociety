from pydantic import BaseModel
from uuid import UUID


class AccountDeleted(BaseModel):
    event: str = 'account.deleted'
    id: UUID