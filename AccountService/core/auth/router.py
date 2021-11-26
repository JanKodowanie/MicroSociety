from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from .handlers import AuthHandler
from .exceptions import InvalidCredentials
from .schemas import TokenSchema


router = APIRouter(
    prefix="/auth",
    tags=['Auth']
)

'''
    Dodać api do weryfikacji tokenu (dla bramki)
'''

@router.post(
    '/login',
    response_model=TokenSchema,
    status_code=status.HTTP_201_CREATED
)
async def login(request: OAuth2PasswordRequestForm = Depends(), auth_handler: AuthHandler = Depends()):
    try:
        token = await auth_handler.authenticate_user(email=request.username, password=request.password)
    except InvalidCredentials as e:   
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=e.details)
    return token