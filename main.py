import streamlit as st
from resume_builder import ResumeBuilder

st.set_page_config(page_title="Advanced Resume Builder", layout="wide")

builder = ResumeBuilder()

# Glassmorphism Theme CSS
st.markdown("""
<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    [data-testid="stMainBlockContainer"] {
        background: transparent;
    }

    .main {
        background: transparent;
    }

    /* Glassmorphism Container */
    .glass-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 40px;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        margin-bottom: 30px;
    }

    .glass-box {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 15px;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(31, 38, 135, 0.2);
    }

    .glass-input-box {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(5px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        border-radius: 12px;
        padding: 15px 20px;
        transition: all 0.3s ease;
    }

    .glass-input-box:focus-within {
        background: rgba(255, 255, 255, 0.15);
        border-color: rgba(255, 255, 255, 0.35);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }

    /* Headings */
    h1 {
        color: white;
        text-align: center;
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 10px;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
        letter-spacing: 1px;
    }

    .tagline {
        text-align: center;
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1rem;
        margin-bottom: 40px;
        font-weight: 300;
    }

    h2 {
        color: white;
        font-size: 1.8rem;
        margin-bottom: 25px;
        font-weight: 600;
        text-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }

    h3 {
        color: rgba(255, 255, 255, 0.95);
        font-size: 1.3rem;
        margin-bottom: 15px;
        font-weight: 600;
    }

    /* Streamlit Input Override */
    input, textarea, select {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(5px) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        color: white !important;
        border-radius: 10px !important;
        padding: 12px 16px !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
    }

    input::placeholder, textarea::placeholder {
        color: rgba(255, 255, 255, 0.6) !important;
    }

    input:focus, textarea:focus, select:focus {
        background: rgba(255, 255, 255, 0.15) !important;
        border-color: rgba(255, 255, 255, 0.4) !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
        outline: none !important;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        padding: 12px 32px !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5) !important;
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%) !important;
    }

    .stButton > button:active {
        transform: translateY(0) !important;
    }

    /* Expander */
    [data-testid="stExpander"] {
        background: rgba(255, 255, 255, 0.08) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 12px !important;
    }

    .streamlit-expanderHeader {
        color: white !important;
        font-weight: 600 !important;
    }

    /* Selectbox */
    [data-baseweb="select"] {
        background: rgba(255, 255, 255, 0.1) !important;
    }

    [data-baseweb="select"] input {
        background: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
    }

    /* Success/Error Messages */
    .stSuccess {
        background: rgba(76, 175, 80, 0.2) !important;
        border: 1px solid rgba(76, 175, 80, 0.4) !important;
        color: #e8f5e9 !important;
        border-radius: 12px !important;
    }

    .stError {
        background: rgba(244, 67, 54, 0.2) !important;
        border: 1px solid rgba(244, 67, 54, 0.4) !important;
        color: #ffebee !important;
        border-radius: 12px !important;
    }

    /* Section Label */
    .section-label {
        color: rgba(255, 255, 255, 0.95);
        font-weight: 600;
        font-size: 0.95rem;
        display: block;
        margin-bottom: 8px;
    }

    /* Form Input Container */
    .form-group {
        margin-bottom: 20px;
    }

    /* Column Layout */
    .column-container {
        display: flex;
        gap: 20px;
    }

    /* Divider */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, rgba(255,255,255,0), rgba(255,255,255,0.3), rgba(255,255,255,0)) !important;
        margin: 30px 0 !important;
    }

    /* Preview Container */
    .preview-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(5px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 15px;
        padding: 40px;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        color: #333;
        font-family: 'Arial', sans-serif;
        min-height: 800px;
    }

    .preview-header {
        text-align: center;
        border-bottom: 3px solid #667eea;
        padding-bottom: 20px;
        margin-bottom: 20px;
    }

    .preview-name {
        font-size: 32px;
        font-weight: bold;
        color: #667eea;
        margin-bottom: 5px;
    }

    .preview-title {
        font-size: 18px;
        color: #555;
        margin-bottom: 10px;
    }

    .preview-contact {
        font-size: 14px;
        color: #666;
        line-height: 1.6;
    }

    .preview-section {
        margin-top: 25px;
    }

    .preview-section-title {
        font-size: 20px;
        font-weight: bold;
        color: #667eea;
        border-bottom: 2px solid #764ba2;
        padding-bottom: 5px;
        margin-bottom: 15px;
    }

    .preview-item {
        margin-bottom: 15px;
    }

    .preview-item-header {
        display: flex;
        justify-content: space-between;
        margin-bottom: 5px;
    }

    .preview-item-title {
        font-weight: bold;
        color: #333;
        font-size: 16px;
    }

    .preview-item-subtitle {
        color: #555;
        font-size: 14px;
        margin-bottom: 5px;
    }

    .preview-item-date {
        color: #777;
        font-size: 14px;
        font-style: italic;
    }

    .preview-text {
        color: #555;
        font-size: 14px;
        line-height: 1.6;
        margin-bottom: 8px;
    }

    .preview-list {
        margin-left: 20px;
        color: #555;
        font-size: 14px;
        line-height: 1.8;
    }

    .preview-skills {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
    }

    .preview-skill-tag {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.2), rgba(118, 75, 162, 0.2));
        border: 1px solid rgba(102, 126, 234, 0.3);
        padding: 6px 14px;
        border-radius: 8px;
        font-size: 13px;
        color: #667eea;
        font-weight: 500;
    }

    /* Responsive */
    @media (max-width: 1024px) {
        h1 {
            font-size: 2.5rem;
        }

        .glass-container {
            padding: 25px;
        }
    }

    @media (max-width: 768px) {
        h1 {
            font-size: 2rem;
        }

        .glass-container {
            padding: 20px;
        }

        h2 {
            font-size: 1.4rem;
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
st.markdown('<h1>📄 Resume Builder Pro</h1>', unsafe_allow_html=True)
st.markdown('<p class="tagline">Create your professional resume with live preview</p>', unsafe_allow_html=True)

# Create two main columns: Form (left) and Preview (right)
form_col, preview_col = st.columns([3, 2], gap="large")

with form_col:
    # -------------------------------------------------------
    # PERSONAL INFORMATION SECTION
    # -------------------------------------------------------
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.markdown('<h2>👤 Personal Information</h2>', unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="medium")

    with col1:
        st.markdown('<label class="section-label">Full Name</label>', unsafe_allow_html=True)
        full_name = st.text_input("", placeholder="John Doe", key="full_name")

        st.markdown('<label class="section-label">Email Address</label>', unsafe_allow_html=True)
        email = st.text_input("", placeholder="john@example.com", key="email")

        st.markdown('<label class="section-label">Phone Number</label>', unsafe_allow_html=True)
        phone = st.text_input("", placeholder="+1 (555) 123-4567", key="phone")

    with col2:
        st.markdown('<label class="section-label">Location</label>', unsafe_allow_html=True)
        location = st.text_input("", placeholder="New York, USA", key="location")

        st.markdown('<label class="section-label">LinkedIn URL</label>', unsafe_allow_html=True)
        linkedin = st.text_input("", placeholder="linkedin.com/in/yourname", key="linkedin")

        st.markdown('<label class="section-label">Portfolio Website</label>', unsafe_allow_html=True)
        portfolio = st.text_input("", placeholder="yourportfolio.com", key="portfolio")

    st.markdown('<label class="section-label">Professional Title</label>', unsafe_allow_html=True)
    title = st.text_input("", placeholder="e.g., Full Stack Developer", key="title")

    st.markdown('</div>', unsafe_allow_html=True)

    # -------------------------------------------------------
    # PROFESSIONAL SUMMARY SECTION
    # -------------------------------------------------------
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.markdown('<h2>✨ Professional Summary</h2>', unsafe_allow_html=True)

    st.markdown('<label class="section-label">Write a brief overview of your professional background</label>', unsafe_allow_html=True)
    summary = st.text_area("", placeholder="Share your professional journey, key skills, and career goals...", height=120, key="summary")

    st.markdown('</div>', unsafe_allow_html=True)

    # -------------------------------------------------------
    # EXPERIENCE SECTION
    # -------------------------------------------------------
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.markdown('<h2>💼 Work Experience</h2>', unsafe_allow_html=True)

    if st.button("➕ Add Experience", use_container_width=True, key="add_exp_btn"):
        st.session_state.experience.append({})
        st.rerun()

    for i, exp in enumerate(st.session_state.experience):
        st.markdown(f'<div class="glass-box">', unsafe_allow_html=True)

        col1, col2 = st.columns([5, 1], gap="small")
        with col2:
            if st.button("❌", key=f"remove_exp_{i}", help="Remove this experience"):
                st.session_state.experience.pop(i)
                st.rerun()

        col1, col2 = st.columns(2, gap="medium")
        with col1:
            st.markdown('<label class="section-label">Company Name</label>', unsafe_allow_html=True)
            company = st.text_input("", placeholder="Tech Company Inc.", key=f"exp_company_{i}")

            st.markdown('<label class="section-label">Position</label>', unsafe_allow_html=True)
            position = st.text_input("", placeholder="Senior Developer", key=f"exp_position_{i}")

        with col2:
            st.markdown('<label class="section-label">Start Date</label>', unsafe_allow_html=True)
            start_date = st.text_input("", placeholder="Jan 2020", key=f"exp_start_{i}")

            st.markdown('<label class="section-label">End Date</label>', unsafe_allow_html=True)
            end_date = st.text_input("", placeholder="Present", key=f"exp_end_{i}")

        st.markdown('<label class="section-label">Role Overview</label>', unsafe_allow_html=True)
        description = st.text_area("", placeholder="Describe your main responsibilities...", height=80, key=f"exp_desc_{i}")

        st.markdown('<label class="section-label">Key Responsibilities (one per line)</label>', unsafe_allow_html=True)
        responsibilities = st.text_area("", placeholder="Led development of new features\nMentored junior developers\nOptimized database queries", height=80, key=f"exp_resp_{i}")

        st.markdown('<label class="section-label">Key Achievements (one per line)</label>', unsafe_allow_html=True)
        achievements = st.text_area("", placeholder="Increased app performance by 40%\nLaunched new product feature\nReduced server costs by 30%", height=80, key=f"exp_ach_{i}")

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
    st.markdown('<h2>🚀 Projects</h2>', unsafe_allow_html=True)

    if st.button("➕ Add Project", use_container_width=True, key="add_proj_btn"):
        st.session_state.projects.append({})
        st.rerun()

    for i, proj in enumerate(st.session_state.projects):
        st.markdown(f'<div class="glass-box">', unsafe_allow_html=True)

        col1, col2 = st.columns([5, 1], gap="small")
        with col2:
            if st.button("❌", key=f"remove_proj_{i}", help="Remove this project"):
                st.session_state.projects.pop(i)
                st.rerun()

        st.markdown('<label class="section-label">Project Name</label>', unsafe_allow_html=True)
        name = st.text_input("", placeholder="E-commerce Platform", key=f"proj_name_{i}")

        st.markdown('<label class="section-label">Technologies Used</label>', unsafe_allow_html=True)
        technologies = st.text_input("", placeholder="React, Node.js, MongoDB, AWS", key=f"proj_tech_{i}")

        st.markdown('<label class="section-label">Project Overview</label>', unsafe_allow_html=True)
        description = st.text_area("", placeholder="Describe what the project does...", height=80, key=f"proj_desc_{i}")

        st.markdown('<label class="section-label">Key Responsibilities (one per line)</label>', unsafe_allow_html=True)
        responsibilities = st.text_area("", placeholder="Designed system architecture\nBuilt REST API endpoints\nImplemented payment integration", height=80, key=f"proj_resp_{i}")

        st.markdown('<label class="section-label">Key Achievements (one per line)</label>', unsafe_allow_html=True)
        achievements = st.text_area("", placeholder="Served 10,000+ users\nAchieved 99.9% uptime\n50% faster checkout process", height=80, key=f"proj_ach_{i}")

        st.markdown('<label class="section-label">Project Link (GitHub / Live URL)</label>', unsafe_allow_html=True)
        link = st.text_input("", placeholder="https://github.com/yourname/project", key=f"proj_link_{i}")

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
    st.markdown('<h2>🎓 Education</h2>', unsafe_allow_html=True)

    if st.button("➕ Add Education", use_container_width=True, key="add_edu_btn"):
        st.session_state.education.append({})
        st.rerun()

    for i, edu in enumerate(st.session_state.education):
        st.markdown(f'<div class="glass-box">', unsafe_allow_html=True)

        col1, col2 = st.columns([5, 1], gap="small")
        with col2:
            if st.button("❌", key=f"remove_edu_{i}", help="Remove this education"):
                st.session_state.education.pop(i)
                st.rerun()

        col1, col2 = st.columns(2, gap="medium")
        with col1:
            st.markdown('<label class="section-label">School / University</label>', unsafe_allow_html=True)
            school = st.text_input("", placeholder="University of Technology", key=f"edu_school_{i}")

            st.markdown('<label class="section-label">Degree</label>', unsafe_allow_html=True)
            degree = st.text_input("", placeholder="Bachelor of Science", key=f"edu_degree_{i}")

        with col2:
            st.markdown('<label class="section-label">Field of Study</label>', unsafe_allow_html=True)
            field = st.text_input("", placeholder="Computer Science", key=f"edu_field_{i}")

            st.markdown('<label class="section-label">Graduation Date</label>', unsafe_allow_html=True)
            graduation_date = st.text_input("", placeholder="May 2023", key=f"edu_grad_{i}")

        st.markdown('<label class="section-label">GPA (Optional)</label>', unsafe_allow_html=True)
        gpa = st.text_input("", placeholder="3.8/4.0", key=f"edu_gpa_{i}")

        st.markdown('<label class="section-label">Achievements & Activities (one per line)</label>', unsafe_allow_html=True)
        achievements = st.text_area("", placeholder="Dean's List - all semesters\nPresident of Programming Club\nPublished research paper on AI", height=80, key=f"edu_ach_{i}")

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
    st.markdown('<h2>⚡ Skills</h2>', unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        st.markdown('<label class="section-label">Technical Skills (one per line)</label>', unsafe_allow_html=True)
        technical_skills = st.text_area("", placeholder="Python\nJavaScript\nReact\nSQL", height=100, key="tech_skills")

        st.markdown('<label class="section-label">Languages (one per line)</label>', unsafe_allow_html=True)
        languages = st.text_area("", placeholder="English (Native)\nSpanish (Fluent)\nFrench (Intermediate)", height=80, key="languages")

    with col2:
        st.markdown('<label class="section-label">Soft Skills (one per line)</label>', unsafe_allow_html=True)
        soft_skills = st.text_area("", placeholder="Leadership\nTeam Collaboration\nCommunication\nProblem Solving", height=100, key="soft_skills")

        st.markdown('<label class="section-label">Tools & Technologies (one per line)</label>', unsafe_allow_html=True)
        tools = st.text_area("", placeholder="Git\nDocker\nJenkins\nAWS", height=80, key="tools")

    st.markdown('</div>', unsafe_allow_html=True)

    # -------------------------------------------------------
    # TEMPLATE SELECTION
    # -------------------------------------------------------
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.markdown('<h2>🎨 Select Resume Template</h2>', unsafe_allow_html=True)

    st.markdown('<label class="section-label">Choose your preferred resume template</label>', unsafe_allow_html=True)
    template = st.selectbox("", ["Modern", "Professional", "Minimal", "Creative"], key="template")

    st.markdown('</div>', unsafe_allow_html=True)

    # -------------------------------------------------------
    # GENERATE RESUME
    # -------------------------------------------------------
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        if st.button("🚀 Generate Resume", use_container_width=True, key="generate_btn"):

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

                st.success("✅ Resume Generated Successfully!")

                file_name = f"{full_name.strip().replace(' ', '_') or 'Resume'}_Resume.docx"

                st.download_button(
                    label="📥 Download Resume",
                    data=buffer,
                    file_name=file_name,
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True,
                    key="download_btn"
                )

            except Exception as e:
                st.error(f"Error generating resume: {e}")

    with col2:
        if st.button("🔄 Clear Form", use_container_width=True, key="clear_btn"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------------
# LIVE PREVIEW SECTION
# -------------------------------------------------------
with preview_col:
    st.markdown('<h2 style="text-align: center; color: white;">📋 Live Preview</h2>', unsafe_allow_html=True)

    preview_html = '<div class="preview-container">'

    # Header Section
    preview_html += '<div class="preview-header">'
    if full_name:
        preview_html += f'<div class="preview-name">{full_name}</div>'
    else:
        preview_html += '<div class="preview-name" style="color: #ccc;">Your Name</div>'

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
        preview_html += '<div class="preview-section-title">PROFESSIONAL SUMMARY</div>'
        preview_html += f'<div class="preview-text">{summary}</div>'
        preview_html += '</div>'

    # Work Experience
    if st.session_state.experience:
        has_content = any(exp.get("company") or exp.get("position") for exp in st.session_state.experience)
        if has_content:
            preview_html += '<div class="preview-section">'
            preview_html += '<div class="preview-section-title">WORK EXPERIENCE</div>'

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
            preview_html += '<div class="preview-section-title">PROJECTS</div>'

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
            preview_html += '<div class="preview-section-title">EDUCATION</div>'

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
        preview_html += '<div class="preview-section-title">SKILLS</div>'

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
