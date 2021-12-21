
class CommentNotFound(Exception):
    def __init__(self):
        details = 'Comment not found'
        super().__init__(details)
        self.details = details