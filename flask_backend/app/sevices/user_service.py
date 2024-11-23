from app.models.database import User, Student
from app.sevices import jwt_service
from sqlalchemy.orm import Session
from app import exceptions
import bcrypt

def registration(db: Session, username: str, first_name: str, last_name: str, email: str, password: str):
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    existing_user_by_username = db.query(User).filter(User.username == username).first()
    if existing_user_by_username:
        raise exceptions.Conflict("Vartotojo vardas jau registruotas!")
    
    existing_user_by_email = db.query(User).filter(User.email == email).first()
    if existing_user_by_email:
        raise exceptions.Conflict("Elektroninis paštas jau registruotas!")

    new_user = User(username=username, name=first_name, surname=last_name, email=email, password_hash=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    new_student = Student(user_id=new_user.user_id)
    db.add(new_student)
    db.commit()

    role = "Student"
    access_token = jwt_service.create_access_token(data={"sub": new_user.username, "role": role})
    refresh_token = jwt_service.create_refresh_token(data={"sub": new_user.username, "role": role})

    return access_token, refresh_token, role, "Registracija sėkminga!"


def login(db: Session, login_identifier: str, password: str):
    user = db.query(User).filter(User.username == login_identifier).first()

    if not user:
        user = db.query(User).filter(User.email == login_identifier).first()

    if user and bcrypt.checkpw(password.encode("utf-8"), user.password_hash.encode("utf-8")):
        student_role = db.query(Student).filter(Student.user_id == user.user_id).first()
        role = "Student" if student_role else "Teacher"

        access_token = jwt_service.create_access_token(
            data={"sub": user.username, "role": role}
        )
        refresh_token = jwt_service.create_refresh_token(
            data={"sub": user.username, "role": role}
        )

        return access_token, refresh_token, role, "Prisijungimas sėkmingas!"

    raise exceptions.Unauthorized("Neteisingi prisijungimo duomenys!")