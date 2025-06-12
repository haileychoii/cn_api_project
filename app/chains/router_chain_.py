from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
import os

from langchain.retrievers import EnsembleRetriever
from utils.prompt_templates import get_qa_prompt

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


def load_conversational_chain():
    embedding = OpenAIEmbeddings(openai_api_key=api_key)

    # ✅ 첫 번째 벡터스토어: 약관/법률/논문 등
    chroma_vectorstore = Chroma(
        persist_directory="app/vectorstore/chroma_db",
        embedding_function=embedding
    )

    # ✅ 두 번째 벡터스토어: Step2/4/5 JSON 개선 평가
    json_vectorstore = Chroma(
        persist_directory="app/vectorstore/step_json_chroma_db",
        embedding_function=embedding
    )

    # ✅ 각각의 retriever 정의
    chroma_retriever = chroma_vectorstore.as_retriever(search_kwargs={"k": 4})
    json_retriever = json_vectorstore.as_retriever(search_kwargs={"k": 4})

    # ✅ Ensemble Retriever로 병합 (단순 평균 방식)
    combined_retriever = EnsembleRetriever(
        retrievers=[chroma_retriever, json_retriever],
        weights=[0.5, 0.5]
    )

    memory = ConversationBufferMemory(
        memory_key = 'chat_history',
        return_messages=True,
        output_key='answer'
    )

    llm = ChatOpenAI(
        temperature=0.3,
        model="gpt-4o-2024-05-13",
        openai_api_key=api_key
    )

    # ✅ LLM + QA Chain
    llm = ChatOpenAI(temperature=0.3, model="gpt-4", openai_api_key=api_key)

    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=combined_retriever,
        memory=ConversationBufferMemory(memory_key="chat_history", return_messages=True, output_key = 'answer'),
        combine_docs_chain_kwargs={"prompt": get_qa_prompt()},
        return_source_documents=True,  # ✅ 출처 반환 설정
        output_key='answer'  # 꼭 추가
    )

    return chain

