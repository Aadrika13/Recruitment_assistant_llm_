# resume_parser.py
import PyPDF2
import ollama
from config import OLLAMA_MODEL

def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def parse_resume_with_llm(resume_text):
    prompt = f"""
You are an expert HR assistant. Parse the following resume and extract:

- Name
- Email
- Phone number
- Education
- Skills
- Work Experience
- Certifications

Resume:
{resume_text}
"""
    response = ollama.chat(model=OLLAMA_MODEL, messages=[{"role": "user", "content": prompt}])
    return response["message"]["content"]
