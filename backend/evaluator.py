import google.generativeai as genai
from backend.config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

def evaluate_answer(question, answer):

    prompt = f"""
You are an expert interviewer.

Question:
{question}

Candidate Answer:
{answer}

Evaluate on:

1. Technical Accuracy (/10)
2. Communication (/10)
3. Completeness (/10)

Provide:
- Overall Score (/10)
- Strengths
- Weaknesses
- Suggestions
"""

    response = model.generate_content(prompt)

    return response.text