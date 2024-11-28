from fastapi import HTTPException

class BadRequest(HTTPException):
    """Exception raised when user submits input that contains forbidden characters."""
    def __init__(self, message="Pateiktuose duomenyse yra draudžiamų simbolių!", status_code=400):
        super().__init__(status_code=status_code, detail=message)

class Unauthorized(HTTPException):
    """Exception raised when user provides incorrect credentials or access/refresh tokens."""
    def __init__(self, message="Pateikti neteisingi duomenys!", status_code=401):
        super().__init__(status_code=status_code, detail=message)

class Forbidden(HTTPException):
    """Exception raised when user tries to access resource without without specific required role to access that resource."""
    def __init__(self, message="Nepakankamos vartotojo teisės atlikti veiksmą!", status_code=403):
        super().__init__(status_code=status_code, detail=message)

class NotFound(HTTPException):
    """Exception raised when resource is not found."""
    def __init__(self, message="Pateiktoje užklausoje nerasti duomenys!", status_code=404):
        super().__init__(status_code=status_code, detail=message)

class Conflict(HTTPException):
    """Exception raised when user provides data which creates conflict."""
    def __init__(self, message="Pateikti duomenys netinkami!", status_code=409):
        super().__init__(status_code=status_code, detail=message)

class UnprocessableEntity(HTTPException):
    """Exception raised when user provides incorrect input formats or input exceeds length restrictions."""
    def __init__(self, message="Pateikti duomenys neteisingo formato!", status_code=422):
        super().__init__(status_code=status_code, detail=message)

class InternalServerError(HTTPException):
    """Exception raised when user provides incorrect input formats or input exceeds length restrictions."""
    def __init__(self, message="Įvyko serverio klaida!", status_code=500):
        super().__init__(status_code=status_code, detail=message)