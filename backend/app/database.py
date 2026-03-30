from pymongo import MongoClient
import os
from pydantic import BaseModel
from typing import List, Optional

# Connect to MongoDB via Environment Variable (or fallback to local)
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)
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
