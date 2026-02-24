from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Database URL - using localhost PostgreSQL
# Format: postgresql://username:password@localhost/database_name
# For local dev, typically no password needed
DATABASE_URL = "postgresql://postgres:Yp102938@localhost/schedula"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Function to create all tables
def create_tables():
    from app.models import Course, Professor, CourseSection
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")