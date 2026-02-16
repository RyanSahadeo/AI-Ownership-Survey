"""
FastAPI Backend for POQ Survey Platform
Capitol Technology University Research Study
"""
from fastapi import FastAPI, APIRouter, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime, timezone
import uuid
import bcrypt
import os
from dotenv import load_dotenv
from pathlib import Path
import psycopg2
from psycopg2.extras import RealDictCursor

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

app = FastAPI(title="POQ Survey Platform API")
api_router = APIRouter(prefix="/api")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = os.environ.get('DATABASE_URL')

def get_db():
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    """Initialize database tables"""
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    # Create tables
    cur.execute("""
        CREATE TABLE IF NOT EXISTS participants (
            id SERIAL PRIMARY KEY,
            participant_id VARCHAR(50) UNIQUE NOT NULL,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            consent_given BOOLEAN DEFAULT FALSE,
            consent_timestamp TIMESTAMPTZ,
            created_at TIMESTAMPTZ DEFAULT NOW()
        )
    """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS survey_responses (
            id SERIAL PRIMARY KEY,
            participant_id VARCHAR(50) REFERENCES participants(participant_id),
            question_number INTEGER NOT NULL CHECK (question_number >= 1 AND question_number <= 16),
            subsection VARCHAR(50) NOT NULL,
            user_response INTEGER NOT NULL CHECK (user_response >= 1 AND user_response <= 6),
            timestamp TIMESTAMPTZ DEFAULT NOW(),
            UNIQUE(participant_id, question_number)
        )
    """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id SERIAL PRIMARY KEY,
            participant_id VARCHAR(50) REFERENCES participants(participant_id),
            start_time TIMESTAMPTZ NOT NULL,
            end_time TIMESTAMPTZ,
            session_duration_seconds INTEGER
        )
    """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS investigators (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            role VARCHAR(50) NOT NULL CHECK (role IN ('primary_investigator', 'platform_designer')),
            first_login BOOLEAN DEFAULT TRUE,
            password_changed BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMPTZ DEFAULT NOW(),
            last_login TIMESTAMPTZ
        )
    """)
    
    conn.commit()
    
    # Create initial investigators
    investigators = [
        ('Dr. Greg I. Voykhansky', 'givoykhansky@captechu.edu', 'CapitolTech2025!', 'primary_investigator'),
        ('Dr. Troy C. Troublefield', 'ttroublefield@captechu.edu', 'CapitolTech2025!', 'primary_investigator'),
        ('Ryan Sahadeo', 'rsahadeo@captechu.edu', 'CapitolTech2025!', 'platform_designer')
    ]
    
    for username, email, password, role in investigators:
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        try:
            cur.execute("""
                INSERT INTO investigators (username, email, password_hash, role)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (email) DO NOTHING
            """, (username, email, password_hash, role))
        except:
            pass
    
    conn.commit()
    cur.close()
    conn.close()

# Initialize DB on startup
@app.on_event("startup")
async def startup():
    init_db()

# Pydantic Models
class ParticipantCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    consent_given: bool

class ParticipantResponse(BaseModel):
    participant_id: str
    first_name: str
    last_name: str
    email: str
    consent_given: bool
    consent_timestamp: Optional[str]
    created_at: Optional[str]

class SurveyResponseCreate(BaseModel):
    participant_id: str
    question_number: int = Field(ge=1, le=16)
    user_response: int = Field(ge=1, le=6)

class SurveyResponseModel(BaseModel):
    participant_id: str
    question_number: int
    subsection: str
    user_response: int
    timestamp: Optional[str]

class SessionCreate(BaseModel):
    participant_id: str

class SessionEnd(BaseModel):
    session_id: int

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class PasswordChangeRequest(BaseModel):
    user_id: int
    new_password: str

class POQScores(BaseModel):
    participant_id: str
    Territoriality: Optional[float]
    Self_Efficacy: Optional[float]
    Accountability: Optional[float]
    Belongingness: Optional[float]
    Self_Identity: Optional[float]
    Overall_PO: Optional[float]

# Subsection mapping
SUBSECTION_MAP = {
    1: "Territoriality", 2: "Territoriality", 3: "Territoriality", 4: "Territoriality",
    5: "Self_Efficacy", 6: "Self_Efficacy", 7: "Self_Efficacy",
    8: "Accountability", 9: "Accountability", 10: "Accountability",
    11: "Belongingness", 12: "Belongingness", 13: "Belongingness",
    14: "Self_Identity", 15: "Self_Identity", 16: "Self_Identity"
}

# API Routes
@api_router.get("/")
async def root():
    return {"message": "POQ Survey Platform API", "status": "running"}

@api_router.get("/health")
async def health():
    return {"status": "healthy"}

@api_router.post("/participants", response_model=ParticipantResponse)
async def create_participant(data: ParticipantCreate, conn=Depends(get_db)):
    if not data.consent_given:
        raise HTTPException(status_code=400, detail="Consent must be given to participate")
    
    cur = conn.cursor()
    participant_id = f"POQ-{uuid.uuid4().hex[:8].upper()}"
    
    try:
        cur.execute("""
            INSERT INTO participants (participant_id, first_name, last_name, email, consent_given, consent_timestamp)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING participant_id, first_name, last_name, email, consent_given, consent_timestamp, created_at
        """, (participant_id, data.first_name.strip(), data.last_name.strip(), 
              data.email.lower().strip(), True, datetime.now(timezone.utc)))
        
        result = cur.fetchone()
        conn.commit()
        
        return {
            "participant_id": result['participant_id'],
            "first_name": result['first_name'],
            "last_name": result['last_name'],
            "email": result['email'],
            "consent_given": result['consent_given'],
            "consent_timestamp": result['consent_timestamp'].isoformat() if result['consent_timestamp'] else None,
            "created_at": result['created_at'].isoformat() if result['created_at'] else None
        }
    except psycopg2.IntegrityError:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")
    finally:
        cur.close()

@api_router.post("/responses")
async def save_response(data: SurveyResponseCreate, conn=Depends(get_db)):
    cur = conn.cursor()
    subsection = SUBSECTION_MAP.get(data.question_number, "Unknown")
    
    try:
        cur.execute("""
            INSERT INTO survey_responses (participant_id, question_number, subsection, user_response, timestamp)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (participant_id, question_number) 
            DO UPDATE SET user_response = EXCLUDED.user_response, timestamp = EXCLUDED.timestamp
            RETURNING id
        """, (data.participant_id, data.question_number, subsection, data.user_response, datetime.now(timezone.utc)))
        
        conn.commit()
        return {"success": True, "question_number": data.question_number}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()

@api_router.get("/responses/{participant_id}", response_model=List[SurveyResponseModel])
async def get_responses(participant_id: str, conn=Depends(get_db)):
    cur = conn.cursor()
    cur.execute("""
        SELECT participant_id, question_number, subsection, user_response, timestamp
        FROM survey_responses WHERE participant_id = %s ORDER BY question_number
    """, (participant_id,))
    
    results = cur.fetchall()
    cur.close()
    
    return [{
        "participant_id": r['participant_id'],
        "question_number": r['question_number'],
        "subsection": r['subsection'],
        "user_response": r['user_response'],
        "timestamp": r['timestamp'].isoformat() if r['timestamp'] else None
    } for r in results]

@api_router.post("/sessions")
async def create_session(data: SessionCreate, conn=Depends(get_db)):
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO sessions (participant_id, start_time)
        VALUES (%s, %s) RETURNING id
    """, (data.participant_id, datetime.now(timezone.utc)))
    
    result = cur.fetchone()
    conn.commit()
    cur.close()
    
    return {"session_id": result['id']}

@api_router.post("/sessions/end")
async def end_session(data: SessionEnd, conn=Depends(get_db)):
    cur = conn.cursor()
    end_time = datetime.now(timezone.utc)
    
    cur.execute("SELECT start_time FROM sessions WHERE id = %s", (data.session_id,))
    session = cur.fetchone()
    
    if session:
        duration = int((end_time - session['start_time']).total_seconds())
        cur.execute("""
            UPDATE sessions SET end_time = %s, session_duration_seconds = %s WHERE id = %s
        """, (end_time, duration, data.session_id))
        conn.commit()
    
    cur.close()
    return {"success": True, "duration_seconds": duration if session else 0}

@api_router.post("/auth/login")
async def login(data: LoginRequest, conn=Depends(get_db)):
    cur = conn.cursor()
    cur.execute("SELECT * FROM investigators WHERE email = %s", (data.email.lower(),))
    user = cur.fetchone()
    
    if user and bcrypt.checkpw(data.password.encode('utf-8'), user['password_hash'].encode('utf-8')):
        cur.execute("UPDATE investigators SET last_login = %s WHERE id = %s", (datetime.now(timezone.utc), user['id']))
        conn.commit()
        cur.close()
        
        return {
            "success": True,
            "user": {
                "id": user['id'],
                "username": user['username'],
                "email": user['email'],
                "role": user['role'],
                "first_login": user['first_login'],
                "password_changed": user['password_changed']
            }
        }
    
    cur.close()
    raise HTTPException(status_code=401, detail="Invalid credentials")

@api_router.post("/auth/change-password")
async def change_password(data: PasswordChangeRequest, conn=Depends(get_db)):
    cur = conn.cursor()
    password_hash = bcrypt.hashpw(data.new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    cur.execute("""
        UPDATE investigators SET password_hash = %s, first_login = FALSE, password_changed = TRUE
        WHERE id = %s
    """, (password_hash, data.user_id))
    
    conn.commit()
    cur.close()
    return {"success": True}

@api_router.get("/dashboard/participants")
async def get_all_participants(conn=Depends(get_db)):
    cur = conn.cursor()
    cur.execute("SELECT * FROM participants ORDER BY created_at DESC")
    results = cur.fetchall()
    cur.close()
    
    return [{
        "participant_id": r['participant_id'],
        "first_name": r['first_name'],
        "last_name": r['last_name'],
        "email": r['email'],
        "consent_given": r['consent_given'],
        "consent_timestamp": r['consent_timestamp'].isoformat() if r['consent_timestamp'] else None,
        "created_at": r['created_at'].isoformat() if r['created_at'] else None
    } for r in results]

@api_router.get("/dashboard/responses")
async def get_all_responses(conn=Depends(get_db)):
    cur = conn.cursor()
    cur.execute("SELECT * FROM survey_responses ORDER BY participant_id, question_number")
    results = cur.fetchall()
    cur.close()
    
    return [{
        "participant_id": r['participant_id'],
        "question_number": r['question_number'],
        "subsection": r['subsection'],
        "user_response": r['user_response'],
        "timestamp": r['timestamp'].isoformat() if r['timestamp'] else None
    } for r in results]

@api_router.get("/dashboard/scores", response_model=List[POQScores])
async def get_all_scores(conn=Depends(get_db)):
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT participant_id FROM survey_responses")
    participants = cur.fetchall()
    
    scores = []
    for p in participants:
        pid = p['participant_id']
        cur.execute("""
            SELECT question_number, user_response FROM survey_responses WHERE participant_id = %s
        """, (pid,))
        
        responses = {r['question_number']: r['user_response'] for r in cur.fetchall()}
        
        def calc_mean(items):
            vals = [responses.get(i) for i in items if i in responses]
            return round(sum(vals) / len(vals), 3) if vals else None
        
        territoriality = calc_mean([1, 2, 3, 4])
        self_efficacy = calc_mean([5, 6, 7])
        accountability = calc_mean([8, 9, 10])
        belongingness = calc_mean([11, 12, 13])
        self_identity = calc_mean([14, 15, 16])
        
        dims = [territoriality, self_efficacy, accountability, belongingness, self_identity]
        valid_dims = [d for d in dims if d is not None]
        overall_po = round(sum(valid_dims) / len(valid_dims), 3) if valid_dims else None
        
        scores.append({
            "participant_id": pid,
            "Territoriality": territoriality,
            "Self_Efficacy": self_efficacy,
            "Accountability": accountability,
            "Belongingness": belongingness,
            "Self_Identity": self_identity,
            "Overall_PO": overall_po
        })
    
    cur.close()
    return scores

@api_router.get("/dashboard/stats")
async def get_stats(conn=Depends(get_db)):
    cur = conn.cursor()
    
    cur.execute("SELECT COUNT(*) as count FROM participants")
    total_participants = cur.fetchone()['count']
    
    cur.execute("SELECT COUNT(*) as count FROM survey_responses")
    total_responses = cur.fetchone()['count']
    
    cur.execute("SELECT COUNT(*) as count FROM sessions WHERE end_time IS NOT NULL")
    completed_surveys = cur.fetchone()['count']
    
    cur.close()
    
    return {
        "total_participants": total_participants,
        "total_responses": total_responses,
        "completed_surveys": completed_surveys
    }

app.include_router(api_router)
