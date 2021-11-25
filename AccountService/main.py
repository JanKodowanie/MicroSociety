from pydantic.types import UUID4
import uvicorn
from fastapi import FastAPI, HTTPException, Depends
import settings
from core.accounts.schemas import *
from core.accounts.exceptions import *
from core.accounts.managers import AccountManager
from typing import List


app = FastAPI()

try:
    settings.create_db_connection(app)
except Exception:
    print("Failed to create database connection")


@app.post('/', response_model=AccountOutSchema)
async def register_account(request: AccountCreateSchema, manager: AccountManager = Depends()):
    print(request)
    try:
        account = await manager.register_account(request)
    except CredentialsAlreadyTaken as e:
        raise HTTPException(422, detail=e.details) 
    return account


@app.get(
    '/list', 
    response_model=List[AccountListSchema]
)
async def get_users(manager: AccountManager = Depends()):
    users = await manager.get_user_list()
    return users


@app.put(
    '/edit/{id}', 
    response_model=AccountOutSchema
)
async def edit_account_data(id: UUID4, request: AccountEditSchema, manager: AccountManager = Depends()):
    try:
        account = await manager.get_account(id)
    except AccountNotFound as e:
        raise HTTPException(404, detail=e.details)
    # some permission checks
    try:
        account = await manager.edit_account(account, request)
    except CredentialsAlreadyTaken as e:
        raise HTTPException(422, detail=e.details) 
    
    return account
    

if __name__ == "__main__":
    uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)