
class PostNotFound(Exception):
    def __init__(self):
        self.detail = "Nie istnieje post o podanym id."
        super().__init__(self.detail)
        
        
class TagNotFound(Exception):
    def __init__(self):
        self.detail = "Nie istnieje tag o podanej nazwie."
        super().__init__(self.detail)
        
          
class InvalidBlogPostData(Exception):
    
    def __init__(self, message: str, detail=dict):
        self.detail = detail
        super().__init__(message)