import uvicorn
from fastapi import FastAPI
from tortoise.models import Model
from tortoise.contrib.fastapi import register_tortoise
from tortoise import fields
from pydantic import BaseModel
from uuid import UUID


app = FastAPI()


class Group(Model):
    id = fields.IntField(pk=True)
    owner_id = fields.UUIDField()
    name = fields.CharField(max_length=30, unique=True)
    description = fields.TextField(max_length=200)


class GroupSchemaIn(BaseModel):
    owner_id: UUID
    name: str
    description: str
    
    
class GroupSchemaOut(GroupSchemaIn):
    group_id: int
    
    class Config:
        orm_mode = True
    
    
register_tortoise(
    app,
    db_url='postgres://msociety:msociety@db:5432/group_db',
    modules={'models': ['main']},
    generate_schemas=True,
    add_exception_handlers=True
)


@app.post(
    '/create', 
    response_model=GroupSchemaOut,
    tags=['groups']
)
async def create_group(request: GroupSchemaIn):
    new_group = await Group.create(**request.dict())
    return new_group


if __name__ == "__main__":
    uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)