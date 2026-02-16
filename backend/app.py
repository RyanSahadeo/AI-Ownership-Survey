"""
Main Streamlit Application for POQ Survey Platform
Capitol Technology University Research Study

"Experimental Investigation of Psychological Ownership in AI-Human Interactions:
Comparative Analysis of AI Tool Types and Ownership Dynamics"
"""
import streamlit as st
import pandas as pd
import uuid
import io
from datetime import datetime, timezone
from pathlib import Path

# Import custom modules
from database import init_db, get_db_session, Participant, SurveyResponse, Session
from auth import authenticate_user, change_password, create_initial_investigators
from survey_data import SURVEY_QUESTIONS, RESPONSE_SCALE, CONSENT_FORM, get_subsection
from scoring import (
    calculate_dimension_scores, 
    get_all_scores_dataframe, 
    get_raw_responses_dataframe,
    get_participants_dataframe
)

# Page configuration
st.set_page_config(
    page_title="POQ Research Survey - Capitol Technology University",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    /* Main container styling */
    .main .block-container {
        padding-top: 2rem;
        max-width: 1200px;
    }
    
    /* Header styling */
    .header-container {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 1rem 0;
        margin-bottom: 2rem;
        border-bottom: 3px solid #c41230;
    }
    
    .header-logo {
        max-height: 80px;
        margin-right: 20px;
    }
    
    .header-title {
        color: #333;
        font-size: 1.5rem;
        font-weight: 600;
    }
    
    /* Consent form styling */
    .consent-box {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 20px;
        margin: 20px 0;
        max-height: 500px;
        overflow-y: auto;
    }
    
    /* Survey question styling */
    .question-card {
        background-color: #ffffff;
        border: 1px solid #e9ecef;
        border-radius: 8px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .question-number {
        color: #c41230;
        font-weight: 700;
        font-size: 1.1rem;
    }
    
    .subsection-badge {
        background-color: #c41230;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
    }
    
    /* Button styling */
    .stButton>button {
        background-color: #c41230;
        color: white;
        border: none;
        padding: 10px 30px;
        font-weight: 600;
        border-radius: 5px;
    }
    
    .stButton>button:hover {
        background-color: #a30f28;
    }
    
    /* Success/Error messages */
    .success-message {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    
    .error-message {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    
    /* Dashboard styling */
    .metric-card {
        background-color: #fff;
        border: 1px solid #e9ecef;
        border-radius: 8px;
        padding: 20px;
        text-align: center;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #c41230;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #6c757d;
        margin-top: 5px;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


def generate_participant_id() -> str:
    """Generate a unique participant ID"""
    return f"POQ-{uuid.uuid4().hex[:8].upper()}"


def show_header():
    """Display the application header with Capitol Technology University logo"""
    col1, col2 = st.columns([1, 4])
    with col1:
        st.image(
            "https://customer-assets.emergentagent.com/job_ownership-dynamics/artifacts/bp5fqhs8_capitol-logo--color.png",
            width=150
        )
    with col2:
        st.markdown("""
        ## Psychological Ownership Research Survey
        **Capitol Technology University**
        
        *Experimental Investigation of Psychological Ownership in AI-Human Interactions*
        """)
    st.markdown("---")


def registration_page():
    """Participant registration and consent page"""
    show_header()
    
    st.markdown("### Participant Registration")
    st.markdown("Please complete the registration form below to participate in this research study.")
    
    # Check if already registered in this session
    if st.session_state.get('registered', False):
        st.success("✅ You are already registered! Please proceed to the survey.")
        if st.button("Continue to Survey", key="continue_survey"):
            st.session_state.page = 'survey'
            st.rerun()
        return
    
    # Registration form
    with st.form("registration_form"):
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name *", placeholder="Enter your first name")
        with col2:
            last_name = st.text_input("Last Name *", placeholder="Enter your last name")
        
        email = st.text_input("Email Address *", placeholder="Enter your email address")
        
        st.markdown("---")
        st.markdown("### Informed Consent Form")
        st.markdown("Please read the following consent form carefully before agreeing to participate.")
        
        # Display consent form in a scrollable container
        st.markdown(f'<div class="consent-box">{CONSENT_FORM}</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### Eligibility Confirmation")
        
        consent = st.checkbox(
            "**I have read and understood the informed consent form above. I voluntarily agree to participate in this research study. I confirm that I am 18 years of age or older, a United States citizen or permanent resident, and have at least one (1) year of project management experience.**",
            key="consent_checkbox"
        )
        
        submitted = st.form_submit_button("Register and Begin Survey", use_container_width=True)
        
        if submitted:
            # Validation
            if not first_name or not last_name or not email:
                st.error("❌ Please fill in all required fields.")
                return
            
            if not consent:
                st.error("❌ You must agree to the consent form to participate in this study.")
                return
            
            if '@' not in email:
                st.error("❌ Please enter a valid email address.")
                return
            
            # Check if email already exists
            db = get_db_session()
            try:
                existing = db.query(Participant).filter(Participant.email == email).first()
                if existing:
                    st.error("❌ This email is already registered. Please use a different email or contact the research team.")
                    return
                
                # Create participant
                participant_id = generate_participant_id()
                new_participant = Participant(
                    participant_id=participant_id,
                    first_name=first_name.strip(),
                    last_name=last_name.strip(),
                    email=email.strip().lower(),
                    consent_given=True,
                    consent_timestamp=datetime.now(timezone.utc)
                )
                db.add(new_participant)
                
                # Create session record
                new_session = Session(
                    participant_id=participant_id,
                    start_time=datetime.now(timezone.utc)
                )
                db.add(new_session)
                
                db.commit()
                
                # Store in session state
                st.session_state.participant_id = participant_id
                st.session_state.session_id = new_session.id
                st.session_state.registered = True
                st.session_state.session_start = datetime.now(timezone.utc)
                st.session_state.page = 'survey'
                
                st.success(f"✅ Registration successful! Your Participant ID is: **{participant_id}**")
                st.rerun()
                
            except Exception as e:
                db.rollback()
                st.error(f"❌ Registration failed: {str(e)}")
            finally:
                db.close()


def survey_page():
    """Survey questions page"""
    show_header()
    
    if not st.session_state.get('registered', False):
        st.warning("⚠️ Please complete registration first.")
        if st.button("Go to Registration"):
            st.session_state.page = 'registration'
            st.rerun()
        return
    
    participant_id = st.session_state.participant_id
    
    st.markdown(f"### Survey Questions")
    st.markdown(f"**Participant ID:** {participant_id}")
    st.markdown("Please answer each question based on your experiences. Select one response per question using the scale from 1 (Strongly Disagree) to 6 (Strongly Agree).")
    
    # Initialize responses in session state
    if 'responses' not in st.session_state:
        st.session_state.responses = {}
    
    # Check for existing responses in database
    db = get_db_session()
    try:
        existing_responses = db.query(SurveyResponse).filter(
            SurveyResponse.participant_id == participant_id
        ).all()
        
        for resp in existing_responses:
            st.session_state.responses[resp.question_number] = resp.user_response
    finally:
        db.close()
    
    # Display survey questions
    st.markdown("---")
    
    current_subsection = None
    
    for question in SURVEY_QUESTIONS:
        q_num = question['number']
        q_text = question['text']
        q_subsection = question['subsection']
        
        # Display subsection header when it changes
        if q_subsection != current_subsection:
            current_subsection = q_subsection
            st.markdown(f"#### {q_subsection.replace('_', ' ')}")
        
        # Question card
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.markdown(f"**Q{q_num}.** {q_text}")
        
        with col2:
            # Get default value from session state or None
            default_idx = st.session_state.responses.get(q_num, None)
            if default_idx:
                default_idx = default_idx - 1  # Convert to 0-based index
            
            response = st.radio(
                f"Response for Q{q_num}",
                options=[1, 2, 3, 4, 5, 6],
                format_func=lambda x: f"{x} - {RESPONSE_SCALE[x]}",
                key=f"q_{q_num}",
                index=default_idx,
                horizontal=True,
                label_visibility="collapsed"
            )
            
            # Auto-save response
            if response and response != st.session_state.responses.get(q_num):
                db = get_db_session()
                try:
                    # Check if response exists
                    existing = db.query(SurveyResponse).filter(
                        SurveyResponse.participant_id == participant_id,
                        SurveyResponse.question_number == q_num
                    ).first()
                    
                    if existing:
                        existing.user_response = response
                        existing.timestamp = datetime.now(timezone.utc)
                    else:
                        new_response = SurveyResponse(
                            participant_id=participant_id,
                            question_number=q_num,
                            subsection=q_subsection,
                            user_response=response
                        )
                        db.add(new_response)
                    
                    db.commit()
                    st.session_state.responses[q_num] = response
                except Exception as e:
                    db.rollback()
                    st.error(f"Error saving response: {e}")
                finally:
                    db.close()
        
        st.markdown("---")
    
    # Submit button
    st.markdown("### Survey Completion")
    
    # Check if all questions answered
    answered = len(st.session_state.responses)
    total = len(SURVEY_QUESTIONS)
    
    progress = answered / total
    st.progress(progress)
    st.markdown(f"**Progress:** {answered}/{total} questions answered ({progress*100:.0f}%)")
    
    if answered == total:
        if st.button("Submit Survey", type="primary", use_container_width=True):
            # Update session end time
            db = get_db_session()
            try:
                session = db.query(Session).filter(
                    Session.id == st.session_state.session_id
                ).first()
                
                if session:
                    session.end_time = datetime.now(timezone.utc)
                    duration = (session.end_time - session.start_time).total_seconds()
                    session.session_duration_seconds = int(duration)
                    db.commit()
                
                st.session_state.page = 'complete'
                st.rerun()
            finally:
                db.close()
    else:
        st.info(f"📝 Please answer all {total} questions to submit the survey.")


def completion_page():
    """Survey completion page"""
    show_header()
    
    st.markdown("## 🎉 Survey Completed!")
    st.markdown("---")
    
    participant_id = st.session_state.get('participant_id', 'N/A')
    
    st.success(f"""
    **Thank you for participating in this research study!**
    
    Your responses have been securely recorded.
    
    **Participant ID:** {participant_id}
    
    Please save your Participant ID for your records. If you have any questions about the study, 
    please contact the research team:
    
    - **Dr. Greg I. Voykhansky** – givoykhansky@captechu.edu
    - **Dr. Troy C. Troublefield** – ttroublefield@captechu.edu
    """)
    
    # Calculate and display session duration
    if 'session_start' in st.session_state:
        duration = (datetime.now(timezone.utc) - st.session_state.session_start).total_seconds()
        minutes = int(duration // 60)
        seconds = int(duration % 60)
        st.info(f"⏱️ **Session Duration:** {minutes} minutes and {seconds} seconds")
    
    st.markdown("---")
    st.markdown("### What happens next?")
    st.markdown("""
    - Your responses will be analyzed as part of the research study
    - All data is stored securely and confidentially
    - Results will be aggregated and no individual responses will be identifiable in publications
    - Data will be retained for 3 years following study completion
    """)
    
    # Option to view scores (for demo purposes)
    if st.checkbox("View my POQ Scores (Optional)"):
        scores = calculate_dimension_scores(participant_id)
        if scores:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Territoriality", scores.get('Territoriality', 'N/A'))
                st.metric("Self Efficacy", scores.get('Self_Efficacy', 'N/A'))
            with col2:
                st.metric("Accountability", scores.get('Accountability', 'N/A'))
                st.metric("Belongingness", scores.get('Belongingness', 'N/A'))
            with col3:
                st.metric("Self Identity", scores.get('Self_Identity', 'N/A'))
                st.metric("Overall PO", scores.get('Overall_PO', 'N/A'))


def investigator_login():
    """Investigator login page"""
    show_header()
    
    st.markdown("### Investigator Login")
    st.markdown("Access restricted to authorized research personnel only.")
    
    with st.form("login_form"):
        email = st.text_input("Email Address", placeholder="Enter your email")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        submitted = st.form_submit_button("Login", use_container_width=True)
        
        if submitted:
            if not email or not password:
                st.error("Please enter both email and password.")
                return
            
            user = authenticate_user(email, password)
            
            if user:
                st.session_state.logged_in = True
                st.session_state.user = user
                
                # Check if first login - require password change
                if user['first_login']:
                    st.session_state.page = 'change_password'
                else:
                    st.session_state.page = 'dashboard'
                
                st.success(f"Welcome, {user['username']}!")
                st.rerun()
            else:
                st.error("Invalid email or password.")


def change_password_page():
    """Password change page for first-time login"""
    show_header()
    
    st.markdown("### Change Password Required")
    st.warning("⚠️ For security purposes, you must change your password on first login.")
    
    with st.form("change_password_form"):
        new_password = st.text_input("New Password", type="password", placeholder="Enter new password")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm new password")
        
        submitted = st.form_submit_button("Change Password", use_container_width=True)
        
        if submitted:
            if not new_password or not confirm_password:
                st.error("Please fill in both password fields.")
                return
            
            if new_password != confirm_password:
                st.error("Passwords do not match.")
                return
            
            if len(new_password) < 8:
                st.error("Password must be at least 8 characters long.")
                return
            
            # Change password
            user_id = st.session_state.user['id']
            if change_password(user_id, new_password):
                st.success("✅ Password changed successfully!")
                st.session_state.user['first_login'] = False
                st.session_state.page = 'dashboard'
                st.rerun()
            else:
                st.error("Failed to change password. Please try again.")


def dashboard_page():
    """Principal Investigator dashboard"""
    show_header()
    
    user = st.session_state.get('user', {})
    role = user.get('role', '')
    
    st.markdown(f"### Research Dashboard")
    st.markdown(f"**Logged in as:** {user.get('username', 'Unknown')} ({role.replace('_', ' ').title()})")
    
    # Logout button
    col1, col2 = st.columns([4, 1])
    with col2:
        if st.button("Logout", key="logout_btn"):
            for key in list(st.session_state.keys()):
                if key != 'page':
                    del st.session_state[key]
            st.session_state.page = 'login'
            st.rerun()
    
    st.markdown("---")
    
    # Dashboard tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "📋 Raw Responses", "📈 POQ Scores", "👥 Participants"])
    
    with tab1:
        # Overview metrics
        db = get_db_session()
        try:
            total_participants = db.query(Participant).count()
            total_responses = db.query(SurveyResponse).count()
            completed_surveys = db.query(Session).filter(Session.end_time.isnot(None)).count()
        finally:
            db.close()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Participants", total_participants)
        with col2:
            st.metric("Total Responses", total_responses)
        with col3:
            st.metric("Completed Surveys", completed_surveys)
        
        st.markdown("---")
        st.markdown("### Study Information")
        st.info("""
        **Study Title:** Experimental Investigation of Psychological Ownership in AI-Human Interactions
        
        **Principal Investigators:**
        - Dr. Greg I. Voykhansky
        - Dr. Troy C. Troublefield
        
        **Institution:** Capitol Technology University
        """)
    
    with tab2:
        st.markdown("### Raw Survey Responses")
        
        df_responses = get_raw_responses_dataframe()
        
        if not df_responses.empty:
            st.dataframe(df_responses, use_container_width=True)
            
            # Export button (only for primary_investigator)
            if role == 'primary_investigator':
                st.markdown("---")
                # Export to Excel
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                    df_responses.to_excel(writer, sheet_name='Raw_Responses', index=False)
                
                st.download_button(
                    label="📥 Export to Excel",
                    data=buffer.getvalue(),
                    file_name=f"raw_responses_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.info("📌 Export functionality is restricted to Primary Investigators.")
        else:
            st.info("No survey responses recorded yet.")
    
    with tab3:
        st.markdown("### POQ Dimension Scores")
        st.markdown("""
        Automated scoring for each participant across five dimensions:
        - **Territoriality** (Items 1-4)
        - **Self_Efficacy** (Items 5-7)
        - **Accountability** (Items 8-10)
        - **Belongingness** (Items 11-13)
        - **Self_Identity** (Items 14-16)
        - **Overall_PO** (Mean of all five dimensions)
        """)
        
        df_scores = get_all_scores_dataframe()
        
        if not df_scores.empty:
            st.dataframe(df_scores, use_container_width=True)
            
            # Statistics
            st.markdown("---")
            st.markdown("### Descriptive Statistics")
            
            numeric_cols = ['Territoriality', 'Self_Efficacy', 'Accountability', 'Belongingness', 'Self_Identity', 'Overall_PO']
            stats_df = df_scores[numeric_cols].describe()
            st.dataframe(stats_df, use_container_width=True)
            
            # Export button (only for primary_investigator)
            if role == 'primary_investigator':
                st.markdown("---")
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                    df_scores.to_excel(writer, sheet_name='POQ_Scores', index=False)
                    stats_df.to_excel(writer, sheet_name='Statistics')
                
                st.download_button(
                    label="📥 Export Scores to Excel",
                    data=buffer.getvalue(),
                    file_name=f"poq_scores_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.info("📌 Export functionality is restricted to Primary Investigators.")
        else:
            st.info("No scores available yet.")
    
    with tab4:
        st.markdown("### Registered Participants")
        
        df_participants = get_participants_dataframe()
        
        if not df_participants.empty:
            # Hide sensitive info for platform_designer
            if role != 'primary_investigator':
                df_display = df_participants[['participant_id', 'consent_given', 'consent_timestamp', 'created_at']]
                st.info("📌 Personal information (names, emails) is restricted to Primary Investigators.")
            else:
                df_display = df_participants
            
            st.dataframe(df_display, use_container_width=True)
            
            # Export button (only for primary_investigator)
            if role == 'primary_investigator':
                st.markdown("---")
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                    df_participants.to_excel(writer, sheet_name='Participants', index=False)
                
                st.download_button(
                    label="📥 Export Participants to Excel",
                    data=buffer.getvalue(),
                    file_name=f"participants_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        else:
            st.info("No participants registered yet.")


def main():
    """Main application entry point"""
    # Initialize database
    init_db()
    
    # Create initial investigators if they don't exist
    create_initial_investigators()
    
    # Initialize session state
    if 'page' not in st.session_state:
        st.session_state.page = 'home'
    
    # Sidebar navigation
    with st.sidebar:
        st.image(
            "https://customer-assets.emergentagent.com/job_ownership-dynamics/artifacts/bp5fqhs8_capitol-logo--color.png",
            width=200
        )
        st.markdown("---")
        st.markdown("### Navigation")
        
        if st.button("🏠 Home / Registration", use_container_width=True):
            st.session_state.page = 'registration'
            st.rerun()
        
        if st.session_state.get('registered', False):
            if st.button("📝 Survey", use_container_width=True):
                st.session_state.page = 'survey'
                st.rerun()
        
        st.markdown("---")
        st.markdown("### Investigator Access")
        
        if st.session_state.get('logged_in', False):
            if st.button("📊 Dashboard", use_container_width=True):
                st.session_state.page = 'dashboard'
                st.rerun()
            if st.button("🚪 Logout", use_container_width=True):
                for key in ['logged_in', 'user']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.session_state.page = 'login'
                st.rerun()
        else:
            if st.button("🔐 Investigator Login", use_container_width=True):
                st.session_state.page = 'login'
                st.rerun()
        
        st.markdown("---")
        st.markdown("### About")
        st.markdown("""
        **Capitol Technology University**
        
        IRB-Approved Research Study
        
        Data retained for 3 years
        following study completion.
        """)
    
    # Page routing
    page = st.session_state.page
    
    if page == 'home' or page == 'registration':
        registration_page()
    elif page == 'survey':
        survey_page()
    elif page == 'complete':
        completion_page()
    elif page == 'login':
        investigator_login()
    elif page == 'change_password':
        change_password_page()
    elif page == 'dashboard':
        if st.session_state.get('logged_in', False):
            dashboard_page()
        else:
            investigator_login()
    else:
        registration_page()


if __name__ == "__main__":
    main()
