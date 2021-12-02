from pydantic import BaseModel


class AccountDeleted(BaseModel):
    # should be uuid4
    id: str