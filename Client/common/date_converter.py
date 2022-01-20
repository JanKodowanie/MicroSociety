from dateutil import parser, tz
from datetime import datetime


class DateConverter:
    
    @classmethod
    def convert_str_to_datetime(cls, date_str: str) -> datetime:
        to_zone = tz.gettz('Europe/Warsaw')
        date = parser.parse(date_str)
        date_localized = date.astimezone(to_zone)
        return date_localized