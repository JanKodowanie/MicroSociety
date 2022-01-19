
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
        
        
class LikeAlreadyCreated(Exception):
    def __init__(self):
        self.detail = 'Użytkownik polubił już ten post.'
        super().__init__(self.detail)
        
        
class LikeCreationAttemptByCreator(Exception):
    def __init__(self):
        self.detail = 'Użytkownik nie może polubić swojego posta.'
        super().__init__(self.detail)