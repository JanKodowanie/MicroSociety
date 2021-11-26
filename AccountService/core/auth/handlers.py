from fastapi import Depends, HTTPException
from datetime import datetime, timedelta
from jose import jwt
from .schemas import *
from .exceptions import *
from core.accounts.exceptions import AccountNotFound
import settings
from core.accounts.managers import AccountManager
from core.accounts.models import Account
from utils.hash import Hash
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

'''
    Dodać weryfikację tokena po expiration time i po obecności użytkownika w bazie
'''


class TokenManager:

    def create_token(self, account: Account):
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode = self._create_jwt_data(account, expire)
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    def decode_token(self, token: str) -> TokenDataSchema:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            token_data = TokenDataSchema(**payload)
        except Exception:
            raise MalformedAccessToken()
        
        return token_data
            
    def _create_jwt_data(self, account: Account, exp: datetime) -> dict:
        to_encode = {
            'sub': str(account.id),
            'username': account.username,
            'role': account.role.value,
            'status': account.status.value,
            'exp': exp
        }
        
        return to_encode
    

class AuthHandler:
    
    async def authenticate_user(self, email, password) -> TokenSchema:
        try:
            user = await AccountManager().get_account_by_email(email)
        except AccountNotFound:
            raise InvalidCredentials()
        
        if not Hash().verify(user.password, password):
            raise InvalidCredentials()
        
        access_token = TokenManager().create_token(user)
        token_type = 'bearer'
        
        return TokenSchema(access_token=access_token, token_type=token_type)
    
    @classmethod
    async def get_user_from_token(cls, token: str = Depends(oauth2_scheme)) -> Account:
        try:
            data = TokenManager().decode_token(token)
            user = await AccountManager().get_account(data.sub)
        except Exception as e:
            raise HTTPException(401, detail=e.details)
        
        return user