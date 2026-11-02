# 🎯 RoleFit AI

[Open the live app](https://rolefit-ai-new.streamlit.app/)

RoleFit AI is an explainable web app that helps Diploma and entry-level students compare their skills and profile summary with technology roles.

## Features

- Matches a student's skills with job requirements
- Shows matched and missing skills
- Calculates an exact skill-match score
- Uses NLP text similarity with TF-IDF and cosine similarity
- Combines both scores into a transparent final score
- Ranks Data Analyst, Web Developer, and QA Tester roles
- Displays a comparison chart

## How it works

1. The user enters skills and a short profile summary.
2. The app checks exact matches against required role skills.
3. TF-IDF converts the profile and role description into numeric text features.
4. Cosine similarity calculates text similarity.
5. The final score is calculated as:

```text
Final score = 65% exact skill match + 35% NLP text similarity
