import pydantic
from typing import Optional
from common.enums import *
from core.accounts.schemas import *


class BlogUserCreateSchema(AccountCreateSchema):
    pass


class BlogUserEditSchema(AccountEditSchema):
    bio: Optional[pydantic.constr(strip_whitespace=True, min_length=1, max_length=300)]
    
    
class BlogUserGetDetailsSchema(AccountGetDetailsSchema):
    bio: Optional[str]
    points: int
    rank: AccountRank
    
    
class BlogUserGetListSchema(AccountGetListSchema):
    rank: AccountRank
    
    
class BlogUserGetProfileSchema(AccountGetProfileSchema):
    bio: Optional[str]
    points: int
    rank: AccountRank