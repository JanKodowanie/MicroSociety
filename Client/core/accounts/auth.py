import json
import httpx
import settings
from fastapi import Cookie, status, Response
from .schemas import UserSession, Credentials, LoginResponse
from typing import Optional
from starlette.responses import RedirectResponse


async def get_user_session(user_data: Optional[str] = Cookie(None),
                           credentials: Optional[str] = Cookie(None)) -> Optional[UserSession]:
    if not user_data or not credentials:
        return None
    user_data = json.loads(user_data)
    access_token = json.loads(credentials)['access_token']
    session = UserSession(**user_data, access_token=access_token)
    return session


async def remove_user_data_cookies(response: Response):
    response.delete_cookie('credentials')
    response.delete_cookie('user_data')


async def save_data_and_credentials_in_cookies(user_data: LoginResponse, response: Response):
    credentials = Credentials(
            access_token=f'{user_data.token_type} {user_data.access_token}',
            refresh_token=f'{user_data.token_type} {user_data.refresh_token}',
            exp=user_data.exp)
    response.set_cookie('user_data', user_data.user.json(), httponly=False)
    response.set_cookie('credentials', credentials.json(), httponly=True)
    

async def get_refreshed_credentials(credentials: Credentials):
    async with httpx.AsyncClient() as client:
        headers = {'authorization': credentials.refresh_token}
        refresh_response = await client.post(f'{settings.BACKEND_URL}/refresh-token', headers=headers)
        if refresh_response.status_code == status.HTTP_401_UNAUTHORIZED:
            response = RedirectResponse('/login')
            await remove_user_data_cookies(response)
            return response
        updated_data = LoginResponse(**refresh_response.json()) 
        
    return updated_data