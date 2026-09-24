# Answer Quality & Evaluation Report

## 1. Retrieval Relevance Score
- **Sample Queries Evaluated**: 10 test profile queries.
- **Top Job Match Hit Rate**: 90% (9/10 relevant job role matches in top 6 FAISS search results).

## 2. Grounding & Hallucination Check
- **Test Case**: Asked about roles not present in job corpus (e.g. Quantum Physics Researcher).
- **Result**: AI Career Mentor strictly refused open-ended hallucination and stated that the information was not available in the documents.

## 3. Before & After Prompt Comparison
- **Original Prompt**: "Parse this resume and output JSON."
- **Optimized Prompt**: Structured system prompt enforcing null returns for missing fields and strict non-inference for target role.
- **Improvement**: 0% hallucinated target roles on incomplete resumes.
