# chatbot.py
import ollama
from config import OLLAMA_MODEL

def get_chatbot_response(resume_info, question, history):
    # Combine chat history and resume info into the prompt
    history_prompt = "\n".join([f"Q: {q}\nA: {a}" for q, a in history])

    prompt = f"""
You are a virtual assistant helping with recruitment. 
Use the following parsed resume info to answer recruiter questions.

Resume Info:
{resume_info}

Conversation History:
{history_prompt}

Now answer the next question clearly and professionally:
Q: {question}
"""

    response = ollama.chat(
        model=OLLAMA_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]
