from app.models.database import User, Test
from app.models.database import Test
from sqlalchemy.orm import Session

def create_test(db: Session, title: str, description: str, teacher_id: int):
    new_test = Test(title=title, description=description, fk_teacheruser_id=teacher_id)
    db.add(new_test)
    db.commit()
    db.refresh(new_test)

    return True, new_test.test_id

def get_created_tests(db: Session, teacher_name: str):
    user = db.query(User).filter(User.username == teacher_name).first()

    if user: 
        tests = db.query(Test).filter(Test.fk_teacheruser_id == user.user_id).all()
        return tests
    return None