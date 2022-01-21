import httpx
import settings
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form, Request, status, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from common.responses import *
from .schemas import *
from core.accounts.schemas import UserSession
from core.accounts.auth import get_user_session
from typing import Optional


router = APIRouter(
    tags=['Blog'],
    responses= {
        status.HTTP_401_UNAUTHORIZED: NotAuthenticatedResponse().dict(),
        status.HTTP_403_FORBIDDEN: ForbiddenResponse().dict(),
        status.HTTP_404_NOT_FOUND: NotFoundResponse().dict()
    }
)


templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def get_blog_page(
    request: Request,
    user: Optional[UserSession] = Depends(get_user_session)
):
    async with httpx.AsyncClient() as client:
        response = await client.get(f'{settings.BACKEND_URL}/blog-read/posts')
        data = response.json()
        posts = PostListSchema(posts=data)
         
    return templates.TemplateResponse("blog.html", {"request": request, "user": user, "posts": posts.dict()})


@router.get("/tag/{name}", response_class=HTMLResponse)
async def get_tag_view(
    name: str,
    request: Request,
    user: Optional[UserSession] = Depends(get_user_session)
):
    async with httpx.AsyncClient() as client:
        params = {"tag": name}
        response = await client.get(f'{settings.BACKEND_URL}/blog-read/posts', params=params)
        if response.status_code == status.HTTP_200_OK:
            data = response.json()
        else:
            data = []
        posts = PostListSchema(posts=data)
         
    return templates.TemplateResponse("blog_tag.html", {"request": request, "tag": name, "user": user, "posts": posts.dict()})


@router.post(
    "/post", 
    response_model=CreatedResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_post(
    content: str = Form(...),
    picture: UploadFile = File(None),
    user: Optional[UserSession] = Depends(get_user_session)
):
    if not user: 
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Nie możesz wykonać tej operacji.")
    
    data = {
        "content": content
    }
    
    files = {
        "picture": (picture.filename, await picture.read())
    }
    
    async with httpx.AsyncClient() as client:
        headers = {'authorization': user.access_token}
        response = await client.post(f'{settings.BACKEND_URL}/blog-write/post', 
                                     data=data, files=files, headers=headers)
        response_data = response.json()
        if response.status_code != status.HTTP_201_CREATED:
            raise HTTPException(response.status_code, detail="Nie udało się utworzyć posta.")
        
    return CreatedResponse(id=response_data.get('id'))


@router.get("/post/{id}", response_class=HTMLResponse)
async def get_post_discussion(
    id: int,
    request: Request,
    user: Optional[UserSession] = Depends(get_user_session)
):
    async with httpx.AsyncClient() as client:
        response = await client.get(f'{settings.BACKEND_URL}/blog-read/post/{id}')
        if response.status_code == status.HTTP_404_NOT_FOUND:
            raise HTTPException(response.status_code, detail="Nie istnieje post o podanym id.")
        data = response.json()
        post = PostGetDetailsSchema(**data)
         
    return templates.TemplateResponse("post_discussion.html", {"request": request, "user": user, "post": post.dict()})


@router.delete(
    "/post/{id}", 
    response_model=OkResponse,
    status_code=status.HTTP_200_OK
)
async def delete_post(
    id: int,
    user: Optional[UserSession] = Depends(get_user_session)
):
    if not user: 
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Nie możesz wykonać tej operacji.")
    
    async with httpx.AsyncClient() as client:
        headers = {'authorization': user.access_token}
        response = await client.delete(f'{settings.BACKEND_URL}/blog-write/post/{id}', headers=headers)
        if response.status_code != status.HTTP_204_NO_CONTENT:
            raise HTTPException(response.status_code, detail="Nie możesz skasować tego posta.")
    
    return OkResponse(detail="Post został usunięty.")


@router.post(
    "/post/{id}/like", 
    status_code=status.HTTP_204_NO_CONTENT
)
async def create_post_like(
    id: int,
    user: Optional[UserSession] = Depends(get_user_session)
):
    if not user: 
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Nie możesz wykonać tej operacji.")
    
    async with httpx.AsyncClient() as client:
        headers = {'authorization': user.access_token}
        response = await client.post(f'{settings.BACKEND_URL}/blog-write/post/{id}/like', headers=headers)
        if response.status_code != status.HTTP_204_NO_CONTENT:
            response_data = response.json()
            raise HTTPException(response.status_code, detail=response_data['detail'])
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete(
    "/post/{id}/like", 
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_post_like(
    id: int,
    user: Optional[UserSession] = Depends(get_user_session)
):
    if not user: 
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Nie możesz wykonać tej operacji.")
    
    async with httpx.AsyncClient() as client:
        headers = {'authorization': user.access_token}
        response = await client.delete(f'{settings.BACKEND_URL}/blog-write/post/{id}/like', headers=headers)
        if response.status_code != status.HTTP_204_NO_CONTENT:
            response_data = response.json()
            raise HTTPException(response.status_code, detail=response_data['detail'])
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    "/post/{id}/comment", 
    response_model=CreatedResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_post_comment(
    id: int,
    content: str = Form(...),
    user: Optional[UserSession] = Depends(get_user_session)
):
    if not user: 
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Nie możesz wykonać tej operacji.")
    data = {
        "content": content
    }   
    async with httpx.AsyncClient() as client:
        headers = {'authorization': user.access_token}
        response = await client.post(f'{settings.BACKEND_URL}/blog-write/post/{id}/comment', 
                                            json=data, headers=headers)
        response_data = response.json()
        if response.status_code != status.HTTP_201_CREATED:
            raise HTTPException(response.status_code, detail="Nie udało się utworzyć komentarza.")
        
    return CreatedResponse(id=response_data.get('id'))


@router.delete(
    "/comment/{id}", 
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_post_comment(
    id: int,
    user: Optional[UserSession] = Depends(get_user_session)
):
    if not user: 
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Nie możesz wykonać tej operacji.")

    async with httpx.AsyncClient() as client:
        headers = {'authorization': user.access_token}
        response = await client.delete(f'{settings.BACKEND_URL}/blog-write/comment/{id}', headers=headers)
        if response.status_code != status.HTTP_204_NO_CONTENT:
            raise HTTPException(response.status_code, detail="Nie możesz skasować tego komentarza.")
        
    return Response(status_code=status.HTTP_204_NO_CONTENT)