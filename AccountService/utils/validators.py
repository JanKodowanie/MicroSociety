import pydantic
import re


def check_is_alphanumeric(value: str) -> str:
    if not value.isalnum(): 
        raise ValueError('Field can contain only letters and numbers')
    return value


def check_is_alphabetic(value: str) -> str:
    if not value.isalpha():
        raise ValueError('Field can contain only letters')


def check_is_valid_phone_number(value: str) -> str:
    if not re.match('[0-9]{9}', value):
        raise ValueError('Invalid phone number')
    return value


def alphanumeric_validator(field: str) -> classmethod:
    decorator = pydantic.validator(field, allow_reuse=True)
    validator = decorator(check_is_alphanumeric)
    return validator


def alphabetic_validator(field: str) -> classmethod:
    decorator = pydantic.validator(field, allow_reuse=True)
    validator = decorator(check_is_alphabetic)
    return validator


def phone_number_validator(field: str) -> classmethod:
    decorator = pydantic.validator(field, allow_reuse=True)
    validator = decorator(check_is_valid_phone_number)
    return validator