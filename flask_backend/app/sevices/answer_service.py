from app.models.database import Question, Answer, TestResult
from sqlalchemy.orm import Session

def create_answer(db: Session, submitted_answer: str, question_id: int, test_result_id: int):
    db_question = db.query(Question).filter(Question.question_id == question_id).first()

    if not db_question:
        raise ValueError(f"Question with ID {question_id} not found")

    db_test_result = db.query(TestResult).filter(TestResult.test_result_id == test_result_id).first()

    if not db_test_result:
        raise ValueError(f"TestResult with ID {test_result_id} not found")

    is_correct = db_question.correct_answer == submitted_answer

    new_answer = Answer(
        fk_questionquestion_id=question_id,
        submitted_answer=submitted_answer,
        question=db_question.question_text,
        is_correct=is_correct,
        fk_test_resulttest_result_id=test_result_id
    )

    db.add(new_answer)
    db.commit()
    db.refresh(new_answer)

    return new_answer
