from flask_backend.app.sevices.user_service import registration, login
from fastapi import APIRouter, HTTPException, Depends, Response
from app.config.db_connection import SessionLocal
from app.config.db_connection import get_db
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.models import requests
from datetime import timedelta
import os

auth_router = APIRouter()

@auth_router.post('/register')
async def registration_route(data: requests.RegisterRequest, db: Session = Depends(get_db)):
    success, message = registration(db=db, username=data.username, first_name=data.firstName, last_name=data.lastName, email=data.email, password=data.password)

    if success is True:
        return JSONResponse(content={"message": f"{message}"}, status_code=200)
    elif success is False:
        return JSONResponse(content={"message": f"{message}"}, status_code=401)
    else:
        raise HTTPException(status_code=400, detail="Įvyko serverio klaida registruojantis")

@auth_router.post('/login')
async def login_route(data: requests.LoginRequest, response: Response, db: Session = Depends(get_db)):
    success, access_token, refresh_token, role, message = login(db=db, login_identifier=data.login_identifier, password=data.password)
    
    if success:
        refresh_token_expiration = timedelta(days=int(os.getenv('REFRESH_TOKEN_EXPIRE_DAYS', '7')))
        
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            max_age=refresh_token_expiration.total_seconds(),
            secure=True,
            samesite="strict"
        )
        
        return {
                "message": message,
                "access_token": access_token,
                "token_type": "bearer",
                "role": role
            }
    else:
        return JSONResponse(content={"message": message}, status_code=401)