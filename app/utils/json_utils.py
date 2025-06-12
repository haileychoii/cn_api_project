import os
import json
import difflib

STEP2_PATH = "step2_results"
STEP4_PATH = "merged_step4_results"
STEP5_PATH = "step5_results"

def search_step_json_results(query):
    results = []

    # STEP 4 & 5
    for path in [STEP4_PATH, STEP5_PATH]:
        for fname in os.listdir(path):
            if not fname.endswith(".json"):
                continue
            with open(os.path.join(path, fname), encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except Exception as e:
                    continue

            # ✅ 데이터가 리스트 형태일 경우 처리
            if isinstance(data, list):
                for item in data:
                    if not isinstance(item, dict):
                        continue
                    match_score = difflib.SequenceMatcher(None, query, item.get("핵심문제요약", "")).ratio()
                    if query in item.get("핵심문제요약", "") or query in item.get("개선방안", "") or match_score > 0.5:
                        results.append({
                            "filename": fname,
                            "data": item,
                            "step": os.path.basename(path)
                        })

            # ✅ 데이터가 딕셔너리 형태일 경우 처리
            elif isinstance(data, dict):
                for item in data.get("평가결과", []):
                    match_score = difflib.SequenceMatcher(None, query, item.get("핵심문제요약", "")).ratio()
                    if query in item.get("핵심문제요약", "") or query in item.get("개선방안", "") or match_score > 0.5:
                        results.append({
                            "filename": fname,
                            "data": item,
                            "step": os.path.basename(path)
                        })

    # STEP 2
    for fname in os.listdir(STEP2_PATH):
        if not fname.endswith(".json"):
            continue
        with open(os.path.join(STEP2_PATH, fname), encoding="utf-8") as f:
            try:
                data = json.load(f)
            except Exception as e:
                continue

        if isinstance(data, dict):
            for item in data.get("문제점목록", []):
                fields_to_check = [
                    item.get("질문", ""),
                    item.get("요약", ""),
                    item.get("문제점", ""),
                    item.get("관련조항", "")
                ]
                if any(query in field for field in fields_to_check):
                    results.append({
                        "filename": fname,
                        "data": item,
                        "step": "step2"
                    })
                else:
                    score = max(difflib.SequenceMatcher(None, query, field).ratio() for field in fields_to_check)
                    if score > 0.5:
                        results.append({
                            "filename": fname,
                            "data": item,
                            "step": "step2"
                        })

    return results

