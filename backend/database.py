"""
Database Models and Connection for POQ Survey Platform
Capitol Technology University Research Study
"""
import os
from datetime import datetime, timezone
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Boolean, ForeignKey, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

DATABASE_URL = os.environ.get('DATABASE_URL')

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Participant(Base):
    """Participant registration and consent information"""
    __tablename__ = 'participants'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    participant_id = Column(String(50), unique=True, nullable=False, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    consent_given = Column(Boolean, default=False, nullable=False)
    consent_timestamp = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    # Relationships
    responses = relationship("SurveyResponse", back_populates="participant")
    sessions = relationship("Session", back_populates="participant")


class SurveyResponse(Base):
    """Individual survey question responses"""
    __tablename__ = 'survey_responses'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    participant_id = Column(String(50), ForeignKey('participants.participant_id'), nullable=False, index=True)
    question_number = Column(Integer, nullable=False)
    subsection = Column(String(50), nullable=False)
    user_response = Column(Integer, nullable=False)
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    # Constraint to validate response range 1-6
    __table_args__ = (
        CheckConstraint('user_response >= 1 AND user_response <= 6', name='valid_response_range'),
        CheckConstraint('question_number >= 1 AND question_number <= 16', name='valid_question_number'),
    )
    
    # Relationship
    participant = relationship("Participant", back_populates="responses")


class Session(Base):
    """Session tracking for participants"""
    __tablename__ = 'sessions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    participant_id = Column(String(50), ForeignKey('participants.participant_id'), nullable=False, index=True)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=True)
    session_duration_seconds = Column(Integer, nullable=True)
    
    # Relationship
    participant = relationship("Participant", back_populates="sessions")


class Investigator(Base):
    """Authenticated investigators with role-based access"""
    __tablename__ = 'investigators'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False)  # 'primary_investigator' or 'platform_designer'
    first_login = Column(Boolean, default=True)
    password_changed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    # Constraint for valid roles
    __table_args__ = (
        CheckConstraint("role IN ('primary_investigator', 'platform_designer')", name='valid_role'),
    )


def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_db_session():
    """Get database session for direct use"""
    return SessionLocal()
