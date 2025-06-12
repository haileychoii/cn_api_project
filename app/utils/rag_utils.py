

def query_step_json_chroma_db(query: str, top_k: int = 3):
    import os
    import json
    from pathlib import Path
    import re
    from langchain.embeddings import OpenAIEmbeddings
    from langchain_community.vectorstores import Chroma



    # ✅ 경로 직접 정의
    STEP_JSON_DB_DIR = "../vectorstore/step_json_chroma_db"
    STEP_JSON_RESULT_PATHS = [
        "../../step3_results",  # Step3 평가 결과
        "../../step4_results",  # Step4 개선안 제안 결과
        "../../step5_results"  # Step5 개선안 평가 결과
    ]

    # ✅ 벡터스토어 로드
    db = Chroma(
        persist_directory=STEP_JSON_DB_DIR,
        embedding_function=OpenAIEmbeddings()
    )

    # ✅ 의미 기반 검색 수행
    docs = db.similarity_search(query, k=top_k)

    results = []

    for doc in docs:
        filename = Path(doc.metadata['source']).name

        # ✅ 여러 경로 중 실제 json 파일이 존재하는 곳 탐색
        found = False
        for path in STEP_JSON_RESULT_PATHS:
            file_path = os.path.join(path, filename)
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    json_data = json.load(f)
                    results.append({
                        "filename": filename,
                        "data": json_data,
                        "page_content": doc.page_content  # → 원문도 같이 전달
                    })
                found = True
                break  # 파일 찾았으면 더는 안찾아도 됨

        if not found:
            # 파일을 찾지 못한 경우도 표시할 수 있음 (선택)
            results.append({
                "filename": filename,
                "data": None,
                "page_content": doc.page_content,
                "error": "원본 JSON 파일을 찾을 수 없습니다."
            })

    return results