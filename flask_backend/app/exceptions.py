from fastapi import HTTPException

class Conflict(HTTPException):
    """Exception raised when user provides data which creates conflict."""
    def __init__(self, message="Pateikti duomenys netinkami!", status_code=409):
        super().__init__(status_code=status_code, detail=message)

class Unauthorized(HTTPException):
    """Exception raised when user provides incorrect credentials or access/refresh tokens."""
    def __init__(self, message="Pateikti neteisingi duomenys!", status_code=401):
        super().__init__(status_code=status_code, detail=message)
