from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from fastapi import Response
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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def validate_settings():
    if not (COOKIE_KEY and 
            COOKIE_HTTP_ONLY and 
            REFRESH_TOKEN_EXPIRE_DAYS and 
            COOKIE_SECURE and 
            COOKIE_SAMESITE):
        raise RuntimeError("Critical cookie settings are missing. Check environment variables.")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + access_token_expires
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_JWT_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + refresh_token_expires
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_JWT_KEY, algorithm=ALGORITHM)

def refresh_access_token(refresh_token: str, response: Response):
    try:
        payload = jwt.decode(refresh_token, SECRET_JWT_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        role = payload.get("role")

        new_access_token = create_access_token(data={"sub": username, "role": role})

        return {"access_token": new_access_token, "token_type": "bearer"}
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Neteisingas prieigos žetonas")

def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        payload = jwt.decode(token, SECRET_JWT_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")

        if username is None or role is None:
            raise HTTPException(status_code=401, detail="Neteisingas prieigos žetonas")
        
        return {"username": username, "role": role}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Prieigos žetonas negalioja")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Neteisingas prieigos žetonas")

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

def remove_cookie(response: Response):
    response.delete_cookie(
        key=COOKIE_KEY,
        httponly=COOKIE_HTTP_ONLY,
        secure=COOKIE_SECURE,
        samesite=COOKIE_SAMESITE
    )