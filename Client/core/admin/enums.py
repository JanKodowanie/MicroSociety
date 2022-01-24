from enum import Enum


class EmployeeRole(str, Enum):
    MODERATOR = 'moderator'
    ADMINISTRATOR = 'administrator'