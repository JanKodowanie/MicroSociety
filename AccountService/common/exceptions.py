
class InvalidFileExtension(Exception):
    def __init__(self, details: str):
        super().__init__(details)
        self.details = details