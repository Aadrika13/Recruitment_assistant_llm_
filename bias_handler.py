# bias_handler.py

import re

def anonymize_resume(resume_text):
    # Remove names, emails, phones, genders (basic simulation)
    text = re.sub(r'\b(Name|Gender|Email|Phone)[^\n]*', '', resume_text, flags=re.I)
    text = re.sub(r'\b(Mr\.|Mrs\.|Ms\.|Dr\.)', '', text)
    text = re.sub(r'\b(Male|Female|She|He|Her|His)\b', '', text, flags=re.I)
    return text.strip()
