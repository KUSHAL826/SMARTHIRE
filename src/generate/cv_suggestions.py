from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from src.config import MODEL


llm = ChatGoogleGenerativeAI(
    model=MODEL,
    max_output_tokens=1500
)


prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are an AI career analysis assistant.

Compare the candidate resume profile with the selected job role requirements.

Identify:
- Skills already present
- Missing skills
- Missing experience or qualifications
- Areas that need improvement
- Specific suggestions to become better prepared for the role

Use only the information provided.
Do not invent candidate experience, skills, education, or job requirements."""
    ),
    (
        "human",
        """CANDIDATE PROFILE:

{profile}

SELECTED JOB ROLE:

{job}

Analyze the candidate's eligibility and requirements still needed."""
    )
])


def create_cv_suggestion_chain():

    suggestion_chain = (
        prompt
        | llm
        | StrOutputParser()
    )

    return suggestion_chain