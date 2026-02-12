import streamlit as st
import random
import json
import pdfplumber
from docx import Document
from groq import Groq

# =========================================
# PAGE CONFIG
# =========================================
st.set_page_config(page_title="Resume Parser & Builder", layout="wide")

# =========================================
# GROQ + LLAMA 3.3-70B (MULTI KEY)
# =========================================
def get_groq_client():
    api_keys = st.secrets["GROQ_API_KEYS"]
    api_key = random.choice(api_keys)
    return Groq(api_key=api_key)

# =========================================
# RESUME TEXT EXTRACTION (PDF / DOCX)
# =========================================
def extract_resume_text(uploaded_file):
    if uploaded_file.name.lower().endswith(".pdf"):
        text = ""
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                if page.extract_text():
                    text += page.extract_text() + "\n"
        return text

    elif uploaded_file.name.lower().endswith(".docx"):
        doc = Document(uploaded_file)
        return "\n".join(p.text for p in doc.paragraphs)

    else:
        raise ValueError("Unsupported file format")

# =========================================
# RESUME PARSER (ANY FORMAT → STRUCTURED JSON)
# =========================================
def parse_resume_llama(resume_text):
    client = get_groq_client()

    prompt = f"""
You are an ATS-grade resume parser.

RULES:
- Return ONLY valid JSON
- No markdown
- No explanations
- If a field is missing, use empty string or empty array

JSON FORMAT:
{{
  "personal_info": {{
    "full_name": "",
    "email": "",
    "phone": "",
    "location": "",
    "linkedin": "",
    "portfolio": "",
    "title": ""
  }},
  "summary": "",
  "skills": {{
    "technical": [],
    "soft": [],
    "languages": [],
    "tools": []
  }},
  "experience": [
    {{
      "company": "",
      "position": "",
      "start_date": "",
      "end_date": "",
      "description": ""
    }}
  ],
  "education": [
    {{
      "school": "",
      "degree": "",
      "field": "",
      "graduation_date": "",
      "gpa": ""
    }}
  ]
}}

RESUME TEXT:
\"\"\"{resume_text}\"\"\"
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0,
        messages=[{"role": "user", "content": prompt}]
    )

    return json.loads(response.choices[0].message.content)

# =========================================
# SESSION STATE INITIALIZATION
# =========================================
defaults = {
    "full_name": "",
    "email": "",
    "phone": "",
    "location": "",
    "linkedin": "",
    "portfolio": "",
    "title": "",
    "summary": "",
    "tech_skills": "",
    "soft_skills": "",
    "languages": "",
    "tools": "",
    "experience": [],
    "education": []
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# =========================================
# RESUME UPLOAD + PARSE UI
# =========================================
st.markdown("## 📄 Upload Resume (PDF / DOCX)")

uploaded_resume = st.file_uploader(
    "Upload your resume",
    type=["pdf", "docx"]
)

if uploaded_resume:
    if st.button("⚡ Parse Resume & Autofill", use_container_width=True):
        with st.spinner("Parsing resume using LLaMA-3.3-70B..."):
            try:
                resume_text = extract_resume_text(uploaded_resume)
                parsed = parse_resume_llama(resume_text)

                # Autofill session state
                pi = parsed["personal_info"]
                st.session_state.full_name = pi["full_name"]
                st.session_state.email = pi["email"]
                st.session_state.phone = pi["phone"]
                st.session_state.location = pi["location"]
                st.session_state.linkedin = pi["linkedin"]
                st.session_state.portfolio = pi["portfolio"]
                st.session_state.title = pi["title"]
                st.session_state.summary = parsed["summary"]

                skills = parsed["skills"]
                st.session_state.tech_skills = "\n".join(skills["technical"])
                st.session_state.soft_skills = "\n".join(skills["soft"])
                st.session_state.languages = "\n".join(skills["languages"])
                st.session_state.tools = "\n".join(skills["tools"])

                st.session_state.experience = parsed["experience"]
                st.session_state.education = parsed["education"]

                st.success("Resume parsed and form auto-filled!")
                st.rerun()

            except Exception as e:
                st.error(f"Parsing failed: {e}")

# =========================================
# RESUME BUILDER FORM
# =========================================

import streamlit as st
from resume_builder import ResumeBuilder

st.set_page_config(page_title="Advanced Resume Builder", layout="wide")

builder = ResumeBuilder()

# Dark Theme with Blue Glassmorphism CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        min-height: 100vh;
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }

    [data-testid="stAppViewContainer"]::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background:
            radial-gradient(circle at 20% 50%, rgba(41, 128, 185, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(52, 152, 219, 0.15) 0%, transparent 50%);
        pointer-events: none;
        z-index: 0;
    }

    [data-testid="stMainBlockContainer"] {
        background: transparent;
        position: relative;
        z-index: 1;
    }

    .main {
        background: transparent;
    }

    /* Glassmorphism Container */
    .glass-container {
        background: rgba(30, 41, 59, 0.4);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 24px;
        padding: 32px;
        box-shadow:
            0 8px 32px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        margin-bottom: 24px;
        transition: all 0.3s ease;
    }

    .glass-container:hover {
        border-color: rgba(59, 130, 246, 0.3);
        box-shadow:
            0 12px 48px rgba(0, 0, 0, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.15);
    }

    .glass-box {
        background: rgba(51, 65, 85, 0.3);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 20px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow:
            0 4px 16px rgba(0, 0, 0, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.05);
        position: relative;
        transition: all 0.3s ease;
    }

    .glass-box:hover {
        border-color: rgba(59, 130, 246, 0.25);
        transform: translateY(-2px);
    }

    /* Headings */
    h1 {
        color: #ffffff;
        text-align: center;
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 8px;
        text-shadow: 0 2px 20px rgba(59, 130, 246, 0.3);
        letter-spacing: -0.5px;
        background: linear-gradient(135deg, #ffffff 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .tagline {
        text-align: center;
        color: rgba(203, 213, 225, 0.9);
        font-size: 1.15rem;
        margin-bottom: 48px;
        font-weight: 400;
        letter-spacing: 0.3px;
    }

    h2 {
        color: #f1f5f9;
        font-size: 1.5rem;
        margin-bottom: 24px;
        font-weight: 600;
        letter-spacing: -0.3px;
        display: flex;
        align-items: center;
        gap: 12px;
    }

    h3 {
        color: rgba(241, 245, 249, 0.95);
        font-size: 1.25rem;
        margin-bottom: 16px;
        font-weight: 600;
    }

    /* Section Label */
    .section-label {
        color: #e2e8f0;
        font-weight: 500;
        font-size: 0.875rem;
        display: block;
        margin-bottom: 8px;
        letter-spacing: 0.2px;
        text-transform: uppercase;
        font-size: 0.75rem;
        opacity: 0.9;
    }

    /* Streamlit Input Override */
    input, textarea, select {
        background: rgba(51, 65, 85, 0.5) !important;
        backdrop-filter: blur(8px) !important;
        border: 1.5px solid rgba(148, 163, 184, 0.2) !important;
        color: #f1f5f9 !important;
        border-radius: 12px !important;
        padding: 14px 18px !important;
        font-size: 0.95rem !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        font-weight: 400 !important;
    }

    input::placeholder, textarea::placeholder {
        color: rgba(148, 163, 184, 0.5) !important;
        font-weight: 400 !important;
    }

    input:hover, textarea:hover, select:hover {
        border-color: rgba(59, 130, 246, 0.4) !important;
        background: rgba(51, 65, 85, 0.6) !important;
    }

    input:focus, textarea:focus, select:focus {
        background: rgba(51, 65, 85, 0.7) !important;
        border-color: #3b82f6 !important;
        box-shadow:
            0 0 0 3px rgba(59, 130, 246, 0.1),
            0 4px 20px rgba(59, 130, 246, 0.2) !important;
        outline: none !important;
    }

    /* Textarea specific */
    textarea {
        line-height: 1.6 !important;
        resize: vertical !important;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
        color: white !important;
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
        border-radius: 12px !important;
        padding: 14px 28px !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow:
            0 4px 16px rgba(59, 130, 246, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
        cursor: pointer !important;
        letter-spacing: 0.3px !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow:
            0 8px 24px rgba(59, 130, 246, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
        border-color: rgba(59, 130, 246, 0.5) !important;
    }

    .stButton > button:active {
        transform: translateY(0) !important;
        box-shadow:
            0 2px 8px rgba(59, 130, 246, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
    }

    /* Remove Button (Red variant) */
    .stButton > button[kind="secondary"] {
        background: rgba(239, 68, 68, 0.2) !important;
        border-color: rgba(239, 68, 68, 0.3) !important;
    }

    .stButton > button[kind="secondary"]:hover {
        background: rgba(239, 68, 68, 0.3) !important;
        border-color: rgba(239, 68, 68, 0.5) !important;
    }

    /* Download Button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        border-color: rgba(16, 185, 129, 0.3) !important;
    }

    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #059669 0%, #047857 100%) !important;
        box-shadow:
            0 8px 24px rgba(16, 185, 129, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
    }

    /* Expander */
    [data-testid="stExpander"] {
        background: rgba(51, 65, 85, 0.3) !important;
        border: 1px solid rgba(148, 163, 184, 0.15) !important;
        border-radius: 16px !important;
        backdrop-filter: blur(12px) !important;
    }

    .streamlit-expanderHeader {
        color: #f1f5f9 !important;
        font-weight: 600 !important;
    }

    /* Selectbox */
    [data-baseweb="select"] {
        background: rgba(51, 65, 85, 0.5) !important;
        border-radius: 12px !important;
    }

    [data-baseweb="select"] > div {
        background: rgba(51, 65, 85, 0.5) !important;
        border-color: rgba(148, 163, 184, 0.2) !important;
    }

    [data-baseweb="select"]:hover > div {
        border-color: rgba(59, 130, 246, 0.4) !important;
    }

    /* Dropdown menu */
    [data-baseweb="popover"] {
        background: rgba(30, 41, 59, 0.95) !important;
        backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(148, 163, 184, 0.2) !important;
        border-radius: 12px !important;
    }

    [role="option"] {
        color: #f1f5f9 !important;
        transition: all 0.2s ease !important;
    }

    [role="option"]:hover {
        background: rgba(59, 130, 246, 0.2) !important;
    }

    /* Success/Error Messages */
    .stSuccess {
        background: rgba(16, 185, 129, 0.15) !important;
        border: 1px solid rgba(16, 185, 129, 0.3) !important;
        color: #d1fae5 !important;
        border-radius: 12px !important;
        backdrop-filter: blur(12px) !important;
    }

    .stError {
        background: rgba(239, 68, 68, 0.15) !important;
        border: 1px solid rgba(239, 68, 68, 0.3) !important;
        color: #fee2e2 !important;
        border-radius: 12px !important;
        backdrop-filter: blur(12px) !important;
    }

    /* Divider */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg,
            rgba(148, 163, 184, 0),
            rgba(148, 163, 184, 0.3),
            rgba(148, 163, 184, 0)) !important;
        margin: 32px 0 !important;
    }

    /* Preview Container */
    .preview-container {
        background: rgba(255, 255, 255, 0.98);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 20px;
        padding: 48px;
        box-shadow:
            0 8px 32px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.5);
        color: #1e293b;
        font-family: 'Inter', 'Arial', sans-serif;
        min-height: 800px;
    }

    .preview-header {
        text-align: center;
        border-bottom: 3px solid #3b82f6;
        padding-bottom: 24px;
        margin-bottom: 24px;
    }

    .preview-name {
        font-size: 36px;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 8px;
        letter-spacing: -0.5px;
    }

    .preview-title {
        font-size: 18px;
        color: #3b82f6;
        margin-bottom: 12px;
        font-weight: 500;
    }

    .preview-contact {
        font-size: 14px;
        color: #64748b;
        line-height: 1.8;
    }

    .preview-section {
        margin-top: 28px;
    }

    .preview-section-title {
        font-size: 20px;
        font-weight: 700;
        color: #1e293b;
        border-bottom: 2px solid #3b82f6;
        padding-bottom: 8px;
        margin-bottom: 16px;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        font-size: 16px;
    }

    .preview-item {
        margin-bottom: 20px;
        padding-bottom: 16px;
        border-bottom: 1px solid rgba(148, 163, 184, 0.15);
    }

    .preview-item:last-child {
        border-bottom: none;
    }

    .preview-item-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 8px;
    }

    .preview-item-title {
        font-weight: 600;
        color: #1e293b;
        font-size: 16px;
    }

    .preview-item-subtitle {
        color: #3b82f6;
        font-size: 14px;
        margin-bottom: 4px;
        font-weight: 500;
    }

    .preview-item-date {
        color: #64748b;
        font-size: 13px;
        font-style: italic;
        white-space: nowrap;
    }

    .preview-text {
        color: #475569;
        font-size: 14px;
        line-height: 1.7;
        margin-bottom: 10px;
    }

    .preview-list {
        margin-left: 20px;
        color: #475569;
        font-size: 14px;
        line-height: 1.8;
    }

    .preview-list ul {
        margin-top: 6px;
    }

    .preview-list li {
        margin-bottom: 4px;
    }

    .preview-skills {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: 8px;
    }

    .preview-skill-tag {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(37, 99, 235, 0.15));
        border: 1px solid rgba(59, 130, 246, 0.3);
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 13px;
        color: #1e40af;
        font-weight: 500;
        transition: all 0.2s ease;
    }

    /* Column gaps */
    [data-testid="column"] {
        padding: 0 8px;
    }

    /* Remove default streamlit padding */
    .block-container {
        padding-top: 3rem !important;
        padding-bottom: 3rem !important;
    }

    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }

    ::-webkit-scrollbar-track {
        background: rgba(30, 41, 59, 0.3);
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb {
        background: rgba(59, 130, 246, 0.5);
        border-radius: 10px;
        border: 2px solid rgba(30, 41, 59, 0.3);
    }

    ::-webkit-scrollbar-thumb:hover {
        background: rgba(59, 130, 246, 0.7);
    }

    /* Responsive */
    @media (max-width: 1024px) {
        h1 {
            font-size: 2.5rem;
        }

        .glass-container {
            padding: 24px;
        }

        .preview-container {
            padding: 32px;
        }
    }

    @media (max-width: 768px) {
        h1 {
            font-size: 2rem;
        }

        .glass-container {
            padding: 20px;
        }

        .glass-box {
            padding: 16px;
        }

        h2 {
            font-size: 1.25rem;
        }

        .preview-container {
            padding: 24px;
        }
    }

    /* Loading animation */
    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.5;
        }
    }

    /* Subtle animations */
    .glass-container, .glass-box {
        animation: fadeIn 0.5s ease-in-out;
    }

    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# SESSION STATE INITIALIZATION
# -------------------------------------------------------
if "experience" not in st.session_state:
    st.session_state.experience = []

if "projects" not in st.session_state:
    st.session_state.projects = []

if "education" not in st.session_state:
    st.session_state.education = []

# Main Title
st.markdown('<h1>Resume Builder Pro</h1>', unsafe_allow_html=True)
st.markdown('<p class="tagline">Create your professional resume with live preview</p>', unsafe_allow_html=True)

# Create two main columns: Form (left) and Preview (right)
form_col, preview_col = st.columns([3, 2], gap="large")

with form_col:
    # -------------------------------------------------------
    # PERSONAL INFORMATION SECTION
    # -------------------------------------------------------
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.markdown('<h2><span>👤</span> Personal Information</h2>', unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="medium")

    with col1:
        st.markdown('<label class="section-label">Full Name</label>', unsafe_allow_html=True)
        full_name = st.text_input("", placeholder="John Doe", key="full_name", label_visibility="collapsed")

        st.markdown('<label class="section-label">Email Address</label>', unsafe_allow_html=True)
        email = st.text_input("", placeholder="john@example.com", key="email", label_visibility="collapsed")

        st.markdown('<label class="section-label">Phone Number</label>', unsafe_allow_html=True)
        phone = st.text_input("", placeholder="+1 (555) 123-4567", key="phone", label_visibility="collapsed")

    with col2:
        st.markdown('<label class="section-label">Location</label>', unsafe_allow_html=True)
        location = st.text_input("", placeholder="New York, USA", key="location", label_visibility="collapsed")

        st.markdown('<label class="section-label">LinkedIn URL</label>', unsafe_allow_html=True)
        linkedin = st.text_input("", placeholder="linkedin.com/in/yourname", key="linkedin", label_visibility="collapsed")

        st.markdown('<label class="section-label">Portfolio Website</label>', unsafe_allow_html=True)
        portfolio = st.text_input("", placeholder="yourportfolio.com", key="portfolio", label_visibility="collapsed")

    st.markdown('<label class="section-label">Professional Title</label>', unsafe_allow_html=True)
    title = st.text_input("", placeholder="e.g., Full Stack Developer", key="title", label_visibility="collapsed")

    st.markdown('</div>', unsafe_allow_html=True)

    # -------------------------------------------------------
    # PROFESSIONAL SUMMARY SECTION
    # -------------------------------------------------------
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.markdown('<h2><span>✨</span> Professional Summary</h2>', unsafe_allow_html=True)

    st.markdown('<label class="section-label">Write a brief overview of your professional background</label>', unsafe_allow_html=True)
    summary = st.text_area("", placeholder="Share your professional journey, key skills, and career goals...", height=120, key="summary", label_visibility="collapsed")

    st.markdown('</div>', unsafe_allow_html=True)

    # -------------------------------------------------------
    # EXPERIENCE SECTION
    # -------------------------------------------------------
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.markdown('<h2><span>💼</span> Work Experience</h2>', unsafe_allow_html=True)

    if st.button("+ Add Experience", use_container_width=True, key="add_exp_btn"):
        st.session_state.experience.append({})
        st.rerun()

    for i, exp in enumerate(st.session_state.experience):
        st.markdown(f'<div class="glass-box">', unsafe_allow_html=True)

        col_main, col_remove = st.columns([6, 1], gap="small")
        with col_remove:
            if st.button("✕", key=f"remove_exp_{i}", help="Remove this experience"):
                st.session_state.experience.pop(i)
                st.rerun()

        col1, col2 = st.columns(2, gap="medium")
        with col1:
            st.markdown('<label class="section-label">Company Name</label>', unsafe_allow_html=True)
            company = st.text_input("", placeholder="Tech Company Inc.", key=f"exp_company_{i}", label_visibility="collapsed")

            st.markdown('<label class="section-label">Position</label>', unsafe_allow_html=True)
            position = st.text_input("", placeholder="Senior Developer", key=f"exp_position_{i}", label_visibility="collapsed")

        with col2:
            st.markdown('<label class="section-label">Start Date</label>', unsafe_allow_html=True)
            start_date = st.text_input("", placeholder="Jan 2020", key=f"exp_start_{i}", label_visibility="collapsed")

            st.markdown('<label class="section-label">End Date</label>', unsafe_allow_html=True)
            end_date = st.text_input("", placeholder="Present", key=f"exp_end_{i}", label_visibility="collapsed")

        st.markdown('<label class="section-label">Role Overview</label>', unsafe_allow_html=True)
        description = st.text_area("", placeholder="Describe your main responsibilities...", height=80, key=f"exp_desc_{i}", label_visibility="collapsed")

        st.markdown('<label class="section-label">Key Responsibilities (one per line)</label>', unsafe_allow_html=True)
        responsibilities = st.text_area("", placeholder="Led development of new features\nMentored junior developers\nOptimized database queries", height=80, key=f"exp_resp_{i}", label_visibility="collapsed")

        st.markdown('<label class="section-label">Key Achievements (one per line)</label>', unsafe_allow_html=True)
        achievements = st.text_area("", placeholder="Increased app performance by 40%\nLaunched new product feature\nReduced server costs by 30%", height=80, key=f"exp_ach_{i}", label_visibility="collapsed")

        st.session_state.experience[i] = {
            "company": company,
            "position": position,
            "start_date": start_date,
            "end_date": end_date,
            "description": description,
            "responsibilities": responsibilities,
            "achievements": achievements
        }

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # -------------------------------------------------------
    # PROJECTS SECTION
    # -------------------------------------------------------
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.markdown('<h2><span>🚀</span> Projects</h2>', unsafe_allow_html=True)

    if st.button("+ Add Project", use_container_width=True, key="add_proj_btn"):
        st.session_state.projects.append({})
        st.rerun()

    for i, proj in enumerate(st.session_state.projects):
        st.markdown(f'<div class="glass-box">', unsafe_allow_html=True)

        col_main, col_remove = st.columns([6, 1], gap="small")
        with col_remove:
            if st.button("✕", key=f"remove_proj_{i}", help="Remove this project"):
                st.session_state.projects.pop(i)
                st.rerun()

        st.markdown('<label class="section-label">Project Name</label>', unsafe_allow_html=True)
        name = st.text_input("", placeholder="E-commerce Platform", key=f"proj_name_{i}", label_visibility="collapsed")

        st.markdown('<label class="section-label">Technologies Used</label>', unsafe_allow_html=True)
        technologies = st.text_input("", placeholder="React, Node.js, MongoDB, AWS", key=f"proj_tech_{i}", label_visibility="collapsed")

        st.markdown('<label class="section-label">Project Overview</label>', unsafe_allow_html=True)
        description = st.text_area("", placeholder="Describe what the project does...", height=80, key=f"proj_desc_{i}", label_visibility="collapsed")

        st.markdown('<label class="section-label">Key Responsibilities (one per line)</label>', unsafe_allow_html=True)
        responsibilities = st.text_area("", placeholder="Designed system architecture\nBuilt REST API endpoints\nImplemented payment integration", height=80, key=f"proj_resp_{i}", label_visibility="collapsed")

        st.markdown('<label class="section-label">Key Achievements (one per line)</label>', unsafe_allow_html=True)
        achievements = st.text_area("", placeholder="Served 10,000+ users\nAchieved 99.9% uptime\n50% faster checkout process", height=80, key=f"proj_ach_{i}", label_visibility="collapsed")

        st.markdown('<label class="section-label">Project Link (GitHub / Live URL)</label>', unsafe_allow_html=True)
        link = st.text_input("", placeholder="https://github.com/yourname/project", key=f"proj_link_{i}", label_visibility="collapsed")

        st.session_state.projects[i] = {
            "name": name,
            "technologies": technologies,
            "description": description,
            "responsibilities": responsibilities,
            "achievements": achievements,
            "link": link
        }

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # -------------------------------------------------------
    # EDUCATION SECTION
    # -------------------------------------------------------
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.markdown('<h2><span>🎓</span> Education</h2>', unsafe_allow_html=True)

    if st.button("+ Add Education", use_container_width=True, key="add_edu_btn"):
        st.session_state.education.append({})
        st.rerun()

    for i, edu in enumerate(st.session_state.education):
        st.markdown(f'<div class="glass-box">', unsafe_allow_html=True)

        col_main, col_remove = st.columns([6, 1], gap="small")
        with col_remove:
            if st.button("✕", key=f"remove_edu_{i}", help="Remove this education"):
                st.session_state.education.pop(i)
                st.rerun()

        col1, col2 = st.columns(2, gap="medium")
        with col1:
            st.markdown('<label class="section-label">School / University</label>', unsafe_allow_html=True)
            school = st.text_input("", placeholder="University of Technology", key=f"edu_school_{i}", label_visibility="collapsed")

            st.markdown('<label class="section-label">Degree</label>', unsafe_allow_html=True)
            degree = st.text_input("", placeholder="Bachelor of Science", key=f"edu_degree_{i}", label_visibility="collapsed")

        with col2:
            st.markdown('<label class="section-label">Field of Study</label>', unsafe_allow_html=True)
            field = st.text_input("", placeholder="Computer Science", key=f"edu_field_{i}", label_visibility="collapsed")

            st.markdown('<label class="section-label">Graduation Date</label>', unsafe_allow_html=True)
            graduation_date = st.text_input("", placeholder="May 2023", key=f"edu_grad_{i}", label_visibility="collapsed")

        st.markdown('<label class="section-label">GPA (Optional)</label>', unsafe_allow_html=True)
        gpa = st.text_input("", placeholder="3.8/4.0", key=f"edu_gpa_{i}", label_visibility="collapsed")

        st.markdown('<label class="section-label">Achievements & Activities (one per line)</label>', unsafe_allow_html=True)
        achievements = st.text_area("", placeholder="Dean's List - all semesters\nPresident of Programming Club\nPublished research paper on AI", height=80, key=f"edu_ach_{i}", label_visibility="collapsed")

        st.session_state.education[i] = {
            "school": school,
            "degree": degree,
            "field": field,
            "graduation_date": graduation_date,
            "gpa": gpa,
            "achievements": achievements
        }

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # -------------------------------------------------------
    # SKILLS SECTION
    # -------------------------------------------------------
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.markdown('<h2><span>⚡</span> Skills</h2>', unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        st.markdown('<label class="section-label">Technical Skills (one per line)</label>', unsafe_allow_html=True)
        technical_skills = st.text_area("", placeholder="Python\nJavaScript\nReact\nSQL", height=100, key="tech_skills", label_visibility="collapsed")

        st.markdown('<label class="section-label">Languages (one per line)</label>', unsafe_allow_html=True)
        languages = st.text_area("", placeholder="English (Native)\nSpanish (Fluent)\nFrench (Intermediate)", height=80, key="languages", label_visibility="collapsed")

    with col2:
        st.markdown('<label class="section-label">Soft Skills (one per line)</label>', unsafe_allow_html=True)
        soft_skills = st.text_area("", placeholder="Leadership\nTeam Collaboration\nCommunication\nProblem Solving", height=100, key="soft_skills", label_visibility="collapsed")

        st.markdown('<label class="section-label">Tools & Technologies (one per line)</label>', unsafe_allow_html=True)
        tools = st.text_area("", placeholder="Git\nDocker\nJenkins\nAWS", height=80, key="tools", label_visibility="collapsed")

    st.markdown('</div>', unsafe_allow_html=True)

    # -------------------------------------------------------
    # TEMPLATE SELECTION
    # -------------------------------------------------------
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.markdown('<h2><span>🎨</span> Select Resume Template</h2>', unsafe_allow_html=True)

    st.markdown('<label class="section-label">Choose your preferred resume template</label>', unsafe_allow_html=True)
    template = st.selectbox("", ["Modern", "Professional", "Minimal", "Creative"], key="template", label_visibility="collapsed")

    st.markdown('</div>', unsafe_allow_html=True)

    # -------------------------------------------------------
    # GENERATE RESUME
    # -------------------------------------------------------
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        if st.button("Generate Resume", use_container_width=True, key="generate_btn"):

            resume_data = {
                "template": template,
                "personal_info": {
                    "full_name": full_name,
                    "title": title,
                    "email": email,
                    "phone": phone,
                    "location": location,
                    "linkedin": linkedin,
                    "portfolio": portfolio
                },
                "summary": summary,
                "experience": st.session_state.experience,
                "projects": st.session_state.projects,
                "education": st.session_state.education,
                "skills": {
                    "technical": technical_skills,
                    "soft": soft_skills,
                    "languages": languages,
                    "tools": tools
                }
            }

            try:
                buffer = builder.generate_resume(resume_data)

                st.success("Resume Generated Successfully!")

                file_name = f"{full_name.strip().replace(' ', '_') or 'Resume'}_Resume.docx"

                st.download_button(
                    label="Download Resume",
                    data=buffer,
                    file_name=file_name,
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True,
                    key="download_btn"
                )

            except Exception as e:
                st.error(f"Error generating resume: {e}")

    with col2:
        if st.button("Clear Form", use_container_width=True, key="clear_btn"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------------
# LIVE PREVIEW SECTION
# -------------------------------------------------------
with preview_col:
    st.markdown('<h2 style="text-align: center; color: white; margin-bottom: 24px;">📋 Live Preview</h2>', unsafe_allow_html=True)

    preview_html = '<div class="preview-container">'

    # Header Section
    preview_html += '<div class="preview-header">'
    if full_name:
        preview_html += f'<div class="preview-name">{full_name}</div>'
    else:
        preview_html += '<div class="preview-name" style="color: #94a3b8;">Your Name</div>'

    if title:
        preview_html += f'<div class="preview-title">{title}</div>'

    preview_html += '<div class="preview-contact">'
    contact_parts = []
    if email:
        contact_parts.append(email)
    if phone:
        contact_parts.append(phone)
    if location:
        contact_parts.append(location)

    if contact_parts:
        preview_html += ' | '.join(contact_parts) + '<br>'

    if linkedin:
        preview_html += f'LinkedIn: {linkedin}<br>'
    if portfolio:
        preview_html += f'Portfolio: {portfolio}'

    preview_html += '</div></div>'

    # Professional Summary
    if summary:
        preview_html += '<div class="preview-section">'
        preview_html += '<div class="preview-section-title">Professional Summary</div>'
        preview_html += f'<div class="preview-text">{summary}</div>'
        preview_html += '</div>'

    # Work Experience
    if st.session_state.experience:
        has_content = any(exp.get("company") or exp.get("position") for exp in st.session_state.experience)
        if has_content:
            preview_html += '<div class="preview-section">'
            preview_html += '<div class="preview-section-title">Work Experience</div>'

            for exp in st.session_state.experience:
                if exp.get("company") or exp.get("position"):
                    preview_html += '<div class="preview-item">'

                    preview_html += '<div class="preview-item-header">'
                    preview_html += '<div>'
                    if exp.get("position"):
                        preview_html += f'<div class="preview-item-title">{exp["position"]}</div>'
                    if exp.get("company"):
                        preview_html += f'<div class="preview-item-subtitle">{exp["company"]}</div>'
                    preview_html += '</div>'

                    if exp.get("start_date") or exp.get("end_date"):
                        date_str = f'{exp.get("start_date", "")} - {exp.get("end_date", "")}'
                        preview_html += f'<div class="preview-item-date">{date_str}</div>'

                    preview_html += '</div>'

                    if exp.get("description"):
                        preview_html += f'<div class="preview-text">{exp["description"]}</div>'

                    if exp.get("responsibilities"):
                        responsibilities = [r.strip() for r in exp["responsibilities"].split('\n') if r.strip()]
                        if responsibilities:
                            preview_html += '<div class="preview-list"><strong>Key Responsibilities:</strong><ul>'
                            for resp in responsibilities:
                                preview_html += f'<li>{resp}</li>'
                            preview_html += '</ul></div>'

                    if exp.get("achievements"):
                        achievements = [a.strip() for a in exp["achievements"].split('\n') if a.strip()]
                        if achievements:
                            preview_html += '<div class="preview-list"><strong>Key Achievements:</strong><ul>'
                            for ach in achievements:
                                preview_html += f'<li>{ach}</li>'
                            preview_html += '</ul></div>'

                    preview_html += '</div>'

            preview_html += '</div>'

    # Projects
    if st.session_state.projects:
        has_content = any(proj.get("name") for proj in st.session_state.projects)
        if has_content:
            preview_html += '<div class="preview-section">'
            preview_html += '<div class="preview-section-title">Projects</div>'

            for proj in st.session_state.projects:
                if proj.get("name"):
                    preview_html += '<div class="preview-item">'

                    preview_html += f'<div class="preview-item-title">{proj["name"]}</div>'

                    if proj.get("technologies"):
                        preview_html += f'<div class="preview-item-subtitle">Technologies: {proj["technologies"]}</div>'

                    if proj.get("description"):
                        preview_html += f'<div class="preview-text">{proj["description"]}</div>'

                    if proj.get("responsibilities"):
                        responsibilities = [r.strip() for r in proj["responsibilities"].split('\n') if r.strip()]
                        if responsibilities:
                            preview_html += '<div class="preview-list"><strong>Key Responsibilities:</strong><ul>'
                            for resp in responsibilities:
                                preview_html += f'<li>{resp}</li>'
                            preview_html += '</ul></div>'

                    if proj.get("achievements"):
                        achievements = [a.strip() for a in proj["achievements"].split('\n') if a.strip()]
                        if achievements:
                            preview_html += '<div class="preview-list"><strong>Key Achievements:</strong><ul>'
                            for ach in achievements:
                                preview_html += f'<li>{ach}</li>'
                            preview_html += '</ul></div>'

                    if proj.get("link"):
                        preview_html += f'<div class="preview-text"><strong>Link:</strong> {proj["link"]}</div>'

                    preview_html += '</div>'

            preview_html += '</div>'

    # Education
    if st.session_state.education:
        has_content = any(edu.get("school") or edu.get("degree") for edu in st.session_state.education)
        if has_content:
            preview_html += '<div class="preview-section">'
            preview_html += '<div class="preview-section-title">Education</div>'

            for edu in st.session_state.education:
                if edu.get("school") or edu.get("degree"):
                    preview_html += '<div class="preview-item">'

                    preview_html += '<div class="preview-item-header">'
                    preview_html += '<div>'
                    if edu.get("degree"):
                        degree_str = edu["degree"]
                        if edu.get("field"):
                            degree_str += f' in {edu["field"]}'
                        preview_html += f'<div class="preview-item-title">{degree_str}</div>'
                    if edu.get("school"):
                        preview_html += f'<div class="preview-item-subtitle">{edu["school"]}</div>'
                    preview_html += '</div>'

                    if edu.get("graduation_date"):
                        preview_html += f'<div class="preview-item-date">{edu["graduation_date"]}</div>'

                    preview_html += '</div>'

                    if edu.get("gpa"):
                        preview_html += f'<div class="preview-text"><strong>GPA:</strong> {edu["gpa"]}</div>'

                    if edu.get("achievements"):
                        achievements = [a.strip() for a in edu["achievements"].split('\n') if a.strip()]
                        if achievements:
                            preview_html += '<div class="preview-list"><ul>'
                            for ach in achievements:
                                preview_html += f'<li>{ach}</li>'
                            preview_html += '</ul></div>'

                    preview_html += '</div>'

            preview_html += '</div>'

    # Skills
    has_skills = technical_skills or soft_skills or languages or tools
    if has_skills:
        preview_html += '<div class="preview-section">'
        preview_html += '<div class="preview-section-title">Skills</div>'

        if technical_skills:
            tech_list = [s.strip() for s in technical_skills.split('\n') if s.strip()]
            if tech_list:
                preview_html += '<div class="preview-item">'
                preview_html += '<div class="preview-item-subtitle">Technical Skills</div>'
                preview_html += '<div class="preview-skills">'
                for skill in tech_list:
                    preview_html += f'<span class="preview-skill-tag">{skill}</span>'
                preview_html += '</div></div>'

        if soft_skills:
            soft_list = [s.strip() for s in soft_skills.split('\n') if s.strip()]
            if soft_list:
                preview_html += '<div class="preview-item">'
                preview_html += '<div class="preview-item-subtitle">Soft Skills</div>'
                preview_html += '<div class="preview-skills">'
                for skill in soft_list:
                    preview_html += f'<span class="preview-skill-tag">{skill}</span>'
                preview_html += '</div></div>'

        if languages:
            lang_list = [l.strip() for l in languages.split('\n') if l.strip()]
            if lang_list:
                preview_html += '<div class="preview-item">'
                preview_html += '<div class="preview-item-subtitle">Languages</div>'
                preview_html += '<div class="preview-skills">'
                for lang in lang_list:
                    preview_html += f'<span class="preview-skill-tag">{lang}</span>'
                preview_html += '</div></div>'

        if tools:
            tools_list = [t.strip() for t in tools.split('\n') if t.strip()]
            if tools_list:
                preview_html += '<div class="preview-item">'
                preview_html += '<div class="preview-item-subtitle">Tools & Technologies</div>'
                preview_html += '<div class="preview-skills">'
                for tool in tools_list:
                    preview_html += f'<span class="preview-skill-tag">{tool}</span>'
                preview_html += '</div></div>'

        preview_html += '</div>'

    preview_html += '</div>'

    # Display the preview
    st.markdown(preview_html, unsafe_allow_html=True)
