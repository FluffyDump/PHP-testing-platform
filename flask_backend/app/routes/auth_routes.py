from flask_backend.app.sevices.user_service import registration, login
from fastapi import APIRouter, HTTPException, Depends, Response
from app.config.db_connection import get_db
from sqlalchemy.exc import SQLAlchemyError
from app.sevices import jwt_service
from sqlalchemy.orm import Session
from app.models import requests
from app import exceptions
from jose import jwt
import logging

auth_router = APIRouter()

@auth_router.post("/register", status_code=200)
async def registration_route(data: requests.RegisterRequest, response: Response, db: Session = Depends(get_db)):
    try:
        access_token, refresh_token, role, message = registration(db=db, username=data.username, first_name=data.firstName, last_name=data.lastName, email=data.email, password=data.password)

        jwt_service.set_cookie(response=response, refresh_token=refresh_token)

        return {
                "message": message,
                "access_token": access_token,
                "token_type": "bearer",
                "role": role
            }
    except exceptions.UserAlreadyExistsError as user_ex:
        logging.warning(f"User already exists: {user_ex.message}")
        raise HTTPException(status_code=user_ex.status_code, detail=user_ex.message)
    except SQLAlchemyError as db_ex:
        logging.error(f"Database error: {db_ex}")
        raise HTTPException(status_code=500, detail="Vidinė serverio klaida")
    except jwt.JWTError as jwt_err:
        logging.error(f"JWT error: {jwt_err}")
        raise HTTPException(status_code=401, detail="Neįmanoma patikrinti naudotojo duomenų")
    finally:
        db.rollback()


@auth_router.post("/login", status_code=200)
async def login_route(data: requests.LoginRequest, response: Response, db: Session = Depends(get_db)):
    try:
        access_token, refresh_token, role, message = login(db=db, login_identifier=data.login_identifier, password=data.password)
    
        jwt_service.set_cookie(response=response, refresh_token=refresh_token)
        
        return {
                "message": message,
                "access_token": access_token,
                "token_type": "bearer",
                "role": role
            }
    except exceptions.IncorrectUserCredentials as user_cred:
        logging.warning(f"Incorrect credentials: {user_cred.message}")
        raise HTTPException(status_code=user_cred.status_code, detail=user_cred.message)
    except SQLAlchemyError as db_ex:
        logging.error(f"Database error: {db_ex}")
        raise HTTPException(status_code=500, detail="Vidinė serverio klaida")
    except jwt.JWTError as jwt_err:
        logging.error(f"JWT error: {jwt_err}")
        raise HTTPException(status_code=401, detail="Neįmanoma patikrinti naudotojo duomenų")


@auth_router.post('/logout', status_code=200)
def logout_route(response: Response):
    try:
        jwt_service.remove_cookie(response=response)
        return {"message": "Logout successful"}
    except jwt.JWTError as jwt_err:
        logging.error(f"JWT error: {jwt_err}")
        raise HTTPException(status_code=401, detail="Neįmanoma patikrinti naudotojo duomenų")