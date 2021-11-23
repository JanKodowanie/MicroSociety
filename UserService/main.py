import uvicorn
from fastapi import FastAPI
from tortoise.models import Model
from tortoise.contrib.fastapi import register_tortoise
from tortoise import fields
from pydantic import BaseModel
from uuid import UUID


app = FastAPI()


class Account(Model):
    id = fields.UUIDField(pk=True)
    username = fields.CharField(max_length=30, unique=True)
    email = fields.CharField(max_length=30, unique=True)
    password = fields.CharField(max_length=60)


class AccountSchemaIn(BaseModel):
    username: str
    email: str
    password: str
    
    
class AccountSchemaOut(BaseModel):
    id: UUID
    username: str
    email: str
    
    class Config:
        orm_mode = True
    
    
register_tortoise(
    app,
    db_url='postgres://msociety:msociety@db:5432/user_db',
    modules={'models': ['main']},
    generate_schemas=True,
    add_exception_handlers=True
)


@app.post(
    '/register', 
    response_model=AccountSchemaOut,
    tags=['accounts']
)
async def register_user(request: AccountSchemaIn):
    new_account = await Account.create(**request.dict())
    return new_account


if __name__ == "__main__":
    uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)