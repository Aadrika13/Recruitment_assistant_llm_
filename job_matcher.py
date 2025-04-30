# job_matcher.py
import ollama
from config import OLLAMA_MODEL

def match_resume_to_job(resume_info, job_description):
    prompt = f"""
You are an HR expert. Given the parsed resume info and a job description, do the following:
1. Compare the resume to the job description.
2. Score the match out of 100.
3. Explain the match in 3-4 bullet points.
4. Suggest one improvement for the candidate.

Resume Info:
{resume_info}

Job Description:
{job_description}

Return this in a JSON format like:
{{
    "match_score": 85,
    "analysis": ["...bullet 1", "...bullet 2"],
    "suggestion": "..."
}}
"""
    response = ollama.chat(model=OLLAMA_MODEL, messages=[{"role": "user", "content": prompt}])
    return response["message"]["content"]
