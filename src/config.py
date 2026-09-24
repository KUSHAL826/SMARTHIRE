import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

try:
    import streamlit as st
    if not gemini_key and hasattr(st, "secrets"):
        if "GEMINI_API_KEY" in st.secrets:
            gemini_key = st.secrets["GEMINI_API_KEY"]
        elif "GOOGLE_API_KEY" in st.secrets:
            gemini_key = st.secrets["GOOGLE_API_KEY"]
except Exception:
    pass

if gemini_key:
    os.environ["GOOGLE_API_KEY"] = str(gemini_key)
    os.environ["GEMINI_API_KEY"] = str(gemini_key)
MODEL = "gemini-3.5-flash-lite"
EMB_MODEL = "gemini-embedding-001"

BASE_DIR=Path(__file__).resolve().parent.parent
DATA_DIR=BASE_DIR/"data"

JOBS_DIR=DATA_DIR/"jobs"
CAREER_DIR=DATA_DIR/"career_notes"

Chunk_size=800
Chunk_overlap=150


