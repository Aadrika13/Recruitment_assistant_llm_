import streamlit as st
import datetime
import os
import json

from resume_parser import parse_resume_with_llm
from job_matcher import match_resume_to_job
from chatbot import get_chatbot_response

from bias_handler import anonymize_resume
from explainer import generate_explanation



CANDIDATE_FILE = "data/candidates.json"

st.set_page_config(page_title="Recruitment Assistant", layout="wide")
st.title("🤖 Recruitment Assistant")

# --- Upload Resume ---
st.header("📄 Upload Resume")
uploaded_file = st.file_uploader("Upload Resume PDF", type=["pdf"])
if uploaded_file:
    with st.spinner("Parsing resume..."):
        resume_text = parse_resume_with_llm(uploaded_file)
        st.session_state.parsed_resume = resume_text
    st.success("✅ Resume uploaded and parsed.")

# --- Job Description ---
st.header("📌 Paste Job Description")
job_description = st.text_area("Enter the job description here:")

# --- Resume Matching ---
if st.button("🎯 Match Candidate to Job"):
    if "parsed_resume" not in st.session_state:
        st.error("Please upload a resume first.")
    elif not job_description:
        st.error("Please enter a job description.")
    else:
        with st.spinner("Matching..."):
            anonymized_resume = anonymize_resume(st.session_state.parsed_resume)
            match_result_raw = match_resume_to_job(anonymized_resume, job_description)
        try:
            st.session_state.match_result = json.loads(match_result_raw)
            st.success("✅ Candidate matched!")
            st.session_state.match_explanation = generate_explanation(st.session_state.match_result)
            st.markdown("### 📖 Match Explanation")
            st.markdown(st.session_state.match_explanation)
        except Exception as e:
            st.error("⚠️ Couldn't parse LLM response. Check formatting.")
            st.text(match_result_raw)

# --- Candidate Chatbot ---
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

st.header("💬 Candidate Chatbot")

if uploaded_file and job_description:
    if 'parsed_resume' in st.session_state:
        user_question = st.text_input("Ask a question to the candidate (based on resume)")
        if st.button("🗨️ Ask"):
            with st.spinner("Thinking..."):
                answer = get_chatbot_response(
                    st.session_state.parsed_resume,
                    user_question,
                    st.session_state.chat_history,
                )
                st.session_state.chat_history.append((user_question, answer))

        if st.session_state.chat_history:
            st.subheader("🧾 Chat History")
            for idx, (q, a) in enumerate(st.session_state.chat_history):
                st.markdown(f"**Q{idx+1}:** {q}")
                st.markdown(f"**A{idx+1}:** {a}")

# --- Interview Scheduler: Show if match score >= 60 ---
if "match_result" in st.session_state:
    score = st.session_state.match_result.get("match_score", 0)
    if score >= 60:
        st.header("📅 Interview Scheduler")
        candidate_name = st.text_input("Candidate Name", value="Unknown")
        interview_date = st.date_input("Interview Date")
        interview_time = st.time_input("Interview Time")

        if st.button("💾 Save Candidate"):
            new_candidate = {
                "name": candidate_name,
                "match_score": score,
                "analysis": st.session_state.match_result["analysis"],
                "interview_date": interview_date.strftime("%Y-%m-%d"),
                "interview_time": interview_time.strftime("%H:%M"),
                "explanation": st.session_state.match_explanation
            }

            if os.path.exists(CANDIDATE_FILE):
                with open(CANDIDATE_FILE, "r") as f:
                    candidates = json.load(f)
            else:
                candidates = []

            candidates.append(new_candidate)
            with open(CANDIDATE_FILE, "w") as f:
                json.dump(candidates, f, indent=2)

            st.success("✅ Candidate saved!")

# --- Candidate Dashboard ---

if os.path.exists(CANDIDATE_FILE):
    st.header("📊 Candidate Dashboard")
    with open(CANDIDATE_FILE, "r") as f:
        candidates = json.load(f)

    for idx, c in enumerate(candidates):
        st.subheader(f"🧑 Candidate {idx+1}: {c['name']}")
        st.markdown(f"**Match Score:** {c['match_score']}%")
        st.markdown(f"**Interview Scheduled:** {c['interview_date']} at {c['interview_time']}")
        st.markdown("**Top Analysis Points:**")
        if "explanation" in c:
            st.markdown("**🧠 Match Explanation:**")
            st.markdown(c["explanation"])
        else:
            st.info("No explanation available for this candidate (added before Week 5).")

        for point in c["analysis"]:
            st.write(f"- {point}")
        st.markdown("---")
