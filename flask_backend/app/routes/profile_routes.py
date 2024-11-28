from app.sevices import user_service, jwt_service, test_service, question_service
from fastapi import APIRouter, HTTPException, Depends
from fastapi import APIRouter, HTTPException
from app.config.db_connection import get_db
from sqlalchemy.exc import SQLAlchemyError
from app.models import requests, responses
from sqlalchemy.orm import Session
from app import exceptions
from typing import List
import logging

router = APIRouter()

@router.get('/user', response_model=responses.UserAccount, status_code=200, tags=["Profile Management"])
async def get_user(db: Session = Depends(get_db), current_user: dict = Depends(jwt_service.get_current_user)):
    user = user_service.get_user(db=db, username=current_user["username"])
    return user