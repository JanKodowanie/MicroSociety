
class AccountNotFound(Exception):
    def __init__(self):
        self.detail = 'Konto nie istnieje.'
        super().__init__(self.detail)


class CredentialsAlreadyTaken(Exception):
    
    def __init__(self, detail=dict):
        self.detail = detail
        super().__init__('Istnieje już konto z podanym emailem/nazwą użytkownika.')
        
        
class MalformedAccessToken(Exception):
    def __init__(self):
        self.detail = 'Podano nieprawidłowy token.'
        super().__init__(self.detail)
    
    
class AccessTokenExpired(Exception):
    def __init__(self):
        self.detail = 'Token utracił ważność.'
        super().__init__(self.detail)
        
        
class InvalidCredentials(Exception):
    def __init__(self):
        self.detail = "Niepoprawne dane logowania."
        super().__init__(self.detail)
        
        
class PasswordResetCodeExpired(Exception):
    def __init__(self):
        self.detail = 'Link do resetu hasła utracił ważność.'
        super().__init__(self.detail)
        
        
class PasswordResetCodeNotFound(Exception):
    def __init__(self):
        self.detail = 'Link do resetu hasła utracił ważność.'
        super().__init__(self.detail)