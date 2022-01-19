from enum import Enum


class PostListOrdering(str, Enum):
    DATE_CREATED_DESCENDING = '-date_created'
    LIKE_COUNT_DESCENDING = '-like_count'