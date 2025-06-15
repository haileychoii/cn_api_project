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

# 🎨 파스텔 색상 팔레트 중 일부 (버튼용으로 다양화)
pastel_button_colors = ["#CCD3CA", "#B5C0D0"]

theme_modes = {
    "Pastel 모드": {
        "primary": random.choice(pastel_button_colors),  # 버튼마다 랜덤하게 다양화
        "accent": "#F48FB1",         # 파스텔 핑크
        "secondary": "#81D4FA",      # 파스텔 블루
        "background": "#EED3D9",     #💡 더 연한 파스텔 핑크
        "text": "#222222",           # 어두운 글자색
        "font": "'AppleGothic Neo', sans-serif"
    },
    "Dark 모드": {
        # cl 미정의 오류 방지 - 기본 색상 대체
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
    sidebar_bg = "#F5E8DD"

def set_custom_theme(primary, background, text, font, accent=None, secondary=None):
    sidebar_bg = "#F5E8DD"  # 💡 연한 민트 (진한 핑크로 바꾸려면 "#F8BBD0")

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

        /* ✅ 사이드바 전체 배경 색상 */
        section[data-testid="stSidebar"] > div:first-child {{
            background-color: {sidebar_bg} !important;
        }}

        /* ✅ 사이드바 내부 항목 간격 + 배경 제거 */
        section[data-testid="stSidebar"] .stRadio,
        section[data-testid="stSidebar"] .stSelectbox,
        section[data-testid="stSidebar"] label {{
            background-color: transparent !important;
            margin-bottom: 1.2rem !important;
        }}

        /* ✅ hover 시 bold 효과 */
        section[data-testid="stSidebar"] label:hover {{
            font-weight: bold !important;
            cursor: pointer;
        }}

        /* ✅ 버튼 스타일 개선: 다양한 파스텔 배경색, 투명 글씨 배경 */
        .stButton > button {{
            background-image: linear-gradient(135deg, #FFDEE9 0%, #B5FFFC 100%);
            color: {text} !important;
            border-radius: 8px;
            padding: 0.5em 1em;
            border: none;
            font-weight: 500;
        }}

        .stButton > button:hover {{
            filter: brightness(1.1);
            font-weight: 600;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


# 🎨 최종 적용
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
if menu == "🏠 홈":
    st.title("🏠 반려묘 보험 챗봇 대시보드")
    st.markdown("왼쪽 메뉴에서 원하는 기능을 선택하세요.")

elif menu == "📘 프로젝트 소개":
    st.title("📘 프로젝트 개요")
    st.markdown("""
    반려묘 보험 약관 분석 결과를 기반으로 한 RAG 챗봇 시스템입니다. 
    - GPT-4 기반 LLM + Chroma DB + LangChain 
    - Step2~Step5 결과 및 외부 정보 기반 개선안 탐색
    """)

elif menu == "📗 사용 가이드":
    st.title("📗 사용 방법")
    st.markdown("""
    1. '챗봇' 메뉴에서 자연어로 질문을 입력하세요.
    2. 관련 약관 요약 및 개선안을 기반으로 GPT가 답변을 생성합니다.
    3. 문서 출처와 Step4~5의 개선안도 함께 확인하세요.
    """)
# FAQ-------------
elif menu in ["📙 FAQ", "FAQ"]:
    st.title("📙 자주 묻는 질문")
    st.markdown("""
    **Q. 법률 자문을 제공하나요?**
    > 아니요. 참고용 정보 제공 도우미입니다.

    **Q. 어떤 데이터로 작동하나요?**
    > Step2~5 결과, Chroma 벡터 DB, 외부 검색 정보를 기반으로 합니다.
    """)

# 챗봇 ----------------
elif menu == "🤖 챗봇":

    st.title("🐾 보험 약관 분석 챗봇 - 반려묘 보험 중심")

    # ✅ 소개 및 활용 안내
    st.markdown("""
    🐱 **반려묘 보험 약관 분석 챗봇**은 복잡한 보험 약관 및 평가 문서를 바탕으로  
    사용자의 질문에 맞는 정보를 **직접 찾아서 설명**해주는 도우미입니다.

    🤔 **이 챗봇은 어떤 질문에 유용할까요?**
    - 보험 보장 내용이 궁금할 때 (예: _입원비는 어디까지 보장되나요?_)
    - 보장 제한 이유가 궁금할 때 (예: _치료비 보장은 왜 조건이 붙나요?_)
    - 개선된 약관 내용을 알고 싶을 때 (예: _보장 확대 방안은 어떤 게 있나요?_)
    - 평가 기준과 개선 효과가 궁금할 때 (예: _이 개선안이 실현 가능한가요?_)
    """)

    # ✅ 예시 질문 버튼
    st.markdown("📌 **질문 예시를 선택해보세요:**")
    example_questions = [
        "입원비는 어디까지 보장되나요?",
        "치료비 보장은 왜 조건이 붙나요?",
        "보장 확대 방안은 어떤 게 있나요?",
        "이 개선안이 실현 가능한가요?",
        "다른 보험사에 비해 어떤 점이 부족한가요?"
    ]

    cols = st.columns(len(example_questions))
    for i, (col, q) in enumerate(zip(cols, example_questions)):
        if col.button(f"❓ {q}"):
            st.session_state.example_question = q

    # ✅ 입력창 연결
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
        chroma_docs = []
        json_docs = []

        for doc in sources:
            src = doc.metadata.get("source", "")
            if "step4" in src or "step5" in src or "step_json_chroma_db" in src:
                json_docs.append(doc)
            else:
                chroma_docs.append(doc)

        # ✅ 원문 기반 문서 출처
        if chroma_docs:
            st.markdown("### 📚 원문 기반 문서 출처")
            for i, doc in enumerate(chroma_docs, 1):
                st.markdown(f"**[{i}]** `{doc.metadata.get('source', 'Unknown')}`")
                st.code(doc.page_content[:500] + "...")

        # ✅ 개선안 기반 문서 출처
        if json_docs:
            st.markdown("### 🛠️ 개선안 기반 평가 문서")

            # 핵심 개선안 요약 추출 함수
            def extract_core_summary(text):
                pattern = r"(?:###?\s*)?핵심\s*개선안\s*요약[:：]?\s*\n?(.*?)(?:\n#+\s|\Z)"
                match = re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL)
                if match:
                    return match.group(1).strip()
                return None

            for i, doc in enumerate(json_docs, 1):
                st.markdown(f"**[{i}]** `{doc.metadata.get('source', 'Unknown')}`")

                # 핵심 개선안 요약 추출
                core_summary = extract_core_summary(doc.page_content)
                if core_summary:
                    st.markdown("✅ **핵심 개선안 요약**")
                    st.success(core_summary)
                else:
                    st.markdown("ℹ️ 핵심 개선안 요약을 추출할 수 없습니다.")

                # 전체 내용 일부 보기
                with st.expander("📄 전체 내용 보기", expanded=False):
                    st.code(doc.page_content[:800] + "...")

        # ✅ Step4~5 개선 요약 분석 (기존 search 함수 → RAG 방식으로 변경)
        st.markdown("### 📂 보험 개선 요약 분석 (RAG 기반)")

        rag_matched = query_step_json_chroma_db(user_query, top_k=3)

        if rag_matched:
            for match in rag_matched:
                title = match['filename'].replace("evaluation_", "").replace(".json", "").replace("_", " ").strip()
                st.markdown(f"#### 📄 `{title} 개선 요약`")

                # 핵심 개선안 요약 추출
                page_content = match.get("page_content", "")
                core_summary = extract_core_summary(page_content)
                if core_summary:
                    st.markdown("✅ **핵심 개선안 요약**")
                    st.success(core_summary)

                # 전체 JSON 데이터 보기
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

# 보험 요약 보기---------------------------------
elif menu == "📄 보험 요약 보기":
    st.title("📄 보험 약관 요약 보기")
    summary_path = "data/보험약관/summary/"

    if os.path.exists(summary_path):
        file_labels = []
        file_map = {}

        for f in os.listdir(summary_path):
            if f.endswith('.txt'):
                # 파일명에서 .txt, _summary 제거 + _ → 공백
                label = f.replace(".txt", "").replace("_summary", "").replace("_", " ")
                file_labels.append(label)
                file_map[label] = f

        selected_title = st.selectbox("📑 요약 파일 선택", file_labels)
        selected_file = file_map[selected_title]

        if selected_file:
            file_path = os.path.join(summary_path, selected_file)
            with open(file_path, "r", encoding="utf-8") as f:
                summary_text = f.read()

            # ✅ 1. "청크 * 요약" 형태 제거 (청크+숫자+요약)
            summary_text = re.sub(r"청크\s*[-–]?\s*\d+\s*요약", "", summary_text, flags=re.IGNORECASE)

            # ✅ 2. "~~~ 요약" 같은 문장: 첫 등장 외 모두 제거
            요약_문장_패턴 = re.compile(r"^.*?요약\s*$", re.IGNORECASE | re.MULTILINE)
            matches = list(요약_문장_패턴.finditer(summary_text))
            if len(matches) > 1:
                # 첫 번째 이후 문장 제거
                for match in matches[1:]:
                    summary_text = summary_text.replace(match.group(), "")

            # ✅ 공백 정리
            summary_text = re.sub(r"\n{2,}", "\n\n", summary_text).strip()

            # ✅ 주요 목차: 2단계 헤더(##) 추출
            toc_lines = []
            for line in summary_text.splitlines():
                if line.startswith("## "):
                    title = line.strip("#").strip()
                    short_title = (title[:30] + "…") if len(title) > 30 else title
                    anchor = title.lower().replace(" ", "-").replace(".", "").replace(":", "")
                    toc_lines.append(f"- [{short_title}](#{anchor})")

            st.subheader(f"📘 `{selected_title}` 요약 내용")

            # ✅ 주요 목차 토글로 숨기기
            if toc_lines:
                with st.expander("🗂️ 주요 목차 보기", expanded=False):
                    st.markdown("\n".join(toc_lines))

            st.markdown("---")
            st.markdown(summary_text, unsafe_allow_html=True)

    else:
        st.error("`data/보험약관/summary/` 폴더가 존재하지 않습니다.")


