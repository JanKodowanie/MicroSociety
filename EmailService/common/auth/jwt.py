from fastapi import HTTPException, Header
from jose import jwt
from .schemas import *
from .exceptions import *
import settings
from typing import Optional


class JWTHandler:

    @classmethod
    def authenticate_user(cls, Authorization: str = Header(None)) -> TokenDataSchema:
        try:
            token_data = Authorization.split()
            if token_data[0] != 'Bearer':
                raise HTTPException(401, detail="Could not authenticate user",
                            headers={'WWW-Authenticate': 'Bearer'})
            
            user_data = cls.decode_token(token_data[1])
        except Exception:
            raise HTTPException(401, detail="Could not authenticate user",
                            headers={'WWW-Authenticate': 'Bearer'})
        
        return user_data
        
    @classmethod    
    def decode_token(cls, token: str) -> TokenDataSchema:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            token_data = TokenDataSchema(**payload)
        except Exception as e:
            raise e
        
        return token_data