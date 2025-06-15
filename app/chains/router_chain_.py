# router_chain_.py

from langchain.chains import ConversationalRetrievalChain
from langchain_community.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.retrievers import EnsembleRetriever
from dotenv import load_dotenv
import os
from utils.prompt_templates import get_qa_prompt
from pathlib import Path
import re
import os

def load_conversational_chain():
    # ✅ API 키는 app.py에서 이미 .env를 통해 설정되었다고 가정

    # ✅ .env 파일을 프로젝트 루트에서 명시적으로 불러오기
    env_path = Path(__file__).resolve().parents[1] / ".env"
    print("📁 .env 경로:", env_path)

    load_dotenv(dotenv_path=env_path)

    api_key = os.getenv("OPENAI_API_KEY")

    embedding = OpenAIEmbeddings(openai_api_key=api_key)

    chroma_vectorstore = Chroma(
        persist_directory="app/vectorstore/chroma_db",
        embedding_function=embedding
    )

    json_vectorstore = Chroma(
        persist_directory="app/vectorstore/step_json_chroma_db",
        embedding_function=embedding
    )

    chroma_retriever = chroma_vectorstore.as_retriever(search_kwargs={"k": 4})
    json_retriever = json_vectorstore.as_retriever(search_kwargs={"k": 4})

    combined_retriever = EnsembleRetriever(
        retrievers=[chroma_retriever, json_retriever],
        weights=[0.5, 0.5]
    )

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer"
    )

    llm = ChatOpenAI(
        temperature=0.3,
        model="gpt-4o-2024-05-13",
        openai_api_key=api_key
    )

    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=combined_retriever,
        memory=memory,
        combine_docs_chain_kwargs={"prompt": get_qa_prompt()},
        return_source_documents=True,
        output_key="answer"
    )

    return chain
