"""
Authentication utilities for POQ Survey Platform
Capitol Technology University Research Study
"""
import bcrypt
import os
from datetime import datetime, timezone
from database import Investigator, get_db_session


def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a password against its hash"""
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))


def authenticate_user(email: str, password: str):
    """Authenticate a user and return user info if successful"""
    db = get_db_session()
    try:
        user = db.query(Investigator).filter(Investigator.email == email).first()
        if user and verify_password(password, user.password_hash):
            # Update last login time
            user.last_login = datetime.now(timezone.utc)
            db.commit()
            return {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role,
                'first_login': user.first_login,
                'password_changed': user.password_changed
            }
        return None
    finally:
        db.close()


def change_password(user_id: int, new_password: str) -> bool:
    """Change user password and mark as changed"""
    db = get_db_session()
    try:
        user = db.query(Investigator).filter(Investigator.id == user_id).first()
        if user:
            user.password_hash = hash_password(new_password)
            user.first_login = False
            user.password_changed = True
            db.commit()
            return True
        return False
    finally:
        db.close()


def create_initial_investigators():
    """Create initial investigator accounts if they don't exist"""
    db = get_db_session()
    try:
        investigators = [
            {
                'username': 'Dr. Greg I. Voykhansky',
                'email': 'givoykhansky@captechu.edu',
                'password': 'CapitolTech2025!',
                'role': 'primary_investigator'
            },
            {
                'username': 'Dr. Troy C. Troublefield',
                'email': 'ttroublefield@captechu.edu',
                'password': 'CapitolTech2025!',
                'role': 'primary_investigator'
            },
            {
                'username': 'Ryan Sahadeo',
                'email': 'rsahadeo@captechu.edu',
                'password': 'CapitolTech2025!',
                'role': 'platform_designer'
            }
        ]
        
        for inv in investigators:
            existing = db.query(Investigator).filter(Investigator.email == inv['email']).first()
            if not existing:
                new_investigator = Investigator(
                    username=inv['username'],
                    email=inv['email'],
                    password_hash=hash_password(inv['password']),
                    role=inv['role'],
                    first_login=True,
                    password_changed=False
                )
                db.add(new_investigator)
        
        db.commit()
        print("Initial investigators created successfully")
    except Exception as e:
        db.rollback()
        print(f"Error creating investigators: {e}")
    finally:
        db.close()
