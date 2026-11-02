import streamlit as st
import pandas as pd

st.set_page_config(page_title="RoleFit AI", page_icon="🎯")

roles = {
    "Data Analyst": ["python", "sql", "excel", "data analysis"],
    "Web Developer": ["html", "css", "javascript", "git"],
    "QA Tester": ["testing", "python", "sql", "git"]
}

def get_skill_score(student_skills, job_skills):
    matched = []
    missing = []

    for skill in job_skills:
        if skill in student_skills:
            matched.append(skill)
        else:
            missing.append(skill)

    score = (len(matched) / len(job_skills)) * 100
    return score, matched, missing


st.title("🎯 RoleFit AI")
st.write("Find your skill match for entry-level technology roles.")

skill_input = st.text_input(
    "Enter your skills, separated by commas",
    "python, sql, git"
)

selected_role = st.selectbox(
    "Choose a target role",
    list(roles.keys())
)

student_skills = [
    skill.strip().lower()
    for skill in skill_input.split(",")
    if skill.strip()
]

job_skills = roles[selected_role]
score, matched, missing = get_skill_score(student_skills, job_skills)

st.metric("RoleFit score", f"{score:.1f}%")
st.progress(int(score))

if score >= 75:
    st.success("Strong match — you should apply.")
elif score >= 50:
    st.warning("Partial match — learn the missing skills, then apply.")
else:
    st.error("Low match — build more skills before applying.")

left, right = st.columns(2)

with left:
    st.subheader("Matched skills")
    st.write(matched if matched else "No matched skills yet.")

with right:
    st.subheader("Skills to learn")
    st.write(missing if missing else "Great—you have all required skills!")

all_scores = []

for role_name, required_skills in roles.items():
    role_score, _, _ = get_skill_score(student_skills, required_skills)
    all_scores.append({
        "Role": role_name,
        "Match score": role_score
    })

chart_data = pd.DataFrame(all_scores).set_index("Role")
st.subheader("Match scores for all roles")
st.bar_chart(chart_data)
