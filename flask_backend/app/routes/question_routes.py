from flask_backend.app.sevices.question_service import create_question
from fastapi import APIRouter, HTTPException
from app.models import requests

router = APIRouter()

@router.post('/create_question')
async def create_question_route(data: requests.CreateQuestionRequest):
    success, result = create_question(data.question_text, data.correct_answer, data.test_id)
    
    if success:
        return {"message": result}
    else:
        raise HTTPException(status_code=500, detail=result)