from pymongo import MongoClient
from pydantic import BaseModel
from typing import List, Optional

# Connect to local MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["ai_recruiter_db"]

# Collections
jobs_collection = db["jobs"]
candidates_collection = db["candidates"]
screening_collection = db["screening_results"]

# Pydantic Schemas for FastAPI
class JobCreate(BaseModel):
    title: str
    description: str = ""
    skills: List[str]
    experience: float
    education: str

class CandidateCreate(BaseModel):
    name: str

class ScreeningResultCreate(BaseModel):
    candidate_id: str
    job_id: str
    score: float
    status: str
