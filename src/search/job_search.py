from src.config import JOBS_DIR, CAREER_DIR, DATA_DIR, BASE_DIR
from src.parsing.loader import load_chunk_documents
from src.search.embed import create_retriever

def get_jobs_dir():
    if JOBS_DIR.exists():
        return JOBS_DIR
    if (DATA_DIR / "jobs").exists():
        return DATA_DIR / "jobs"
    if (BASE_DIR / "jobs").exists():
        return BASE_DIR / "jobs"
    target = DATA_DIR / "jobs"
    target.mkdir(parents=True, exist_ok=True)
    return target

def create_job_retriever():
    target_dir = get_jobs_dir()
    job_files = [f for f in target_dir.iterdir() if f.is_file() and f.suffix.lower() in ('.pdf', '.docx')]
    if not job_files:
        raise ValueError("NO FILES IN DIRECTORY")

    all_chunks = []

    for file in job_files:
        _, chunks = load_chunk_documents(file)
        all_chunks.extend(chunks)

    if not all_chunks:
        raise ValueError("NO CHUNKS FOUND")

    retriever = create_retriever(all_chunks)
    return retriever

def create_mentor_retriever():
    job_dir = get_jobs_dir()
    career_dir = CAREER_DIR if CAREER_DIR.exists() else DATA_DIR / "career_notes"
    career_dir.mkdir(parents=True, exist_ok=True)

    job_files = [f for f in job_dir.iterdir() if f.is_file() and f.suffix.lower() in ('.pdf', '.docx')]
    career_files = [f for f in career_dir.iterdir() if f.is_file() and f.suffix.lower() in ('.pdf', '.docx')]

    total_files = job_files + career_files
    all_chunks = []

    for file in total_files:
        try:
            _, chunks = load_chunk_documents(file)
            all_chunks.extend(chunks)
        except Exception:
            continue

    if not all_chunks:
        return create_job_retriever()

    return create_retriever(all_chunks)