# 📁 utils/injest_json_chunks.py
import os
import json
from typing import List

# 최신 방식
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings


from langchain.schema import Document
from tiktoken import encoding_for_model

from dotenv import load_dotenv
load_dotenv()

import tiktoken

def count_tokens(text, model = 'text-embedding-3-small'):
    enc = tiktoken.encoding_for_model(model)
    return len(enc.encode(text))

def split_documents_by_token_limit(docs: list[Document], max_tokens_per_batch: int = 200_000) -> list[list[Document]]:
    batches = []
    current_batch = []
    current_tokens = 0

    for doc in docs:
        tokens = count_tokens(doc.page_content)
        if current_tokens + tokens > max_tokens_per_batch:
            if current_batch:
                batches.append(current_batch)
            current_batch = [doc]
            current_tokens = tokens
        else:
            current_batch.append(doc)
            current_tokens += tokens

    if current_batch:
        batches.append(current_batch)

    return batches

# 설정
STEP_PATHS = {
    "step2": "../../step2_results",
    "step4": "../../merged_step4_results",
    "step5": "../../step5_results"
}
CHROMA_PERSIST_DIR = "../vectorstore/step_json_chroma_db"
CHUNK_SIZE = 2000  # 글자 수 기준 (token 기반으로 바꾸고 싶으면 따로 설정 필요)
EMBEDDING_MODEL = "text-embedding-3-small"
openai_api_key = os.getenv("OPENAI_API_KEY")  # 또는 직접 할당

# 토큰 분리기
enc = encoding_for_model(EMBEDDING_MODEL)

def process_json_file(filepath: str, step: str) -> List[Document]:
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    docs = []

    # STEP2, 4, 5에서 구조가 다르므로 분기
    if isinstance(data, list):  # 리스트인 경우
        items = data
    elif isinstance(data, dict):  # 딕셔너리인 경우
        items = data.get("문제점목록", []) if step == "step2" else data.get("개선방안목록", [])
    else:
        print(f"⚠️ 알 수 없는 데이터 형식: {filepath}")
        return []

    for item in items:
        content = json.dumps(item, ensure_ascii=False, indent=2)
        metadata = {"source": filepath, "step": step}
        docs.append(Document(page_content=content, metadata=metadata))

    return docs

def injest_all():
    all_docs = []

    for step, folder in STEP_PATHS.items():
        for fname in os.listdir(folder):
            if fname.endswith(".json"):
                fpath = os.path.join(folder, fname)
                docs = process_json_file(fpath, step)
                all_docs.extend(docs)

    print(f"총 문서 수: {len(all_docs)}")
    batches = split_documents_by_token_limit(all_docs)

    for i, batch in enumerate(batches):
        print(f"✅ 배치 {i+1}/{len(batches)} - 문서 수: {len(batch)}")
        db = Chroma.from_documents(
            documents=batch,
            embedding=OpenAIEmbeddings(openai_api_key=openai_api_key),
            persist_directory=CHROMA_PERSIST_DIR
        )

    print("🎉 모든 문서 인덱싱 완료.")

if __name__ == "__main__":
    injest_all()

