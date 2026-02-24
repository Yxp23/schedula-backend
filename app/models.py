from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Course(Base):
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), unique=True, nullable=False, index=True)  # e.g., "CMPSC 132"
    title = Column(String(200), nullable=False)
    description = Column(Text)
    credits = Column(Integer)
    department = Column(String(100), index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    sections = relationship("CourseSection", back_populates="course")

class Professor(Base):
    __tablename__ = "professors"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    department = Column(String(100))
    rmp_rating = Column(Float)  # RateMyProfessor rating (0-5)
    rmp_difficulty = Column(Float)  # Difficulty rating (0-5)
    rmp_would_take_again = Column(Float)  # Percentage
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    sections = relationship("CourseSection", back_populates="professor")

class CourseSection(Base):
    __tablename__ = "course_sections"
    
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    professor_id = Column(Integer, ForeignKey("professors.id"))
    semester = Column(String(20))  # e.g., "Fall 2024"
    section_number = Column(String(10))
    days = Column(String(20))  # e.g., "MWF"
    time = Column(String(50))  # e.g., "10:00 AM - 10:50 AM"
    location = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    course = relationship("Course", back_populates="sections")
    professor = relationship("Professor", back_populates="sections")