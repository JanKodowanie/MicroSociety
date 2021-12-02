from pydantic import BaseModel
from uuid import UUID


class AccountDeleted(BaseModel):
    id: UUID