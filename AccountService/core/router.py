from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from .schemas import *
from .exceptions import *
from .managers import *
from .auth import AuthHandler
from common.responses import *


router = APIRouter(
    tags=['General'],
    responses= {
        status.HTTP_401_UNAUTHORIZED: NotAuthenticatedResponse().dict(),
        status.HTTP_403_FORBIDDEN: ForbiddenResponse().dict(),
        status.HTTP_404_NOT_FOUND: NotFoundResponse().dict()
    }
)


@router.post(
    '/login',
    response_model=LoginResponse,
    status_code=status.HTTP_201_CREATED
)
async def login(
    request: OAuth2PasswordRequestForm = Depends()
):
    try:
        response = await AuthHandler.authenticate_user(email=request.username, 
                                                     password=request.password)
    except InvalidCredentials as e:   
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=e.detail)
    return response


@router.post(
    '/refresh-token',
    response_model=LoginResponse,
    status_code=status.HTTP_201_CREATED
)
async def refresh_access_token(
    response: LoginResponse = Depends(AuthHandler.refresh_access_token)
):
    return response


@router.post(
    '/full-logout',
    status_code=status.HTTP_204_NO_CONTENT
)
async def logout_on_all_devices(
    account: Account = Depends(AuthHandler.get_user_from_token),
    auth: AuthHandler = Depends()
):
    await auth.perform_full_logout(account)
    return Response(status_code=status.HTTP_204_NO_CONTENT)  


@router.delete(
    '/delete', 
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_account(
    manager: AccountManager = Depends(),
    account: Account = Depends(AuthHandler.get_user_from_token)
):
    await manager.delete_account(account)
    return Response(status_code=status.HTTP_204_NO_CONTENT)  


@router.post(
    '/password-reset-code',
    status_code=status.HTTP_204_NO_CONTENT
)
async def get_password_reset_code(
    request: PassResetCodeRequestSchema,
    reset_code_manager: PasswordResetCodeManager = Depends(),
    account_manager: AccountManager = Depends() 
):
    try:
        account = await account_manager.get_account_by_email(request.email)
        await reset_code_manager.create_password_reset_code(account)
    except AccountNotFound:
        pass
    
    return Response(status_code=status.HTTP_204_NO_CONTENT) 
    
    
@router.patch(
    '/reset-password',
    response_model=OkResponse,
    status_code=status.HTTP_200_OK
)
async def reset_password(
    request: PasswordResetSchema,
    reset_code_manager: PasswordResetCodeManager = Depends(),
    auth: AuthHandler = Depends()
):
    try:
        code = await reset_code_manager.get_password_reset_code(request.code)
    except PasswordResetCodeNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=e.detail)
    try:
        await reset_code_manager.reset_password(code, request.password)
    except PasswordResetCodeExpired as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=e.detail)
        
    await auth.perform_full_logout(code.user)
    return OkResponse(detail="Hasło zostało zresetowane.")