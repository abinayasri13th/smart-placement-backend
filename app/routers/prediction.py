from fastapi import APIRouter

router = APIRouter()

@router.get("/info")
def prediction_info():
    return {
        "message": "Placement and salary prediction features are coming soon!",
        "available_features": [
            "ATS Score Analysis",
            "Skill Gap Analysis",
            "Company Recommendations",
            "Resume Parsing",
            "Career Chatbot"
        ]
    }