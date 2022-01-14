
class CommentNotFound(Exception):
    def __init__(self):
        self.detail = 'Komentarz o podanym id nie istnieje.'
        super().__init__(self.detail)