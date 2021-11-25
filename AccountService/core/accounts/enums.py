from enum import IntEnum


class AccountStatus(IntEnum):
    ACTIVE = 1
    INACTIVE = 2
    BANNED = 3
    
    
class AccountRank(IntEnum):
    RANK_1 = 1
    RANK_2 = 2
    RANK_3 = 3
    
    
class AccountType(IntEnum):
    STANDARD = 1
    MODERATOR = 2
    ADMINISTRATOR = 3
    
    
class AccountGender(IntEnum):
    MALE = 1
    FEMALE = 2