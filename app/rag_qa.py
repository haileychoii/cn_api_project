
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from utils.prompt_templates import get_qa_prompt

def load_enhanced_rag_chain(vectorstore_path="vectorstore"):
    embeddings = OpenAIEmbeddings()
    db = FAISS.load_local(vectorstore_path, embeddings, allow_dangerous_deserialization=True)
    retriever = db.as_retriever(search_kwargs={"k": 4})
    llm = ChatOpenAI(temperature=0.2, model_name="gpt-4")

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={
            "prompt": get_qa_prompt()
        },
        return_source_documents=True
    )
    return chain


# def load_conversational_chain(vectorstore_path="vectorstore"):
#     embeddings = OpenAIEmbeddings()
#     db = FAISS.load_local(vectorstore_path, embeddings, allow_dangerous_deserialization=True)
#     retriever = db.as_retriever(search_kwargs={"k": 4})
#
#     llm = ChatOpenAI(temperature=0.3, model_name="gpt-4")
#
#     qa_chain = ConversationalRetrievalChain.from_llm(
#         llm=llm,
#         retriever=retriever,
#         return_source_documents=True  # 문서 출처 반환
#     )
#     return qa_chain
