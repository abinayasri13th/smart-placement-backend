from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, ats, prediction, company, skillgap, chatbot, resume, jobanalyzer

app = FastAPI(title="QuickShot Placement API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router,        prefix="/api/v1/auth",        tags=["Authentication"])
app.include_router(ats.router,         prefix="/api/v1/ats",         tags=["ATS Analysis"])
app.include_router(prediction.router,  prefix="/api/v1/prediction",  tags=["Prediction"])
app.include_router(company.router,     prefix="/api/v1/company",     tags=["Company"])
app.include_router(skillgap.router,    prefix="/api/v1/skills",      tags=["Skill Gap"])
app.include_router(chatbot.router,     prefix="/api/v1/chatbot",     tags=["Chatbot"])
app.include_router(resume.router,      prefix="/api/v1/resume",      tags=["Resume ML"])
app.include_router(jobanalyzer.router, prefix="/api/v1/jobanalyzer", tags=["Job Analyzer"])

@app.get("/")
def root():
    return {"message": "QuickShot Placement API is running!"}

@app.get("/health")
def health():
    return {"status": "healthy", "version": "1.0.0"}