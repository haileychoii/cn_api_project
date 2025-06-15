import streamlit as st
import colorlover as cl
# app.py
import re
import random

import os
from dotenv import load_dotenv


# ✅ Streamlit 설정 가장 먼저
st.set_page_config(
    page_title='반려묘보험 분석 챗봇 대시보드', page_icon= "😺",
    layout='wide',
    initial_sidebar_state='expanded'
)
# ✅ .env 가장 먼저 로드
load_dotenv(dotenv_path=".env")  # 정확한 경로 지정
api_key = os.getenv("OPENAI_API_KEY")

from chains.router_chain_ import load_conversational_chain

# ---------- Streamlit 설정 ----------

# ---------- 라디오 버튼 스타일 숨기기 ----------
st.markdown("""
    <style>
    div[role="radiogroup"] > label > div:first-child {
        display: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- 테마 모드 정의 및 적용 ----------
import random
import streamlit as st



# 🎨 테마 정의
theme_modes = {
    "Pastel 모드": {
        "primary": "#CCD3CA",
        "accent": "#F48FB1",         # 파스텔 핑크
        "secondary": "#81D4FA",      # 파스텔 블루
        "background": "#EED3D9",     # 연한 파스텔 배경
        "text": "#222222",           # 어두운 글자색
        "font": "'Pretendard', 'SUIT', 'AppleGothic Neo'"
    },
    "Dark 모드": {
        "primary": "#BB86FC",
        "background": "#1E1E1E",
        "text": "#EEEEEE",
        "font": "'AppleGothic Neo', sans-serif"
    }
}

# 🎛️ 테마 선택
mode = st.sidebar.selectbox("🎨 테마 모드 선택", list(theme_modes.keys()))
colors = theme_modes[mode]

# ✅ 테마 적용 함수
def set_custom_theme(primary, background, text, font, accent=None, secondary=None):
    sidebar_bg = "#F5E8DD"  # 💡 진한 핑크로 바꾸려면 "#F8BBD0"

    st.markdown(
        f"""
        <style>
        html, body, [class*="st-"] {{
            background-color: {background} !important;
            color: {text} !important;
            font-family: {font};
        }}

        h1, h2, h3, h4, h5, h6 {{
            color: {text} !important;
        }}

        /* ✅ 사이드바 배경 */
        section[data-testid="stSidebar"], 
        section[data-testid="stSidebar"] > div:first-child {{
            background-color: {sidebar_bg} !important;
        }}

        /* ✅ 사이드바 내부 간격 */
        section[data-testid="stSidebar"] .stRadio,
        section[data-testid="stSidebar"] .stSelectbox,
        section[data-testid="stSidebar"] label {{
            background-color: transparent !important;
            margin-bottom: 1.0rem !important;
        }}

        /* ✅ hover 효과 */
        section[data-testid="stSidebar"] label:hover {{
            font-weight: bold !important;
            cursor: pointer;
        }}

        
        </style>
        """,
        unsafe_allow_html=True
    )

# ✅ 최종 테마 적용
set_custom_theme(
    colors["primary"],
    colors["background"],
    colors["text"],
    colors["font"],
    accent=colors.get("accent"),
    secondary=colors.get("secondary")
)


# ---------- 사이드바 메뉴 ----------
st.sidebar.title("📚 챗봇 메뉴")
menu = st.sidebar.radio(
    "",
    ["🏠 홈", "📘 프로젝트 소개", "📗 사용 가이드", "📙 FAQ", "📄 보험 요약 보기", "🤖 챗봇", "📊 개선안 평가", "📁 파일 업로드"],
    label_visibility="collapsed"
)

# ---------- 세션 상태 초기화 ----------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "qa_chain" not in st.session_state:
    st.session_state.qa_chain = load_conversational_chain()

# ---------- 챗봇 안내 ----------
with st.expander("ℹ️ 챗봇 안내"):
    st.markdown("""
    이 챗봇은 **반려묘 보험 약관 분석 프로젝트**를 기반으로 설계되었습니다.  
    사용자가 입력한 질문에 대해 다음을 수행합니다:

    - 📄 관련 문서를 검색(RAG)하여 GPT 기반 답변 생성  
    - 🧠 Step 4의 '핵심문제요약' 및 개선안 참고  
    - 🎯 Step 5의 평가 결과 및 최적 개선안 표시  

    ### 질문 예시
    - '입원비 보장은 어디까지 가능하나요?'
    - '질병 보장 제외 조건이 불리한 이유는?'
    - '삼성화재 고양이 보험에서 개선안 제안은?'  
    """)

# ---------- 메뉴 처리 ----------
# ---------- 메뉴 처리 ----------
if menu == "🤖 챗봇":
    st.title("🐾 보험 약관 분석 챗봇 - 반려묘 보험 중심")

    # ✅ 버튼 스타일 정의
    button_style = """
    <style>
    div.stButton > button {
        height: 4.5em;
        white-space: normal;
        background-color: #f0f2f6;
        color: #222222;
        border: 1px solid #ccc;
        border-radius: 6px;
        font-size: 0.9em;
        padding: 0.5em;
        text-align: left;
        line-height: 1.3em;
    }
    div.stButton > button:hover {
        background-color: #e0e2e6;
    }
    </style>
    """
    st.markdown(button_style, unsafe_allow_html=True)

    # ✅ 화면 2열로 분리: 왼쪽은 소개 / 오른쪽은 입력
    col1, col2 = st.columns([1.3, 1.2])  # 비율 조절 가능

    with col1:
        # ✅ 소개 및 안내
        st.markdown(""" 
        🐱 **반려묘 보험 약관 분석 챗봇**은 복잡한 보험 약관 및 평가 문서를 바탕으로  
        사용자의 질문에 맞는 정보를 **직접 찾아서 설명**해주는 도우미입니다.

        🤖 **질문 가능 보험사 및 분석 범위 예시**  
        본 챗봇은 다음과 같은 보험 약관과 평가 자료를 분석하여 답변합니다:  
        - 삼성 애니펫 반려묘 보험  
        - 한화 LIFEPLUS 스마일펫 보험  
        - 기타 수집된 반려묘 보험 약관 및 관련 평가 문서  

        💡 **어떤 질문을 하면 좋을까요?**  
        - 특정 보험의 보장 범위나 세부 조건  
        - 보장 제한 이유나 조건  
        - 개선된 약관이나 보장 확대 방안  
        - 소비자 관점의 평가 및 실현 가능성 등  
        """)

        st.markdown("📌 **예시 질문을 선택해보세요:**")
        example_questions = [
            "삼성 애니펫 반려묘 보험에서 입원비는 어디까지 보장되나요?",
            "한화 LIFEPLUS 스마일펫 보험의 치료비 보장은 왜 조건이 붙나요?",
            "보장 확대 방안은 어떤 게 있나요?",
            "이 개선안이 실현 가능한가요?",
            "다른 보험사에 비해 어떤 점이 부족한가요?"
        ]
        for q in example_questions:
            if st.button(q):
                st.session_state.example_question = q

    with col2:
        # ✅ 사용자 입력 및 질의창
        default_query = st.session_state.get("example_question", "")
        user_query = st.text_input("질문을 입력하세요", value=default_query, placeholder="예: 입원비 보장이 왜 제한되나요?")

        if st.button("답변 생성") and user_query:
            with st.spinner("GPT가 문서를 검색하고 답변 중..."):
                qa_chain = st.session_state.qa_chain
                chat_history = st.session_state.chat_history
                result = qa_chain({"question": user_query, "chat_history": chat_history})

                answer = result["answer"]
                sources = result.get("source_documents", [])
                st.session_state.chat_history.append((user_query, answer))

            st.markdown("### 📌 GPT 응답")
            st.write(answer)

            # ✅ 출처 문서 분리
            chroma_docs, json_docs = [], []
            for doc in sources:
                src = doc.metadata.get("source", "")
                if "step4" in src or "step5" in src or "step_json_chroma_db" in src:
                    json_docs.append(doc)
                else:
                    chroma_docs.append(doc)

            if chroma_docs:
                st.markdown("### 📚 원문 기반 문서 출처")
                for i, doc in enumerate(chroma_docs, 1):
                    st.markdown(f"**[{i}]** `{doc.metadata.get('source', 'Unknown')}`")
                    st.code(doc.page_content[:500] + "...")

            if json_docs:
                st.markdown("### 🛠️ 개선안 기반 평가 문서")

                def extract_core_summary(text):
                    import re
                    pattern = r"(?:###?\s*)?핵심\s*개선안\s*요약[:：]?\s*\n?(.*?)(?:\n#+\s|\Z)"
                    match = re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL)
                    return match.group(1).strip() if match else None

                for i, doc in enumerate(json_docs, 1):
                    st.markdown(f"**[{i}]** `{doc.metadata.get('source', 'Unknown')}`")
                    core_summary = extract_core_summary(doc.page_content)
                    if core_summary:
                        st.markdown("✅ **핵심 개선안 요약**")
                        st.success(core_summary)
                    else:
                        st.markdown("ℹ️ 핵심 개선안 요약을 추출할 수 없습니다.")
                    with st.expander("📄 전체 내용 보기", expanded=False):
                        st.code(doc.page_content[:800] + "...")

            # ✅ Step4~5 개선 요약 분석 (RAG 기반 검색)
            st.markdown("### 📂 보험 개선 요약 분석 (RAG 기반)")
            rag_matched = query_step_json_chroma_db(user_query, top_k=3)

            if rag_matched:
                for match in rag_matched:
                    title = match['filename'].replace("evaluation_", "").replace(".json", "").replace("_", " ").strip()
                    st.markdown(f"#### 📄 `{title} 개선 요약`")
                    page_content = match.get("page_content", "")
                    core_summary = extract_core_summary(page_content)
                    if core_summary:
                        st.markdown("✅ **핵심 개선안 요약**")
                        st.success(core_summary)
                    with st.expander("📄 전체 JSON 보기", expanded=False):
                        st.json(match["data"])
            else:
                st.info("관련된 개선 요약을 찾을 수 없습니다.")

    # 🔁 이전 대화 표시
    if st.session_state.chat_history:
        st.markdown("---")
        st.markdown("### 💬 이전 대화 기록")
        for i, (q, a) in enumerate(reversed(st.session_state.chat_history[-5:]), 1):
            st.markdown(f"**Q{i}.** {q}")
            st.markdown(f"**A{i}.** {a}")









# ---------- FAQ ----------
elif menu == "FAQ":
    st.title("📙 자주 묻는 질문")
    st.markdown("""
    **Q. 법률 자문을 제공하나요?**
    > 아니요. 참고용 정보 제공 도우미입니다.

    **Q. 어떤 데이터로 작동하나요?**
    > Step2~5 결과, Chroma 벡터 DB, 외부 검색 정보를 기반으로 합니다.
    """)


elif menu == "📄 보험 요약 보기":
    st.title("📄 보험 약관 요약 보기")
    summary_path = "data/보험약관/summary/"

    if not os.path.exists(summary_path):
        st.error("`data/보험약관/summary/` 폴더가 존재하지 않습니다.")
    else:
        file_options = []
        file_map = {}

        for filename in os.listdir(summary_path):
            if filename.endswith(".txt"):
                file_path = os.path.join(summary_path, filename)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                    # 1. "청크 * 요약" + 앞뒤 ### (임의의 # 1개 이상) 제거
                    content = re.sub(r"\n*#{1,}\s*청크\s*[-–(]?\s*\d+\s*[)–]?\s*요약\s*#{1,}\n*", "\n", content, flags=re.IGNORECASE)
                    content = re.sub(r"청크\s*[-–(]?\s*\d+\s*[)–]?\s*요약", "", content, flags=re.IGNORECASE)

                    # 줄 단위로 나누기
                    lines = content.splitlines()

                    # 2. 보험명은 첫 또는 두 번째 줄에 있는 #으로 시작하는 줄에서 추출 (요약 제거)
                    display_title = None
                    for i in range(min(2, len(lines))):
                        line = lines[i].strip()
                        if line.startswith("#"):
                            temp_title = line.lstrip("#").strip()
                            temp_title = temp_title.replace("요약", "").strip()
                            if temp_title:
                                display_title = temp_title
                                break

                    # 없으면 파일명 기반 대체
                    if not display_title:
                        display_title = filename.replace(".txt", "").replace("_summary", "").replace("_", " ")

                    file_options.append(display_title)
                    file_map[display_title] = (filename, content)

        if not file_options:
            st.warning("요약 파일이 존재하지 않습니다.")
        else:
            selected_title = st.selectbox("📑 요약 파일 선택", file_options)
            selected_file, summary_text = file_map[selected_title]

            # 3. # 보험명 요약 형태: 첫 번째 줄만 남기고 나머지는 제거 (대소문자 구분 없이)
            header_pattern = re.compile(r"^#.*요약\s*$", re.IGNORECASE | re.MULTILINE)
            matches = list(header_pattern.finditer(summary_text))
            if len(matches) > 1:
                for match in matches[1:]:
                    summary_text = summary_text.replace(match.group(), "")

            # 4. 공백 정리
            summary_text = re.sub(r"\n{2,}", "\n\n", summary_text).strip()

            # 5. 목차 추출: ## 헤더만, 숫자 포함 제외, 중복 제거
            seen_titles = set()
            toc_lines = []
            for line in summary_text.splitlines():
                if line.startswith("## "):
                    title = line.strip("#").strip()

                    if any(char.isdigit() for char in title):
                        continue
                    if title in seen_titles:
                        continue
                    seen_titles.add(title)

                    anchor = title.lower().replace(" ", "-").replace(".", "").replace(":", "")
                    short_title = title if len(title) <= 30 else title[:30] + "…"
                    toc_lines.append(f"- [{short_title}](#{anchor})")

            st.subheader(f"📘 `{selected_title}` 요약 내용")

            if toc_lines:
                with st.expander("🗂️ 주요 목차 보기", expanded=False):
                    st.markdown("\n".join(toc_lines), unsafe_allow_html=True)

            st.markdown("---")
            st.markdown(summary_text, unsafe_allow_html=True)
