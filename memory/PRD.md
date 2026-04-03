# POQ Survey Platform - Product Requirements Document

## Study Information
**Title:** Experimental Investigation of Psychological Ownership in AI-Human Interactions: Comparative Analysis of AI Tool Types and Ownership Dynamics

**Institution:** Capitol Technology University

**Principal Investigators:**
- Dr. Greg I. Voykhansky (givoykhansky@captechu.edu)
- Dr. Troy C. Troublefield (ttroublefield@captechu.edu)

**Platform Designer:** Ryan Sahadeo (rsahadeo@captechu.edu)

---

## User Personas
1. **Participants** - Project management professionals (18+, US citizen/resident, 1+ year PM experience)
2. **Primary Investigators** - Full dashboard access and data export capabilities
3. **Platform Designer** - View-only dashboard access, no export capability

---

## Core Requirements (Static)
- IRB-approved informed consent form with mandatory checkbox
- Participant registration (first name, last name, email)
- Unique Participant ID generation (POQ-XXXXXXXX)
- 16-question Psychological Ownership Questionnaire (POQ)
- 1-6 Likert scale responses (Strongly Disagree → Strongly Agree)
- Auto-save survey responses
- Session tracking (start/end time, duration)
- Role-based access control
- POQ scoring by dimension
- Data export (CSV) for primary investigators only
- 3-year data retention policy

---

## What's Been Implemented ✅

### Date: March 16, 2026

**Backend (FastAPI + MongoDB):**
- Participant registration with consent validation
- Survey response storage with auto-save (upsert)
- Session creation and completion tracking
- Authentication with bcrypt password hashing
- Password change on first login requirement
- Dashboard endpoints (stats, participants, responses, scores)
- POQ dimension scoring calculations

**Frontend (React):**
- Capitol Technology University branding with logo
- Full IRB consent form with mandatory checkbox
- Registration form with validation
- 16-question survey with progress bar
- Response options (1-6 scale with labels)
- Subsection headers (Territoriality, Self-Efficacy, Accountability, Belongingness, Self-Identity)
- Survey completion page with participant ID display
- Investigator login portal
- Password change form
- Research dashboard with tabs:
  - Overview (statistics)
  - Raw Responses table
  - POQ Scores table
  - Participants table
- CSV export functionality (primary investigators only)
- Role-based UI restrictions

**Survey Questions (POQ):**
1-4: Territoriality
5-7: Self-Efficacy  
8-10: Accountability
11-13: Belongingness
14-16: Self-Identity

**POQ Scoring:**
- Dimension means calculated per participant
- Overall_PO = mean of all five dimensions

---

## Prioritized Backlog

### P0 (Critical) - COMPLETED
- [x] Consent form with checkbox
- [x] Participant registration
- [x] Survey implementation
- [x] Session tracking
- [x] Authentication system
- [x] Dashboard with scoring

### P0.5 (Completed - April 3, 2026)
- [x] Added survey instructions with 5 experimental conditions table above questionnaire

### P1 (Important)
- [ ] Excel export (currently CSV only)
- [ ] PostgreSQL migration for AWS RDS deployment
- [ ] SSL database connections
- [ ] AWS Secrets Manager integration

### P2 (Enhancement)
- [ ] Audit logging
- [ ] Login rate limiting
- [ ] Multi-factor authentication
- [ ] Automated backup system
- [ ] CloudWatch integration

---

## Investigator Credentials
| Username | Email | Role | Default Password |
|----------|-------|------|------------------|
| Dr. Greg I. Voykhansky | givoykhansky@captechu.edu | primary_investigator | CapitolTech2025! |
| Dr. Troy C. Troublefield | ttroublefield@captechu.edu | primary_investigator | CapitolTech2025! |
| Ryan Sahadeo | rsahadeo@captechu.edu | platform_designer | CapitolTech2025! |

*Note: Password change required on first login*

---

## Technical Architecture
- **Frontend:** React 18, CSS3
- **Backend:** FastAPI (Python 3.11+)
- **Database:** MongoDB (AWS RDS PostgreSQL compatible schema available)
- **Authentication:** bcrypt password hashing
- **Deployment:** AWS-ready (EC2/Elastic Beanstalk + RDS)

---

## Data Retention
All research data retained for 3 years following study completion, then permanently deleted per IRB requirements.
