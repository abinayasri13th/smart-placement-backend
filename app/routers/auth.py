from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json, hashlib

router = APIRouter()

# Store users in memory AND file
USERS = []
USERS_FILE = r"C:\Users\LENOVO\Desktop\smart-placement-backend\users.json"

def save():
    with open(USERS_FILE, "w") as f:
        json.dump(USERS, f, indent=2)

def load():
    global USERS
    try:
        with open(USERS_FILE, "r") as f:
            USERS = json.load(f)
    except:
        USERS = []

load()

def hashpw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str
    college: str = ""
    branch: str = ""
    year: str = ""

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/register")
def register(data: RegisterRequest):
    load()
    for u in USERS:
        if u["email"] == data.email:
            raise HTTPException(status_code=400, detail="Email already exists!")
    user = {
        "id": len(USERS) + 1,
        "name": data.name,
        "email": data.email,
        "password": hashpw(data.password),
        "college": data.college,
        "branch": data.branch,
        "year": data.year
    }
    USERS.append(user)
    save()
    return {"message": "Account created!", "name": data.name, "email": data.email, "token": f"token_{user['id']}"}

@router.post("/login")
def login(data: LoginRequest):
    load()
    for u in USERS:
        if u["email"] == data.email:
            if u["password"] == hashpw(data.password):
                return {"message": "Login successful", "name": u["name"], "email": u["email"], "token": f"token_{u['id']}"}
            else:
                raise HTTPException(status_code=401, detail="Wrong password!")
    raise HTTPException(status_code=404, detail="Email not found! Please signup first.")