"""
POQ Scoring Calculator for Survey Platform
Capitol Technology University Research Study
"""
import pandas as pd
from database import get_db_session, SurveyResponse, Participant


def calculate_dimension_scores(participant_id: str) -> dict:
    """
    Calculate POQ dimension scores for a participant.
    
    Dimensions:
    - Territoriality: Items 1-4
    - Self_Efficacy: Items 5-7
    - Accountability: Items 8-10
    - Belongingness: Items 11-13
    - Self_Identity: Items 14-16
    - Overall_PO: Mean of all five dimensions
    """
    db = get_db_session()
    try:
        responses = db.query(SurveyResponse).filter(
            SurveyResponse.participant_id == participant_id
        ).all()
        
        if not responses:
            return None
        
        # Organize responses by question number
        response_dict = {r.question_number: r.user_response for r in responses}
        
        # Calculate dimension means
        territoriality_items = [response_dict.get(i) for i in [1, 2, 3, 4] if i in response_dict]
        self_efficacy_items = [response_dict.get(i) for i in [5, 6, 7] if i in response_dict]
        accountability_items = [response_dict.get(i) for i in [8, 9, 10] if i in response_dict]
        belongingness_items = [response_dict.get(i) for i in [11, 12, 13] if i in response_dict]
        self_identity_items = [response_dict.get(i) for i in [14, 15, 16] if i in response_dict]
        
        def safe_mean(items):
            valid_items = [i for i in items if i is not None]
            return sum(valid_items) / len(valid_items) if valid_items else None
        
        territoriality = safe_mean(territoriality_items)
        self_efficacy = safe_mean(self_efficacy_items)
        accountability = safe_mean(accountability_items)
        belongingness = safe_mean(belongingness_items)
        self_identity = safe_mean(self_identity_items)
        
        # Calculate Overall_PO as mean of all five dimensions
        dimension_scores = [territoriality, self_efficacy, accountability, belongingness, self_identity]
        valid_dimensions = [d for d in dimension_scores if d is not None]
        overall_po = sum(valid_dimensions) / len(valid_dimensions) if valid_dimensions else None
        
        return {
            'participant_id': participant_id,
            'Territoriality': round(territoriality, 3) if territoriality else None,
            'Self_Efficacy': round(self_efficacy, 3) if self_efficacy else None,
            'Accountability': round(accountability, 3) if accountability else None,
            'Belongingness': round(belongingness, 3) if belongingness else None,
            'Self_Identity': round(self_identity, 3) if self_identity else None,
            'Overall_PO': round(overall_po, 3) if overall_po else None
        }
    finally:
        db.close()


def get_all_scores_dataframe() -> pd.DataFrame:
    """Get POQ scores for all participants as a DataFrame"""
    db = get_db_session()
    try:
        participants = db.query(Participant).all()
        
        all_scores = []
        for p in participants:
            scores = calculate_dimension_scores(p.participant_id)
            if scores:
                all_scores.append(scores)
        
        if not all_scores:
            return pd.DataFrame()
        
        return pd.DataFrame(all_scores)
    finally:
        db.close()


def get_raw_responses_dataframe() -> pd.DataFrame:
    """Get all raw survey responses as a DataFrame"""
    db = get_db_session()
    try:
        responses = db.query(
            SurveyResponse.participant_id,
            SurveyResponse.question_number,
            SurveyResponse.subsection,
            SurveyResponse.user_response,
            SurveyResponse.timestamp
        ).all()
        
        if not responses:
            return pd.DataFrame()
        
        data = [{
            'participant_id': r.participant_id,
            'question_number': r.question_number,
            'subsection': r.subsection,
            'user_response': r.user_response,
            'timestamp': r.timestamp.isoformat() if r.timestamp else None
        } for r in responses]
        
        return pd.DataFrame(data)
    finally:
        db.close()


def get_participants_dataframe() -> pd.DataFrame:
    """Get all participants as a DataFrame"""
    db = get_db_session()
    try:
        participants = db.query(Participant).all()
        
        if not participants:
            return pd.DataFrame()
        
        data = [{
            'participant_id': p.participant_id,
            'first_name': p.first_name,
            'last_name': p.last_name,
            'email': p.email,
            'consent_given': p.consent_given,
            'consent_timestamp': p.consent_timestamp.isoformat() if p.consent_timestamp else None,
            'created_at': p.created_at.isoformat() if p.created_at else None
        } for p in participants]
        
        return pd.DataFrame(data)
    finally:
        db.close()
