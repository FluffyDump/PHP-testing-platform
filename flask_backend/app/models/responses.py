from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional
from typing import List

class QuestionList(BaseModel):
    question_id: int
    question_text: str
    correct_answer: str

    class Config:
        from_attributes = False
        extra = "forbid"

class CreatedTest(BaseModel):
    message: str
    test_id: int

    class Config:
        from_attributes = False
        extra = "forbid"

class EditTest(BaseModel):
    test_id: int
    title: str
    description: str
    questions: List[QuestionList]

    class Config:
        from_attributes = True
        extra = "forbid"

class TestList(BaseModel):
    title: str
    description: str
    question_count: int
    created_at: datetime
    test_id: int

    class Config:
        from_attributes = True
        extra = "forbid"

class AuthResponse(BaseModel):
    message: str
    access_token: str
    token_type: str = "bearer"

    class Config:
        from_attributes = True
        extra = "forbid"

class UserAccount(BaseModel):
    username: str
    name: str
    surname: str
    email: str
    registration_date: datetime

    class Config:
        from_attributes = True
        extra = "forbid"

class QuestionUpdate(BaseModel):
    text: str
    correct_answer: str

class TestPatch(BaseModel):
    title: str
    description: Optional[str] = None
    questions: List[QuestionUpdate]

    class Config:
        from_attributes = True
        extra = "forbid"

class TestDetails(BaseModel):
    test_id: int
    title: str
    description: Optional[str] = None
    questions: List[QuestionList]

    class Config:
        from_attributes = True

class SubmitTestResult(BaseModel):
    result_id: int
    correct_count: int
    total_questions: int
    score: float

class TestHistoryResponse(BaseModel):
    test_id: int
    test_name: str
    correct_count: int
    question_count: int
    score: float
    completed_at: Optional[datetime]

    class Config:
        from_attributes = True

    @field_validator('score')
    def format_score(cls, value):
        return round(value, 2)