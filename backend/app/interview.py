def generate_interview_questions(missing_skills: list) -> list:
    """
    Innovation 4: Interview Question Generator based on missing skills.
    """
    questions = []
    templates = {
        "python": ["Explain decorators in Python.", "What is the GIL in Python?"],
        "machine learning": ["Explain the tradeoff between bias and variance.", "How do you handle overfitting?", "What is cross-validation?"],
        "nlp": ["Explain tokenization and Named Entity Recognition.", "What are word embeddings and how do they work?"],
        "docker": ["What is the difference between a container and an image?", "Explain Docker volumes."],
        "react": ["What is the virtual DOM?", "Explain useEffect hook in React."],
        "java": ["Explain object-oriented concepts.", "What is the JVM?"],
        "kubernetes": ["What is a Pod in Kubernetes?", "Explain how services route traffic in K8s."],
        "aws": ["What is the difference between EC2 and ECS?", "Explain S3 storage classes."]
    }
    
    for skill in missing_skills:
        skill_lower = skill.lower()
        if skill_lower in templates:
            questions.extend(templates[skill_lower])
        else:
            questions.append(f"How would you approach learning {skill}?")
            questions.append(f"Can you describe a scenario where you might use {skill}?")
            
    return questions[:5] # Limit to 5 questions
