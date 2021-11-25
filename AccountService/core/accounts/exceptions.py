
class AccountNotFound(Exception):
    def __init__(self):
        self.details = {'error': 'Account not found'}
        super().__init__('Account not found')


class CredentialsAlreadyTaken(Exception):
    
    def __init__(self, message: str, details=dict):
        self.details = details
        super().__init__(message)
        