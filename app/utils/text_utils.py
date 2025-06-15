# 핵심 개선안 요약 추출 통합
import re

def extract_core_summary_from_text(text: str):
    pattern = r"(?:###?\s*)?핵심\s*개선안\s*요약[:：]?\s*\n?(.*?)(?:\n#+\s|\Z)"
    match = re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL)
    return match.group(1).strip() if match else None
