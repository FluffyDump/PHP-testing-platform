from app.sevices import user_service, jwt_service, test_service, question_service, answer_service
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi import APIRouter, HTTPException, Depends
from fastapi import APIRouter, HTTPException
from app.config.db_connection import get_db
from app.validators import shared_validator
from app.models import requests, responses, database
from sqlalchemy.orm import Session
from app import exceptions
from typing import List
import logging

router = APIRouter()

@router.post('/tests', response_model=responses.CreatedTest, status_code=200, tags=["Tests Management"])
async def create_test_route(data: requests.CreateTestRequest, db: Session = Depends(get_db), current_user: dict = Depends(jwt_service.get_current_user)):
    try:
        if current_user.get("role") != "Teacher":
            raise HTTPException(status_code=403, detail="Nepakankamos naudotojo teisės!")
        
        teacher_id = user_service.get_user_id(db=db, username=current_user["username"])

        question_count = len(data.questions)

        shared_validator.validate_sql_malicious_input(data.title)
        shared_validator.validate_sql_malicious_input(data.description)

        if len(data.title) > 255:
            logging.warning("Provided new test title is too long")
            raise HTTPException(status_code=400, detail="Testo pavadinimo laukas negali būti ilgesnis nei 255 simboliai!")
        
        if len(data.description) > 255:
            logging.warning("Provided new test description is too long")
            raise HTTPException(status_code=400, detail="Testo aprašymo laukas negali būti ilgesnis nei 255 simboliai!")
        
        if data.title is None or data.title == "":
            logging.warning("New test title is None")
            raise HTTPException(status_code=400, detail="Testo pavadinimas yra privalomas!")
        
        if question_count == 0:
            logging.warning("Question count is 0.")
            raise HTTPException(status_code=400, detail="Testas privalo turėti bent 1 klausimą!")
        
        for question in data.questions:
            shared_validator.validate_sql_malicious_input(question.text)
            if question.text is None or question.text == "":
                logging.warning("Empty question supplied")
                raise HTTPException(status_code=400, detail="Testo klausimai negali būti tušti!")
            if len(question.text) > 255:
                logging.warning("Provided question is too long")
                raise HTTPException(status_code=400, detail="Testo kiekvieno klausimo laukas negali būti ilgesnis nei 255 simboliai!")
            
        for answer in data.answers:
            shared_validator.validate_sql_malicious_input(answer.text)
            if answer.text is None or answer.text == "":
                logging.warning("Empty question supplied")
                raise HTTPException(status_code=400, detail="Testo atsakymai negali būti tušti!")
            if len(answer.text) > 255:
                logging.warning("Provided answer is too long")
                raise HTTPException(status_code=400, detail="Testo kiekvieno rezulto laukas negali būti ilgesnis nei 255 simboliai!")
        
        test_id = test_service.create_test(db=db, title=data.title, description=data.description, question_count=question_count, teacher_id=teacher_id)

        if test_id:
            for question, answer in zip(data.questions, data.answers):
                question_service.create_question(db=db, question_text=question.text, correct_answer=answer.text, test_id=test_id)

        db.commit()
        return {
            "message": "Testas sukurtas!",
            "test_id": test_id
        }
    except exceptions.Unauthorized as user_cred:
        logging.warning(f"Incorrect credentials: {user_cred.detail}")
        raise HTTPException(status_code=user_cred.status_code, detail=user_cred.detail)
    except exceptions.NotFound as not_found:
        logging.warning(f"User not found: {not_found.detail}")
        raise HTTPException(status_code=not_found.status_code, detail=not_found.detail)
    except SQLAlchemyError as db_ex:
        logging.error(f"Database error: {db_ex}")
        raise HTTPException(status_code=500, detail="Vidinė serverio klaida!")
    finally:
        db.rollback()
    
@router.get('/tests', response_model=List[responses.TestList], status_code=200, tags=["Tests Management"])
async def list_tests_route(db: Session = Depends(get_db), current_user: dict = Depends(jwt_service.get_current_user)):
    try:
        if current_user.get("role") != "Teacher":
            tests = test_service.get_all_non_removed_tests(db=db)
        else:
            tests = test_service.get_created_tests(db=db, teacher_name=current_user["username"])
        return tests
    except SQLAlchemyError as db_ex:
        logging.error(f"Database error: {db_ex}")
        raise HTTPException(status_code=500, detail="Vidinė serverio klaida!")
    
@router.get('/test/{test_id}', response_model=responses.EditTest, status_code=200, tags=["Tests Management"])
async def get_test_by_id(test_id: int, db: Session = Depends(get_db), current_user: dict = Depends(jwt_service.get_current_user)):
    try:
        if current_user.get("role") == "Student":
            student_id = user_service.get_user_id(db=db, username=current_user["username"])

            test_data = test_service.get_test_by_test_id(db=db, test_id=test_id)

            if not test_data:
                raise HTTPException(status_code=404, detail="Testas nerastas!")
            
            questions_data = question_service.get_questions_by_test_id(db=db, test_id=test_id)

            if not questions_data:
                raise HTTPException(status_code=404, detail="Klausimai nerasti!")
        else:
        
            teacher_id = user_service.get_user_id(db=db, username=current_user["username"])

            test_data = test_service.get_test_by_id(db=db, test_id=test_id, teacher_id=teacher_id)

            if not test_data:
                raise HTTPException(status_code=404, detail="Testas nerastas!")

            questions_data = question_service.get_questions_by_test_id(db=db, test_id=test_id)

            if not questions_data:
                raise HTTPException(status_code=404, detail="Klausimai nerasti!")

        return {
                "test_id": test_data["test_id"],
                "title": test_data["title"],
                "description": test_data["description"],
                "questions": questions_data["questions"]
            }
    except Exception as e:
        logging.error(f"Error fetching test by id: {e}")
        raise HTTPException(status_code=500, detail="Vidinė serverio klaida!")

@router.delete('/test', status_code=204, tags=["Tests Management"])
async def remove_test(data: requests.TestRemovalRequest, db: Session = Depends(get_db), current_user: dict = Depends(jwt_service.get_current_user)):
    try:
        if current_user.get("role") != "Teacher":
            raise HTTPException(status_code=403, detail="Nepakankamos naudotojo teisės!")
        
        teacher_id = user_service.get_user_id(db=db, username=current_user["username"])
        test_service.remove_test(db=db, test_id=data.test_id, teacher_id=teacher_id)
    except SQLAlchemyError as db_ex:
        logging.error(f"Database error: {db_ex}")
        raise HTTPException(status_code=500, detail="Vidinė serverio klaida!")
    except exceptions.Unauthorized as unauthorized:
        logging.warning(f"User do not own the test: {unauthorized.detail}")
        raise HTTPException(status_code=unauthorized.status_code, detail=unauthorized.detail)
    
@router.patch("/test/{test_id}", status_code=204)
async def update_test(test_id: int, data: requests.TestPatch, db: Session = Depends(get_db), current_user: dict = Depends(jwt_service.get_current_user)):
    try:
        if current_user.get("role") != "Teacher":
            raise HTTPException(status_code=403, detail="Nepakankamos naudotojo teisės!")
        
        teacher_id = user_service.get_user_id(db=db, username=current_user["username"])

        test_data = test_service.get_test_object_by_id(db=db, test_id=test_id, teacher_id=teacher_id)

        if test_data is None:
            raise HTTPException(status_code=404, detail="Testas nerastas!")

        if data.title is not None:
            test_data.title = data.title
        if data.description is not None:
            test_data.description = data.description

        questions_data = question_service.get_question_objects_by_test_id(db=db, test_id=test_id)

        updated_questions = []
        existing_question_ids = [q.question_id for q in questions_data]

        for idx, question_update in enumerate(data.questions):
            if idx < len(questions_data):
                db_question = questions_data[idx]
                if db_question:
                    question_service.update_question(db=db, question_id=db_question.question_id, question_text=question_update.text, correct_answer=question_update.correct_answer)
                    updated_questions.append(db_question)
            else:
                new_question = {
                    'question_text': question_update.text,
                    'correct_answer': question_update.correct_answer,
                    'fk_testtest_id': test_id
                }
                new_question_instance = database.Question(**new_question)

                db.add(new_question_instance)
                updated_questions.append(new_question_instance)

        test_data.questions = updated_questions

        db.commit()
        db.refresh(test_data)

    except SQLAlchemyError as db_ex:
        logging.error(f"Database error: {db_ex}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Vidinė serverio klaida!")
    
@router.get('/tests/{test_id}', response_model=responses.TestDetails, status_code=200, tags=["Tests Management"])
async def get_test_by_id(test_id: int, db: Session = Depends(get_db), current_user: dict = Depends(jwt_service.get_current_user)):
    try:
        if current_user.get("role") != "Student":
            raise HTTPException(status_code=403, detail="Nepakankamos naudotojo teisės!")
        
        test_teacher_id = test_service.get_test_teacher_id(db=db, test_id=test_id)

        test_data = test_service.get_test_object_by_id(db=db, test_id=test_id, teacher_id=test_teacher_id)
        if not test_data or test_data.removed:
            raise HTTPException(status_code=404, detail="Testas nerastas!")
        
        questions_data = question_service.get_question_objects_by_test_id(db=db, test_id=test_id)
        if not questions_data:
            raise HTTPException(status_code=404, detail="Klausimai nerasti!")

        return {
            "test_id": test_data.test_id,
            "title": test_data.title,
            "description": test_data.description,
            "questions": questions_data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail="Vidinė serverio klaida!")
    
@router.post("/tests/{test_id}/submit", response_model=responses.SubmitTestResult, status_code=201, tags=["Tests Management"])
async def submit_test_answers(test_id: int, data: requests.SubmitAnswersRequest, db: Session = Depends(get_db), current_user: dict = Depends(jwt_service.get_current_user)):
    try:
        if current_user.get("role") != "Student":
            raise HTTPException(status_code=403, detail="Nepakankamos naudotojo teisės!")
        
        user_id = user_service.get_user_id(db=db, username=current_user["username"])

        test_teacher_id = test_service.get_test_teacher_id(db=db, test_id=test_id)
        test_data = test_service.get_test_object_by_id(db=db, test_id=test_id, teacher_id=test_teacher_id)
        if not test_data:
            raise HTTPException(status_code=404, detail="Testas nerastas!")

        answers = []
        for question_id, submitted_answer in data.answers.items():
            db_question = question_service.get_question_object_by_test_id(db=db, question_id=question_id)
            if db_question:
                is_correct = db_question.correct_answer == submitted_answer
                answer = {
                    "question_id": question_id,
                    "submitted_answer": submitted_answer,
                    "is_correct": is_correct,
                    "question_text": db_question.question_text
                }
                answers.append(answer)
            else:
                raise HTTPException(status_code=404, detail=f"Klausimas su ID {question_id} nerastas!")

        result = test_service.process_test_results(db=db, user_id=user_id, test_id=test_id, answers=answers)

        for answer in answers:
            answer_service.create_answer(
                db=db,
                submitted_answer=answer["submitted_answer"],
                question_id=answer["question_id"],
                test_result_id=result["result_id"]
            )

        return result

    except SQLAlchemyError as db_ex:
        logging.error(f"Database error: {db_ex}")
        raise HTTPException(status_code=500, detail="Vidinė serverio klaida!")
    except IntegrityError as e:
        logging.error(f"Integrity error while creating answer: {e}")
    except Exception as e:
        logging.error(f"Error processing test results: {e}")
        raise HTTPException(status_code=500, detail="Vidinė serverio klaida!")
    finally:
        db.rollback()

@router.get('/history', response_model=List[responses.TestHistoryResponse], status_code=200, tags=["Tests Management"])
async def get_test_history(db: Session = Depends(get_db), current_user: dict = Depends(jwt_service.get_current_user)):
    try:
        if current_user.get("role") != "Student":
            raise HTTPException(status_code=403, detail="Nepakankamos naudotojo teisės!")
        
        student_username = current_user["username"]
        student_id = user_service.get_user_id(db=db, username=student_username)
        test_results = test_service.get_test_history(db=db, student_id=student_id)

        if not test_results:
            raise HTTPException(status_code=404, detail="Testai nerasti!")
        
        return test_results

    except Exception as e:
        logging.error(f"Error fetching test history: {e}")
        raise HTTPException(status_code=500, detail="Vidinė serverio klaida!")
