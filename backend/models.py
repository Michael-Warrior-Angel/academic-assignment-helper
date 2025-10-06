from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text, JSON, Float, TIMESTAMP
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector

Base = declarative_base()

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password_hash = Column(String)
    full_name = Column(String)
    student_id = Column(String)
    created_at = Column(TIMESTAMP, server_default=func.now())

class Assignment(Base):
    __tablename__ = "assignments"
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    filename = Column(String)
    original_text = Column(Text)
    topic = Column(String)
    academic_level = Column(String)
    word_count = Column(Integer)
    uploaded_at = Column(TIMESTAMP, server_default=func.now())

class AnalysisResult(Base):
    __tablename__ = "analysis_results"
    id = Column(Integer, primary_key=True)
    assignment_id = Column(Integer, ForeignKey("assignments.id"))
    suggested_sources = Column(JSON)
    plagiarism_score = Column(Float)
    flagged_sections = Column(JSON)
    research_suggestions = Column(Text)
    citation_recommendations = Column(Text)
    confidence_score = Column(Float)
    analyzed_at = Column(TIMESTAMP, server_default=func.now())

class AcademicSource(Base):
    __tablename__ = "academic_sources"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    authors = Column(Text)
    publication_year = Column(Integer)
    abstract = Column(Text)
    full_text = Column(Text)
    source_type = Column(String)  # 'paper', 'textbook', 'course_material'
    embedding = Column(Vector(1536))
