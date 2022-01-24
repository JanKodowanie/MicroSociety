from enum import Enum


class PostOrdering(str, Enum):
    NEWEST = '-date_created'
    MOST_POPULAR = '-like_count'
    
    
class ProfileStatus(str, Enum):
    ACTIVE = 'active'
    BANNED = 'banned'