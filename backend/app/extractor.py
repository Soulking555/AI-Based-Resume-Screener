from sentence_transformers import SentenceTransformer, util
import re

try:
    model = SentenceTransformer('all-MiniLM-L6-v2')
except Exception as e:
    print("Could not load sentence transformer:", e)
    model = None

# Predefined skill database
PREDEFINED_SKILLS = [
    "python", "java", "c++", "c", "c#", "go", "ruby", "rust", "javascript", "typescript",
    "react", "angular", "vue", "svelte", "node.js", "express", "nest.js", "next.js", "nuxt",
    "fastapi", "django", "flask", "spring boot", "asp.net", "laravel", "ruby on rails",
    "docker", "kubernetes", "jenkins", "gitlab ci", "github actions", "terraform", "ansible",
    "aws", "gcp", "azure", "linux", "bash", "powershell", "unix", "shell scripting",
    "sql", "mysql", "postgresql", "mongodb", "redis", "cassandra", "elasticsearch", "dynamodb",
    "machine learning", "deep learning", "nlp", "computer vision", "tensorflow", "pytorch", 
    "scikit-learn", "pandas", "numpy", "matplotlib", "seaborn", "keras", "opencv",
    "git", "agile", "scrum", "jira", "confluence", "trello",
    "html", "css", "sass", "less", "tailwind", "bootstrap", "material ui",
    "php", "swift", "kotlin", "objective-c", "dart", "flutter", "react native",
    "graphql", "rest api", "soap", "grpc", "websockets", "microservices",
    "hadoop", "spark", "kafka", "rabbitmq", "celery", "airflow",
    "cybersecurity", "penetration testing", "cryptography", "blockchain", "solidity",
    "figma", "ui/ux", "photoshop", "illustrator", "wireframing"
]

def extract_skills(text: str) -> list:
    """
    Extracts explicit skills from text using token matching against predefined DB.
    """
    text_lower = text.lower()
    found_skills = set()
    
    for skill in PREDEFINED_SKILLS:
        # Use regex to match whole words safely (avoid matching 'c' inside 'machine')
        # Handle special characters in skills like c++ and node.js
        pattern = r'\b' + re.escape(skill) + r'(?!\w)'
        if re.search(pattern, text_lower):
            found_skills.add(skill)
            
    return list(found_skills)

def calculate_skill_similarity(job_skills: list, candidate_skills: list) -> float:
    """
    Advanced: sentence transformers to measure semantic similarity of skills.
    Returns a score between 0.0 and 1.0.
    """
    if not job_skills:
        return 0.0
        
    if not model or not candidate_skills:
        # Fallback to pure exact match ratio (Jaccard-like subset score)
        intersection = set(job_skills).intersection(set(candidate_skills))
        return len(intersection) / len(job_skills)
        
    # Semantic similarity computing
    j_embeddings = model.encode(job_skills, convert_to_tensor=True)
    c_embeddings = model.encode(candidate_skills, convert_to_tensor=True)
    
    cosine_scores = util.cos_sim(j_embeddings, c_embeddings)
    
    score_sum = 0.0
    for i in range(len(job_skills)):
        # Max semantic similarity for each required job skill to any candidate skill
        max_score = float(max(cosine_scores[i]).item())
        score_sum += max_score
        
    return min(1.0, max(0.0, score_sum / len(job_skills)))

def calculate_jd_similarity(jd_text: str, resume_text: str) -> float:
    """
    Measures semantic similarity between the entire raw Job Description and Resume.
    """
    if not jd_text or not resume_text:
        return 0.0
        
    if not model:
        # Fallback: simple Jaccard on words
        jd_words = set(jd_text.lower().split())
        res_words = set(resume_text.lower().split())
        if not jd_words: return 0.0
        return len(jd_words.intersection(res_words)) / max(len(jd_words), 1)
        
    # Semantic similarity
    jd_emb = model.encode(jd_text, convert_to_tensor=True)
    res_emb = model.encode(resume_text, convert_to_tensor=True)
    
    score = util.cos_sim(jd_emb, res_emb).item()
    return max(0.0, min(1.0, score))
