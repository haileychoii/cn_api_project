from langchain.chains import ConversationalRetrievalChain
from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings

def load_rag_chain(vectorstore_path="vectorstore"):
    embeddings = OpenAIEmbeddings()
    db = FAISS.load_local(vectorstore_path, embeddings, allow_dangerous_deserialization=True)

    retriever = db.as_retriever(search_kwargs={"k": 4})
    llm = ChatOpenAI(temperature=0.3, model_name="gpt-4")  # 또는 gpt-3.5

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff"
    )
    return chain

def load_conversational_chain(vectorstore_path="vectorstore"):
    embeddings = OpenAIEmbeddings()
    db = FAISS.load_local(vectorstore_path, embeddings, allow_dangerous_deserialization=True)
    retriever = db.as_retriever(search_kwargs={"k": 4})

    llm = ChatOpenAI(temperature=0.3, model_name="gpt-4")

    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        return_source_documents=True  # 문서 출처 반환
    )
    return qa_chain
