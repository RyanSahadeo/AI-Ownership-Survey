"""
Survey Questions and Data for POQ Survey Platform
Capitol Technology University Research Study
"""

# Response scale options
RESPONSE_SCALE = {
    1: "Strongly Disagree",
    2: "Disagree",
    3: "Somewhat Disagree",
    4: "Somewhat Agree",
    5: "Agree",
    6: "Strongly Agree"
}

# Subsection mappings
SUBSECTION_MAPPING = {
    1: "Territoriality",
    2: "Territoriality",
    3: "Territoriality",
    4: "Territoriality",
    5: "Self_Efficacy",
    6: "Self_Efficacy",
    7: "Self_Efficacy",
    8: "Accountability",
    9: "Accountability",
    10: "Accountability",
    11: "Belongingness",
    12: "Belongingness",
    13: "Belongingness",
    14: "Self_Identity",
    15: "Self_Identity",
    16: "Self_Identity"
}

# Survey questions
SURVEY_QUESTIONS = [
    {
        "number": 1,
        "text": "I feel I need to protect my ideas from being used by others in my organization.",
        "subsection": "Territoriality"
    },
    {
        "number": 2,
        "text": "I feel that people I work with in my organization should not invade my workspace.",
        "subsection": "Territoriality"
    },
    {
        "number": 3,
        "text": "I feel I need to protect my property from being used by others in this organization.",
        "subsection": "Territoriality"
    },
    {
        "number": 4,
        "text": "I feel I have to tell people in my organization to 'back off' from projects that are mine.",
        "subsection": "Territoriality"
    },
    {
        "number": 5,
        "text": "I am confident in my ability to contribute to my organization's success.",
        "subsection": "Self_Efficacy"
    },
    {
        "number": 6,
        "text": "I am confident I can make a positive difference in this organization.",
        "subsection": "Self_Efficacy"
    },
    {
        "number": 7,
        "text": "I am confident setting high performance goals in my organization.",
        "subsection": "Self_Efficacy"
    },
    {
        "number": 8,
        "text": "I would challenge anyone in my organization if I thought something was done wrong.",
        "subsection": "Accountability"
    },
    {
        "number": 9,
        "text": "I would not hesitate to tell my organization if I saw something that was done wrong.",
        "subsection": "Accountability"
    },
    {
        "number": 10,
        "text": "I would challenge the direction of my organization to assure it's correct.",
        "subsection": "Accountability"
    },
    {
        "number": 11,
        "text": "I feel I belong in this organization.",
        "subsection": "Belongingness"
    },
    {
        "number": 12,
        "text": "This place is home for me.",
        "subsection": "Belongingness"
    },
    {
        "number": 13,
        "text": "I am totally comfortable being in this organization.",
        "subsection": "Belongingness"
    },
    {
        "number": 14,
        "text": "I feel this organization's success is my success.",
        "subsection": "Self_Identity"
    },
    {
        "number": 15,
        "text": "I feel being a member in this organization helps define who I am.",
        "subsection": "Self_Identity"
    },
    {
        "number": 16,
        "text": "I feel the need to defend my organization when it is criticized.",
        "subsection": "Self_Identity"
    }
]

# IRB Consent Form Text
CONSENT_FORM = """
## Informed Consent Form

You have been invited to participate in an online survey entitled **"Experimental Investigation of Psychological Ownership in AI-Human Interactions: Comparative Analysis of AI Tool Types and Ownership Dynamics"**. This online survey supports a research project undertaken by Dr. Greg I. Voykhansky and Dr. Troy C. Troublefield at Capitol Technology University.

---

### VOLUNTARY INVITATION TO PARTICIPATE

You are invited to participate in an academic research study examining psychological ownership in task-based collaborations between humans and artificial intelligence (AI) systems. This study is being conducted by Dr. Greg I. Voykhansky and Dr. Troy C. Troublefield as part of an approved research project at Capitol Technology University.

Your participation is requested because you have professional familiarity with project management tasks and workflows, which are central to the experimental scenarios used in this research.

**Participation in this study is entirely voluntary.** You may decline to participate, discontinue participation at any time, or skip any question you do not wish to answer without penalty or loss of benefits to which you are otherwise entitled.

---

### PURPOSE OF THE STUDY

The purpose of this study is to investigate how different types of AI tools (e.g., rule-based, adaptive, explainable, generative, and human-in-the-loop systems) influence individuals' perceptions of psychological ownership during collaborative task performance.

Psychological ownership refers to feelings of control, responsibility, identity, and personal investment in work outcomes. Findings from this study aim to contribute to the academic literature on human–AI collaboration and inform the ethical and organizational design of AI-enabled systems.

---

### STUDY PROCEDURES

If you agree to participate, you will be asked to complete an online study consisting of:

- Interaction with one AI system configured under a specific experimental condition
- Completion of approximately 20 survey questions related to your experience
- Optional short, open-ended responses reflecting on perceived control, responsibility, and engagement

Your total participation time is expected to be approximately **10 to 20 minutes**. All activities will be completed remotely via a secure web-based platform.

---

### BENEFITS

There is no direct compensation or personal benefit for participating in this study. However, your participation may contribute to:

- Improved understanding of psychological ownership in AI-assisted work environments
- Evidence-based guidance for ethical AI system design
- Advancements in research related to human–AI collaboration and organizational behavior

---

### RISKS

This study involves **minimal risk**. No foreseeable physical, psychological, legal, or professional risks are anticipated beyond those encountered in everyday online task activities. Should you experience discomfort, you may withdraw from the study at any time.

---

### CONFIDENTIALITY AND DATA SECURITY

All data collected in this study will be treated as confidential and handled in accordance with U.S. data protection standards and institutional research ethics requirements.

- Survey responses and system interaction data will be stored in a password-protected PostgreSQL database hosted on a secure cloud infrastructure.
- Access to raw data is restricted to the investigators and protected through multi-factor authentication.
- Identifying information (first name, last name, and email address) may be collected at sign-up for study administration purposes but will be anonymized immediately through assignment of a unique participant identification number.
- No personally identifiable information will be linked to published results or shared outside the research team.
- All research data will be retained for **three (3) years** following completion of the study and then permanently deleted.

---

### CONTACT INFORMATION

If you have questions about the study, procedures, or your rights as a participant, you may contact:

- **Dr. Greg I. Voykhansky** – givoykhansky@captechu.edu
- **Dr. Troy C. Troublefield** – ttroublefield@captechu.edu

If you feel you have not been treated according to the descriptions above, or that your participation rights have not been honored, you may contact Capitol Technology University's Institutional Review Board at **irb@captechu.edu**.

If you have any questions, concerns, or complaints that you wish to address to someone other than the primary investigator, you may contact the university at:

**Capitol Technology University**  
11301 Springfield Road  
Laurel, MD, 20708  
+1 (800)-950-1992  
+1 (301)-369-2800  
https://www.captechu.edu/

---

### ELECTRONIC CONSENT

You may print or save a copy of this consent form for your records.

**By checking the box below and clicking Submit, you acknowledge that:**

- You have read and understood the information provided above.
- You voluntarily agree to participate in this research study.
- You are 18 years of age or older and are a United States citizen or permanent resident.
- You are a working project management professional with at least one (1) year of relevant experience.
"""


def get_subsection(question_number: int) -> str:
    """Get the subsection for a given question number"""
    return SUBSECTION_MAPPING.get(question_number, "Unknown")


def get_question_text(question_number: int) -> str:
    """Get the question text for a given question number"""
    for q in SURVEY_QUESTIONS:
        if q["number"] == question_number:
            return q["text"]
    return ""
