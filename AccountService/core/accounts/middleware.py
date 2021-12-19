import settings
from fastapi import Depends, HTTPException
from datetime import datetime, timedelta, timezone
from jose import jwt
from .schemas import *
from .exceptions import *
from .managers import AccountManager
from .models import Account
from common.auth.schemas import *
from utils.hash import Hash
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/account/login")


class TokenManager:

    def create_token(self, account: Account):
        to_encode = self._create_jwt_data(account)
        data = UserDataSchema(**to_encode)
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt, data

    def decode_token(self, token: str) -> UserDataSchema:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            token_data = UserDataSchema(**payload)
        except Exception:
            raise MalformedAccessToken()
        
        if token_data.exp < datetime.now(timezone.utc):
            raise AccessTokenExpired()
        
        return token_data
            
    def _create_jwt_data(self, account: Account) -> dict:
        iat = datetime.now(timezone.utc)
        exp = iat + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode = {
            'sub': str(account.id),
            'username': account.username,
            'role': account.role.value,
            'status': account.status.value,
            'iat': iat,
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
        
        access_token, data = TokenManager().create_token(user)
        token_type = 'bearer'
        
        return TokenSchema(access_token=access_token, token_type=token_type, data=data)
    
    @classmethod
    async def get_user_from_token(cls, token: str = Depends(oauth2_scheme)) -> Account:
        try:
            data = TokenManager().decode_token(token)
            user = await AccountManager().get_account(data.sub)
        except Exception as e:
            raise HTTPException(401, detail=e.details)
        
        return user