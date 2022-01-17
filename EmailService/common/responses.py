import pydantic


class OkResponse(pydantic.BaseModel):
    detail: str = 'Operacja powiodła się.'


class NotAuthenticatedResponse(pydantic.BaseModel):
    detail: str = 'Zaloguj się, aby wykonać tę operację.'


class ForbiddenResponse(pydantic.BaseModel):
    detail: str = 'Nie możesz wykonać tej operacji.'
    
    
class NotFoundResponse(pydantic.BaseModel):
    detail: str = 'Nie znaleziono.'
    

class FileUrlResponse(pydantic.BaseModel):
    url: str