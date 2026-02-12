import streamlit as st
from resume_builder import ResumeBuilder

st.set_page_config(page_title="Advanced Resume Builder", layout="wide")

builder = ResumeBuilder()

st.title("📄 Advanced Resume Builder")

# -------------------------------------------------------
# SESSION STATE INITIALIZATION
# -------------------------------------------------------
if "experience" not in st.session_state:
    st.session_state.experience = []

if "projects" not in st.session_state:
    st.session_state.projects = []

if "education" not in st.session_state:
    st.session_state.education = []

# -------------------------------------------------------
# PERSONAL INFORMATION
# -------------------------------------------------------
st.header("Personal Information")

col1, col2 = st.columns(2)

with col1:
    full_name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone")

with col2:
    location = st.text_input("Location")
    linkedin = st.text_input("LinkedIn URL")
    portfolio = st.text_input("Portfolio Website")

title = st.text_input("Professional Title")

# -------------------------------------------------------
# PROFESSIONAL SUMMARY
# -------------------------------------------------------
st.header("Professional Summary")
summary = st.text_area("Write your professional summary", height=150)

# -------------------------------------------------------
# EXPERIENCE SECTION
# -------------------------------------------------------
st.header("Work Experience")

if st.button("➕ Add Experience"):
    st.session_state.experience.append({})

for i, exp in enumerate(st.session_state.experience):
    with st.expander(f"Experience {i+1}", expanded=True):

        col1, col2 = st.columns([5, 1])
        with col2:
            if st.button("❌ Remove", key=f"remove_exp_{i}"):
                st.session_state.experience.pop(i)
                st.rerun()

        company = st.text_input("Company Name", key=f"exp_company_{i}")
        position = st.text_input("Position", key=f"exp_position_{i}")
        start_date = st.text_input("Start Date", key=f"exp_start_{i}")
        end_date = st.text_input("End Date", key=f"exp_end_{i}")
        description = st.text_area("Role Overview", key=f"exp_desc_{i}")
        responsibilities = st.text_area("Key Responsibilities (one per line)", key=f"exp_resp_{i}")
        achievements = st.text_area("Key Achievements (one per line)", key=f"exp_ach_{i}")

        st.session_state.experience[i] = {
            "company": company,
            "position": position,
            "start_date": start_date,
            "end_date": end_date,
            "description": description,
            "responsibilities": responsibilities,
            "achievements": achievements
        }

# -------------------------------------------------------
# PROJECTS SECTION
# -------------------------------------------------------
st.header("Projects")

if st.button("➕ Add Project"):
    st.session_state.projects.append({})

for i, proj in enumerate(st.session_state.projects):
    with st.expander(f"Project {i+1}", expanded=True):

        col1, col2 = st.columns([5, 1])
        with col2:
            if st.button("❌ Remove", key=f"remove_proj_{i}"):
                st.session_state.projects.pop(i)
                st.rerun()

        name = st.text_input("Project Name", key=f"proj_name_{i}")
        technologies = st.text_input("Technologies Used", key=f"proj_tech_{i}")
        description = st.text_area("Project Overview", key=f"proj_desc_{i}")
        responsibilities = st.text_area("Key Responsibilities (one per line)", key=f"proj_resp_{i}")
        achievements = st.text_area("Key Achievements (one per line)", key=f"proj_ach_{i}")
        link = st.text_input("Project Link (GitHub / Live URL)", key=f"proj_link_{i}")

        st.session_state.projects[i] = {
            "name": name,
            "technologies": technologies,
            "description": description,
            "responsibilities": responsibilities,
            "achievements": achievements,
            "link": link
        }

# -------------------------------------------------------
# EDUCATION SECTION
# -------------------------------------------------------
st.header("Education")

if st.button("➕ Add Education"):
    st.session_state.education.append({})

for i, edu in enumerate(st.session_state.education):
    with st.expander(f"Education {i+1}", expanded=True):

        col1, col2 = st.columns([5, 1])
        with col2:
            if st.button("❌ Remove", key=f"remove_edu_{i}"):
                st.session_state.education.pop(i)
                st.rerun()

        school = st.text_input("School / University", key=f"edu_school_{i}")
        degree = st.text_input("Degree", key=f"edu_degree_{i}")
        field = st.text_input("Field of Study", key=f"edu_field_{i}")
        graduation_date = st.text_input("Graduation Date", key=f"edu_grad_{i}")
        gpa = st.text_input("GPA (Optional)", key=f"edu_gpa_{i}")
        achievements = st.text_area("Achievements & Activities (one per line)", key=f"edu_ach_{i}")

        st.session_state.education[i] = {
            "school": school,
            "degree": degree,
            "field": field,
            "graduation_date": graduation_date,
            "gpa": gpa,
            "achievements": achievements
        }

# -------------------------------------------------------
# SKILLS SECTION
# -------------------------------------------------------
st.header("Skills")

technical_skills = st.text_area("Technical Skills (one per line)")
soft_skills = st.text_area("Soft Skills (one per line)")
languages = st.text_area("Languages (one per line)")
tools = st.text_area("Tools & Technologies (one per line)")

# -------------------------------------------------------
# TEMPLATE SELECTION
# -------------------------------------------------------
st.header("Select Resume Template")

template = st.selectbox(
    "Choose Template",
    ["Modern", "Professional", "Minimal", "Creative"]
)

# -------------------------------------------------------
# GENERATE RESUME
# -------------------------------------------------------
if st.button("🚀 Generate Resume", use_container_width=True):

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
            use_container_width=True
        )

    except Exception as e:
        st.error(f"Error generating resume: {e}")
