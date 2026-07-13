from sqlalchemy import Column, Integer, String, Text
from backend.database import Base

class Interview(Base):
    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True, index=True)
    candidate = Column(String(100))
    role = Column(String(100))
    resume_text = Column(Text)
    questions = Column(Text)
    answers = Column(Text)
    score = Column(Integer)
    feedback = Column(Text)