# SmartHire GenAI — Capstone Final Report

## Executive Summary
SmartHire GenAI is an end-to-end career portal leveraging Generative AI, embeddings, vector search (FAISS), and RAG to match candidate CVs with target jobs and provide AI career mentoring.

## Key System Components
1. **Resume Parser**: Parses PDF/DOCX CVs using Gemini LLM structured outputs into a Pydantic `ResumeProfile`.
2. **Semantic Search**: Generates embeddings using `GoogleGenerativeAIEmbeddings` and queries FAISS vector store.
3. **CV Improvement**: Analyzes candidate skills against selected job roles to generate actionable recommendations.
4. **AI Career Mentor**: RAG chatbot using LangChain to provide grounded career guidance.
5. **Guardrails**: Input validation and length checks to block off-topic or empty prompts.

## Design Choices & Limitations
- **FAISS Vector Store**: Fast in-memory vector indexing for job corpus documents.
- **Streamlit Portal**: Clean, interactive light theme UI with animated RAG chatbot box.
