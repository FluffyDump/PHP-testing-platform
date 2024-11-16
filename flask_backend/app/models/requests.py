from pydantic import BaseModel, Field
from app.models import database
from typing import Optional

# Authentication request models
class RegisterRequest(BaseModel):
    username: str
    firstName: str
    lastName: str
    email: str
    password: str

class LoginRequest(BaseModel):
    login_identifier: str
    password: str


# Question request models
class CreateQuestionRequest(BaseModel):
    question_text: str
    correct_answer: str
    test_id: int


# Test request models
class CreateTestRequest(BaseModel):
    title: str
    description: Optional[str] = Field(None)
    teacher_id: int