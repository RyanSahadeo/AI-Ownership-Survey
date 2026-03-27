"""
FastAPI Backend for POQ Survey Platform
Capitol Technology University Research Study
Using MongoDB for data storage
"""
from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime, timezone
import uuid
import bcrypt
import os
from dotenv import load_dotenv
from pathlib import Path
from motor.motor_asyncio import AsyncIOMotorClient

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

# MongoDB connection
mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
db_name = os.environ.get('DB_NAME', 'poq_survey')
client = AsyncIOMotorClient(mongo_url)
db = client[db_name]

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
    session_id: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class PasswordChangeRequest(BaseModel):
    user_id: str
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

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))

@app.on_event("startup")
async def startup():
    """Initialize investigators on startup"""
    default_password = os.environ.get('DEFAULT_INVESTIGATOR_PASSWORD', 'ChangeMe123!')
    investigators = [
        {'username': 'Dr. Greg I. Voykhansky', 'email': 'givoykhansky@captechu.edu', 'password': default_password, 'role': 'primary_investigator'},
        {'username': 'Dr. Troy C. Troublefield', 'email': 'ttroublefield@captechu.edu', 'password': default_password, 'role': 'primary_investigator'},
        {'username': 'Ryan Sahadeo', 'email': 'rsahadeo@captechu.edu', 'password': default_password, 'role': 'platform_designer'}
    ]
    
    for inv in investigators:
        existing = await db.investigators.find_one({'email': inv['email']})
        if not existing:
            await db.investigators.insert_one({
                'id': str(uuid.uuid4()),
                'username': inv['username'],
                'email': inv['email'],
                'password_hash': hash_password(inv['password']),
                'role': inv['role'],
                'first_login': True,
                'password_changed': False,
                'created_at': datetime.now(timezone.utc).isoformat()
            })

@app.on_event("shutdown")
async def shutdown():
    client.close()

# API Routes
@api_router.get("/")
async def root():
    return {"message": "POQ Survey Platform API", "status": "running"}

@api_router.get("/health")
async def health():
    return {"status": "healthy"}

@api_router.post("/participants", response_model=ParticipantResponse)
async def create_participant(data: ParticipantCreate):
    if not data.consent_given:
        raise HTTPException(status_code=400, detail="Consent must be given to participate")
    
    existing = await db.participants.find_one({'email': data.email.lower().strip()})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    participant_id = f"POQ-{uuid.uuid4().hex[:8].upper()}"
    now = datetime.now(timezone.utc)
    
    participant = {
        'participant_id': participant_id,
        'first_name': data.first_name.strip(),
        'last_name': data.last_name.strip(),
        'email': data.email.lower().strip(),
        'consent_given': True,
        'consent_timestamp': now.isoformat(),
        'created_at': now.isoformat()
    }
    
    await db.participants.insert_one(participant)
    
    return {
        'participant_id': participant_id,
        'first_name': participant['first_name'],
        'last_name': participant['last_name'],
        'email': participant['email'],
        'consent_given': participant['consent_given'],
        'consent_timestamp': participant['consent_timestamp'],
        'created_at': participant['created_at']
    }

@api_router.post("/responses")
async def save_response(data: SurveyResponseCreate):
    subsection = SUBSECTION_MAP.get(data.question_number, "Unknown")
    
    await db.survey_responses.update_one(
        {'participant_id': data.participant_id, 'question_number': data.question_number},
        {'$set': {
            'participant_id': data.participant_id,
            'question_number': data.question_number,
            'subsection': subsection,
            'user_response': data.user_response,
            'timestamp': datetime.now(timezone.utc).isoformat()
        }},
        upsert=True
    )
    
    return {"success": True, "question_number": data.question_number}

@api_router.get("/responses/{participant_id}")
async def get_responses(participant_id: str):
    responses = await db.survey_responses.find(
        {'participant_id': participant_id},
        {'_id': 0}
    ).sort('question_number', 1).to_list(100)
    
    return responses

@api_router.post("/sessions")
async def create_session(data: SessionCreate):
    session_id = str(uuid.uuid4())
    
    await db.sessions.insert_one({
        'session_id': session_id,
        'participant_id': data.participant_id,
        'start_time': datetime.now(timezone.utc).isoformat(),
        'end_time': None,
        'session_duration_seconds': None
    })
    
    return {"session_id": session_id}

@api_router.post("/sessions/end")
async def end_session(data: SessionEnd):
    session = await db.sessions.find_one({'session_id': data.session_id})
    
    if session:
        end_time = datetime.now(timezone.utc)
        start_time = datetime.fromisoformat(session['start_time'])
        duration = int((end_time - start_time).total_seconds())
        
        await db.sessions.update_one(
            {'session_id': data.session_id},
            {'$set': {
                'end_time': end_time.isoformat(),
                'session_duration_seconds': duration
            }}
        )
        
        return {"success": True, "duration_seconds": duration}
    
    return {"success": False, "duration_seconds": 0}

@api_router.post("/auth/login")
async def login(data: LoginRequest):
    user = await db.investigators.find_one({'email': data.email.lower()})
    
    if user and verify_password(data.password, user['password_hash']):
        await db.investigators.update_one(
            {'email': data.email.lower()},
            {'$set': {'last_login': datetime.now(timezone.utc).isoformat()}}
        )
        
        return {
            "success": True,
            "user": {
                "id": user['id'],
                "username": user['username'],
                "email": user['email'],
                "role": user['role'],
                "first_login": user.get('first_login', True),
                "password_changed": user.get('password_changed', False)
            }
        }
    
    raise HTTPException(status_code=401, detail="Invalid credentials")

@api_router.post("/auth/change-password")
async def change_password(data: PasswordChangeRequest):
    password_hash = hash_password(data.new_password)
    
    await db.investigators.update_one(
        {'id': data.user_id},
        {'$set': {
            'password_hash': password_hash,
            'first_login': False,
            'password_changed': True
        }}
    )
    
    return {"success": True}

@api_router.get("/dashboard/participants")
async def get_all_participants():
    participants = await db.participants.find({}, {'_id': 0}).sort('created_at', -1).to_list(1000)
    return participants

@api_router.get("/dashboard/responses")
async def get_all_responses():
    responses = await db.survey_responses.find({}, {'_id': 0}).sort([('participant_id', 1), ('question_number', 1)]).to_list(10000)
    return responses

@api_router.get("/dashboard/scores")
async def get_all_scores():
    # Get unique participant IDs
    participant_ids = await db.survey_responses.distinct('participant_id')
    
    scores = []
    for pid in participant_ids:
        responses = await db.survey_responses.find({'participant_id': pid}, {'_id': 0}).to_list(20)
        response_dict = {r['question_number']: r['user_response'] for r in responses}
        
        def calc_mean(items):
            vals = [response_dict.get(i) for i in items if i in response_dict]
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
    
    return scores

@api_router.get("/dashboard/stats")
async def get_stats():
    total_participants = await db.participants.count_documents({})
    total_responses = await db.survey_responses.count_documents({})
    completed_surveys = await db.sessions.count_documents({'end_time': {'$ne': None}})
    
    return {
        "total_participants": total_participants,
        "total_responses": total_responses,
        "completed_surveys": completed_surveys
    }

@api_router.delete("/dashboard/participants/{participant_id}")
async def delete_participant(participant_id: str, user_role: str = ""):
    """
    Delete a participant and all associated data (responses, sessions).
    Only primary_investigator role can perform this action.
    """
    # Verify the participant exists
    participant = await db.participants.find_one({'participant_id': participant_id})
    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found")
    
    # Delete all associated survey responses
    deleted_responses = await db.survey_responses.delete_many({'participant_id': participant_id})
    
    # Delete all associated sessions
    deleted_sessions = await db.sessions.delete_many({'participant_id': participant_id})
    
    # Delete the participant
    await db.participants.delete_one({'participant_id': participant_id})
    
    return {
        "success": True,
        "deleted_participant": participant_id,
        "deleted_responses_count": deleted_responses.deleted_count,
        "deleted_sessions_count": deleted_sessions.deleted_count
    }

app.include_router(api_router)
