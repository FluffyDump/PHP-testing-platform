from fastapi import APIRouter, HTTPException, Depends, Response
from app.sevices.user_service import registration, login
from app.config.dependencies import oauth2_scheme
from app.config.db_connection import get_db
from sqlalchemy.exc import SQLAlchemyError
from app.models import requests, responses
from app.sevices import jwt_service
from sqlalchemy.orm import Session
from app import exceptions
from jose import jwt
import logging

auth_router = APIRouter()

@auth_router.post("/register", status_code=201, response_model=responses.AuthResponse, tags=["Authentication Management"])
async def registration_route(data: requests.RegisterRequest, response: Response, db: Session = Depends(get_db)):
    try:
        access_token, refresh_token, role, message = registration(db=db, username=data.username, first_name=data.firstName, last_name=data.lastName, email=data.email, password=data.password)
        logging.info("User account created, created new refresh and access tokens")

        jwt_service.set_cookie(response=response, refresh_token=refresh_token)
        logging.info("New refresh token issued")

        return {
            "message": message,
            "access_token": access_token,
            "role": role
        }
    except exceptions.Conflict as user_ex:
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


@auth_router.post("/login", status_code=201, response_model=responses.AuthResponse, tags=["Authentication Management"])
async def login_route(data: requests.LoginRequest, response: Response, db: Session = Depends(get_db)):
    try:
        access_token, refresh_token, role, message = login(db=db, login_identifier=data.login_identifier, password=data.password)
        logging.info("User logged in, created new refresh and access tokens")
    
        jwt_service.set_cookie(response=response, refresh_token=refresh_token)
        logging.info("New refresh token issued")
        
        return {
            "message": message,
            "access_token": access_token,
            "role": role
        }
    except exceptions.Unauthorized as user_cred:
        logging.warning(f"Incorrect credentials: {user_cred.message}")
        raise HTTPException(status_code=user_cred.status_code, detail=user_cred.message)
    except SQLAlchemyError as db_ex:
        logging.error(f"Database error: {db_ex}")
        raise HTTPException(status_code=500, detail="Vidinė serverio klaida")
    except jwt.JWTError as jwt_err:
        logging.error(f"JWT error: {jwt_err}")
        raise HTTPException(status_code=401, detail="Neįmanoma patikrinti naudotojo duomenų")
    

@auth_router.post("/refresh", status_code=200, tags=["Authentication Management"])
async def refresh_route(response: Response, 
                        refresh_token: str = Depends(jwt_service.get_refresh_token_from_cookie),
                        access_token: str = Depends(oauth2_scheme)):
    try:
        access_token_expired = jwt_service.validate_expired_access_token(response=response, access_token=access_token)
        if access_token_expired:
            access_token = jwt_service.refresh_access_token(refresh_token=refresh_token)
            logging.info("User access token expired - updated access token")
            return access_token
        else:
            logging.info("User access token is still valid")
            raise HTTPException(status_code=400, detail="Prieigos žetonas vis dar galioja")
    except HTTPException as http_ex:
        logging.error(f"HTTP exception: {http_ex}")
        raise http_ex
    

@auth_router.post('/logout', status_code=204, tags=["Authentication Management"])
def logout_route(response: Response):
    try:
        jwt_service.remove_cookie(response=response)
        logging.info("User logged out successfully.")
    except jwt.JWTError as jwt_err:
        logging.error(f"JWT error: {jwt_err}")
        raise HTTPException(status_code=401, detail="Neįmanoma patikrinti naudotojo duomenų")