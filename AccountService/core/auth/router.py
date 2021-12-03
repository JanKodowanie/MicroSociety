from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from .handlers import AuthHandler
from .exceptions import *
from .schemas import *
from .managers import PasswordResetCodeManager
from core.accounts.managers import AccountManager
from core.accounts.exceptions import AccountNotFound
from core.events.event_publisher import EventPublisher
from datetime import datetime, timezone


router = APIRouter(
    prefix="/auth",
    tags=['Auth']
)


@router.post(
    '/login',
    response_model=TokenSchema,
    status_code=status.HTTP_201_CREATED
)
async def login(
    request: OAuth2PasswordRequestForm = Depends(), 
    auth_handler: AuthHandler = Depends()
):
    try:
        token = await auth_handler.authenticate_user(email=request.username, 
                                                     password=request.password)
    except InvalidCredentials as e:   
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=e.details)
    return token


@router.post(
    '/password-reset/code',
    status_code=status.HTTP_204_NO_CONTENT
)
async def get_password_reset_code(
    request: PassResetCodeRequestSchema,
    reset_code_manager: PasswordResetCodeManager = Depends(),
    account_manager: AccountManager = Depends(),
    event_publisher: EventPublisher = Depends() 
    
):
    try:
        account = await account_manager.get_account_by_email(request.email)
    except AccountNotFound:
        return
    
    code = await reset_code_manager.create_password_reset_code(account)
    await event_publisher.publish_password_reset_code_created(
                        code.code, account.username, account.email)
    
    
@router.patch(
    '/password-reset',
    status_code=status.HTTP_200_OK
)
async def reset_password(
    request: PasswordResetSchema,
    reset_code_manager: PasswordResetCodeManager = Depends(),
    account_manager: AccountManager = Depends()
):
    try:
        code = await reset_code_manager.get_password_reset_code(request.code)
    except PasswordResetCodeNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=e.details)
    
    if code.exp < datetime.now(timezone.utc):
        await code.delete()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Password reset code has expired')
        
    await account_manager.change_users_password(code.user, request.password)
    await code.delete()
    
    return({"detail": "Password reseted successfully."})