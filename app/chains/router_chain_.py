# chains/router_chain_.py

from langchain.chains import ConversationalRetrievalChain
from langchain_community.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.retrievers import EnsembleRetriever
from dotenv import load_dotenv
from pathlib import Path
import os
from utils.prompt_templates import get_qa_prompt


def load_vectorstores():
    embedding = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

    chroma_vectorstore = Chroma(
        persist_directory="app/vectorstore/chroma_db",
        embedding_function=embedding
    )
    json_vectorstore = Chroma(
        persist_directory="app/vectorstore/step_json_chroma_db",
        embedding_function=embedding
    )

    return chroma_vectorstore, json_vectorstore


def load_router_chain(mode="default"):
    """
    mode:
      - "default": 약관 + 개선안 (Ensemble)
      - "json_only": 개선안 JSON만 사용
      - "original_only": 약관 원문만 사용
    """

    # ✅ 환경 변수 로딩
    env_path = Path(__file__).resolve().parents[1] / ".env"
    load_dotenv(dotenv_path=env_path)

    api_key = os.getenv("OPENAI_API_KEY")
    chroma_vectorstore, json_vectorstore = load_vectorstores()

    # ✅ mode 기반 retriever 선택
    if mode == "json_only":
        retriever = json_vectorstore.as_retriever(search_kwargs={"k": 4})
    elif mode == "original_only":
        retriever = chroma_vectorstore.as_retriever(search_kwargs={"k": 4})
    else:
        retriever = EnsembleRetriever(
            retrievers=[
                chroma_vectorstore.as_retriever(search_kwargs={"k": 4}),
                json_vectorstore.as_retriever(search_kwargs={"k": 4})
            ],
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
        retriever=retriever,
        memory=memory,
        combine_docs_chain_kwargs={"prompt": get_qa_prompt()},
        return_source_documents=True,
        output_key="answer"
    )

    return chain


# 기존 이름을 유지하고 싶으면 이걸 통해 기존 방식과 호환 유지
def load_conversational_chain():
    return load_router_chain(mode="default")
