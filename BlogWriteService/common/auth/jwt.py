from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
from .schemas import UserDataSchema
import settings


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(401, detail="Could not authenticate user",
                            headers={'WWW-Authenticate': 'Bearer'})
             
            token_data = self.decode_token(credentials.credentials)
                
            if not token_data:
                raise HTTPException(401, detail="Could not authenticate user",
                            headers={'WWW-Authenticate': 'Bearer'})
            
            return token_data
        else:
            raise HTTPException(401, detail="Could not authenticate user",
                            headers={'WWW-Authenticate': 'Bearer'})

    def decode_token(self, token: str) -> UserDataSchema:
        try:
            '''important: it also checks if signature is expired'''
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            token_data = UserDataSchema(**payload)
        except Exception as e:
            token_data = None

        return token_data