from app.models.database import User, Test, TestResult
from app.models.database import Test
from sqlalchemy.orm import Session
from app import exceptions
from typing import List

def create_test(db: Session, title: str, description: str, question_count: int, teacher_id: int):
    new_test = Test(title=title, description=description, question_count=question_count, fk_teacheruser_id=teacher_id)
    db.add(new_test)
    db.commit()
    db.refresh(new_test)
    return new_test.test_id

def remove_test(db: Session, test_id: int, teacher_id: int):
    existing_test = db.query(Test).filter(Test.test_id == test_id).first()

    if existing_test and existing_test.fk_teacheruser_id == teacher_id:
        existing_test.removed = True
        db.commit()
    else:
        raise exceptions.Unauthorized("Naudotojas nėra testo savininkas!")

def get_created_tests(db: Session, teacher_name: str):
    user = db.query(User).filter(User.username == teacher_name).first()

    if user: 
        tests = db.query(Test).filter(Test.fk_teacheruser_id == user.user_id, Test.removed == False).all()
        return tests
    return None

def get_all_non_removed_tests(db: Session):
    tests = db.query(Test).filter(Test.removed == False).all()
    if tests:
        return tests
    return None

def get_test_by_id(db: Session, test_id: int, teacher_id: int):
    test_data = db.query(Test).filter(Test.test_id == test_id, Test.fk_teacheruser_id == teacher_id).first()

    if test_data:
        return {
            "test_id": test_data.test_id,
            "title": test_data.title,
            "description": test_data.description
        }
    return None

def get_test_by_test_id(db: Session, test_id: int):
    test_data = db.query(Test).filter(Test.test_id == test_id).first()

    if test_data:
        return {
            "test_id": test_data.test_id,
            "title": test_data.title,
            "description": test_data.description
        }
    return None

def get_result_test_id_by_id(db: Session, test_result_id: int, student_id: int):
    test_data = db.query(TestResult).filter(TestResult.test_result_id == test_result_id, TestResult.fk_studentuser_id == student_id).first()

    if test_data:
        return test_data.fk_testtest_id
    return None

def get_test_object_by_id(db: Session, test_id: int, teacher_id: int):
    test_data = db.query(Test).filter(Test.test_id == test_id, Test.fk_teacheruser_id == teacher_id).first()

    if test_data:
        return test_data
    return None

def get_test_teacher_id(db: Session, test_id: int):
    test_data = db.query(Test).filter(Test.test_id == test_id).first()

    if test_data:
        return test_data.fk_teacheruser_id
    return None

def process_test_results(db: Session, user_id: int, test_id: int, answers: list):
    correct_count = sum(1 for answer in answers if answer.get("is_correct", False))
    total_questions = len(answers)
    score = (correct_count / total_questions) * 100 if total_questions else 0
    
    finished_test = TestResult(
        fk_studentuser_id=user_id,
        fk_testtest_id=test_id,
        correct_count=correct_count,
        total_questions=total_questions,
        score=score
    )

    db.add(finished_test)
    db.commit()
    db.refresh(finished_test)

    return {
        "result_id": finished_test.test_result_id,
        "correct_count": correct_count,
        "total_questions": total_questions,
        "score": score
    }

def get_test_history(db: Session, student_id: int) -> List[dict]:
    test_result_data = db.query(TestResult).filter(TestResult.fk_studentuser_id == student_id).all()

    if not test_result_data:
        return []

    test_data = []
    for result in test_result_data:
        test = db.query(Test).filter(Test.test_id == result.fk_testtest_id).one_or_none()

        if test:
            test_data.append({
                "test_id": test.test_id,
                "test_name": test.title,
                "correct_count": result.correct_count,
                "question_count": result.total_questions,
                "score": result.score,
                "completed_at": result.completed_at
            })

    return test_data
