from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

COMPANY_JOB_DESCRIPTIONS = {
    "google": """python algorithms data structures system design machine learning
    distributed systems problem solving coding computer science software engineer
    golang kubernetes bigquery tensorflow artificial intelligence""",

    "amazon": """java aws python sql data structures algorithms microservices
    docker leadership principles distributed systems backend software development
    kafka dynamodb system design problem solving""",

    "microsoft": """python azure sql c# agile typescript dotnet software engineer
    algorithms data structures system design cloud computing visual studio""",

    "zoho": """java sql html css javascript react problem solving web development
    spring boot mysql git communication teamwork software developer""",

    "tcs": """java sql html communication testing agile software development
    problem solving teamwork spring hibernate angular jira""",

    "infosys": """java python sql communication agile cloud devops react nodejs
    software development problem solving teamwork leadership"""
}

def calculate_ats_score(resume_text: str, company: str) -> dict:
    company = company.lower()
    jd = COMPANY_JOB_DESCRIPTIONS.get(company, COMPANY_JOB_DESCRIPTIONS["tcs"])

    vectorizer = TfidfVectorizer(stop_words='english')
    try:
        tfidf_matrix = vectorizer.fit_transform([resume_text.lower(), jd.lower()])
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        score = round(float(similarity[0][0]) * 100, 1)
    except:
        score = 0

    score = min(score * 2.5, 100)

    jd_words = set(jd.lower().split())
    resume_words = set(resume_text.lower().split())
    matched = list(jd_words & resume_words)[:15]
    missing = list(jd_words - resume_words)[:15]

    grade = "A" if score >= 80 else "B" if score >= 60 else "C" if score >= 40 else "D"

    suggestions = []
    if score < 80:
        suggestions.append("Add more relevant keywords from the job description")
    if len(resume_text) < 500:
        suggestions.append("Add more detail to your resume")
    suggestions.append("Use action verbs: Built, Designed, Developed, Led")
    suggestions.append("Add quantified achievements (e.g. 'Improved speed by 30%')")
    suggestions.append("Include relevant projects with tech stack details")

    return {
        "ats_score": round(score, 1),
        "grade": grade,
        "matched_keywords": matched,
        "missing_keywords": missing,
        "suggestions": suggestions,
        "message": f"ATS Score: {round(score, 1)}/100 for {company.title()}"
    }