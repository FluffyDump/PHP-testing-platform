from app.models.database import Test
from sqlalchemy.orm import Session

def create_test(db: Session, title: str, description: str, teacher_id: int):
    new_test = Test(title=title, description=description, fk_teacheruser_id=teacher_id)
    db.add(new_test)
    db.commit()
    db.refresh(new_test)

    return True, new_test.test_id