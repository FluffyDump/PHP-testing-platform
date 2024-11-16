from app.models.database import User, Student
from sqlalchemy.orm import Session
import bcrypt

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
        if student_role:
            return True, 'student', 'Prisijungimas sėkmingas!'
        else:
            return True, 'teacher', 'Prisijungimas sėkmingas!'
    return False, None, 'Neteisingas vartotojo vardas/el. paštas arba slaptažodis!'