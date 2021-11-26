
class MalformedAccessToken(Exception):
    def __init__(self):
        details = 'Access token is malformed'
        super().__init__(details)
        self.details = details
    
    
class AccessTokenExpired(Exception):
    def __init__(self):
        details = 'Access token has expired'
        super().__init__('Access token has expired')
        self.details = details
        
        
class InvalidCredentials(Exception):
    def __init__(self):
        details = "Couldn't login with credentials given"
        super().__init__("Couldn't login with credentials given")
        self.details = details