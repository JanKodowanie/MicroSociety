import httpx
import settings
from fastapi import APIRouter, HTTPException, Form, Request, status, Response, Depends, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from common.responses import *
from .schemas import *
from core.blog.schemas import BlogUserGetDetailsSchema
from .auth import *


router = APIRouter(
    tags=['Accounts'],
    responses= {
        status.HTTP_401_UNAUTHORIZED: NotAuthenticatedResponse().dict(),
        status.HTTP_403_FORBIDDEN: ForbiddenResponse().dict(),
        status.HTTP_404_NOT_FOUND: NotFoundResponse().dict()
    }
)


templates = Jinja2Templates(directory="templates")


@router.get("/sign-up", response_class=HTMLResponse)
async def get_registration_page(request: Request):
    return templates.TemplateResponse("accounts/registration.html", {"request": request})


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


@router.get("/login", response_class=HTMLResponse)
async def get_login_page(request: Request):
    return templates.TemplateResponse("accounts/login.html", {"request": request})


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
    status_code=status.HTTP_307_TEMPORARY_REDIRECT)
async def logout_user():
    return await redirect_to_login()


@router.post(
    "/logout-all",
    status_code=status.HTTP_204_NO_CONTENT)
async def logout_user_on_all_devices(
    response: Response,
    user: Optional[UserSession] = Depends(get_user_session)
):
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Nie możesz wykonać tej operacji.")
    
    async with httpx.AsyncClient() as client:
        headers = {'authorization': user.access_token}
        await client.post(f'{settings.BACKEND_URL}/user-management/full-logout', headers=headers)
    
    await remove_user_data_cookies(response)
    response.status_code = status.HTTP_204_NO_CONTENT
    return response


@router.get("/password-reset-code", response_class=HTMLResponse)
async def get_password_reset_code_form(request: Request):
    return templates.TemplateResponse("accounts/pass_reset_code.html", {"request": request})


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


@router.put(
    "/account", 
    status_code=status.HTTP_200_OK, 
    response_model=OkResponse
)
async def edit_account(
    data: BlogUserEditSchema,
    response: Response,
    user: Optional[UserSession] = Depends(get_user_session)
):
    if not user or user.role == AccountRole.ADMINISTRATOR:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Nie możesz wykonać tej operacji.")
    
    async with httpx.AsyncClient() as client:
        headers = {'authorization': user.access_token}
        edit_response = await client.put(f'{settings.BACKEND_URL}/user-management/blog-user', 
                                        json=data.dict(), headers=headers)
        response_data = edit_response.json()
        if edit_response.status_code != status.HTTP_200_OK:
            if edit_response.status_code == status.HTTP_401_UNAUTHORIZED:
                return await redirect_to_login()
            raise HTTPException(response.status_code, detail=response_data['detail'])
    
    updated_data = AccountGetBasicSchema(**response_data)
    await update_user_data_in_cookies(updated_data, response)
    return OkResponse(detail="Dane użytkownika zostały zaktualizowane.")


@router.patch(
    "/account/profile-picture", 
    status_code=status.HTTP_200_OK, 
    response_model=OkResponse
)
async def add_profile_picture(
    response: Response,
    picture: UploadFile = File(None),
    user: Optional[UserSession] = Depends(get_user_session)
):
    if not user or user.role == AccountRole.ADMINISTRATOR:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Nie możesz wykonać tej operacji.")
    
    files = {
        "picture": (picture.filename, await picture.read())
    }
    
    async with httpx.AsyncClient() as client:
        headers = {'authorization': user.access_token}
        response = await client.patch(f'{settings.BACKEND_URL}/user-management/blog-user/add-picture', 
                                    files=files, headers=headers)
        response_data = response.json()
        if response.status_code != status.HTTP_201_CREATED:
            if response.status_code == status.HTTP_401_UNAUTHORIZED:
                return await redirect_to_login()
            raise HTTPException(response.status_code, detail=response_data['detail'])
    
    return OkResponse(detail="Zdjęcie profilowe zostało dodane.")


@router.delete(
    "/account/profile-picture", 
    status_code=status.HTTP_200_OK, 
    response_model=OkResponse
)
async def delete_profile_picture(
    response: Response,
    user: Optional[UserSession] = Depends(get_user_session)
):
    if not user or user.role == AccountRole.ADMINISTRATOR:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Nie możesz wykonać tej operacji.")
    
    async with httpx.AsyncClient() as client:
        headers = {'authorization': user.access_token}
        response = await client.delete(f'{settings.BACKEND_URL}/user-management/blog-user/delete-picture', 
                                    headers=headers)
        if response.status_code != status.HTTP_204_NO_CONTENT:
            if response.status_code == status.HTTP_401_UNAUTHORIZED:
                return await redirect_to_login()
            raise HTTPException(response.status_code, detail="Nie udało się usunąć zdjęcia profilowego.")
    
    return OkResponse(detail="Zdjęcie profilowe zostało usunięte.")


@router.get(
    "/account/edit-form", 
    response_model=OkResponse,
    status_code=status.HTTP_200_OK
)
async def get_account_edit_form(
    request: Request,
    response: Response,
    user: Optional[UserSession] = Depends(get_user_session)
):
    if not user or user.role == AccountRole.ADMINISTRATOR: 
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Nie możesz wykonać tej operacji.")
    
    async with httpx.AsyncClient() as client:
        headers = {'authorization': user.access_token}
        data_response = await client.get(f'{settings.BACKEND_URL}/user-management/blog-user', headers=headers)
        if data_response.status_code == status.HTTP_401_UNAUTHORIZED:
            return await redirect_to_login()
        account_data = BlogUserGetDetailsSchema(**data_response.json())
    
    return templates.TemplateResponse("accounts/blog_user_edit.html", {"request": request, 
                                            "user": user, "data": account_data.dict()})


@router.get("/account/reset-password/{code}", response_class=HTMLResponse)
async def get_password_reset_form(
    request: Request,
    code: UUID
):
    return templates.TemplateResponse("accounts/pass_reset_form.html", {"request": request})


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
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Nie możesz wykonać tej operacji.")
    
    if user.id == id:
        request_url = "/user-management/delete"
    elif user.role == AccountRole.MODERATOR:
        request_url = f"/user-management/blog-user/{id}"
    else:
        request_url = f"/user-management/employee/{id}"
    
    async with httpx.AsyncClient() as client:
        headers = {'authorization': user.access_token}
        await client.delete(f'{settings.BACKEND_URL}{request_url}', headers=headers)
    
    if user.id == id:
        await remove_user_data_cookies(response)
    return OkResponse(detail="Konto zostało usunięte.")


@router.patch(
    "/account/{id}/ban", 
    status_code=status.HTTP_204_NO_CONTENT
)
async def ban_account(
    id: UUID,
    user: Optional[UserSession] = Depends(get_user_session)
):
    if not user or not user.role == AccountRole.MODERATOR:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Nie możesz wykonać tej operacji.")
    async with httpx.AsyncClient() as client:
        headers = {'authorization': user.access_token}
        await client.patch(f'{settings.BACKEND_URL}/user-management/blog-user/{id}/ban', headers=headers)
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch(
    "/account/{id}/unban", 
    status_code=status.HTTP_204_NO_CONTENT
)
async def unban_account(
    id: UUID,
    user: Optional[UserSession] = Depends(get_user_session)
):
    if not user or not user.role == AccountRole.MODERATOR:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Nie możesz wykonać tej operacji.")
    async with httpx.AsyncClient() as client:
        headers = {'authorization': user.access_token}
        await client.patch(f'{settings.BACKEND_URL}/user-management/blog-user/{id}/unban', headers=headers)
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)