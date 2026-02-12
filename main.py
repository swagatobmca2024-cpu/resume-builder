import streamlit as st
from resume_builder import ResumeBuilder
import datetime

st.set_page_config(page_title="Resume Builder", layout="centered")

st.title("📄 Resume Builder")

builder = ResumeBuilder()

# -------------------------------
# Personal Information
# -------------------------------
st.header("Personal Information")

full_name = st.text_input("Full Name")
title = st.text_input("Professional Title")
email = st.text_input("Email")
phone = st.text_input("Phone")
location = st.text_input("Location")
linkedin = st.text_input("LinkedIn URL")
portfolio = st.text_input("Portfolio URL")

# -------------------------------
# Professional Summary
# -------------------------------
st.header("Professional Summary")
summary = st.text_area("Write your summary")

# -------------------------------
# Experience Section
# -------------------------------
st.header("Experience")

experience_list = []
num_exp = st.number_input("Number of Experiences", min_value=0, max_value=5, step=1)

for i in range(num_exp):
    st.subheader(f"Experience {i+1}")
    position = st.text_input(f"Position {i}", key=f"pos_{i}")
    company = st.text_input(f"Company {i}", key=f"comp_{i}")
    start_date = st.text_input(f"Start Date {i}", key=f"start_{i}")
    end_date = st.text_input(f"End Date {i}", key=f"end_{i}")
    description = st.text_area(f"Description {i}", key=f"desc_{i}")
    responsibilities = st.text_area(f"Responsibilities (one per line) {i}", key=f"resp_{i}")

    experience_list.append({
        "position": position,
        "company": company,
        "start_date": start_date,
        "end_date": end_date,
        "description": description,
        "responsibilities": responsibilities
    })

# -------------------------------
# Education Section
# -------------------------------
st.header("Education")

education_list = []
num_edu = st.number_input("Number of Education Entries", min_value=0, max_value=5, step=1)

for i in range(num_edu):
    st.subheader(f"Education {i+1}")
    school = st.text_input(f"School {i}", key=f"school_{i}")
    degree = st.text_input(f"Degree {i}", key=f"degree_{i}")
    field = st.text_input(f"Field of Study {i}", key=f"field_{i}")
    graduation_date = st.text_input(f"Graduation Date {i}", key=f"grad_{i}")
    gpa = st.text_input(f"GPA {i}", key=f"gpa_{i}")

    education_list.append({
        "school": school,
        "degree": degree,
        "field": field,
        "graduation_date": graduation_date,
        "gpa": gpa
    })

# -------------------------------
# Skills Section
# -------------------------------
st.header("Skills")

technical_skills = st.text_area("Technical Skills (one per line)")
soft_skills = st.text_area("Soft Skills (one per line)")
languages = st.text_area("Languages (one per line)")
tools = st.text_area("Tools & Technologies (one per line)")

# -------------------------------
# Template Selection
# -------------------------------
st.header("Select Template")

template = st.selectbox(
    "Choose Resume Template",
    ["Modern", "Professional", "Minimal", "Creative"]
)

# -------------------------------
# Generate Resume
# -------------------------------
if st.button("Generate Resume"):

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
        "experience": experience_list,
        "education": education_list,
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

        st.download_button(
            label="📥 Download Resume",
            data=buffer,
            file_name=f"{full_name.replace(' ', '_')}_Resume.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

    except Exception as e:
        st.error(f"Error generating resume: {e}")
