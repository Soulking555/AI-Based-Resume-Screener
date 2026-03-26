from app.extractor import calculate_skill_similarity, calculate_jd_similarity
import re

def evaluate_experience(text: str) -> float:
    """
    Rudimentary baseline logic to score experience from raw text.
    In a full ML system, this would be an NER model extracting temporal values.
    Returns 0.0 to 1.0
    """
    text_lower = text.lower()
    
    # Look for years experience keywords
    years_pattern = r'(\d+)\+?\s+years'
    matches = re.findall(years_pattern, text_lower)
    
    max_years = 0
    if matches:
        max_years = max([int(m) for m in matches])
    
    # Simple curve: 0 years = 0.2, 5+ years = 1.0
    if max_years >= 5: return 1.0
    if max_years >= 3: return 0.8
    if max_years >= 1: return 0.5
    
    # Secondary check: mention of "experience" section
    if "experience" in text_lower:
        return 0.4
        
    return 0.1

def evaluate_education(text: str) -> float:
    """
    Score education presence and degree levels. 0.0 to 1.0.
    """
    text_lower = text.lower()
    score = 0.0
    if "phd" in text_lower or "ph.d" in text_lower:
        score = 1.0
    elif "master" in text_lower or "m.s" in text_lower or "ms " in text_lower or "m.sc" in text_lower:
        score = 0.85
    elif "bachelor" in text_lower or "b.s" in text_lower or "bs " in text_lower or "b.sc" in text_lower:
        score = 0.70
    elif "education" in text_lower or "university" in text_lower or "college" in text_lower:
        score = 0.50
    return score

def evaluate_projects(text: str) -> float:
    """
    Score project involvement based on keyword evidence.
    """
    text_lower = text.lower()
    if "projects" in text_lower and ("github" in text_lower or "portfolio" in text_lower):
        return 0.9
    if "projects" in text_lower:
        return 0.6
    return 0.3

def generate_explainable_score(
    candidate_skills: list, 
    job_skills: list, 
    resume_text: str,
    job_description: str = ""
) -> dict:
    """
    Generates explainable score logic requested:
    Final Score = 0.4 skill + 0.2 similarity + 0.2 experience + 0.1 education + 0.1 projects
    (If job_description is provided, redistributes to include 0.2 JD similarity)
    """
    # 1. Skill Score (Direct Match Ratio)
    matched_skills = set(candidate_skills).intersection(set(job_skills))
    skill_score_raw = len(matched_skills) / len(job_skills) if job_skills else 1.0
    
    # 2. Semantic Similarity Score
    similarity_score_raw = calculate_skill_similarity(job_skills, candidate_skills)
    
    # 3. Experience Score
    experience_score_raw = evaluate_experience(resume_text)
    
    # 4. Education Score
    education_score_raw = evaluate_education(resume_text)
    
    # 5. Projects Score
    projects_score_raw = evaluate_projects(resume_text)
    
    # 6. JD Similarity Score
    jd_match_score_raw = calculate_jd_similarity(job_description, resume_text) if job_description else 0.0
    
    # Weights sum to 1.0
    if job_description:
        final_score = (
            0.20 * skill_score_raw +
            0.20 * similarity_score_raw +
            0.20 * jd_match_score_raw +
            0.20 * experience_score_raw +
            0.10 * education_score_raw +
            0.10 * projects_score_raw
        )
    else:
        final_score = (
            0.40 * skill_score_raw +
            0.20 * similarity_score_raw +
            0.20 * experience_score_raw +
            0.10 * education_score_raw +
            0.10 * projects_score_raw
        )
    
    # Identify gaps
    missing_skills = list(set(job_skills) - set(candidate_skills))
    
    # Generate Recommendation Logic (Innovation 1 Preview)
    recommendation = []
    if missing_skills:
        recommendation.append(f"Learn {', '.join(missing_skills[:3])}")
    if experience_score_raw < 0.5:
        recommendation.append("Highlight more years of experience or practical roles.")
    if not recommendation:
        recommendation.append("Strong candidate. Ready for technical interview.")
        
    return {
        "final_score": round(final_score * 100, 1),
        "explainable_breakdown": {
            "skill_match": round((0.20 if job_description else 0.40) * skill_score_raw * 100, 1),
            "similarity": round(0.20 * similarity_score_raw * 100, 1),
            "jd_match": round(0.20 * jd_match_score_raw * 100, 1) if job_description else 0.0,
            "experience": round(0.20 * experience_score_raw * 100, 1),
            "education": round(0.10 * education_score_raw * 100, 1),
            "projects": round(0.10 * projects_score_raw * 100, 1)
        },
        "matched_skills": list(matched_skills),
        "missing_skills": missing_skills,
        "recommendation": "; ".join(recommendation)
    }
