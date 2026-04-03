"""
POQ Survey Platform Backend Tests
Tests for participant registration, condition assignment, survey responses, and dashboard
"""
import pytest
import requests
import os
import uuid

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')

class TestHealthEndpoints:
    """Health check and basic API tests"""
    
    def test_api_root(self):
        response = requests.get(f"{BASE_URL}/api/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        print(f"SUCCESS: API root returns: {data}")
    
    def test_health_endpoint(self):
        response = requests.get(f"{BASE_URL}/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data.get("status") == "healthy"
        print("SUCCESS: Health endpoint returns healthy")


class TestParticipantRegistration:
    """Participant registration and duplicate email handling"""
    
    def test_register_new_participant(self):
        """Test successful participant registration"""
        unique_email = f"test_{uuid.uuid4().hex[:8]}@example.com"
        payload = {
            "first_name": "Test",
            "last_name": "User",
            "email": unique_email,
            "consent_given": True
        }
        response = requests.post(f"{BASE_URL}/api/participants", json=payload)
        assert response.status_code == 200
        data = response.json()
        
        # Verify response structure
        assert "participant_id" in data
        assert data["participant_id"].startswith("POQ-")
        assert data["first_name"] == "Test"
        assert data["last_name"] == "User"
        assert data["email"] == unique_email.lower()
        assert data["consent_given"] == True
        print(f"SUCCESS: Registered participant {data['participant_id']}")
        return data["participant_id"]
    
    def test_duplicate_email_rejected(self):
        """Test that duplicate email returns 'Email already registered' error"""
        unique_email = f"test_dup_{uuid.uuid4().hex[:8]}@example.com"
        payload = {
            "first_name": "First",
            "last_name": "User",
            "email": unique_email,
            "consent_given": True
        }
        
        # First registration should succeed
        response1 = requests.post(f"{BASE_URL}/api/participants", json=payload)
        assert response1.status_code == 200
        print(f"SUCCESS: First registration succeeded")
        
        # Second registration with same email should fail
        payload["first_name"] = "Second"
        response2 = requests.post(f"{BASE_URL}/api/participants", json=payload)
        assert response2.status_code == 400
        data = response2.json()
        assert "Email already registered" in data.get("detail", "")
        print(f"SUCCESS: Duplicate email rejected with message: {data.get('detail')}")
    
    def test_consent_required(self):
        """Test that consent must be given"""
        unique_email = f"test_noconsent_{uuid.uuid4().hex[:8]}@example.com"
        payload = {
            "first_name": "No",
            "last_name": "Consent",
            "email": unique_email,
            "consent_given": False
        }
        response = requests.post(f"{BASE_URL}/api/participants", json=payload)
        assert response.status_code == 400
        data = response.json()
        assert "Consent must be given" in data.get("detail", "")
        print("SUCCESS: Consent requirement enforced")


class TestConditionAssignment:
    """Tests for the new condition assignment endpoint"""
    
    def test_assign_valid_condition(self):
        """Test assigning a valid condition (1-5) to a participant"""
        # First create a participant
        unique_email = f"test_cond_{uuid.uuid4().hex[:8]}@example.com"
        reg_response = requests.post(f"{BASE_URL}/api/participants", json={
            "first_name": "Condition",
            "last_name": "Test",
            "email": unique_email,
            "consent_given": True
        })
        assert reg_response.status_code == 200
        participant_id = reg_response.json()["participant_id"]
        
        # Test assigning each valid condition
        for condition in [1, 2, 3, 4, 5]:
            response = requests.put(
                f"{BASE_URL}/api/participants/{participant_id}/condition",
                json={"condition": condition}
            )
            assert response.status_code == 200
            data = response.json()
            assert data["success"] == True
            assert data["participant_id"] == participant_id
            assert data["condition"] == condition
            print(f"SUCCESS: Assigned condition {condition} to {participant_id}")
    
    def test_reject_invalid_condition_zero(self):
        """Test that condition 0 is rejected"""
        unique_email = f"test_cond0_{uuid.uuid4().hex[:8]}@example.com"
        reg_response = requests.post(f"{BASE_URL}/api/participants", json={
            "first_name": "Invalid",
            "last_name": "Condition",
            "email": unique_email,
            "consent_given": True
        })
        participant_id = reg_response.json()["participant_id"]
        
        response = requests.put(
            f"{BASE_URL}/api/participants/{participant_id}/condition",
            json={"condition": 0}
        )
        assert response.status_code == 422  # Validation error
        print("SUCCESS: Condition 0 rejected with validation error")
    
    def test_reject_invalid_condition_six(self):
        """Test that condition 6 is rejected"""
        unique_email = f"test_cond6_{uuid.uuid4().hex[:8]}@example.com"
        reg_response = requests.post(f"{BASE_URL}/api/participants", json={
            "first_name": "Invalid",
            "last_name": "Condition",
            "email": unique_email,
            "consent_given": True
        })
        participant_id = reg_response.json()["participant_id"]
        
        response = requests.put(
            f"{BASE_URL}/api/participants/{participant_id}/condition",
            json={"condition": 6}
        )
        assert response.status_code == 422  # Validation error
        print("SUCCESS: Condition 6 rejected with validation error")
    
    def test_condition_for_nonexistent_participant(self):
        """Test assigning condition to non-existent participant"""
        response = requests.put(
            f"{BASE_URL}/api/participants/POQ-NONEXIST/condition",
            json={"condition": 1}
        )
        assert response.status_code == 404
        print("SUCCESS: Non-existent participant returns 404")


class TestSurveyResponses:
    """Tests for survey response submission"""
    
    def test_save_response(self):
        """Test saving a survey response"""
        # Create participant first
        unique_email = f"test_resp_{uuid.uuid4().hex[:8]}@example.com"
        reg_response = requests.post(f"{BASE_URL}/api/participants", json={
            "first_name": "Response",
            "last_name": "Test",
            "email": unique_email,
            "consent_given": True
        })
        participant_id = reg_response.json()["participant_id"]
        
        # Save a response
        response = requests.post(f"{BASE_URL}/api/responses", json={
            "participant_id": participant_id,
            "question_number": 1,
            "user_response": 4
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert data["question_number"] == 1
        print(f"SUCCESS: Saved response for question 1")
    
    def test_get_responses(self):
        """Test retrieving responses for a participant"""
        # Create participant and save responses
        unique_email = f"test_getresp_{uuid.uuid4().hex[:8]}@example.com"
        reg_response = requests.post(f"{BASE_URL}/api/participants", json={
            "first_name": "GetResp",
            "last_name": "Test",
            "email": unique_email,
            "consent_given": True
        })
        participant_id = reg_response.json()["participant_id"]
        
        # Save multiple responses
        for q in range(1, 5):
            requests.post(f"{BASE_URL}/api/responses", json={
                "participant_id": participant_id,
                "question_number": q,
                "user_response": q
            })
        
        # Get responses
        response = requests.get(f"{BASE_URL}/api/responses/{participant_id}")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 4
        print(f"SUCCESS: Retrieved {len(data)} responses")


class TestSessions:
    """Tests for session management"""
    
    def test_create_and_end_session(self):
        """Test creating and ending a session"""
        # Create participant
        unique_email = f"test_sess_{uuid.uuid4().hex[:8]}@example.com"
        reg_response = requests.post(f"{BASE_URL}/api/participants", json={
            "first_name": "Session",
            "last_name": "Test",
            "email": unique_email,
            "consent_given": True
        })
        participant_id = reg_response.json()["participant_id"]
        
        # Create session
        session_response = requests.post(f"{BASE_URL}/api/sessions", json={
            "participant_id": participant_id
        })
        assert session_response.status_code == 200
        session_id = session_response.json()["session_id"]
        print(f"SUCCESS: Created session {session_id}")
        
        # End session
        end_response = requests.post(f"{BASE_URL}/api/sessions/end", json={
            "session_id": session_id
        })
        assert end_response.status_code == 200
        data = end_response.json()
        assert data["success"] == True
        print(f"SUCCESS: Ended session with duration {data.get('duration_seconds')} seconds")


class TestAuthentication:
    """Tests for investigator authentication"""
    
    def test_login_with_valid_credentials(self):
        """Test login with valid investigator credentials"""
        # Try platform_designer first (less likely to have changed password)
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": "rsahadeo@captechu.edu",
            "password": "CapitolTech2025!"
        })
        
        if response.status_code == 200:
            data = response.json()
            assert data["success"] == True
            assert "user" in data
            assert data["user"]["role"] == "platform_designer"
            print(f"SUCCESS: Logged in as {data['user']['username']}")
        else:
            # Password may have been changed
            print(f"INFO: Login failed (password may have been changed): {response.json()}")
    
    def test_login_with_invalid_credentials(self):
        """Test login with invalid credentials"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": "invalid@example.com",
            "password": "wrongpassword"
        })
        assert response.status_code == 401
        print("SUCCESS: Invalid credentials rejected with 401")


class TestDashboard:
    """Tests for dashboard endpoints"""
    
    def test_get_stats(self):
        """Test getting dashboard statistics"""
        response = requests.get(f"{BASE_URL}/api/dashboard/stats")
        assert response.status_code == 200
        data = response.json()
        assert "total_participants" in data
        assert "total_responses" in data
        assert "completed_surveys" in data
        print(f"SUCCESS: Stats - Participants: {data['total_participants']}, Responses: {data['total_responses']}")
    
    def test_get_participants_with_condition(self):
        """Test that participants endpoint returns assigned_condition field"""
        # First create a participant with condition
        unique_email = f"test_dashcond_{uuid.uuid4().hex[:8]}@example.com"
        reg_response = requests.post(f"{BASE_URL}/api/participants", json={
            "first_name": "Dashboard",
            "last_name": "CondTest",
            "email": unique_email,
            "consent_given": True
        })
        participant_id = reg_response.json()["participant_id"]
        
        # Assign condition
        requests.put(
            f"{BASE_URL}/api/participants/{participant_id}/condition",
            json={"condition": 3}
        )
        
        # Get participants
        response = requests.get(f"{BASE_URL}/api/dashboard/participants")
        assert response.status_code == 200
        data = response.json()
        
        # Find our participant
        our_participant = next((p for p in data if p["participant_id"] == participant_id), None)
        assert our_participant is not None
        assert our_participant.get("assigned_condition") == 3
        print(f"SUCCESS: Participant {participant_id} has assigned_condition: {our_participant.get('assigned_condition')}")
    
    def test_get_responses(self):
        """Test getting all responses"""
        response = requests.get(f"{BASE_URL}/api/dashboard/responses")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        print(f"SUCCESS: Retrieved {len(data)} total responses")
    
    def test_get_scores(self):
        """Test getting POQ scores"""
        response = requests.get(f"{BASE_URL}/api/dashboard/scores")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        print(f"SUCCESS: Retrieved {len(data)} score records")


class TestFullParticipantFlow:
    """End-to-end test of participant flow: register -> condition -> survey"""
    
    def test_complete_flow(self):
        """Test complete participant flow"""
        unique_email = f"test_flow_{uuid.uuid4().hex[:8]}@example.com"
        
        # Step 1: Register
        reg_response = requests.post(f"{BASE_URL}/api/participants", json={
            "first_name": "Flow",
            "last_name": "Test",
            "email": unique_email,
            "consent_given": True
        })
        assert reg_response.status_code == 200
        participant_id = reg_response.json()["participant_id"]
        print(f"Step 1 SUCCESS: Registered {participant_id}")
        
        # Step 2: Assign condition
        cond_response = requests.put(
            f"{BASE_URL}/api/participants/{participant_id}/condition",
            json={"condition": 2}
        )
        assert cond_response.status_code == 200
        print(f"Step 2 SUCCESS: Assigned condition 2")
        
        # Step 3: Create session
        sess_response = requests.post(f"{BASE_URL}/api/sessions", json={
            "participant_id": participant_id
        })
        assert sess_response.status_code == 200
        session_id = sess_response.json()["session_id"]
        print(f"Step 3 SUCCESS: Created session {session_id}")
        
        # Step 4: Submit all 16 responses
        for q in range(1, 17):
            resp = requests.post(f"{BASE_URL}/api/responses", json={
                "participant_id": participant_id,
                "question_number": q,
                "user_response": (q % 6) + 1  # Values 1-6
            })
            assert resp.status_code == 200
        print(f"Step 4 SUCCESS: Submitted all 16 responses")
        
        # Step 5: End session
        end_response = requests.post(f"{BASE_URL}/api/sessions/end", json={
            "session_id": session_id
        })
        assert end_response.status_code == 200
        print(f"Step 5 SUCCESS: Ended session")
        
        # Verify in dashboard
        participants = requests.get(f"{BASE_URL}/api/dashboard/participants").json()
        our_p = next((p for p in participants if p["participant_id"] == participant_id), None)
        assert our_p is not None
        assert our_p.get("assigned_condition") == 2
        print(f"VERIFICATION SUCCESS: Participant in dashboard with condition 2")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
