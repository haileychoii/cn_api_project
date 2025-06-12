# /app/utils/vectorstore_loader.py

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.retrievers import EnsembleRetriever

def load_dual_vectorstores():
    embedding = OpenAIEmbeddings()

    vs1 = Chroma(
        persist_directory="app/vectorstore/chroma_db",
        embedding_function=embedding
    )

    vs2 = Chroma(
        persist_directory="app/vectorstore/step_json_chroma_db",
        embedding_function=embedding
    )

    retriever1 = vs1.as_retriever(search_kwargs={"k": 4})  # 원문+법률+논문
    retriever2 = vs2.as_retriever(search_kwargs={"k": 4})  # step2/4/5 JSON

    return retriever1, retriever2