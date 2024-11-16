from app.models.database import Question
from sqlalchemy.orm import Session

def create_question(db: Session, question_text: str, correct_answer: str, test_id: int):
    new_question = Question(question_text=question_text, correct_answer=correct_answer, fk_testtest_id=test_id)
    db.add(new_question)
    db.commit()
    return True