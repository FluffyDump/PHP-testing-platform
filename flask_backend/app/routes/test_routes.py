from fastapi import APIRouter, HTTPException, Depends, Response
from flask_backend.app.sevices import test_service
from fastapi import APIRouter, HTTPException
from app.config.db_connection import get_db
from app.models import requests, response
from app.sevices import jwt_service
from sqlalchemy.orm import Session
from typing import List

router = APIRouter()

@router.post('/create_test', status_code=200)
async def create_test_route(data: requests.CreateTestRequest, db: Session = Depends(get_db)):
    success, result = test_service.create_test(data.title, data.description, data.teacher_id)
    
    if success:
        return {"message": "Test created successfully!", "test_id": result}
    else:
        raise HTTPException(status_code=500, detail=result)
    
@router.get('/tests', response_model=List[response.TestList], status_code=200)
async def list_tests_route(db: Session = Depends(get_db), current_user: dict = Depends(jwt_service.get_current_user)):
    if current_user["role"] != "Teacher":
        raise HTTPException(status_code=403, detail="Nepakankamos naudotojo teisės")
    
    tests = test_service.get_created_tests(db=db, teacher_name=current_user["username"])
    return tests