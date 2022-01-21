import httpx
import settings
from fastapi import APIRouter, HTTPException, Form, Request, status, Response, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from common.responses import *
from .schemas import *
from .auth import *
from core.blog.schemas import PostListSchema


router = APIRouter(
    tags=['Accounts'],
    responses= {
        status.HTTP_401_UNAUTHORIZED: NotAuthenticatedResponse().dict(),
        status.HTTP_403_FORBIDDEN: ForbiddenResponse().dict(),
        status.HTTP_404_NOT_FOUND: NotFoundResponse().dict()
    }
)


templates = Jinja2Templates(directory="templates")


@router.get("/login", response_class=HTMLResponse)
async def get_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post(
    "/login", 
    response_model=OkResponse,
    status_code=status.HTTP_201_CREATED
)
async def login_user(
    response: Response,
    email: str = Form(...),
    password: str = Form(...),
):
    login_data = LoginRequest(username=email, password=password)
    async with httpx.AsyncClient() as client:
        backend_response = await client.post(f'{settings.BACKEND_URL}/user-management/login', data=login_data.dict())
        response_data = backend_response.json()
        if backend_response.status_code == status.HTTP_401_UNAUTHORIZED:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail=response_data['detail'])
    
    response_data = LoginResponse(**response_data)
    await save_data_and_credentials_in_cookies(response_data, response)
    return OkResponse(detail="Logowanie powiodło się.")


@router.get(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT)
async def logout_user(response: Response):
    await remove_user_data_cookies(response)
    response.status_code = status.HTTP_204_NO_CONTENT
    return response


@router.get(
    "/logout-all",
    status_code=status.HTTP_204_NO_CONTENT)
async def logout_user_on_all_devices(
    response: Response,
    user: Optional[UserSession] = Depends(get_user_session)
):
    await remove_user_data_cookies(response)
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Nie możesz wykonać tej operacji.")
    
    async with httpx.AsyncClient() as client:
        headers = {'authorization': user.access_token}
        logout_response = await client.post(f'{settings.BACKEND_URL}/user-management/full-logout', headers=headers)
        if logout_response.status_code == status.HTTP_204_NO_CONTENT:
            raise HTTPException(logout_response.status_code, detail=logout_response.json())
        
    response.status_code = status.HTTP_204_NO_CONTENT
    return response


@router.get("/sign-up", response_class=HTMLResponse)
async def get_registration_page(request: Request):
    return templates.TemplateResponse("registration.html", {"request": request})


@router.post(
    "/sign-up", 
    response_model=OkResponse,
    status_code=status.HTTP_201_CREATED
)
async def register_user(
    username: str = Form(...),
    password: str = Form(...),
    email: str = Form(...),
    gender: str = Form(...)
):
    data = BlogUserCreateSchema(username=username, email=email, password=password, gender=gender)
    async with httpx.AsyncClient() as client:
        response = await client.post(f'{settings.BACKEND_URL}/user-management/blog-user', json=data.dict())
        response_data = response.json()
        if response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail=response_data['detail'])
        
    return OkResponse(detail="Konto zostało utworzone.")


@router.get("/password-reset-code", response_class=HTMLResponse)
async def get_password_reset_code_form(request: Request):
    return templates.TemplateResponse("pass_reset_code.html", {"request": request})


@router.post(
    "/password-reset-code", 
    response_model=OkResponse,
    status_code=status.HTTP_201_CREATED
)
async def get_password_reset_code(
    email: str = Form(...)
):
    msg = "Email z linkiem do resetu hasła został wysłany."
    try:
        data = PassResetCodeRequestSchema(email=email)
    except Exception:
        return OkResponse(detail=msg)
        
    async with httpx.AsyncClient() as client:
        await client.post(f'{settings.BACKEND_URL}/user-management/password-reset-code', json=data.dict())
        
    return OkResponse(detail=msg)


@router.get("/account/reset-password/{code}", response_class=HTMLResponse)
async def get_password_reset_form(
    request: Request,
    code: UUID
):
    return templates.TemplateResponse("pass_reset_form.html", {"request": request})


@router.patch(
    "/account/reset-password/{code}", 
    response_model=OkResponse,
    status_code=status.HTTP_200_OK
)
async def reset_password(
    code: UUID,
    new_pass1: str = Form(...)
):
    data = PasswordResetSchema(code=code, password=new_pass1)
        
    async with httpx.AsyncClient() as client:
        response = await client.patch(f'{settings.BACKEND_URL}/user-management/reset-password', json=data.dict())
        response_data = response.json()
        if response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail=response_data['detail'])
    
    return OkResponse(detail=response_data['detail'])


@router.delete(
    "/account/{id}", 
    response_model=OkResponse,
    status_code=status.HTTP_200_OK
)
async def delete_account(
    id: UUID,
    response: Response,
    user: Optional[UserSession] = Depends(get_user_session)
):
    if user and user.id == id:
        request_url = "/user-management/delete"
    elif user and user.role == AccountRole.MODERATOR:
        request_url = f"/user-management/blog-user/{id}"
    else:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Nie możesz wykonać tej operacji.")
    
    async with httpx.AsyncClient() as client:
        headers = {'authorization': user.access_token}
        await client.delete(f'{settings.BACKEND_URL}{request_url}', headers=headers)
    
    remove_user_data_cookies(response)
    return OkResponse(detail="Konto zostało usunięte.")


@router.get("/profile/{id}", response_class=HTMLResponse)
async def get_user_profile(
    id: UUID,
    request: Request,
    user: Optional[UserSession] = Depends(get_user_session)
):
    async with httpx.AsyncClient() as client:
        profile_response = await client.get(f'{settings.BACKEND_URL}/user-management/blog-user/{id}')
        profile = profile_response.json()
        if profile_response.status_code == status.HTTP_404_NOT_FOUND:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail=profile['detail'])

        profile = BlogUserGetProfileSchema(**profile)
        params = {"creator_id": id}
        response = await client.get(f'{settings.BACKEND_URL}/blog-read/posts', params=params)
        posts = response.json()
        posts = PostListSchema(posts=posts)
         
    return templates.TemplateResponse("user_profile.html", {"request": request, "user": user, "posts": posts.dict(), "profile": profile})