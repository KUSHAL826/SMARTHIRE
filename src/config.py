import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

os.environ["GOOGLE_API_KEY"]=os.getenv("GEMINI_API_KEY")
MODEL = "gemini-3.5-flash-lite"
EMB_MODEL = "gemini-embedding-001"

BASE_DIR=Path(__file__).resolve().parent.parent
DATA_DIR=BASE_DIR/"data"

JOBS_DIR=DATA_DIR/"jobs"
CAREER_DIR=DATA_DIR/"career_notes"

Chunk_size=800
Chunk_overlap=150


