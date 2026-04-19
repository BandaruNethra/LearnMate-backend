import json
import os
import random
import httpx
import asyncio
import email.utils
import zipfile
import io
from datetime import datetime, timezone
from typing import List

from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from bs4 import BeautifulSoup
from groq import Groq

# Internal Imports
import database, models, ai_engine, auth
from ai_engine import generate_learning_response

# --- 1. INITIALIZATION ---
app = FastAPI()

# Initialize Groq client (Ensure your ENV variable is set on Render)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# --- 2. CORS MIDDLEWARE (Must stay at the top) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Debug route to verify deployment
@app.get("/debug-cors")
async def debug_cors():
    return {"status": "Force active", "message": "Backend is finally updated", "timestamp": str(datetime.now())}

# Database Tables
models.Base.metadata.create_all(bind=database.engine)

# --- 3. DATA MODELS ---
class UserCreate(BaseModel):
    email: str
    full_name: str
    password: str
    skill_level: str

class UserLogin(BaseModel):
    email: str
    password: str

class QuestionRequest(BaseModel):
    user_id: int
    question: str

class ChatRequest(BaseModel):
    user_id: int
    message: str

class ProgressUpdate(BaseModel):
    user_id: int
    course_id: str
    score: int
    status: str

# --- 4. AUTH ROUTES ---

@app.post("/signup")
def signup(user_data: UserCreate, db: Session = Depends(database.get_db)):
    existing = db.query(models.User).filter(models.User.email == user_data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = models.User(
        full_name=user_data.full_name,
        email=user_data.email,
        hashed_password=auth.hash_password(user_data.password),
        skill_level=user_data.skill_level
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    token = auth.create_access_token({"sub": new_user.email, "id": new_user.id})
    return {"access_token": token, "token_type": "bearer", "user": {"id": new_user.id, "full_name": new_user.full_name, "email": new_user.email}}

@app.post("/login")
def login(user_data: UserLogin, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_data.email).first()
    if not user or not auth.verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    token = auth.create_access_token({"sub": user.email, "id": user.id})
    return {"access_token": token, "token_type": "bearer", "user": {"id": user.id, "email": user.email, "full_name": user.full_name}}

# --- 5. CORE LOGIC ROUTES ---

@app.get("/")
def health_check():
    return {"status": "LearnMate Backend is Running"}

@app.get("/user/{user_id}")
def get_user_profile(user_id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "id": user.id,
        "username": user.full_name,
        "skill_level": user.skill_level,
        "progress": user.progress or 0
    }

@app.post("/chat")
async def chat(request: ChatRequest, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == request.user_id).first()
    user_context = user.interests if (user and user.interests) else "General Programming"
    ai_text = generate_learning_response(request.message, user_context)
    return {"response": ai_text}

@app.get("/generate-quiz/{course_title}")
async def generate_quiz(course_title: str):
    random_seed = random.randint(1, 1000)
    prompt = f"Create a professional 10-question JSON quiz for: {course_title}. Seed: {random_seed}. Return ONLY JSON."
    try:
        completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192", 
            response_format={"type": "json_object"}
        )
        return json.loads(completion.choices[0].message.content)
    except Exception:
        return {"questions": [{"q": f"Basic check for {course_title}", "a": ["Yes", "No"], "correct": "Yes", "level": "Easy"}]}

# --- 6. NEWS & HACKATHONS ---

@app.get("/api/news")
async def get_mega_news():
    categories = {"TECH": "https://news.google.com/rss/search?q=technology+india+when:1d&hl=en-IN&gl=IN&ceid=IN:en"}
    all_headlines = []
    async with httpx.AsyncClient(timeout=10.0) as client_http:
        for cat, url in categories.items():
            try:
                r = await client_http.get(url)
                soup = BeautifulSoup(r.text, "html.parser")
                for item in soup.find_all("item")[:10]:
                    all_headlines.append({"title": item.title.text, "link": item.link.text, "source": cat})
            except: pass
    return {"headlines": all_headlines}

db_hackathons = []

@app.post("/sync-hackathons")
async def sync_hackathons():
    global db_hackathons
    db_hackathons = [
        {"title": "Google Girl Hackathon 2026", "organizer": "Google", "link": "https://buildyourfuture.withgoogle.com/"},
        {"title": "AI Global Build", "organizer": "Meta", "link": "https://devpost.com"}
    ]
    return {"message": "Sync complete"}

@app.get("/get-hackathons")
async def get_hackathons():
    return db_hackathons if db_hackathons else []

# --- 7. BACKGROUND TASKS ---

@app.on_event("startup")
async def schedule_daily_tasks():
    async def periodic_sync():
        while True:
            await sync_hackathons()
            await asyncio.sleep(86400)
    asyncio.create_task(periodic_sync())