
class AccountNotFound(Exception):
    def __init__(self):
        self.details = 'Account not found'
        super().__init__('Account not found')


class CredentialsAlreadyTaken(Exception):
    
    def __init__(self, message: str, details=dict):
        self.details = details
        super().__init__(message)
        
        
class MalformedAccessToken(Exception):
    def __init__(self):
        details = 'Access token is malformed'
        super().__init__(details)
        self.details = details
    
    
class AccessTokenExpired(Exception):
    def __init__(self):
        details = 'Access token has expired'
        super().__init__(details)
        self.details = details
        
        
class InvalidCredentials(Exception):
    def __init__(self):
        details = "Couldn't login with credentials given"
        super().__init__(details)
        self.details = details
        
        
class PasswordResetCodeExpired(Exception):
    def __init__(self):
        details = 'Password reset code has expired'
        super().__init__(details)
        self.details = details
        
        
class PasswordResetCodeNotFound(Exception):
    def __init__(self):
        details = 'Password reset code not found'
        super().__init__(details)
        self.details = details