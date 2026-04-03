import React, { useState, useEffect } from 'react';
import './App.css';

const LOGO_URL = "https://customer-assets.emergentagent.com/job_ownership-dynamics/artifacts/bp5fqhs8_capitol-logo--color.png";
const API_URL = process.env.REACT_APP_BACKEND_URL || '';

// Survey Questions
const QUESTIONS = [
  { number: 1, text: "I feel I need to protect my ideas from being used by others in my organization.", subsection: "Territoriality" },
  { number: 2, text: "I feel that people I work with in my organization should not invade my workspace.", subsection: "Territoriality" },
  { number: 3, text: "I feel I need to protect my property from being used by others in this organization.", subsection: "Territoriality" },
  { number: 4, text: "I feel I have to tell people in my organization to 'back off' from projects that are mine.", subsection: "Territoriality" },
  { number: 5, text: "I am confident in my ability to contribute to my organization's success.", subsection: "Self Efficacy" },
  { number: 6, text: "I am confident I can make a positive difference in this organization.", subsection: "Self Efficacy" },
  { number: 7, text: "I am confident setting high performance goals in my organization.", subsection: "Self Efficacy" },
  { number: 8, text: "I would challenge anyone in my organization if I thought something was done wrong.", subsection: "Accountability" },
  { number: 9, text: "I would not hesitate to tell my organization if I saw something that was done wrong.", subsection: "Accountability" },
  { number: 10, text: "I would challenge the direction of my organization to assure it's correct.", subsection: "Accountability" },
  { number: 11, text: "I feel I belong in this organization.", subsection: "Belongingness" },
  { number: 12, text: "This place is home for me.", subsection: "Belongingness" },
  { number: 13, text: "I am totally comfortable being in this organization.", subsection: "Belongingness" },
  { number: 14, text: "I feel this organization's success is my success.", subsection: "Self Identity" },
  { number: 15, text: "I feel being a member in this organization helps define who I am.", subsection: "Self Identity" },
  { number: 16, text: "I feel the need to defend my organization when it is criticized.", subsection: "Self Identity" }
];

const SCALE = [
  { value: 1, label: "Strongly Disagree" },
  { value: 2, label: "Disagree" },
  { value: 3, label: "Somewhat Disagree" },
  { value: 4, label: "Somewhat Agree" },
  { value: 5, label: "Agree" },
  { value: 6, label: "Strongly Agree" }
];

// Header Component
function Header() {
  return (
    <header className="header" data-testid="header">
      <img src={LOGO_URL} alt="Capitol Technology University" className="logo" />
      <div className="header-text">
        <h1>Psychological Ownership Research Survey</h1>
      </div>
    </header>
  );
}

// Consent Form Component
function ConsentForm({ onAccept }) {
  const [agreed, setAgreed] = useState(false);

  return (
    <div className="consent-form" data-testid="consent-form">
      <h2>Informed Consent Form</h2>
      <div className="consent-content">
        <p>You have been invited to participate in an online survey entitled <strong>"Experimental Investigation of Psychological Ownership in AI-Human Interactions: Comparative Analysis of AI Tool Types and Ownership Dynamics"</strong>. This online survey supports a research project undertaken by Dr. Greg I. Voykhansky and Dr. Troy C. Troublefield at Capitol Technology University.</p>
        
        <h3>VOLUNTARY INVITATION TO PARTICIPATE</h3>
        <p>You are invited to participate in an academic research project examining psychological ownership in task-based collaborations between humans and artificial intelligence (AI) systems. This project is being conducted by Dr. Greg I. Voykhansky and Dr. Troy C. Troublefield as part of an approved research project at Capitol Technology University.</p>
        <p>Your participation is requested because you have professional familiarity with project management tasks and workflows, which are central to the experimental scenarios used in this research. Participation in this study is entirely voluntary. You may decline to participate, discontinue participation at any time, or skip any question you do not wish to answer without penalty or loss of benefits to which you are otherwise entitled.</p>
        
        <h3>PURPOSE OF THE STUDY</h3>
        <p>The purpose of this study is to investigate how different types of AI tools (e.g., rule-based, adaptive, explainable, generative, and human-in-the-loop systems) influence individuals' perceptions of psychological ownership during collaborative task performance. Psychological ownership refers to feelings of control, responsibility, identity, and personal investment in work outcomes. Findings from this study aim to contribute to the academic literature on human–AI collaboration and inform the ethical and organizational design of AI-enabled systems.</p>
        
        <h3>STUDY PROCEDURES</h3>
        <p>If you agree to participate, you will be asked to complete an online study consisting of:</p>
        <ul>
          <li>Interaction with one AI system configured under a specific experimental condition</li>
          <li>Completion of approximately 20 survey questions related to your experience</li>
          <li>Optional short, open-ended responses reflecting on perceived control, responsibility, and engagement</li>
        </ul>
        <p>Your total participation time is expected to be approximately <strong>10 to 20 minutes</strong>. All activities will be completed remotely via a secure web-based platform.</p>
        
        <h3>BENEFITS</h3>
        <p>There is no direct compensation or personal benefit for participating in this study. However, your participation may contribute to:</p>
        <ul>
          <li>Improved understanding of psychological ownership in AI-assisted work environments</li>
          <li>Evidence-based guidance for ethical AI system design</li>
          <li>Advancements in research related to human–AI collaboration and organizational behavior</li>
        </ul>
        
        <h3>RISKS</h3>
        <p>This study involves <strong>minimal risk</strong>. No foreseeable physical, psychological, legal, or professional risks are anticipated beyond those encountered in everyday online task activities. Should you experience discomfort, you may withdraw from the study at any time.</p>
        
        <h3>CONFIDENTIALITY AND DATA SECURITY</h3>
        <p>All data collected in this study will be treated as confidential and handled in accordance with U.S. data protection standards and institutional research ethics requirements.</p>
        <ul>
          <li>Survey responses and system interaction data will be stored in a password-protected PostgreSQL database hosted on a secure cloud infrastructure.</li>
          <li>Access to raw data is restricted to the investigators and protected through multi-factor authentication.</li>
          <li>Identifying information (first name, last name, and email address) may be collected at sign-up for study administration purposes but will be anonymized immediately through assignment of a unique participant identification number.</li>
          <li>No personally identifiable information will be linked to published results or shared outside the research team.</li>
        </ul>
        <p>All research data will be retained for <strong>three (3) years</strong> following completion of the study and then permanently deleted.</p>
        
        <h3>CONTACT INFORMATION</h3>
        <p>If you have questions about the study, procedures, or your rights as a participant, you may contact:</p>
        <ul>
          <li>Dr. Greg I. Voykhansky – givoykhansky@captechu.edu</li>
          <li>Dr. Troy C. Troublefield – ttroublefield@captechu.edu</li>
        </ul>
        <p>If you feel you have not been treated according to the descriptions above, or that your participation rights have not been honored, you may contact Capitol Technology University's Institutional Review Board at <strong>irb@captechu.edu</strong>.</p>
        <p>If you have any questions, concerns, or complaints, that you wish to address to someone other than the primary investigator, you may contact the university at:</p>
        <address>
          11301 Springfield Road<br />
          Laurel, MD, 20708<br />
          +1 (800)-950-1992<br />
          +1 (301)-369-2800<br />
          <a href="https://www.captechu.edu/" target="_blank" rel="noopener noreferrer">https://www.captechu.edu/</a><br />
          <a href="https://www.linkedin.com/school/captechu/" target="_blank" rel="noopener noreferrer">https://www.linkedin.com/school/captechu/</a>
        </address>
        
        <h3>ELECTRONIC CONSENT</h3>
        <p>You may print or save a copy of this consent form for your records.</p>
        <p><strong>By checking the box below and clicking Submit, you acknowledge that:</strong></p>
        <ul>
          <li>You have read and understood the information provided above.</li>
          <li>You voluntarily agree to participate in this research study.</li>
          <li>You are 18 years of age or older and are a United States citizen or permanent resident.</li>
          <li>You are a working project management professional with at least one (1) year of relevant experience.</li>
        </ul>
      </div>
      
      <div className="consent-checkbox">
        <label>
          <input 
            type="checkbox" 
            checked={agreed} 
            onChange={(e) => setAgreed(e.target.checked)}
            data-testid="consent-checkbox"
          />
          <span>I have read and understood the informed consent form above. I voluntarily agree to participate in this research study and confirm I meet all eligibility requirements.</span>
        </label>
      </div>
      
      <button 
        className="btn-primary" 
        disabled={!agreed} 
        onClick={onAccept}
        data-testid="consent-accept-btn"
      >
        Accept and Continue
      </button>
    </div>
  );
}

// Registration Form Component
function RegistrationForm({ onRegister }) {
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/api/participants`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          first_name: firstName,
          last_name: lastName,
          email: email,
          consent_given: true
        })
      });

      const data = await response.json();
      
      if (response.ok) {
        // Create session
        await fetch(`${API_URL}/api/sessions`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ participant_id: data.participant_id })
        });
        
        onRegister(data);
      } else {
        setError(data.detail || 'Registration failed');
      }
    } catch (err) {
      setError('Connection error. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className="registration-form" onSubmit={handleSubmit} data-testid="registration-form">
      <h2>Participant Registration</h2>
      
      {error && <div className="error-message" data-testid="error-message">{error}</div>}
      
      <div className="form-group">
        <label>First Name *</label>
        <input 
          type="text" 
          value={firstName} 
          onChange={(e) => setFirstName(e.target.value)}
          required
          data-testid="first-name-input"
        />
      </div>
      
      <div className="form-group">
        <label>Last Name *</label>
        <input 
          type="text" 
          value={lastName} 
          onChange={(e) => setLastName(e.target.value)}
          required
          data-testid="last-name-input"
        />
      </div>
      
      <div className="form-group">
        <label>Email Address *</label>
        <input 
          type="email" 
          value={email} 
          onChange={(e) => setEmail(e.target.value)}
          required
          data-testid="email-input"
        />
      </div>
      
      <button type="submit" className="btn-primary" disabled={loading} data-testid="register-btn">
        {loading ? 'Registering...' : 'Begin Survey'}
      </button>
    </form>
  );
}

// Survey Component
function Survey({ participant, onComplete }) {
  const [responses, setResponses] = useState({});
  const [saving, setSaving] = useState({});

  const handleResponse = async (questionNumber, value) => {
    setResponses(prev => ({ ...prev, [questionNumber]: value }));
    setSaving(prev => ({ ...prev, [questionNumber]: true }));

    try {
      await fetch(`${API_URL}/api/responses`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          participant_id: participant.participant_id,
          question_number: questionNumber,
          user_response: value
        })
      });
    } catch (err) {
      console.error('Failed to save response:', err);
    } finally {
      setSaving(prev => ({ ...prev, [questionNumber]: false }));
    }
  };

  const answeredCount = Object.keys(responses).length;
  const isComplete = answeredCount === 16;

  let currentSubsection = '';

  return (
    <div className="survey" data-testid="survey">
      <div className="survey-header">
        <h2>Psychological Ownership Questionnaire</h2>
        <p>Participant ID: <strong>{participant.participant_id}</strong></p>
        <div className="progress-bar">
          <div className="progress-fill" style={{ width: `${(answeredCount / 16) * 100}%` }}></div>
        </div>
        <p className="progress-text">{answeredCount} of 16 questions answered</p>
      </div>

      <div className="questions">
        {QUESTIONS.map((q) => {
          const showHeader = q.subsection !== currentSubsection;
          if (showHeader) currentSubsection = q.subsection;

          return (
            <React.Fragment key={q.number}>
              {showHeader && <h3 className="subsection-header">{q.subsection}</h3>}
              <div className="question-card" data-testid={`question-${q.number}`}>
                <div className="question-text">
                  <span className="question-number">Q{q.number}.</span> {q.text}
                </div>
                <div className="response-options">
                  {SCALE.map((s) => (
                    <label key={s.value} className={`option ${responses[q.number] === s.value ? 'selected' : ''}`}>
                      <input
                        type="radio"
                        name={`q${q.number}`}
                        value={s.value}
                        checked={responses[q.number] === s.value}
                        onChange={() => handleResponse(q.number, s.value)}
                        data-testid={`q${q.number}-option-${s.value}`}
                      />
                      <span className="option-value">{s.value}</span>
                      <span className="option-label">{s.label}</span>
                    </label>
                  ))}
                </div>
                {saving[q.number] && <span className="saving">Saving...</span>}
              </div>
            </React.Fragment>
          );
        })}
      </div>

      <div className="survey-submit">
        <button 
          className="btn-primary btn-large" 
          disabled={!isComplete}
          onClick={onComplete}
          data-testid="submit-survey-btn"
        >
          {isComplete ? 'Submit Survey' : `Answer all questions (${16 - answeredCount} remaining)`}
        </button>
      </div>
    </div>
  );
}

// Completion Component
function Completion({ participant }) {
  return (
    <div className="completion" data-testid="completion">
      <div className="completion-icon">✓</div>
      <h2>Survey Completed!</h2>
      <p>Thank you for participating in this research study.</p>
      <div className="completion-details">
        <p><strong>Participant ID:</strong> {participant.participant_id}</p>
        <p>Please save this ID for your records.</p>
      </div>
      <div className="completion-contact">
        <h3>Questions?</h3>
        <p>Contact the research team:</p>
        <ul>
          <li>Dr. Greg I. Voykhansky – givoykhansky@captechu.edu</li>
          <li>Dr. Troy C. Troublefield – ttroublefield@captechu.edu</li>
        </ul>
      </div>
    </div>
  );
}

// Login Component
function Login({ onLogin }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/api/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });

      const data = await response.json();
      
      if (response.ok) {
        onLogin(data.user);
      } else {
        setError(data.detail || 'Invalid credentials');
      }
    } catch (err) {
      setError('Connection error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className="login-form" onSubmit={handleSubmit} data-testid="login-form">
      <h2>Investigator Login</h2>
      {error && <div className="error-message">{error}</div>}
      
      <div className="form-group">
        <label>Email</label>
        <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required data-testid="login-email" />
      </div>
      
      <div className="form-group">
        <label>Password</label>
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required data-testid="login-password" />
      </div>
      
      <button type="submit" className="btn-primary" disabled={loading} data-testid="login-btn">
        {loading ? 'Logging in...' : 'Login'}
      </button>
    </form>
  );
}

// Password Change Component
function PasswordChange({ user, onChanged }) {
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (newPassword !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }
    if (newPassword.length < 8) {
      setError('Password must be at least 8 characters');
      return;
    }

    try {
      const response = await fetch(`${API_URL}/api/auth/change-password`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: user.id, new_password: newPassword })
      });

      if (response.ok) {
        onChanged();
      } else {
        setError('Failed to change password');
      }
    } catch (err) {
      setError('Connection error');
    }
  };

  return (
    <form className="password-form" onSubmit={handleSubmit} data-testid="password-change-form">
      <h2>Change Password Required</h2>
      <p>For security, please change your password on first login.</p>
      {error && <div className="error-message">{error}</div>}
      
      <div className="form-group">
        <label>New Password</label>
        <input type="password" value={newPassword} onChange={(e) => setNewPassword(e.target.value)} required />
      </div>
      
      <div className="form-group">
        <label>Confirm Password</label>
        <input type="password" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} required />
      </div>
      
      <button type="submit" className="btn-primary">Change Password</button>
    </form>
  );
}

// Dashboard Component
function Dashboard({ user, onLogout }) {
  const [activeTab, setActiveTab] = useState('overview');
  const [stats, setStats] = useState({ total_participants: 0, total_responses: 0, completed_surveys: 0 });
  const [participants, setParticipants] = useState([]);
  const [responses, setResponses] = useState([]);
  const [scores, setScores] = useState([]);
  const [deleteConfirm, setDeleteConfirm] = useState(null);
  const [deleting, setDeleting] = useState(false);

  const fetchData = useCallback(async () => {
    try {
      const [statsRes, participantsRes, responsesRes, scoresRes] = await Promise.all([
        fetch(`${API_URL}/api/dashboard/stats`),
        fetch(`${API_URL}/api/dashboard/participants`),
        fetch(`${API_URL}/api/dashboard/responses`),
        fetch(`${API_URL}/api/dashboard/scores`)
      ]);

      setStats(await statsRes.json());
      setParticipants(await participantsRes.json());
      setResponses(await responsesRes.json());
      setScores(await scoresRes.json());
    } catch (err) {
      console.error('Failed to fetch dashboard data:', err);
    }
  }, []);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  const handleDeleteParticipant = async (participantId) => {
    setDeleting(true);
    try {
      const response = await fetch(`${API_URL}/api/dashboard/participants/${participantId}`, {
        method: 'DELETE'
      });
      
      if (response.ok) {
        // Refresh all data after deletion
        await fetchData();
        setDeleteConfirm(null);
      } else {
        alert('Failed to delete participant');
      }
    } catch (err) {
      console.error('Delete error:', err);
      alert('Error deleting participant');
    } finally {
      setDeleting(false);
    }
  };

  const exportToCSV = (data, filename) => {
    if (!data.length) return;
    const headers = Object.keys(data[0]);
    const csv = [headers.join(','), ...data.map(row => headers.map(h => `"${row[h] || ''}"`).join(','))].join('\n');
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
  };

  const canExport = user.role === 'primary_investigator';

  return (
    <div className="dashboard" data-testid="dashboard">
      <div className="dashboard-header">
        <h2>Research Dashboard</h2>
        <div className="user-info">
          <span>{user.username} ({user.role.replace('_', ' ')})</span>
          <button className="btn-secondary" onClick={onLogout} data-testid="logout-btn">Logout</button>
        </div>
      </div>

      <div className="dashboard-tabs">
        {['overview', 'responses', 'scores', 'participants'].map(tab => (
          <button
            key={tab}
            className={`tab ${activeTab === tab ? 'active' : ''}`}
            onClick={() => setActiveTab(tab)}
            data-testid={`tab-${tab}`}
          >
            {tab.charAt(0).toUpperCase() + tab.slice(1)}
          </button>
        ))}
      </div>

      <div className="dashboard-content">
        {activeTab === 'overview' && (
          <div className="overview" data-testid="overview-tab">
            <div className="stats-grid">
              <div className="stat-card">
                <div className="stat-value">{stats.total_participants}</div>
                <div className="stat-label">Total Participants</div>
              </div>
              <div className="stat-card">
                <div className="stat-value">{stats.total_responses}</div>
                <div className="stat-label">Total Responses</div>
              </div>
              <div className="stat-card">
                <div className="stat-value">{stats.completed_surveys}</div>
                <div className="stat-label">Completed Surveys</div>
              </div>
            </div>
            <div className="study-info">
              <h3>Study Information</h3>
              <p><strong>Title:</strong> Experimental Investigation of Psychological Ownership in AI-Human Interactions</p>
              <p><strong>Principal Investigators:</strong> Dr. Greg I. Voykhansky, Dr. Troy C. Troublefield</p>
              <p><strong>Institution:</strong> Capitol Technology University</p>
            </div>
          </div>
        )}

        {activeTab === 'responses' && (
          <div className="responses-tab" data-testid="responses-tab">
            <div className="table-header">
              <h3>Raw Survey Responses</h3>
              {canExport && (
                <button className="btn-secondary" onClick={() => exportToCSV(responses, 'responses.csv')} data-testid="export-responses-btn">
                  Export CSV
                </button>
              )}
            </div>
            <div className="table-container">
              <table>
                <thead>
                  <tr>
                    <th>Participant ID</th>
                    <th>Question #</th>
                    <th>Subsection</th>
                    <th>Response</th>
                    <th>Timestamp</th>
                  </tr>
                </thead>
                <tbody>
                  {responses.map((r, i) => (
                    <tr key={`${r.participant_id}-${r.question_number}`}>
                      <td>{r.participant_id}</td>
                      <td>{r.question_number}</td>
                      <td>{r.subsection}</td>
                      <td>{r.user_response}</td>
                      <td>{r.timestamp ? new Date(r.timestamp).toLocaleString() : ''}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            {!canExport && <p className="export-notice">Export functionality is restricted to Primary Investigators.</p>}
          </div>
        )}

        {activeTab === 'scores' && (
          <div className="scores-tab" data-testid="scores-tab">
            <div className="table-header">
              <h3>POQ Dimension Scores</h3>
              {canExport && (
                <button className="btn-secondary" onClick={() => exportToCSV(scores, 'scores.csv')} data-testid="export-scores-btn">
                  Export CSV
                </button>
              )}
            </div>
            <div className="table-container">
              <table>
                <thead>
                  <tr>
                    <th>Participant ID</th>
                    <th>Territoriality</th>
                    <th>Self Efficacy</th>
                    <th>Accountability</th>
                    <th>Belongingness</th>
                    <th>Self Identity</th>
                    <th>Overall PO</th>
                  </tr>
                </thead>
                <tbody>
                  {scores.map((s, i) => (
                    <tr key={s.participant_id}>
                      <td>{s.participant_id}</td>
                      <td>{s.Territoriality?.toFixed(2) || '-'}</td>
                      <td>{s.Self_Efficacy?.toFixed(2) || '-'}</td>
                      <td>{s.Accountability?.toFixed(2) || '-'}</td>
                      <td>{s.Belongingness?.toFixed(2) || '-'}</td>
                      <td>{s.Self_Identity?.toFixed(2) || '-'}</td>
                      <td><strong>{s.Overall_PO?.toFixed(2) || '-'}</strong></td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            {!canExport && <p className="export-notice">Export functionality is restricted to Primary Investigators.</p>}
          </div>
        )}

        {activeTab === 'participants' && (
          <div className="participants-tab" data-testid="participants-tab">
            <div className="table-header">
              <h3>Registered Participants</h3>
              {canExport && (
                <button className="btn-secondary" onClick={() => exportToCSV(participants, 'participants.csv')} data-testid="export-participants-btn">
                  Export CSV
                </button>
              )}
            </div>
            <div className="table-container">
              <table>
                <thead>
                  <tr>
                    <th>Participant ID</th>
                    {canExport && <th>Name</th>}
                    {canExport && <th>Email</th>}
                    <th>Consent</th>
                    <th>Registered</th>
                    {canExport && <th>Actions</th>}
                  </tr>
                </thead>
                <tbody>
                  {participants.map((p, i) => (
                    <tr key={p.participant_id}>
                      <td>{p.participant_id}</td>
                      {canExport && <td>{p.first_name} {p.last_name}</td>}
                      {canExport && <td>{p.email}</td>}
                      <td>{p.consent_given ? '✓' : '✗'}</td>
                      <td>{p.created_at ? new Date(p.created_at).toLocaleString() : ''}</td>
                      {canExport && (
                        <td>
                          <button 
                            className="btn-delete" 
                            onClick={() => setDeleteConfirm(p.participant_id)}
                            data-testid={`delete-${p.participant_id}`}
                          >
                            Delete
                          </button>
                        </td>
                      )}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            {!canExport && <p className="export-notice">Personal information and delete actions are restricted to Primary Investigators.</p>}
            
            {/* Delete Confirmation Modal */}
            {deleteConfirm && (
              <div className="modal-overlay" data-testid="delete-modal">
                <div className="modal-content">
                  <h3>Confirm Deletion</h3>
                  <p>Are you sure you want to delete participant <strong>{deleteConfirm}</strong>?</p>
                  <p className="warning-text">This will permanently remove:</p>
                  <ul>
                    <li>Participant registration data</li>
                    <li>All survey responses</li>
                    <li>Session tracking data</li>
                  </ul>
                  <p className="warning-text"><strong>This action cannot be undone.</strong></p>
                  <div className="modal-actions">
                    <button 
                      className="btn-secondary" 
                      onClick={() => setDeleteConfirm(null)}
                      disabled={deleting}
                    >
                      Cancel
                    </button>
                    <button 
                      className="btn-delete-confirm" 
                      onClick={() => handleDeleteParticipant(deleteConfirm)}
                      disabled={deleting}
                      data-testid="confirm-delete-btn"
                    >
                      {deleting ? 'Deleting...' : 'Delete Permanently'}
                    </button>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

// Main App Component
function App() {
  const [view, setView] = useState('consent'); // consent, register, survey, complete, login, password, dashboard
  const [participant, setParticipant] = useState(null);
  const [user, setUser] = useState(null);
  const [sessionId, setSessionId] = useState(null);

  const handleConsentAccept = () => setView('register');
  
  const handleRegister = async (data) => {
    setParticipant(data);
    // Get session ID
    try {
      const res = await fetch(`${API_URL}/api/sessions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ participant_id: data.participant_id })
      });
      const session = await res.json();
      setSessionId(session.session_id);
    } catch (error) {
      console.error('Failed to create session:', error);
    }
    setView('survey');
  };
  
  const handleSurveyComplete = async () => {
    if (sessionId) {
      try {
        await fetch(`${API_URL}/api/sessions/end`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ session_id: sessionId })
        });
      } catch (error) {
        console.error('Failed to end session:', error);
      }
    }
    setView('complete');
  };

  const handleLogin = (userData) => {
    setUser(userData);
    if (userData.first_login) {
      setView('password');
    } else {
      setView('dashboard');
    }
  };

  const handlePasswordChanged = () => {
    setUser(prev => ({ ...prev, first_login: false }));
    setView('dashboard');
  };

  const handleLogout = () => {
    setUser(null);
    setView('consent');
  };

  return (
    <div className="app">
      <Header />
      
      <nav className="nav">
        <button 
          className={view === 'consent' || view === 'register' || view === 'survey' || view === 'complete' ? 'active' : ''}
          onClick={() => setView('consent')}
          data-testid="nav-survey"
        >
          Survey
        </button>
        <button 
          className={view === 'login' || view === 'password' || view === 'dashboard' ? 'active' : ''}
          onClick={() => setView(user ? 'dashboard' : 'login')}
          data-testid="nav-investigator"
        >
          Investigator Access
        </button>
      </nav>

      <main className="main-content">
        {view === 'consent' && <ConsentForm onAccept={handleConsentAccept} />}
        {view === 'register' && <RegistrationForm onRegister={handleRegister} />}
        {view === 'survey' && participant && <Survey participant={participant} onComplete={handleSurveyComplete} />}
        {view === 'complete' && participant && <Completion participant={participant} />}
        {view === 'login' && <Login onLogin={handleLogin} />}
        {view === 'password' && user && <PasswordChange user={user} onChanged={handlePasswordChanged} />}
        {view === 'dashboard' && user && <Dashboard user={user} onLogout={handleLogout} />}
      </main>

      <footer className="footer">
        <p>© {new Date().getFullYear()} Capitol Technology University. IRB-Approved Research Study.</p>
        <p>Data retained for 3 years following study completion.</p>
      </footer>
    </div>
  );
}

export default App;
