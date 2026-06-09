from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()

COMPANIES = {
    "google": {
        "name": "Google",
        "role": "Software Engineer",
        "salary": "15-50 LPA",
        "difficulty": "Very Hard",
        "required_skills": ["python", "algorithms", "data structures", "system design"],
        "preferred_skills": ["machine learning", "golang", "kubernetes"],
        "min_cgpa": 7.5,
    },
    "amazon": {
        "name": "Amazon",
        "role": "SDE-1",
        "salary": "12-40 LPA",
        "difficulty": "Hard",
        "required_skills": ["java", "aws", "python", "sql", "data structures"],
        "preferred_skills": ["docker", "microservices", "kafka"],
        "min_cgpa": 7.0,
    },
    "microsoft": {
        "name": "Microsoft",
        "role": "SDE-1",
        "salary": "10-35 LPA",
        "difficulty": "Hard",
        "required_skills": ["python", "sql", "algorithms", "azure"],
        "preferred_skills": ["c#", "typescript", "dotnet"],
        "min_cgpa": 7.0,
    },
    "zoho": {
        "name": "Zoho",
        "role": "Software Developer",
        "salary": "5-18 LPA",
        "difficulty": "Medium",
        "required_skills": ["java", "sql", "html", "css", "javascript"],
        "preferred_skills": ["react", "spring boot", "mysql"],
        "min_cgpa": 6.0,
    },
    "tcs": {
        "name": "TCS",
        "role": "Systems Engineer",
        "salary": "3.5-8 LPA",
        "difficulty": "Easy",
        "required_skills": ["java", "sql", "communication", "html"],
        "preferred_skills": ["spring", "angular", "jira"],
        "min_cgpa": 6.0,
    },
    "infosys": {
        "name": "Infosys",
        "role": "Systems Engineer",
        "salary": "3.5-8 LPA",
        "difficulty": "Easy",
        "required_skills": ["java", "python", "sql", "communication"],
        "preferred_skills": ["cloud", "react", "nodejs"],
        "min_cgpa": 6.0,
    },
}

class RecommendRequest(BaseModel):
    skills: List[str]
    cgpa: float

@router.post("/recommend")
def recommend_companies(data: RecommendRequest):
    student_skills = [s.lower() for s in data.skills]
    results = []

    for key, company in COMPANIES.items():
        # Check CGPA
        if data.cgpa < company["min_cgpa"]:
            match = 0
        else:
            required = company["required_skills"]
            matched = [s for s in required if s in student_skills]
            match = round(len(matched) / len(required) * 100)

        missing = [s for s in company["required_skills"] if s not in student_skills]

        results.append({
            "name": company["name"],
            "role": company["role"],
            "salary": company["salary"],
            "difficulty": company["difficulty"],
            "match_percentage": match,
            "missing_skills": missing,
            "eligible": data.cgpa >= company["min_cgpa"]
        })

    # Sort by match percentage
    results.sort(key=lambda x: x["match_percentage"], reverse=True)

    return {
        "total_companies": len(results),
        "recommendations": results,
        "best_match": results[0]["name"] if results else None
    }

@router.get("/list")
def get_all_companies():
    return {"companies": list(COMPANIES.values())}

@router.get("/{company_name}")
def get_company(company_name: str):
    company = COMPANIES.get(company_name.lower())
    if not company:
        return {"error": "Company not found"}
    return company