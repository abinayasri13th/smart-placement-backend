from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()

COMPANY_SALARY = {
    "google":    {"min": 15, "max": 50},
    "amazon":    {"min": 12, "max": 40},
    "microsoft": {"min": 10, "max": 35},
    "zoho":      {"min": 5,  "max": 18},
    "tcs":       {"min": 3.5,"max": 8},
    "infosys":   {"min": 3.5,"max": 8},
}

class PlacementRequest(BaseModel):
    cgpa: float
    skills: List[str]
    internships: int
    projects: int
    backlogs: int
    communication: int  # 1-5

class SalaryRequest(BaseModel):
    cgpa: float
    skills: List[str]
    company: str
    ats_score: float

@router.post("/placement")
def predict_placement(data: PlacementRequest):
    score = 0

    # CGPA scoring
    if data.cgpa >= 9.0:   score += 30
    elif data.cgpa >= 8.0: score += 25
    elif data.cgpa >= 7.0: score += 20
    elif data.cgpa >= 6.0: score += 10
    else:                  score += 5

    # Skills scoring
    score += min(len(data.skills) * 3, 25)

    # Internship scoring
    score += min(data.internships * 10, 20)

    # Projects scoring
    score += min(data.projects * 5, 15)

    # Communication scoring
    score += data.communication * 2

    # Backlogs penalty
    score -= data.backlogs * 10

    # Clamp between 0-100
    probability = max(0, min(score, 100))

    return {
        "placement_probability": probability,
        "predicted": probability >= 50,
        "level": "High" if probability >= 75 else "Medium" if probability >= 50 else "Low",
        "message": f"Your placement probability is {probability}%",
        "tips": [
            "Improve your CGPA above 7.5" if data.cgpa < 7.5 else "Good CGPA!",
            "Add more projects" if data.projects < 2 else "Good projects count!",
            "Get an internship" if data.internships == 0 else "Good internship experience!",
            "Clear any backlogs immediately" if data.backlogs > 0 else "No backlogs — great!",
        ]
    }

@router.post("/salary")
def predict_salary(data: SalaryRequest):
    company = data.company.lower()
    salary_range = COMPANY_SALARY.get(company, {"min": 3, "max": 10})

    base_min = salary_range["min"]
    base_max = salary_range["max"]

    # Calculate predicted salary
    cgpa_factor = data.cgpa / 10
    ats_factor = data.ats_score / 100
    skill_bonus = len(data.skills) * 0.2

    predicted = base_min + (base_max - base_min) * (cgpa_factor * 0.5 + ats_factor * 0.5)
    predicted = round(min(predicted + skill_bonus, base_max), 1)

    return {
        "company": data.company,
        "predicted_salary_lpa": predicted,
        "salary_range": {
            "min": base_min,
            "max": base_max,
            "currency": "INR",
            "unit": "LPA"
        },
        "confidence": "High" if data.ats_score > 70 else "Medium",
        "message": f"Expected salary at {data.company}: {predicted} LPA"
    }

@router.get("/companies")
def company_salaries():
    return {"salary_ranges": COMPANY_SALARY}