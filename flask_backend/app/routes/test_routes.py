from flask_backend.app.sevices.test_service import create_test
from fastapi import APIRouter, HTTPException
from app.models import requests

router = APIRouter()

@router.post('/create_test')
async def create_test_route(data: requests.CreateTestRequest):
    success, result = create_test(data.title, data.description, data.teacher_id)
    
    if success:
        return {"message": "Test created successfully!", "test_id": result}
    else:
        raise HTTPException(status_code=500, detail=result)