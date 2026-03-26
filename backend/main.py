import os
import shutil
import json
from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from bson import ObjectId

from app.parser import parse_resume
from app.extractor import extract_skills
from app.matcher import generate_explainable_score
from app.database import jobs_collection, candidates_collection, screening_collection
from app.clustering import run_clustering
from app.interview import generate_interview_questions

app = FastAPI(title="AI Hiring Intelligence Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class JobCreate(BaseModel):
    title: str
    description: str = ""
    skills: List[str]
    experience: float
    education: str

@app.post("/api/jobs")
def create_job(job: JobCreate):
    job_data = {
        "title": job.title,
        "description": job.description,
        "skills": job.skills,
        "experience": job.experience,
        "education": job.education
    }
    result = jobs_collection.insert_one(job_data)
    return {"id": str(result.inserted_id), "message": "Job created successfully"}

@app.get("/api/jobs")
def list_jobs():
    jobs = []
    for doc in jobs_collection.find():
        doc["id"] = str(doc.pop("_id"))
        jobs.append(doc)
    return jobs

@app.post("/api/upload_resume")
async def upload_resume(
    job_id: str = Form(...),
    candidate_name: str = Form(...),
    file: UploadFile = File(...)
):
    # Verify Job
    try:
        if job_id != "1": # Fallback for mock job id from frontend
            job_record = jobs_collection.find_one({"_id": ObjectId(job_id)})
        else:
            job_record = jobs_collection.find_one() # grab any available job if ID equals 1 mock
    except Exception:
        job_record = None

    if not job_record:
        raise HTTPException(status_code=404, detail="Job not found")
        
    job_skills_required = job_record.get('skills', [])
    job_description = job_record.get('description', "")
    
    # Save PDF
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Phase 4 Step 1: Parse Text
    parsed_text = parse_resume(file_path)
    
    # Phase 4 Step 2: Extract Skills
    candidate_skills = extract_skills(parsed_text)
    
    # Phase 4 Step 3 & Phase 6 Inn 2: Matching + Explainability + Skill Gap + JD Match
    eval_result = generate_explainable_score(
        candidate_skills=candidate_skills,
        job_skills=job_skills_required,
        resume_text=parsed_text,
        job_description=job_description
    )
    
    final_score = eval_result["final_score"]
    
    # Determine Status
    if final_score >= 70:
        status = "Shortlisted"
    elif final_score < 40:
        status = "Rejected"
    else:
        status = "Pending"
        
    date_str = datetime.now().isoformat()
    
    # Insert Candidate
    candidate_data = {
        "name": candidate_name,
        "resume_text": parsed_text,
        "skills": candidate_skills,
        "experience": eval_result["explainable_breakdown"]["experience"],
        "education": eval_result["explainable_breakdown"]["education"],
        "score": final_score,
        "missing_skills": eval_result["missing_skills"],
        "recommendation": eval_result["recommendation"],
        "date": date_str
    }
    cand_result = candidates_collection.insert_one(candidate_data)
    candidate_id_str = str(cand_result.inserted_id)
    
    # Insert Screening Result
    screening_collection.insert_one({
        "candidate_id": candidate_id_str,
        "job_id": str(job_record["_id"]),
        "score": final_score,
        "status": status
    })
    
    return {
        "candidate_id": candidate_id_str,
        "name": candidate_name,
        "score": final_score,
        "status": status,
        "evaluation": eval_result
    }

@app.get("/api/dashboard/stats")
def get_dashboard_stats():
    total = screening_collection.count_documents({})
    shortlisted = screening_collection.count_documents({"status": "Shortlisted"})
    rejected = screening_collection.count_documents({"status": "Rejected"})
    pending = screening_collection.count_documents({"status": "Pending"})
    
    return {
        "total": total,
        "shortlisted": shortlisted,
        "rejected": rejected,
        "pending": pending
    }

@app.get("/api/candidates")
def list_candidates(search: str = "", min_score: float = 0.0):
    query = {"score": {"$gte": min_score}}
    if search:
        query["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"skills": {"$regex": search, "$options": "i"}}
        ]
        
    cursor = candidates_collection.find(query)
    
    candidates = []
    for doc in cursor:
        d = dict(doc)
        d["id"] = str(d.pop("_id"))
        d['skills'] = d.get('skills', [])
        d['missing_skills'] = d.get('missing_skills', [])
        d['interview_questions'] = generate_interview_questions(d['missing_skills'])
        candidates.append(d)
        
    return candidates

@app.post("/api/cluster")
def cluster_candidates():
    """ Runs KMeans clustering based on resume texts """
    result = run_clustering(num_clusters=3)
    return result
