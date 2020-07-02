class PrekiException(Exception):

    def __init__(self, message, error_code=None, status_code=status.HTTP_400_BAD_REQUEST):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
