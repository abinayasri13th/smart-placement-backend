from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

COMPANY_KEYWORDS = {
    "google": ["python", "algorithms", "data structures", "system design", "machine learning", "distributed systems"],
    "amazon": ["java", "aws", "microservices", "sql", "leadership", "python", "docker"],
    "microsoft": ["python", "azure", "sql", "c#", "agile", "typescript", "dotnet"],
    "zoho": ["java", "sql", "html", "css", "javascript", "react", "problem solving"],
    "tcs": ["java", "sql", "communication", "html", "testing", "agile"],
    "infosys": ["java", "python", "sql", "communication", "agile", "cloud"],
}

SUGGESTIONS = [
    "Add more quantified achievements (e.g. 'Improved performance by 30%')",
    "Include internship experience with clear impact",
    "Add a strong summary/objective at the top",
    "Use more action verbs: Built, Designed, Optimized, Led",
    "Add your GitHub profile link",
    "Include relevant certifications",
    "Make sure resume is 1 page for freshers",
]

class ATSRequest(BaseModel):
    resume_text: str
    company: str

@router.post("/analyze")
def analyze_ats(data: ATSRequest):
    company = data.company.lower()
    resume = data.resume_text.lower()
    
    keywords = COMPANY_KEYWORDS.get(company, COMPANY_KEYWORDS["tcs"])
    
    matched = [k for k in keywords if k in resume]
    missing = [k for k in keywords if k not in resume]
    
    score = round((len(matched) / len(keywords)) * 100)
    grade = "A" if score >= 80 else "B" if score >= 60 else "C"
    
    return {
        "company": data.company,
        "ats_score": score,
        "grade": grade,
        "matched_keywords": matched,
        "missing_keywords": missing,
        "total_keywords": len(keywords),
        "suggestions": SUGGESTIONS[:5],
        "message": f"Your resume scored {score}/100 for {data.company}"
    }

@router.get("/companies")
def get_companies():
    return {
        "companies": list(COMPANY_KEYWORDS.keys()),
        "message": "Supported companies for ATS analysis"
    }