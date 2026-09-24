# SmartHire GenAI — Resume Matching & AI Career Mentor

An end-to-end Generative AI career portal that parses uploaded resumes, finds matching job opportunities via semantic vector search, provides AI-driven CV improvement recommendations, and offers a retrieval-augmented generation (RAG) AI Career Mentor chatbot.

---

## 🌟 Key Features

1. **Resume Parser (Structured Output)**:
   - Extracts structured candidate information (`ResumeProfile`: name, skills, experience, education, target role) from PDF/DOCX CVs using Gemini LLM structured output.

2. **Semantic Job Search (Embeddings & FAISS)**:
   - Indexes job posting documents into a FAISS vector database using `GoogleGenerativeAIEmbeddings`.
   - Runs semantic similarity search based on candidate profile to rank top matching jobs.

3. **CV Improvement Generator**:
   - Compares candidate profile against target job requirements to produce actionable feedback, skill gap analysis, and tailored recommendations.

4. **AI Career Mentor Chatbot (RAG)**:
   - RAG pipeline built with LangChain that retrieves grounded answers from job corpus and career guides.
   - Enclosed UI chatbot container box with live replying animation.

5. **Guardrails & Input Safety**:
   - Implements strict input validation, length checks, and safety filtering before executing LLM requests.

---

## 📁 Directory Structure

```
smarthire-genai/
├── README.md                 # Project Overview & Setup Instructions
├── requirements.txt          # Dependencies (LangChain, FAISS, Streamlit, etc.)
├── .env                      # API Key configuration
├── data/
│   ├── jobs/                 # Job description PDFs / dataset
│   └── career_notes/         # Career guidance & role documents
├── src/
│   ├── config.py             # Model names, paths, parameters
│   ├── parsing/
│   │   ├── loader.py         # PDF/DOCX document loading & chunking
│   │   └── resume_parser.py  # Structured JSON profile parser
│   ├── search/
│   │   ├── embed.py          # GoogleGenerativeAIEmbeddings & FAISS store
│   │   └── job_search.py     # Job search & RAG mentor retrievers
│   ├── generate/
│   │   └── cv_suggestions.py # CV improvement generator chain
│   ├── mentor/
│   │   └── rag_chain.py      # LangChain RAG mentor chain
│   └── safety/
│       └── guardrails.py     # Input safety & guardrails validation
└── app/
    └── streamlit.py          # Streamlit UI Portal
```

---

## 🚀 Setup & Execution

### 1. Environment Configuration
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_google_gemini_api_key_here
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch Streamlit Portal
```bash
streamlit run app/streamlit.py
```
