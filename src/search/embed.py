from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

from src.config import EMB_MODEL
embeddings = GoogleGenerativeAIEmbeddings(
    model=EMB_MODEL
)


def create_retriever(chunks):
    vectorstore=FAISS.from_documents(chunks,embeddings)
    retriever=vectorstore.as_retriever(search_kwargs={'k':6})
    return retriever