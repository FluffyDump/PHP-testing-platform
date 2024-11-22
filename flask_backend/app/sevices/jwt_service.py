from datetime import datetime, timedelta, timezone
from app.config.dependencies import oauth2_scheme
from fastapi import Depends, HTTPException
from fastapi import Response, Request
from app import exceptions
from jose import jwt
import os

SECRET_JWT_KEY = os.getenv("SECRET_JWT_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))

COOKIE_KEY = str(os.getenv("COOKIE_KEY"))
COOKIE_HTTP_ONLY = os.getenv("COOKIE_HTTP_ONLY")
COOKIE_SECURE = os.getenv("COOKIE_SECURE")
COOKIE_SAMESITE = str(os.getenv("COOKIE_SAMESITE"))

access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

#Validate if any fields related to authorization in .env file is missing
def validate_settings():
    if not (COOKIE_KEY and 
            COOKIE_HTTP_ONLY and 
            REFRESH_TOKEN_EXPIRE_DAYS and 
            COOKIE_SECURE and 
            COOKIE_SAMESITE):
        raise RuntimeError("Critical cookie settings are missing. Check environment variables.")
    
#Set refresh token cookie in response
def set_cookie(response: Response, refresh_token: str):
    response.set_cookie(
            key=COOKIE_KEY,
            value=refresh_token,
            httponly=COOKIE_HTTP_ONLY,
            max_age=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS).total_seconds(),
            secure=COOKIE_SECURE,
            samesite=COOKIE_SAMESITE
        )
    return response

#Remove refresh token cookie from response
def remove_cookie(response: Response):
    response.delete_cookie(
        key=COOKIE_KEY,
        httponly=COOKIE_HTTP_ONLY,
        secure=COOKIE_SECURE,
        samesite=COOKIE_SAMESITE
    )

#Create access token object with provided data fields
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + access_token_expires
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_JWT_KEY, algorithm=ALGORITHM)

#Create refresh token object with provided data fields
def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + refresh_token_expires
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_JWT_KEY, algorithm=ALGORITHM)

#Issue new token with the same information as the refresh token
def refresh_access_token(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, SECRET_JWT_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        role = payload.get("role")

        new_access_token = create_access_token(data={"sub": username, "role": role})

        return {"access_token": new_access_token, "token_type": "bearer"}
    except jwt.JWTError:
        raise exceptions.Unauthorized(message="Neteisingas prieigos žetonas")
    
#Parse refresh token cookie
def get_refresh_token_from_cookie(request: Request):
    refresh_token = request.cookies.get(COOKIE_KEY)
    if not refresh_token:
        raise exceptions.Unauthorized(message="Nerastas atnaujinimo žetonas")

    return refresh_token

#Checks if access token is present and expired
def validate_expired_access_token(response: Response, access_token: str):
    try:
        jwt.decode(access_token, SECRET_JWT_KEY, algorithms=[ALGORITHM])
        return False
    except jwt.ExpiredSignatureError:
        return True
    except jwt.JWTError:
        remove_cookie(response=response)
        raise HTTPException(status_code=401, detail="Neteisingas prieigos žetonas", headers=response.headers)

#Parse user with role from access token
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_JWT_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")

        if username is None or role is None:
            raise exceptions.Unauthorized(message="Neteisingas prieigos žetonas")
        
        return {"username": username, "role": role}
    except jwt.ExpiredSignatureError:
        raise exceptions.Unauthorized(message="Prieigos žetonas negalioja")
    except jwt.JWTError:
        raise exceptions.Unauthorized(message="Neteisingas prieigos žetonas")