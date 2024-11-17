from app.models.database import User, Student
from app.sevices import jwt_service
from sqlalchemy.orm import Session
from datetime import timedelta
import os, bcrypt

def registration(db: Session, username: str, first_name: str, last_name: str, email: str, password: str):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    existing_user = db.query(User).filter((User.username == username) | (User.email == email)).first()
    if existing_user:
        if existing_user.username == username:
            return False, 'Vartotojo vardas jau registruotas!'
        return False, 'Elektroninis paštas jau registruotas!'

    new_user = User(username=username, name=first_name, surname=last_name, email=email, password_hash=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    new_student = Student(user_id=new_user.user_id)
    db.add(new_student)
    db.commit()

    return True, 'Registracija sėkminga!'


def login(db: Session, login_identifier: str, password: str):
    user = db.query(User).filter(User.username == login_identifier).first()

    if not user:
        user = db.query(User).filter(User.email == login_identifier).first()

    if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
        student_role = db.query(Student).filter(Student.user_id == user.user_id).first()
        role = 'Student' if student_role else 'Teacher'

        access_token_expires_minutes = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', 15))
        refresh_token_expires_days = int(os.getenv('REFRESH_TOKEN_EXPIRE_DAYS', 7))

        access_token_expires = timedelta(minutes=access_token_expires_minutes)
        refresh_token_expires = timedelta(days=refresh_token_expires_days)

        access_token = jwt_service.create_access_token(
            data={"sub": user.username, "role": role}, expires_delta=access_token_expires
        )
        refresh_token = jwt_service.create_refresh_token(
            data={"sub": user.username, "role": role}, expires_delta=refresh_token_expires
        )

        return True, access_token, refresh_token, role, 'Prisijungimas sėkmingas!'

    return False, None, None, None, 'Neteisingas vartotojo vardas/el. paštas arba slaptažodis!'