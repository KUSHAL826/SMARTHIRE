from pydantic import BaseModel
from typing import Optional,List

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from src.config import MODEL

class ResumeProfile(BaseModel):
    name: Optional[str] = None 
    skills: Optional[List[str]] = None 
    experience: Optional[str] = None 
    education: Optional[str] = None 
    target_role: Optional[str] = None

llm = ChatGoogleGenerativeAI(model=MODEL,max_output_tokens=1500)
str_llm=llm.with_structured_output(ResumeProfile)

prompt = ChatPromptTemplate.from_messages([
    ( "system", """You are an AI resume parser.
       Extract the candidate's information only from the provided resume context. 
       Rules: - Do not invent or assume information. 
       - If information is not present, return null.
         - Extract the candidate's full name. 
         - Extract technical and professional skills explicitly mentioned. 
         - Extract work experience, internships, companies, roles, durations, and responsibilities when available. 
         - Extract education, degree, institution, field of study, and relevant academic details.
         - Extract the target role only if it is explicitly stated in the resume.
         - Do not infer a target role from skills or education. 
         - Return only information supported by the resume context.""" ),
     ( "human", """RESUME CONTEXT: {context} PARSE THE RESUME INTO THE REQUIRED STRUCTURED FORMAT.""" ) ])

def format_docs(docs):
    return "\n-----------\n".join(d.page_content for d in docs) 

def  parse_resume(retriever):

    rag_chain=(
        {'context':retriever | format_docs,'question':RunnablePassthrough()}
        | prompt
        | str_llm
    )
    profile = rag_chain.invoke( "Extract the candidate's name, skills, experience, education and target role." ) 
    
    return profile