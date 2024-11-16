from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, DateTime, func
from app.config.db_connection import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "User"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    registration_date = Column(DateTime, server_default=func.now(), nullable=False)

    # Relationships
    student = relationship("Student", back_populates="user", uselist=False)
    teacher = relationship("Teacher", back_populates="user", uselist=False)
    test_results = relationship("TestResult", back_populates="user")


class Student(Base):
    __tablename__ = "student"

    user_id = Column(Integer, ForeignKey("User.user_id"), primary_key=True)
    user = relationship("User", back_populates="student")


class Teacher(Base):
    __tablename__ = "teacher"

    user_id = Column(Integer, ForeignKey("User.user_id"), primary_key=True)
    user = relationship("User", back_populates="teacher")
    tests = relationship("Test", back_populates="teacher")


class Test(Base):
    __tablename__ = "test"

    test_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    question_count = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    removed = Column(Boolean, default=False, nullable=False)

    # Relationships
    teacher_id = Column(Integer, ForeignKey("teacher.user_id"))
    teacher = relationship("Teacher", back_populates="tests")
    questions = relationship("Question", back_populates="test", cascade="all, delete-orphan")
    test_results = relationship("TestResult", back_populates="test")


class Question(Base):
    __tablename__ = "question"

    question_id = Column(Integer, primary_key=True, index=True)
    question_text = Column(String, nullable=False)
    correct_answer = Column(String, nullable=False)

    # Relationships
    test_id = Column(Integer, ForeignKey("test.test_id"), nullable=False)
    test = relationship("Test", back_populates="questions")
    answer = relationship("Answer", back_populates="question", uselist=False)


class TestResult(Base):
    __tablename__ = "test_result"

    test_result_id = Column(Integer, primary_key=True, index=True)
    correct_count = Column(Integer, nullable=False)
    total_questions = Column(Integer, nullable=False)
    score = Column(Float, nullable=False)
    completed_at = Column(DateTime, server_default=func.now(), nullable=False)

    # Relationships
    user_id = Column(Integer, ForeignKey("User.user_id"), nullable=False)
    user = relationship("User", back_populates="test_results")

    test_id = Column(Integer, ForeignKey("test.test_id"), nullable=False)
    test = relationship("Test", back_populates="test_results")

    answers = relationship("Answer", back_populates="test_result", cascade="all, delete-orphan")


class Answer(Base):
    __tablename__ = "answer"

    answer_id = Column(Integer, primary_key=True, index=True)
    question_text = Column(String, nullable=False)
    submitted_answer = Column(String, nullable=False)
    is_correct = Column(Boolean, default=False, nullable=False)

    # Relationships
    question_id = Column(Integer, ForeignKey("question.question_id"), nullable=False)
    question = relationship("Question", back_populates="answer")

    test_result_id = Column(Integer, ForeignKey("test_result.test_result_id"), nullable=False)
    test_result = relationship("TestResult", back_populates="answers")