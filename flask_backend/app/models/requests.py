from typing import Optional, List, Dict
from pydantic import BaseModel, Field

class Question(BaseModel):
    text: str

class Answer(BaseModel):
    text: str

class TestRemovalRequest(BaseModel):
    test_id: int

class RegisterRequest(BaseModel):
    username: str
    firstName: str
    lastName: str
    email: str
    password: str

class LoginRequest(BaseModel):
    login_identifier: str
    password: str

class CreateQuestionRequest(BaseModel):
    question_text: str
    correct_answer: str
    test_id: int

class CreateTestRequest(BaseModel):
    title: str
    description: Optional[str] = Field(None)
    questions: List[Question]
    answers: List[Answer]

class QuestionUpdate(BaseModel):
    text: str
    correct_answer: str

class TestPatch(BaseModel):
    title: str
    description: Optional[str] = None
    questions: List[QuestionUpdate]

class SubmitAnswersRequest(BaseModel):
    answers: Dict[int, str]