from flask_backend.app.sevices.user_service import registration, login
from fastapi import APIRouter, HTTPException, Depends
from app.config.db_connection import SessionLocal
from app.config.db_connection import get_db
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.models import requests

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
async def login_route(data: requests.LoginRequest, db: Session = Depends(get_db)):
    success, role, message = login(db=db, login_identifier=data.login_identifier, password=data.password)
    if success is True:
        return JSONResponse(content={"message": f"{message}","role": f"{role}"}, status_code=200)
    elif success is False:
        return JSONResponse(content={"message": f"{message}"}, status_code=200)
    else:
        raise HTTPException(status_code=401, detail="Įvyko serverio klaida prisijungiant")