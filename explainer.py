# explainer.py

def generate_explanation(match_result):
    score = match_result["match_score"]
    analysis = match_result["analysis"]

    explanation = f"This candidate received a score of **{score}%**.\n\n"
    explanation += "Here's why:\n"
    for point in analysis:
        explanation += f"- {point}\n"
    
    if score > 70:
        explanation += "\n✅ Likely a strong match."
    elif score > 40:
        explanation += "\n⚠️ Partial fit – consider for support roles."
    else:
        explanation += "\n❌ May not meet required qualifications."

    return explanation
