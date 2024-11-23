from datetime import timedelta
from dotenv import load_dotenv
import os

load_dotenv()

#Database connection variables
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

#User authentication variables
MIN_USER_NAME_LENGTH = int(os.getenv("MIN_USER_NAME_LENGTH"))
MAX_USER_NAME_LENGTH = int(os.getenv("MAX_USER_NAME_LENGTH"))

MIN_USERNAME_LENGTH = int(os.getenv("MIN_USERNAME_LENGTH"))
MAX_USERNAME_LENGTH = int(os.getenv("MAX_USERNAME_LENGTH"))

MIN_EMAIL_LENGTH = int(os.getenv("MIN_EMAIL_LENGTH"))
MAX_EMAIL_LENGTH = int(os.getenv("MAX_EMAIL_LENGTH"))

MIN_PASSWORD_LENGTH = int(os.getenv("MIN_PASSWORD_LENGTH"))
MAX_PASSWORD_LENGTH = int(os.getenv("MAX_PASSWORD_LENGTH"))

#Access/refresh token variables
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

#Validate if any fields related to user authentication in .env file are missing
def validate_settings():
    required_settings = [
        #Database connection settings
        "DB_USER",
        "DB_PASSWORD",
        "DB_HOST",
        "DB_NAME",

        #User authentication settings
        "MIN_USER_NAME_LENGTH",
        "MAX_USER_NAME_LENGTH",
        "MIN_USERNAME_LENGTH",
        "MAX_USERNAME_LENGTH",
        "MIN_EMAIL_LENGTH",
        "MAX_EMAIL_LENGTH",
        "MIN_PASSWORD_LENGTH",
        "MAX_PASSWORD_LENGTH",


        #Access/refresh token settings
        "SECRET_JWT_KEY",
        "ALGORITHM",
        "COOKIE_KEY",
        "COOKIE_HTTP_ONLY",
        "COOKIE_SECURE",
        "COOKIE_SAMESITE"
    ]
    
    missing_vars = [var for var in required_settings if os.getenv(var) is None]

    if missing_vars:
        raise RuntimeError(
            f"Critical user authentication settings are missing: {', '.join(missing_vars)}"
        )