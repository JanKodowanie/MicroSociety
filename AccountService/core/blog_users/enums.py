from enum import Enum


class ProfileListOrdering(str, Enum):
    DATE_JOINED_DESCENDING = '-date_joined'
    DATE_JOINED_ASCENDING = 'date_joined'
    POINTS_DESCENDING = '-points'
    POINTS_ASCENDING = 'points'