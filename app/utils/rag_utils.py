def query_step_json_chroma_db(query: str, top_k: int = 3):
    import os
    import json
    from pathlib import Path
    from langchain.embeddings import OpenAIEmbeddings
    from langchain_community.vectorstores import Chroma
    from langchain.docstore.document import Document

    BASE_DIR = Path(__file__).parent.parent
    STEP_JSON_DB_DIR = BASE_DIR / "app" / "vectorstore" / "step_json_chroma_db"
    STEP_JSON_RESULT_PATHS = [
        BASE_DIR / "step3_results",
        BASE_DIR / "merged_step4_results",
        BASE_DIR / "step5_results",
    ]

    db = Chroma(
        persist_directory=str(STEP_JSON_DB_DIR),
        embedding_function=OpenAIEmbeddings()
    )

    docs = db.similarity_search(query, k=top_k)

    results = []

    for doc in docs:
        source_path = doc.metadata.get('source', '')
        filename = Path(source_path).name

        found = False
        json_data = None
        for folder_path in STEP_JSON_RESULT_PATHS:
            file_path = folder_path / filename
            if file_path.exists():
                with open(file_path, "r", encoding="utf-8") as f:
                    json_data = json.load(f)
                found = True
                break

        # ⛳ 핵심 개선안, 평가 요약 등 추출
        from utils.text_utils import extract_core_summary_from_text
        core_summary = extract_core_summary_from_text(doc.page_content)

        results.append({
            "filename": filename,
            "data": json_data,
            "page_content": doc.page_content,
            "core_summary": core_summary,
            "source": source_path,
            "error": None if found else "원본 JSON 파일을 찾을 수 없습니다."
        })

    return results
