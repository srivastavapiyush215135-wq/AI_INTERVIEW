from fastapi import FastAPI, UploadFile, File
from backend.resume_parser import extract_text_from_pdf
from backend.interview import generate_questions
from backend.evaluator import evaluate_answer
from pydantic import BaseModel
from backend.database import engine
from backend.models import Base
from fastapi import Depends
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Interview

Base.metadata.create_all(bind=engine)
import shutil
import os

app = FastAPI()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.get("/")
def home():
    return {"message": "AI Interview Platform Backend Running Successfully!"}

@app.post("/upload-resume/")
async def upload_resume(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    extracted_text = extract_text_from_pdf(file_path)

    questions = generate_questions(extracted_text)

    return {
        "filename": file.filename,
        "resume_text": extracted_text,
        "interview_questions": questions
    }
class InterviewRequest(BaseModel):
    candidate: str
    role: str
    question: str
    answer: str


@app.post("/evaluate-answer/")
async def evaluate(
    request: InterviewRequest,
    db: Session = Depends(get_db)
):

    feedback = evaluate_answer(
        request.question,
        request.answer
    )

    record = Interview(
        candidate=request.candidate,
        role=request.role,
        resume_text="",
        questions=request.question,
        answers=request.answer,
        score=0,
        feedback=feedback
    )

    db.add(record)
    db.commit()

    return {
        "feedback": feedback
    }