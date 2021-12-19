import pydantic


class ForbiddenResponse(pydantic.BaseModel):
    detail: str = 'Not authorized'
    
    
class NotFoundResponse(pydantic.BaseModel):
    detail: str = 'Not found'
    

class FileUrlResponse(pydantic.BaseModel):
    url: str