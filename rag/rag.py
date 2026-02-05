import os
from decouple import config
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from langchain_chroma import Chroma

os.environ["HUGGINGFACEHUB_API_TOKEN"] = config("HUGGINGFACEHUB_API_TOKEN")

if __name__ == '__main__' :
    file_path = '/app/rag/data/docs.pdf'
    loader = PyPDFLoader(file_path)
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents=docs)

    persists_dir = '/app/chroma-data'
    embedding = HuggingFaceEndpointEmbeddings(model="sentence-transformers/all-MiniLM-L6-v2", task="feature-extraction" )
    vector_store = (
        Chroma.from_documents(documents=chunks, embedding=embedding, persist_directory=persists_dir)
    )





