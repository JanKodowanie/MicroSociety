import pydantic


class OkResponse(pydantic.BaseModel):
    detail: str = 'Action performed successfully'


class NotAuthenticatedResponse(pydantic.BaseModel):
    detail: str = 'Not authenticated'


class ForbiddenResponse(pydantic.BaseModel):
    detail: str = 'Not authorized'
    
    
class NotFoundResponse(pydantic.BaseModel):
    detail: str = 'Not found'
    

class FileUrlResponse(pydantic.BaseModel):
    url: str