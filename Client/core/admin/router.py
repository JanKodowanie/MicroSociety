import httpx
import settings
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from common.responses import *
from .schemas import *
from .enums import *
from core.accounts.schemas import UserSession
from core.accounts.auth import get_user_session, redirect_to_login
from typing import Optional


router = APIRouter(
    tags=['Admin'],
    prefix='/admin',
    responses= {
        status.HTTP_401_UNAUTHORIZED: NotAuthenticatedResponse().dict(),
        status.HTTP_403_FORBIDDEN: ForbiddenResponse().dict(),
        status.HTTP_404_NOT_FOUND: NotFoundResponse().dict()
    }
)


templates = Jinja2Templates(directory="templates")


@router.get("/register-employee", response_class=HTMLResponse)
async def get_employee_registration_form(
    request: Request,
    user: Optional[UserSession] = Depends(get_user_session)
):
    if not user or user.role != AccountRole.ADMINISTRATOR: 
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Nie możesz wykonać tej operacji.")
     
    return templates.TemplateResponse("admin/employee_registration.html", {"request": request, "user": user})


@router.post("/register-employee", 
    response_model=OkResponse,
    status_code=status.HTTP_201_CREATED
)
async def register_employee(
    data: EmployeeCreateSchema,
    user: Optional[UserSession] = Depends(get_user_session)
):
    if not user or user.role != AccountRole.ADMINISTRATOR: 
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Nie możesz wykonać tej operacji.")
    
    async with httpx.AsyncClient() as client:
        headers = {'authorization': user.access_token}
        response = await client.post(f'{settings.BACKEND_URL}/user-management/employee', 
                                     json=data.dict(), headers=headers)
        response_data = response.json()
        if response.status_code != status.HTTP_201_CREATED:
            if response.status_code == status.HTTP_401_UNAUTHORIZED:
                    return await redirect_to_login()
            raise HTTPException(response.status_code, detail=response_data['detail'])
        
    return OkResponse(detail="Konto pracownicze zostało utworzone.")


@router.get("/employee/{id}", response_class=HTMLResponse)
async def get_employee_details(
    id: UUID,
    request: Request,
    user: Optional[UserSession] = Depends(get_user_session)
):
    if not user or user.role != AccountRole.ADMINISTRATOR: 
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Nie możesz wykonać tej operacji.")
      
    async with httpx.AsyncClient() as client:
        headers = {'authorization': user.access_token}
        employee_response = await client.get(f'{settings.BACKEND_URL}/user-management/employee/{id}', 
                                              headers=headers)
        response_data = employee_response.json()
        
        if employee_response.status_code != status.HTTP_200_OK:
            if employee_response.status_code == status.HTTP_401_UNAUTHORIZED:
                return await redirect_to_login()
            raise HTTPException(employee_response.status_code, detail=response_data['detail'])

    employee = EmployeeGetDetailsSchema(**response_data)
    return templates.TemplateResponse("admin/employee_details.html", {"request": request, "user": user, 
                                            "employee": employee.dict()})


@router.get("/employees", response_class=HTMLResponse)
async def get_employee_list(
    request: Request,
    fullname: Optional[str] = None,
    role: Optional[EmployeeRole] = None,
    user: Optional[UserSession] = Depends(get_user_session)
):
    if not user or user.role != AccountRole.ADMINISTRATOR: 
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Nie możesz wykonać tej operacji.")
    
    params = {}
    
    if fullname: 
        params["fullname"] = fullname
    if role:
        params["role"] = role.value
        
    async with httpx.AsyncClient() as client:
        headers = {'authorization': user.access_token}
        employees_response = await client.get(f'{settings.BACKEND_URL}/user-management/employees', 
                                              params=params, headers=headers)
        if employees_response.status_code == status.HTTP_401_UNAUTHORIZED:
            return await redirect_to_login()
        
        employees = employees_response.json()

    employees = EmployeeListSchema(employees=employees)
         
    return templates.TemplateResponse("admin/employees.html", {"request": request, "user": user, 
                                            "employees": employees.dict(), "params": params})