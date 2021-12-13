from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from .schemas import *
from .exceptions import *
from .managers import *
from .middleware import AuthHandler
from core.events.event_publisher import EventPublisher


router = APIRouter(
    prefix="/account",
    tags=['Accounts']
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


@router.delete(
    '/delete', 
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_account(
    manager: AccountManager = Depends(),
    account: Account = Depends(AuthHandler.get_user_from_token),
    broker: EventPublisher = Depends()
):
    user_id = account.id
    await manager.delete_account(account)
    # await broker.publish_account_deleted(user_id)
    return 


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
    # await event_publisher.publish_password_reset_code_created(
    #                     code.code, account.username, account.email)
    
    
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
    
    return({"detail": "Password reset successfully."})