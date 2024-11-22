from pydantic import BaseModel
from datetime import datetime

class TestList(BaseModel):
    title: str
    description: str
    question_count: int
    created_at: datetime

    class Config:
        orm_mode = True
        extra = 'forbid'

class AuthResponse(BaseModel):
    message: str
    access_token: str
    token_type: str = "bearer"
    role: str

    class Config:
        orm_mode = True
        extra = 'forbid'