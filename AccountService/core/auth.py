import settings
from fastapi import Depends, HTTPException
from datetime import datetime, timedelta, timezone
from jose import jwt
from .schemas import *
from .exceptions import *
from .managers import AccountManager
from .models import Account, RefreshToken
from core.events.event_publisher import EventPublisher
from common.auth.schemas import *
from common.auth.models import FullLogoutEvent
from utils.hash import Hash
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user-management/login")

class TokenManager:

    async def generate_auth_tokens(self, account: Account) -> LoginResponse:
        refresh_token = await self._create_refresh_token(account)
        
        iat = datetime.now(timezone.utc)
        exp = iat + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = await self._create_access_token(account, iat, exp)
        
        user_data = AccountGetListSchema.from_orm(account)
        login_response = LoginResponse(access_token=access_token, 
                        refresh_token=refresh_token, token_type='Bearer', exp=exp, user=user_data)
        return login_response

    async def decode_access_token(self, token: str) -> AccessTokenSchema:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            token_data = AccessTokenSchema(**payload)
        except Exception:
            raise MalformedToken()
        
        if await FullLogoutEvent.exists(user_id=token_data.sub, logout_date__gte=token_data.iat):
            raise TokenRevoked()
        
        return token_data
    
    async def decode_refresh_token(self, token: str) -> RefreshTokenSchema:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM], 
                                    options={"verify_exp": False})
            token_data = RefreshTokenSchema(**payload)
        except Exception:
            raise MalformedToken()
        
        if not await RefreshToken.exists(id=token_data.jti, user_id=token_data.sub):
            raise TokenRevoked()
        
        return token_data
    
    async def revoke_refresh_token(self, token_id: UUID):
        await RefreshToken.filter(id=token_id).delete()
    
    async def revoke_users_refresh_tokens(self, user_id: UUID):
        await RefreshToken.filter(user_id=user_id).delete()
    
    async def _create_refresh_token(self, account: Account) -> str:
        instance = await RefreshToken.create(user=account)
        to_encode = {
            'sub': str(account.id),
            'jti': str(instance.id),
            'iat': datetime.now(timezone.utc)
        }
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
           
    async def _create_access_token(self, account: Account, iat: datetime, exp: datetime) -> str:
        to_encode = {
            'sub': str(account.id),
            'role': account.role.value,
            'status': account.status.value,
            'exp': exp,
            'iat': iat
        }
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    

class AuthHandler:
    
    def __init__(self, broker: EventPublisher = Depends()):
        self.broker = broker
        
    async def perform_full_logout(self, account: Account):
        await TokenManager().revoke_users_refresh_tokens(account.id)
        logout_date = datetime.now(timezone.utc)
        await FullLogoutEvent.create(user_id=account.id, logout_date=logout_date)
        await self.broker.publish_full_logout(user_id=account.id, logout_date=logout_date)
    
    @classmethod
    async def authenticate_user(cls, email: str, password: str) -> LoginResponse:
        try:
            user = await AccountManager().get_account_by_email(email)
        except AccountNotFound:
            raise InvalidCredentials()
        
        if not Hash().verify(user.password, password):
            raise InvalidCredentials()
        
        return await TokenManager().generate_auth_tokens(user)
    
    @classmethod
    async def refresh_access_token(cls, refresh_token: str = Depends(oauth2_scheme)) -> LoginResponse:
        token_manager = TokenManager()
        try:
            data = await token_manager.decode_refresh_token(refresh_token)
            account = await  AccountManager().get_account(data.sub)
        except Exception as e:
            raise HTTPException(401, detail=e.detail)
        
        await token_manager.revoke_refresh_token(data.jti)
        return await token_manager.generate_auth_tokens(account)
        
    @classmethod
    async def get_user_from_token(cls, token: str = Depends(oauth2_scheme)) -> Account:
        try:
            data = await TokenManager().decode_access_token(token)
            user = await AccountManager().get_account(data.sub)
        except Exception as e:
            raise HTTPException(401, detail=e.detail)
        
        return user