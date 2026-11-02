import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="RoleFit AI", page_icon="🎯")

roles = {
    "Data Analyst": ["python", "sql", "excel", "data analysis"],
    "Web Developer": ["html", "css", "javascript", "git"],
    "QA Tester": ["testing", "python", "sql", "git"]
}

role_descriptions = {
    "Data Analyst": """
        Junior data analyst role requiring Python, SQL, Excel,
        data cleaning, data analysis, visualization and communication.
    """,
    "Web Developer": """
        Junior web developer role requiring HTML, CSS, JavaScript,
        Git, responsive web design and problem solving.
    """,
    "QA Tester": """
        Junior QA tester role requiring manual testing, Python,
        SQL, Git, bug reporting and attention to detail.
    """
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


def get_nlp_score(student_profile, job_description):
    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )

    vectors = vectorizer.fit_transform(
        [student_profile, job_description]
    )

    return cosine_similarity(vectors[0], vectors[1])[0, 0] * 100


st.title("🎯 RoleFit AI")
st.write("Find your skill match for entry-level technology roles.")

skill_input = st.text_input(
    "Enter your skills, separated by commas",
    "python, sql, git"
)

profile_text = st.text_area(
    "Write a short profile summary",
    "I know Python, SQL and Git. I am a Diploma Computer Engineering student interested in data analysis."
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

skill_score, matched, missing = get_skill_score(
    student_skills,
    job_skills
)

nlp_score = get_nlp_score(
    profile_text,
    role_descriptions[selected_role]
)

final_score = (0.65 * skill_score) + (0.35 * nlp_score)

st.metric("Final RoleFit score", f"{final_score:.1f}%")
st.progress(int(final_score))

first, second = st.columns(2)

with first:
    st.metric("Exact skill match", f"{skill_score:.1f}%")

with second:
    st.metric("NLP text similarity", f"{nlp_score:.1f}%")

st.caption(
    "Final score = 65% exact skill match + 35% NLP text similarity."
)

if final_score >= 75:
    st.success("Strong match — you should apply.")
elif final_score >= 50:
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
    role_skill_score, _, _ = get_skill_score(
        student_skills,
        required_skills
    )

    role_nlp_score = get_nlp_score(
        profile_text,
        role_descriptions[role_name]
    )

    role_final_score = (
        0.65 * role_skill_score
        + 0.35 * role_nlp_score
    )

    all_scores.append({
        "Role": role_name,
        "Match score": role_final_score
    })

chart_data = pd.DataFrame(all_scores).set_index("Role")

st.subheader("Match scores for all roles")
st.bar_chart(chart_data)
