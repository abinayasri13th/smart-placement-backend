from fastapi import APIRouter, UploadFile, File, HTTPException
from app.ml.resume_parser import parse_resume
from app.ml.ats_scorer import calculate_ats_score
from app.ml.skill_analyzer import analyze_skill_gap
from pydantic import BaseModel
from typing import List

router = APIRouter()

class SkillGapRequest(BaseModel):
    skills: List[str]
    company: str

class ATSTextRequest(BaseModel):
    resume_text: str
    company: str

@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(400, "Only PDF files accepted!")
    contents = await file.read()
    result = parse_resume(contents)
    return result

@router.post("/ats-analyze")
def ats_analyze(data: ATSTextRequest):
    return calculate_ats_score(data.resume_text, data.company)

@router.post("/skill-gap")
def skill_gap(data: SkillGapRequest):
    return analyze_skill_gap(data.skills, data.company)