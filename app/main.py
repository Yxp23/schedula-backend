from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Course

app = FastAPI(title="Schedula API")

# Enable CORS so frontend can talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Schedula API is running! 🎓"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "database": "connected"}

@app.get("/api/courses")
def get_courses(
    search: str = None,
    department: str = None,
    db: Session = Depends(get_db)
):
    """
    Get all courses with optional filtering
    - search: Search in course code or title
    - department: Filter by department (e.g., CMPSC, MATH)
    """
    query = db.query(Course)
    
    # Apply filters
    if department:
        query = query.filter(Course.department == department.upper())
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (Course.code.ilike(search_term)) | 
            (Course.title.ilike(search_term))
        )
    
    courses = query.all()
    
    # Convert to dict
    return {
        "courses": [
            {
                "id": c.id,
                "code": c.code,
                "title": c.title,
                "description": c.description,
                "credits": c.credits,
                "department": c.department
            }
            for c in courses
        ]
    }

@app.get("/api/courses/{course_id}")
def get_course(course_id: int, db: Session = Depends(get_db)):
    """Get a single course by ID"""
    course = db.query(Course).filter(Course.id == course_id).first()
    
    if not course:
        return {"error": "Course not found"}
    
    return {
        "id": course.id,
        "code": course.code,
        "title": course.title,
        "description": course.description,
        "credits": course.credits,
        "department": course.department
    }

@app.get("/api/departments")
def get_departments(db: Session = Depends(get_db)):
    """Get list of all departments"""
    departments = db.query(Course.department).distinct().all()
    return {
        "departments": [dept[0] for dept in departments]
    }