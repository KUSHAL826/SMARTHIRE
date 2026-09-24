import sys
from pathlib import Path

# Add root directory to sys.path so 'src' imports work seamlessly on Streamlit Cloud
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
import tempfile
import os

from src.parsing.loader import load_chunk_documents
from src.parsing.resume_parser import parse_resume
from src.search.embed import create_retriever
from src.search.job_search import create_job_retriever
from src.generate.cv_suggestions import create_cv_suggestion_chain
from src.mentor.rag_chain import create_rag_chain
from src.safety.guardrails import validate_input


st.set_page_config(
    page_title="SmartHire GenAI | AI Career Portal",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling - High Contrast Light Theme
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: #0f172a;
}

.stApp {
    background: linear-gradient(135deg, #f8fafc 0%, #eff6ff 50%, #f1f5f9 100%);
    color: #0f172a;
}

/* Ensure headings and paragraphs are crisp dark text */
.main p, .main span, .main label, .main div {
    color: #0f172a;
}

.hero-banner {
    background: linear-gradient(135deg, #ffffff 0%, #e0e7ff 100%);
    border: 1px solid #c7d2fe;
    border-radius: 24px;
    padding: 2.5rem;
    margin-bottom: 2rem;
    box-shadow: 0 10px 30px rgba(99, 102, 241, 0.1);
    text-align: center;
}

.hero-title {
    font-size: 2.8rem;
    font-weight: 800;
    color: #3730a3 !important;
    margin-bottom: 0.8rem;
    letter-spacing: -0.02em;
}

.hero-subtitle {
    color: #475569 !important;
    font-size: 1.15rem;
    font-weight: 500;
    max-width: 750px;
    margin: 0 auto;
    line-height: 1.6;
}

.glass-section {
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 20px;
    padding: 1.8rem;
    margin-bottom: 1.8rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
}

.glass-section h3, .glass-section h2 {
    color: #1e1b4b !important;
}

.job-card {
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 18px;
    padding: 1.5rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.04);
}

.job-card h3 {
    color: #312e81 !important;
}

.badge-tag {
    display: inline-block;
    background: #e0e7ff;
    color: #3730a3 !important;
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 700;
    margin-bottom: 12px;
    border: 1px solid #a5b4fc;
}

.chatbot-wrapper {
    background: #ffffff;
    border: 2px solid #818cf8;
    border-radius: 24px;
    padding: 2rem;
    margin-top: 2.5rem;
    box-shadow: 0 10px 35px rgba(99, 102, 241, 0.12);
}

.chatbot-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-bottom: 1rem;
    border-bottom: 1px solid #e2e8f0;
    margin-bottom: 1.5rem;
}

.mentor-status {
    background: #dcfce7;
    color: #15803d !important;
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 700;
    border: 1px solid #86efac;
}

.stChatMessage {
    background-color: #f8fafc !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 14px !important;
    color: #0f172a !important;
}
</style>
""", unsafe_allow_html=True)

# Hero Header Banner
st.markdown("""
<div class="hero-banner">
    <div class="hero-title">💼 SmartHire GenAI</div>
    <div class="hero-subtitle">
        Next-Generation Career Portal powered by Generative AI, RAG & Vector Search.
        Upload your resume to receive structured profiling, AI job matching, CV improvement analysis, and real-time Career Mentoring.
    </div>
</div>
""", unsafe_allow_html=True)


# Session State Initialization
if "resume_processed" not in st.session_state:
    st.session_state.resume_processed = False

if "profile" not in st.session_state:
    st.session_state.profile = None

if "matched_jobs" not in st.session_state:
    st.session_state.matched_jobs = []

if "selected_job" not in st.session_state:
    st.session_state.selected_job = None

if "suggestion_chain" not in st.session_state:
    st.session_state.suggestion_chain = None

if "mentor_chain" not in st.session_state:
    st.session_state.mentor_chain = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "mentor_active" not in st.session_state:
    st.session_state.mentor_active = True


# Upload Section
st.markdown("### 📄 Resume Upload & Processing")

uploaded_file = st.file_uploader(
    "Upload Candidate CV",
    type=["pdf", "docx"],
    help="Supported formats: PDF, DOCX"
)

if uploaded_file:
    st.info(f"📁 Selected Resume File: **{uploaded_file.name}**")

    if st.button("🚀 Process Resume & Match Jobs", type="primary", use_container_width=True):
        with st.spinner("⚡ Extracting structured profile and generating semantic embeddings..."):
            suffix = os.path.splitext(uploaded_file.name)[1]
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
                temp_file.write(uploaded_file.getbuffer())
                file_path = temp_file.name

            try:
                documents, chunks = load_chunk_documents(file_path)
                resume_retriever = create_retriever(chunks)
                profile = parse_resume(resume_retriever)
                job_retriever = create_job_retriever()

                profile_text = f"""
Name: {profile.name}
Skills: {profile.skills}
Experience: {profile.experience}
Education: {profile.education}
Target Role: {profile.target_role}
"""
                matched_jobs = job_retriever.invoke(profile_text)

                st.session_state.profile = profile
                st.session_state.matched_jobs = matched_jobs
                st.session_state.suggestion_chain = create_cv_suggestion_chain()
                st.session_state.mentor_chain = create_rag_chain(job_retriever)
                st.session_state.resume_processed = True
                st.session_state.selected_job = None
                st.session_state.chat_history = []

                st.success("✨ Resume successfully analyzed!")

            finally:
                os.remove(file_path)


# Structured Resume Profile Section
if st.session_state.profile:
    st.divider()
    st.markdown("## 👤 Extracted Structured Profile")
    profile = st.session_state.profile

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="glass-section">', unsafe_allow_html=True)
        st.markdown("### 📌 Personal & Role Info")
        st.write(f"**Candidate Name:** {profile.name or 'Not specified'}")
        st.write(f"**Target Role:** {profile.target_role or 'Not specified'}")

        st.markdown("### 🎓 Education")
        st.write(profile.education or "Not specified")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="glass-section">', unsafe_allow_html=True)
        st.markdown("### 🛠️ Extracted Skills")
        if profile.skills:
            st.write(" • ".join(profile.skills))
        else:
            st.write("No explicit skills extracted")

        st.markdown("### 💼 Work & Internships Experience")
        st.write(profile.experience or "Not specified")
        st.markdown('</div>', unsafe_allow_html=True)


# Semantic Job Matches Section
if st.session_state.resume_processed:
    st.divider()
    st.markdown("## 🎯 Ranked Job Matches (Semantic Search)")
    st.caption("Jobs retrieved from vector database based on candidate CV similarity score.")

    for index, job in enumerate(st.session_state.matched_jobs, start=1):
        st.markdown('<div class="job-card">', unsafe_allow_html=True)
        st.markdown(f'<span class="badge-tag">Match Rank #{index}</span>', unsafe_allow_html=True)
        st.markdown(f"### Job Description #{index}")
        st.write(job.page_content)
        st.markdown('</div>', unsafe_allow_html=True)

        if st.button(f"🎯 Select Job #{index} as Target Role", key=f"select_job_{index}", use_container_width=True):
            st.session_state.selected_job = job
            st.rerun()


# Target Role Analysis & CV Improvement
if st.session_state.selected_job:
    st.divider()
    st.markdown("## 📈 CV Improvement & Skill Gap Suggestions")
    selected_job = st.session_state.selected_job

    st.info(f"**Selected Target Role Context:**\n\n{selected_job.page_content}")

    if st.button("🔍 Generate AI Suggestions to Improve CV", type="primary", use_container_width=True):
        with st.spinner("🤖 Analyzing CV gaps against target role requirements..."):
            result = st.session_state.suggestion_chain.invoke({
                "profile": st.session_state.profile.model_dump(),
                "job": selected_job.page_content
            })

        st.markdown('<div class="glass-section">', unsafe_allow_html=True)
        st.markdown("### 💡 AI Recommendations")
        st.markdown(result)
        st.markdown('</div>', unsafe_allow_html=True)


# AI Career Mentor Chatbot Box (At the End with Replying Animation)
if st.session_state.resume_processed:
    st.divider()
    
    st.markdown('<div class="chatbot-wrapper">', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="chatbot-header">
        <div>
            <h2 style="margin:0; font-size:1.8rem; color:#312e81;">🤖 AI Career Mentor</h2>
            <span style="color:#64748b; font-size:0.95rem;">Retrieval-Augmented Generation (RAG) Chatbot</span>
        </div>
        <div>
            <span class="mentor-status">🟢 RAG Active</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.mentor_active:
        # Render past chat history
        for message in st.session_state.chat_history:
            avatar = "🤖" if message["role"] == "assistant" else "👤"
            with st.chat_message(message["role"], avatar=avatar):
                st.write(message["content"])

        # Chat Input Box
        question = st.chat_input("Ask your AI Career Mentor a question (e.g. How to prepare for this role?)...")

        if question:
            if validate_input(question):
                # 1. Append & render user message immediately
                st.session_state.chat_history.append({
                    "role": "user",
                    "content": question
                })
                with st.chat_message("user", avatar="👤"):
                    st.write(question)

                # 2. Render Assistant response with custom Replying Animation Spinner
                with st.chat_message("assistant", avatar="🤖"):
                    with st.spinner("💬 AI Career Mentor is searching RAG knowledge base & thinking..."):
                        answer = st.session_state.mentor_chain.invoke(question)
                        st.write(answer)

                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": answer
                })

                st.rerun()
            else:
                st.error("Please enter a valid career question (max 2000 characters).")

        col_left, col_right = st.columns([4, 1])
        with col_right:
            if st.button("Exit Mentor Session", use_container_width=True):
                st.session_state.mentor_active = False
                st.rerun()

    else:
        st.info("Career Mentor session is currently inactive.")
        if st.button("Start Mentor Session Again", type="primary", use_container_width=True):
            st.session_state.mentor_active = True
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)