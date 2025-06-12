from langchain.prompts import PromptTemplate

def get_qa_prompt():
    return PromptTemplate.from_template("""
    다음은 보험 약관 분석 시스템의 대화입니다. 질문에 대해 가장 적절한 답변을 제공하십시오. 필요 시 문서 출처도 함께 제공합니다.

    질문: {question}
    --------
    관련 문서 요약:
    {context}
    --------
    답변:
    """)