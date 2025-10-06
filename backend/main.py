from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Base, Student, Assignment, AnalysisResult
from auth import hash_password, verify_password, create_access_token
import os
import requests
import httpx
from rag_service import search_rag_sources


# -------------------
# Environment variables
# -------------------
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://neondb_owner:your_password@ep-aged-water-adbp7t8k-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require")
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "http://n8n:5678/webhook/assignment")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your_jwt_secret")

# -------------------
# Database setup
# -------------------
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base.metadata.create_all(bind=engine)

# -------------------
# Auth setup
# -------------------
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# -------------------
# FastAPI app
# -------------------
app = FastAPI()

# -------------------
# Auth endpoints
# -------------------
@app.post("/auth/register")
def register(email: str, password: str, full_name: str, student_id: str):
    db = SessionLocal()
    if db.query(Student).filter(Student.email==email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = hash_password(password)
    student = Student(email=email, password_hash=hashed, full_name=full_name, student_id=student_id)
    db.add(student)
    db.commit()
    db.close()
    return {"message": "Student registered successfully"}

@app.post("/auth/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db = SessionLocal()
    student = db.query(Student).filter(Student.email==form_data.username).first()
    if not student or not verify_password(form_data.password, student.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": student.email, "role": "student"})
    db.close()
    return {"access_token": token, "token_type": "bearer"}

# -------------------
# Protected endpoints
# -------------------
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL")

@app.post("/assignments/upload")
async def upload_assignment(file: UploadFile = File(...)):
    # Read file content
    file_content = await file.read()

    # Send to n8n webhook
    async with httpx.AsyncClient() as client:
        files = {"file": (file.filename, file_content, file.content_type)}
        response = await client.post(N8N_WEBHOOK_URL, files=files)

    if response.status_code == 200:
        return {"status": "success", "message": "File sent to n8n"}
    else:
        return {"status": "error", "details": response.text}

@app.get("/analysis/{assignment_id}")
def get_analysis(assignment_id: int, token: str = Depends(oauth2_scheme)):
    db = SessionLocal()
    result = db.query(AnalysisResult).filter(AnalysisResult.assignment_id==assignment_id).first()
    db.close()
    if not result:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return result

@app.get("/sources")
async def get_sources(query: str = Query(..., description="Assignment topic or text")):
    results = search_rag_sources(query)
    if not results:
        raise HTTPException(status_code=404, detail="No sources found")
    return {"query": query, "sources": results}


