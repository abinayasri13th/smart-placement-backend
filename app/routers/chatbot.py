from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

RESPONSES = {
    "ats": "ATS score measures how well your resume matches a job description. Aim for 70+ score by adding relevant keywords!",
    "resume": "A good resume should be 1 page, have clear sections, use action verbs, and include quantified achievements.",
    "placement": "To improve placement chances: maintain 7+ CGPA, get an internship, build 2-3 projects, and practice DSA daily.",
    "salary": "Fresher salaries vary by company: Google (15-50 LPA), Amazon (12-40 LPA), TCS/Infosys (3.5-8 LPA).",
    "google": "Google requires strong DSA, system design, and problem-solving skills. Practice on LeetCode daily!",
    "amazon": "Amazon focuses on Leadership Principles + DSA + AWS knowledge. Read their LP stories carefully.",
    "tcs": "TCS hiring is based on aptitude test + technical interview. Focus on Java, SQL, and communication skills.",
    "infosys": "Infosys looks for Java, Python, SQL skills and good communication. Prepare for InfyTQ platform.",
    "zoho": "Zoho has a tough written test. Practice programming, aptitude, and web development basics.",
    "skill": "Build skills based on your target company. Use free resources: YouTube, freeCodeCamp, GeeksforGeeks.",
    "interview": "Common interview tips: research the company, practice STAR method answers, and prepare 5 questions to ask.",
    "cgpa": "CGPA matters for shortlisting. Try to maintain above 7.0 for most companies, 7.5+ for product companies.",
    "project": "Build 2-3 projects relevant to your target role. Deploy them on GitHub and include them in your resume.",
    "internship": "Internships are very important! Apply on LinkedIn, Internshala, and company career pages early.",
    "default": "I'm your AI placement mentor! Ask me about ATS score, resume tips, company requirements, salary, or interview prep."
}

class ChatRequest(BaseModel):
    message: str

@router.post("/message")
def chat(data: ChatRequest):
    message = data.message.lower()

    response = RESPONSES["default"]
    for keyword, reply in RESPONSES.items():
        if keyword in message:
            response = reply
            break

    return {
        "user_message": data.message,
        "bot_response": response,
        "suggestions": [
            "How to improve ATS score?",
            "What skills does Google need?",
            "How to prepare for TCS?",
            "What salary can I expect?"
        ]
    }