from pathlib import Path
from langchain_community.document_loaders import (PyPDFLoader,Docx2txtLoader)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.config import Chunk_overlap,Chunk_size
def load_documents(file_path):
    extension=Path(file_path).suffix.lower()

    if extension=='.docx':
        documents=Docx2txtLoader(str(file_path)).load()
        if not documents:
            raise ValueError("NO CONTENT IN DOCUMENTS")
        return documents
    elif extension=='.pdf':
        documents=PyPDFLoader(str(file_path)).load()
        if not documents:
                    raise ValueError("NO CONTENT IN DOCUMENTS")
        return documents
    else:
         raise ValueError("Only pdf and docx are supported")

def chunk_documents(documents):
    splitter=RecursiveCharacterTextSplitter(chunk_size=Chunk_size,chunk_overlap=Chunk_overlap)
    chunks=splitter.split_documents(documents)
    return chunks

def load_chunk_documents(file_path):
    documents=load_documents(file_path)
    chunks=chunk_documents(documents)
    return documents,chunks