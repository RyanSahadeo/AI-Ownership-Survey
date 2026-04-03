#!/usr/bin/env python3
"""
Backend API Testing for POQ Survey Platform
Capitol Technology University Research Study
"""

import requests
import sys
import json
from datetime import datetime

class POQAPITester:
    def __init__(self, base_url="https://psych-ownership-ai.preview.emergentagent.com"):
        self.base_url = base_url
        self.token = None
        self.tests_run = 0
        self.tests_passed = 0
        self.participant_id = None
        self.session_id = None
        self.user_id = None

    def run_test(self, name, method, endpoint, expected_status, data=None, headers=None):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        test_headers = {'Content-Type': 'application/json'}
        if headers:
            test_headers.update(headers)
        if self.token:
            test_headers['Authorization'] = f'Bearer {self.token}'

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=test_headers, timeout=10)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=test_headers, timeout=10)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=test_headers, timeout=10)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    print(f"   Response: {json.dumps(response_data, indent=2)[:200]}...")
                    return True, response_data
                except:
                    return True, {}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data}")
                except:
                    print(f"   Error: {response.text}")
                return False, {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_health_endpoints(self):
        """Test basic health endpoints"""
        print("\n" + "="*50)
        print("TESTING HEALTH ENDPOINTS")
        print("="*50)
        
        self.run_test("API Root", "GET", "api/", 200)
        self.run_test("Health Check", "GET", "api/health", 200)

    def test_participant_registration(self):
        """Test participant registration flow"""
        print("\n" + "="*50)
        print("TESTING PARTICIPANT REGISTRATION")
        print("="*50)
        
        # Test participant creation
        participant_data = {
            "first_name": "Test",
            "last_name": "Participant",
            "email": f"test.participant.{datetime.now().strftime('%H%M%S')}@example.com",
            "consent_given": True
        }
        
        success, response = self.run_test(
            "Create Participant",
            "POST",
            "api/participants",
            200,
            data=participant_data
        )
        
        if success and 'participant_id' in response:
            self.participant_id = response['participant_id']
            print(f"   Generated Participant ID: {self.participant_id}")
            
            # Verify participant ID format (POQ-XXXXXXXX)
            if self.participant_id.startswith('POQ-') and len(self.participant_id) == 12:
                print("✅ Participant ID format is correct")
            else:
                print("❌ Participant ID format is incorrect")
        
        # Test duplicate email registration
        self.run_test(
            "Duplicate Email Registration",
            "POST",
            "api/participants",
            400,
            data=participant_data
        )
        
        # Test registration without consent
        no_consent_data = participant_data.copy()
        no_consent_data['consent_given'] = False
        self.run_test(
            "Registration Without Consent",
            "POST",
            "api/participants",
            400,
            data=no_consent_data
        )

    def test_session_management(self):
        """Test session creation and management"""
        print("\n" + "="*50)
        print("TESTING SESSION MANAGEMENT")
        print("="*50)
        
        if not self.participant_id:
            print("❌ No participant ID available for session testing")
            return
        
        # Create session
        session_data = {"participant_id": self.participant_id}
        success, response = self.run_test(
            "Create Session",
            "POST",
            "api/sessions",
            200,
            data=session_data
        )
        
        if success and 'session_id' in response:
            self.session_id = response['session_id']
            print(f"   Generated Session ID: {self.session_id}")
        
        # End session
        if self.session_id:
            end_data = {"session_id": self.session_id}
            self.run_test(
                "End Session",
                "POST",
                "api/sessions/end",
                200,
                data=end_data
            )

    def test_survey_responses(self):
        """Test survey response functionality"""
        print("\n" + "="*50)
        print("TESTING SURVEY RESPONSES")
        print("="*50)
        
        if not self.participant_id:
            print("❌ No participant ID available for response testing")
            return
        
        # Test saving responses for all 16 questions
        for question_num in range(1, 17):
            response_data = {
                "participant_id": self.participant_id,
                "question_number": question_num,
                "user_response": (question_num % 6) + 1  # Cycle through 1-6
            }
            
            self.run_test(
                f"Save Response Q{question_num}",
                "POST",
                "api/responses",
                200,
                data=response_data
            )
        
        # Test retrieving responses
        self.run_test(
            "Get Participant Responses",
            "GET",
            f"api/responses/{self.participant_id}",
            200
        )
        
        # Test invalid question number
        invalid_response = {
            "participant_id": self.participant_id,
            "question_number": 17,  # Invalid
            "user_response": 3
        }
        self.run_test(
            "Invalid Question Number",
            "POST",
            "api/responses",
            422,
            data=invalid_response
        )
        
        # Test invalid response value
        invalid_value = {
            "participant_id": self.participant_id,
            "question_number": 1,
            "user_response": 7  # Invalid (should be 1-6)
        }
        self.run_test(
            "Invalid Response Value",
            "POST",
            "api/responses",
            422,
            data=invalid_value
        )

    def test_investigator_authentication(self):
        """Test investigator login and authentication"""
        print("\n" + "="*50)
        print("TESTING INVESTIGATOR AUTHENTICATION")
        print("="*50)
        
        # Test valid login - Primary Investigator
        login_data = {
            "email": "givoykhansky@captechu.edu",
            "password": "CapitolTech2025!"
        }
        
        success, response = self.run_test(
            "Primary Investigator Login",
            "POST",
            "api/auth/login",
            200,
            data=login_data
        )
        
        if success and 'user' in response:
            user = response['user']
            self.user_id = user['id']
            print(f"   User ID: {user['id']}")
            print(f"   Username: {user['username']}")
            print(f"   Role: {user['role']}")
            print(f"   First Login: {user.get('first_login', 'N/A')}")
            
            # Verify role
            if user['role'] == 'primary_investigator':
                print("✅ Primary investigator role verified")
            else:
                print("❌ Incorrect role for primary investigator")
        
        # Test second primary investigator
        login_data2 = {
            "email": "ttroublefield@captechu.edu",
            "password": "CapitolTech2025!"
        }
        self.run_test(
            "Second Primary Investigator Login",
            "POST",
            "api/auth/login",
            200,
            data=login_data2
        )
        
        # Test platform designer
        login_data3 = {
            "email": "rsahadeo@captechu.edu",
            "password": "CapitolTech2025!"
        }
        success, response = self.run_test(
            "Platform Designer Login",
            "POST",
            "api/auth/login",
            200,
            data=login_data3
        )
        
        if success and 'user' in response:
            user = response['user']
            if user['role'] == 'platform_designer':
                print("✅ Platform designer role verified")
            else:
                print("❌ Incorrect role for platform designer")
        
        # Test invalid credentials
        invalid_login = {
            "email": "invalid@example.com",
            "password": "wrongpassword"
        }
        self.run_test(
            "Invalid Login",
            "POST",
            "api/auth/login",
            401,
            data=invalid_login
        )

    def test_password_change(self):
        """Test password change functionality"""
        print("\n" + "="*50)
        print("TESTING PASSWORD CHANGE")
        print("="*50)
        
        if not self.user_id:
            print("❌ No user ID available for password change testing")
            return
        
        # Test password change
        password_data = {
            "user_id": self.user_id,
            "new_password": "NewTestPassword123!"
        }
        
        self.run_test(
            "Change Password",
            "POST",
            "api/auth/change-password",
            200,
            data=password_data
        )

    def test_dashboard_endpoints(self):
        """Test dashboard data endpoints"""
        print("\n" + "="*50)
        print("TESTING DASHBOARD ENDPOINTS")
        print("="*50)
        
        # Test statistics
        success, stats = self.run_test(
            "Dashboard Statistics",
            "GET",
            "api/dashboard/stats",
            200
        )
        
        if success:
            print(f"   Total Participants: {stats.get('total_participants', 'N/A')}")
            print(f"   Total Responses: {stats.get('total_responses', 'N/A')}")
            print(f"   Completed Surveys: {stats.get('completed_surveys', 'N/A')}")
        
        # Test participants data
        self.run_test(
            "Dashboard Participants",
            "GET",
            "api/dashboard/participants",
            200
        )
        
        # Test responses data
        self.run_test(
            "Dashboard Responses",
            "GET",
            "api/dashboard/responses",
            200
        )
        
        # Test POQ scores
        success, scores = self.run_test(
            "Dashboard POQ Scores",
            "GET",
            "api/dashboard/scores",
            200
        )
        
        if success and scores:
            print(f"   Number of scored participants: {len(scores)}")
            if scores:
                sample_score = scores[0]
                print(f"   Sample score dimensions: {list(sample_score.keys())}")

def main():
    """Main test execution"""
    print("🧪 POQ Survey Platform API Testing")
    print("Capitol Technology University Research Study")
    print("="*60)
    
    tester = POQAPITester()
    
    # Run all test suites
    tester.test_health_endpoints()
    tester.test_participant_registration()
    tester.test_session_management()
    tester.test_survey_responses()
    tester.test_investigator_authentication()
    tester.test_password_change()
    tester.test_dashboard_endpoints()
    
    # Print final results
    print("\n" + "="*60)
    print("📊 FINAL TEST RESULTS")
    print("="*60)
    print(f"Tests Run: {tester.tests_run}")
    print(f"Tests Passed: {tester.tests_passed}")
    print(f"Tests Failed: {tester.tests_run - tester.tests_passed}")
    print(f"Success Rate: {(tester.tests_passed / tester.tests_run * 100):.1f}%")
    
    if tester.tests_passed == tester.tests_run:
        print("🎉 All tests passed!")
        return 0
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())