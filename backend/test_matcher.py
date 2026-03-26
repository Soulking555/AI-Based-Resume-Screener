from app.matcher import generate_explainable_score

result = generate_explainable_score(
    candidate_skills=["python", "react"],
    job_skills=["python", "docker", "machine learning"],
    resume_text="I have 5 years of experience building Python and React applications. Held a Bachelor degree in Computer Science. Worked on several github projects.",
    job_description="We are looking for a software engineer with strong Python skills, experience with Docker, and knowledge of machine learning. A Bachelor's degree and 3+ years experience is required."
)

import json
print(json.dumps(result, indent=2))
