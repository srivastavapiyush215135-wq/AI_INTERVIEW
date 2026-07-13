import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

def generate_questions(resume_text):

    prompt = f"""
You are an expert interviewer.

Read this resume and generate exactly 10 interview questions.

Return ONLY a JSON array.

Example:

[
"Tell me about yourself",
"What is Random Forest?",
"Explain your Predictive Maintenance project"
]

Resume:

{resume_text}
"""

    response = model.generate_content(prompt)

    text = response.text.strip()

    text = text.replace("```json", "")
    text = text.replace("```", "")

    import json

    return json.loads(text)