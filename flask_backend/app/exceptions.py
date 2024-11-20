class AppException(Exception):
    """Base exception class for all custom exceptions."""
    def __init__(self, message: str, status_code: int = 500):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

class UserAlreadyExistsError(AppException):
    """Exception raised when a user already exists."""
    def __init__(self, message="Naudotojas jau egzistuoja!", status_code=400):
        super().__init__(message, status_code)

class IncorrectUserCredentials(AppException):
    """Exception raised when user provides incorrect credentials."""
    def __init__(self, message="Neteisingi prisijungimo duomenys!", status_code=401):
        super().__init__(message, status_code)

