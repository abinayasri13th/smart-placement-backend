COMPANY_REQUIRED_SKILLS = {
    "google": {
        "required": ["python", "algorithms", "data structures", "system design", "machine learning"],
        "preferred": ["golang", "kubernetes", "tensorflow", "bigquery"],
        "roadmap": [
            "Master DSA — Arrays, Trees, Graphs (6 weeks)",
            "System Design fundamentals (4 weeks)",
            "Python advanced concepts (2 weeks)",
            "Machine Learning basics (4 weeks)",
            "Practice 200+ LeetCode problems (ongoing)"
        ]
    },
    "amazon": {
        "required": ["java", "aws", "python", "sql", "data structures"],
        "preferred": ["docker", "kafka", "microservices", "dynamodb"],
        "roadmap": [
            "Java mastery + OOP concepts (3 weeks)",
            "AWS Cloud Practitioner certification (4 weeks)",
            "DSA practice daily (ongoing)",
            "System Design (3 weeks)",
            "Study Amazon Leadership Principles (1 week)"
        ]
    },
    "microsoft": {
        "required": ["python", "sql", "azure", "algorithms"],
        "preferred": ["c#", "typescript", "dotnet"],
        "roadmap": [
            "Python + SQL mastery (2 weeks)",
            "Azure Fundamentals certification (3 weeks)",
            "DSA practice (3 weeks)",
            "C# basics (2 weeks)",
            "Mock interviews (2 weeks)"
        ]
    },
    "zoho": {
        "required": ["java", "sql", "html", "css", "javascript"],
        "preferred": ["react", "spring boot", "mysql"],
        "roadmap": [
            "Java + OOP mastery (2 weeks)",
            "SQL advanced queries (1 week)",
            "React frontend (2 weeks)",
            "Spring Boot backend (2 weeks)",
            "Build 2 full stack projects (2 weeks)"
        ]
    },
    "tcs": {
        "required": ["java", "sql", "communication", "html", "testing"],
        "preferred": ["spring", "angular", "jira"],
        "roadmap": [
            "Java basics + OOP (2 weeks)",
            "SQL practice (1 week)",
            "Communication skills (1 week)",
            "Aptitude preparation (2 weeks)",
            "Mock interviews (1 week)"
        ]
    },
    "infosys": {
        "required": ["java", "python", "sql", "communication", "agile"],
        "preferred": ["cloud", "react", "nodejs"],
        "roadmap": [
            "Java + Python basics (2 weeks)",
            "SQL practice (1 week)",
            "Cloud basics AWS/Azure (2 weeks)",
            "Agile methodology (1 week)",
            "Mock interviews (1 week)"
        ]
    }
}

def analyze_skill_gap(student_skills: list, company: str) -> dict:
    company = company.lower()
    company_data = COMPANY_REQUIRED_SKILLS.get(company, COMPANY_REQUIRED_SKILLS["tcs"])

    student_skills_lower = [s.lower() for s in student_skills]
    required = company_data["required"]
    preferred = company_data["preferred"]

    matched = [s for s in required if s in student_skills_lower]
    missing_required = [s for s in required if s not in student_skills_lower]
    missing_preferred = [s for s in preferred if s not in student_skills_lower]

    match_pct = round(len(matched) / len(required) * 100) if required else 0
    readiness = "High" if match_pct >= 80 else "Medium" if match_pct >= 50 else "Low"

    return {
        "company": company.title(),
        "match_percentage": match_pct,
        "readiness_level": readiness,
        "matched_skills": matched,
        "missing_required_skills": missing_required,
        "missing_preferred_skills": missing_preferred,
        "roadmap": company_data["roadmap"],
        "estimated_prep_time": "4-6 weeks" if match_pct >= 60 else "2-3 months"
    }