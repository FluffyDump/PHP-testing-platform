from app.models.database import Question
from sqlalchemy.orm import Session
from app import exceptions
from typing import List

def create_question(db: Session, question_text:str, correct_answer: str, test_id: int):
    new_question = Question(question_text=question_text, correct_answer=correct_answer, fk_testtest_id=test_id)
    db.add(new_question)
    return new_question

def update_question(db: Session, question_id: int, question_text: str, correct_answer: str):
    db_question = db.query(Question).filter(Question.question_id == question_id).first()
    
    if not db_question:
        raise exceptions.NotFound("Redaguojamas klausimas nerastas!")
    
    if question_text:
        db_question.question_text = question_text
    if correct_answer:
        db_question.correct_answer = correct_answer

    db.commit()
    db.refresh(db_question)

    return {
        "question_id": db_question.question_id,
        "question_text": db_question.question_text,
        "correct_answer": db_question.correct_answer
    }

def get_question_by_id(db: Session, question_id: int):
    question_data = db.query(Question).filter(Question.question_id == question_id).first()

    if question_data:
        return {
        "question_id": question_data.question_id,
        "question_text": question_data.question_text,
        "correct_answer": question_data.correct_answer
    }
    return None

def get_questions_by_test_id(db: Session, test_id: int):
    question_data = db.query(Question).filter(Question.fk_testtest_id == test_id).all()

    if question_data:
        return {
            "questions": [
                {
                    "question_id": q.question_id,
                    "question_text": q.question_text,
                    "correct_answer": q.correct_answer
                }
                for q in question_data
            ]
        }
    return None

def get_question_objects_by_test_id(db: Session, test_id: int) -> List[Question]:
    question_data = db.query(Question).filter(Question.fk_testtest_id == test_id).all()
    
    if question_data:
        return question_data
    return []

def get_question_object_by_test_id(db: Session, question_id: int):
    question_data = db.query(Question).filter(Question.question_id == question_id).first()
    
    if question_data:
        return question_data
    return None
