import settings
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
from .schemas import AccessTokenSchema
from common.auth.models import FullLogoutEvent


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        
        if credentials:
            if credentials.scheme != "Bearer":
                raise HTTPException(401, detail="Niepoprawne dane uwierzytelniające.",
                            headers={'WWW-Authenticate': 'Bearer'})
             
            token_data = await self.decode_token(credentials.credentials)
                
            if not token_data:
                raise HTTPException(401, detail="Niepoprawne dane uwierzytelniające.",
                            headers={'WWW-Authenticate': 'Bearer'})
                
            if await FullLogoutEvent.exists(user_id=token_data.sub, logout_date__gte=token_data.iat):
                raise HTTPException(401, detail="Aby skorzystać z serwisu, zaloguj się ponownie.",
                            headers={'WWW-Authenticate': 'Bearer'})
                
            return token_data
        else:
            raise HTTPException(401, detail="Niepodano danych uwierzytelniających.",
                            headers={'WWW-Authenticate': 'Bearer'})

    async def decode_token(self, token: str) -> AccessTokenSchema:
        try:
            '''important: it also checks if signature is expired'''
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            token_data = AccessTokenSchema(**payload)
        except Exception:
            token_data = None

        return token_data