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
