from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()

COMPANY_SKILLS = {
    "google":    {"required": ["python","algorithms","data structures","system design","machine learning"], "preferred": ["golang","kubernetes","bigquery"]},
    "amazon":    {"required": ["java","aws","python","sql","data structures"], "preferred": ["docker","kafka","microservices"]},
    "microsoft": {"required": ["python","sql","azure","algorithms"], "preferred": ["c#","typescript","dotnet"]},
    "zoho":      {"required": ["java","sql","html","css","javascript"], "preferred": ["react","spring boot","mysql"]},
    "tcs":       {"required": ["java","sql","communication","html","testing"], "preferred": ["spring","angular","jira"]},
    "infosys":   {"required": ["java","python","sql","communication","agile"], "preferred": ["cloud","react","nodejs"]},
}

ROADMAPS = {
    "google":    ["Master DSA (6 weeks)", "System Design (4 weeks)", "Python advanced (2 weeks)", "ML basics (4 weeks)", "Mock interviews (2 weeks)"],
    "amazon":    ["Java mastery (3 weeks)", "AWS certification (4 weeks)", "DSA practice (4 weeks)", "System Design (3 weeks)", "Leadership principles (1 week)"],
    "microsoft": ["Python + Azure (3 weeks)", "SQL advanced (2 weeks)", "DSA practice (3 weeks)", "C# basics (2 weeks)", "Mock interviews (2 weeks)"],
    "zoho":      ["Java + OOP (2 weeks)", "SQL mastery (1 week)", "React frontend (2 weeks)", "Spring Boot (2 weeks)", "Mini project (1 week)"],
    "tcs":       ["Java basics (2 weeks)", "SQL practice (1 week)", "Communication skills (1 week)", "Aptitude prep (2 weeks)", "Mock interviews (1 week)"],
    "infosys":   ["Java + Python (2 weeks)", "SQL practice (1 week)", "Cloud basics (2 weeks)", "Agile methodology (1 week)", "Mock interviews (1 week)"],
}

class SkillGapRequest(BaseModel):
    skills: List[str]
    company: str

@router.post("/analyze")
def skill_gap(data: SkillGapRequest):
    company = data.company.lower()
    student_skills = [s.lower() for s in data.skills]
    company_data = COMPANY_SKILLS.get(company, COMPANY_SKILLS["tcs"])

    required = company_data["required"]
    preferred = company_data["preferred"]

    matched = [s for s in required if s in student_skills]
    missing_required = [s for s in required if s not in student_skills]
    missing_preferred = [s for s in preferred if s not in student_skills]

    match_pct = round(len(matched) / len(required) * 100)

    return {
        "company": data.company,
        "match_percentage": match_pct,
        "readiness": "High" if match_pct >= 80 else "Medium" if match_pct >= 50 else "Low",
        "matched_skills": matched,
        "missing_required_skills": missing_required,
        "missing_preferred_skills": missing_preferred,
        "roadmap": ROADMAPS.get(company, ROADMAPS["tcs"]),
        "estimated_prep_time": "6-8 weeks" if match_pct >= 50 else "3-4 months"
    }