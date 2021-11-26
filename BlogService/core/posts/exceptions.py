
class BlogNotFound(Exception):
    def __init__(self):
        details = 'Blog not found'
        super().__init__(details)
        self.details = details
        
        
class TagNotFound(Exception):
    def __init__(self):
        details = 'Tag not found'
        super().__init__(details)
        self.details = details