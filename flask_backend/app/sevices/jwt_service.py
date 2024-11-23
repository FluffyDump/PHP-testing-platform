from datetime import datetime, timedelta, timezone
from app.config.dependencies import oauth2_scheme
from fastapi import Depends, HTTPException
from fastapi import Response, Request
from app.config import config
from app import exceptions
from jose import jwt

#Set refresh token cookie in response
def set_cookie(response: Response, refresh_token: str):
    response.set_cookie(
            key=config.COOKIE_KEY,
            value=refresh_token,
            httponly=config.COOKIE_HTTP_ONLY,
            max_age=timedelta(days=config.REFRESH_TOKEN_EXPIRE_DAYS).total_seconds(),
            secure=config.COOKIE_SECURE,
            samesite=config.COOKIE_SAMESITE
        )
    return response

#Remove refresh token cookie from response
def remove_cookie(response: Response):
    response.delete_cookie(
        key=config.COOKIE_KEY,
        httponly=config.COOKIE_HTTP_ONLY,
        secure=config.COOKIE_SECURE,
        samesite=config.COOKIE_SAMESITE
    )

#Create access token object with provided data fields
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + config.access_token_expires
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, config.SECRET_JWT_KEY, algorithm=config.ALGORITHM)

#Create refresh token object with provided data fields
def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + config.refresh_token_expires
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, config.SECRET_JWT_KEY, algorithm=config.ALGORITHM)

#Issue new token with the same information as the refresh token
def refresh_access_token(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, config.SECRET_JWT_KEY, algorithms=[config.ALGORITHM])
        username = payload.get("sub")
        role = payload.get("role")

        new_access_token = create_access_token(data={"sub": username, "role": role})

        return {"access_token": new_access_token, "token_type": "bearer"}
    except jwt.JWTError:
        raise exceptions.Unauthorized(message="Neteisingas prieigos žetonas")
    
#Parse refresh token cookie
def get_refresh_token_from_cookie(request: Request):
    refresh_token = request.cookies.get(config.COOKIE_KEY)
    if not refresh_token:
        raise exceptions.Unauthorized(message="Nerastas atnaujinimo žetonas")

    return refresh_token

#Checks if access token is present and expired
def validate_expired_access_token(response: Response, access_token: str):
    try:
        jwt.decode(access_token, config.SECRET_JWT_KEY, algorithms=[config.ALGORITHM])
        return False
    except jwt.ExpiredSignatureError:
        return True
    except jwt.JWTError:
        remove_cookie(response=response)
        raise HTTPException(status_code=401, detail="Neteisingas prieigos žetonas", headers=response.headers)

#Parse user with role from access token
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, config.SECRET_JWT_KEY, algorithms=[config.ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")

        if username is None or role is None:
            raise exceptions.Unauthorized(message="Neteisingas prieigos žetonas")
        
        return {"username": username, "role": role}
    except jwt.ExpiredSignatureError:
        raise exceptions.Unauthorized(message="Prieigos žetonas negalioja")
    except jwt.JWTError:
        raise exceptions.Unauthorized(message="Neteisingas prieigos žetonas")