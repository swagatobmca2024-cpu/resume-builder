import streamlit as st
from resume_builder import ResumeBuilder

st.set_page_config(page_title="Advanced Resume Builder", layout="wide")

builder = ResumeBuilder()

st.title("📄 Advanced Resume Builder with Live Preview")

# Custom CSS for better preview styling
st.markdown("""
<style>
    .preview-container {
        background-color: white;
        padding: 40px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        color: #333;
        font-family: 'Arial', sans-serif;
        min-height: 800px;
    }
    .preview-header {
        text-align: center;
        border-bottom: 3px solid #2c3e50;
        padding-bottom: 20px;
        margin-bottom: 20px;
    }
    .preview-name {
        font-size: 32px;
        font-weight: bold;
        color: #2c3e50;
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
        color: #2c3e50;
        border-bottom: 2px solid #3498db;
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
        color: #2c3e50;
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
        background-color: #ecf0f1;
        padding: 5px 12px;
        border-radius: 5px;
        font-size: 13px;
        color: #2c3e50;
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

# Create two main columns: Form (left) and Preview (right)
form_col, preview_col = st.columns([3, 2])

with form_col:
    st.subheader("Fill in Your Information")

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
        st.rerun()

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
        st.rerun()

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
        st.rerun()

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
    st.divider()
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

# -------------------------------------------------------
# LIVE PREVIEW SECTION
# -------------------------------------------------------
with preview_col:
    st.subheader("Live Preview")

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
