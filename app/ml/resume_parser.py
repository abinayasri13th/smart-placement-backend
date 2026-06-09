import re
import spacy
from pdfminer.high_level import extract_text
import io

nlp = spacy.load("en_core_web_sm")

SKILLS_DATABASE = [
    "python", "java", "javascript", "react", "nodejs", "sql", "mysql",
    "postgresql", "mongodb", "html", "css", "git", "docker", "aws",
    "azure", "machine learning", "deep learning", "tensorflow", "pytorch",
    "scikit-learn", "pandas", "numpy", "flask", "fastapi", "django",
    "spring boot", "hibernate", "angular", "vue", "typescript", "c++",
    "c#", "kotlin", "swift", "flutter", "android", "ios", "linux",
    "agile", "jira", "kubernetes", "jenkins", "ci/cd", "rest api",
    "graphql", "redis", "kafka", "microservices", "system design"
]

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    try:
        pdf_file = io.BytesIO(pdf_bytes)
        text = extract_text(pdf_file)
        return text
    except Exception as e:
        return ""

def extract_email(text: str) -> str:
    emails = re.findall(r'[\w.+-]+@[\w-]+\.[\w.]+', text)
    return emails[0] if emails else ""

def extract_phone(text: str) -> str:
    phones = re.findall(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', text)
    return phones[0] if phones else ""

def extract_skills(text: str) -> list:
    text_lower = text.lower()
    found_skills = []
    for skill in SKILLS_DATABASE:
        if skill.lower() in text_lower:
            found_skills.append(skill)
    return found_skills

def extract_name(text: str) -> str:
    doc = nlp(text[:500])
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    lines = text.strip().split('\n')
    for line in lines[:5]:
        line = line.strip()
        if len(line) > 2 and len(line) < 50:
            return line
    return ""

def parse_resume(pdf_bytes: bytes) -> dict:
    text = extract_text_from_pdf(pdf_bytes)
    if not text:
        return {"error": "Could not extract text from PDF"}

    name = extract_name(text)
    email = extract_email(text)
    phone = extract_phone(text)
    skills = extract_skills(text)

    return {
        "name": name,
        "email": email,
        "phone": phone,
        "skills": skills,
        "skills_count": len(skills),
        "raw_text": text[:500],
        "message": "Resume parsed successfully!"
    }