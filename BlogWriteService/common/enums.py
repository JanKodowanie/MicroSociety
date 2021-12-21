from enum import Enum


class AccountStatus(str, Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    BANNED = 'banned'
    
    
class AccountRank(str,Enum):
    RANK_1 = 'rank_1'
    RANK_2 = 'rank_2'
    RANK_3 = 'rank_3'
    
    
class AccountRole(str,Enum):
    STANDARD = 'standard'
    MODERATOR = 'moderator'
    ADMINISTRATOR = 'administrator'
    
    
class AccountGender(str,Enum):
    MALE = 'male'
    FEMALE = 'female'