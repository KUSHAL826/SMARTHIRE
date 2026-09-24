from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from src.config import MODEL


llm = ChatGoogleGenerativeAI(
    model=MODEL,
    max_output_tokens=1500
)


prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are SmartHire AI Career Mentor.

Answer the user's career questions using only the provided context from job descriptions and career notes.

Rules:
- Do not invent information.
- If the context does not contain enough information, clearly say that the information is not available in the provided documents.
- Give practical and relevant career guidance.
- Keep the answer clear and concise."""
    ),
    (
        "human",
        """CONTEXT:

{context}

USER QUESTION:

{question}"""
    )
])


def format_docs(docs):

    return "\n-----------\n".join(
        d.page_content for d in docs
    )


def create_rag_chain(retriever):

    rag_chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain