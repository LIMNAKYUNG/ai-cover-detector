import streamlit as st
import base64
from pathlib import Path

st.set_page_config(
    page_title="AI Cover Detection System",
    page_icon="🎵",
    layout="wide",
)

# -----------------------------
# 기본 스타일
# -----------------------------
def load_css():
    st.markdown("""
    <style>
    /* 전체 배경 */
    .stApp {
        background: linear-gradient(180deg, #0B0B0D 0%, #111318 100%);
        color: #F3F4F6;
        font-family: 'Inter', sans-serif;
    }

    /* 상단 여백 조정 */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 3rem;
        padding-right: 3rem;
    }

    /* 헤더 영역 */
    .hero-container {
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(192, 196, 204, 0.18);
        border-radius: 24px;
        padding: 3rem 3rem 2.5rem 3rem;
        background:
            radial-gradient(circle at top right, rgba(143,168,201,0.14), transparent 30%),
            linear-gradient(135deg, rgba(255,255,255,0.03), rgba(255,255,255,0.01));
        box-shadow: 0 10px 30px rgba(0,0,0,0.35);
        margin-bottom: 1.8rem;
    }

    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        color: #F8F9FA;
        margin-bottom: 0.5rem;
    }

    .hero-subtitle {
        font-size: 1.1rem;
        line-height: 1.7;
        color: #C0C4CC;
        max-width: 850px;
        margin-bottom: 1.5rem;
    }

    /* 웨이브 장식 */
    .wave-wrap {
        margin-top: 1rem;
        opacity: 0.55;
    }

    .wave-line {
        display: flex;
        align-items: flex-end;
        gap: 4px;
        height: 60px;
    }

    .wave-bar {
        width: 4px;
        border-radius: 999px;
        background: linear-gradient(180deg, #F3F4F6 0%, #8FA8C9 100%);
        opacity: 0.9;
    }

    /* 카드 공통 */
    .glass-card {
        background: linear-gradient(180deg, rgba(21,23,28,0.95), rgba(17,19,24,0.95));
        border: 1px solid rgba(192, 196, 204, 0.16);
        border-radius: 22px;
        padding: 1.4rem 1.4rem;
        box-shadow: 0 10px 24px rgba(0,0,0,0.28);
        height: 100%;
    }

    .card-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #F3F4F6;
        margin-bottom: 0.6rem;
    }

    .card-text {
        font-size: 0.97rem;
        line-height: 1.65;
        color: #B7BBC3;
    }

    .mini-label {
        color: #8FA8C9;
        font-size: 0.82rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 0.4rem;
    }

    /* 결과 카드 */
    .result-box {
        background: linear-gradient(180deg, rgba(16,18,22,1), rgba(20,23,29,1));
        border: 1px solid rgba(192, 196, 204, 0.18);
        border-radius: 24px;
        padding: 1.8rem;
        box-shadow: 0 12px 28px rgba(0,0,0,0.3);
    }

    .result-title {
        font-size: 1rem;
        color: #C0C4CC;
        margin-bottom: 0.6rem;
    }

    .result-main {
        font-size: 2rem;
        font-weight: 800;
        color: #F8F9FA;
        margin-bottom: 0.4rem;
    }

    .result-score {
        font-size: 1rem;
        color: #8FA8C9;
        font-weight: 700;
    }

    /* 구간 카드 */
    .segment-card {
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(192, 196, 204, 0.14);
        border-radius: 16px;
        padding: 0.9rem 1rem;
        margin-bottom: 0.8rem;
    }

    .segment-time {
        font-weight: 700;
        color: #F3F4F6;
        margin-bottom: 0.2rem;
    }

    .segment-score {
        color: #8FA8C9;
        font-size: 0.92rem;
    }

    /* 파일 업로드 영역 */
    [data-testid="stFileUploader"] {
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(192, 196, 204, 0.18);
        border-radius: 18px;
        padding: 1rem;
    }

    [data-testid="stFileUploader"] section {
        border: 1px dashed rgba(192, 196, 204, 0.35) !important;
        border-radius: 16px !important;
        background: rgba(255,255,255,0.01);
    }

    /* 버튼 */
    .stButton > button {
        background: linear-gradient(135deg, #C0C4CC 0%, #8FA8C9 100%);
        color: #0B0B0D;
        border: none;
        border-radius: 14px;
        padding: 0.7rem 1.2rem;
        font-weight: 700;
        font-size: 0.95rem;
        transition: all 0.2s ease;
        box-shadow: 0 8px 18px rgba(0,0,0,0.25);
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        filter: brightness(1.03);
    }

    /* 구분 헤더 */
    .section-title {
        font-size: 1.5rem;
        font-weight: 800;
        color: #F3F4F6;
        margin-top: 0.6rem;
        margin-bottom: 1rem;
    }

    /* 수평선 */
    hr {
        border: none;
        border-top: 1px solid rgba(192, 196, 204, 0.14);
        margin: 1.8rem 0;
    }
    </style>
    """, unsafe_allow_html=True)


# -----------------------------
# 더미 분석 함수
# -----------------------------
def fake_predict():
    return {
        "label": "AI 커버곡 가능성 높음",
        "score": 82,
        "summary": "여러 구간에서 보컬 패턴이 비정상적으로 매끄럽게 나타나 AI 생성 보컬일 가능성이 높게 분석되었습니다.",
        "segments": [
            {"time": "00:21 ~ 00:29", "score": 0.91},
            {"time": "01:02 ~ 01:10", "score": 0.84},
            {"time": "01:34 ~ 01:41", "score": 0.79},
        ]
    }


# -----------------------------
# 헤더
# -----------------------------
def render_hero():
    bars = [18, 42, 26, 55, 20, 48, 32, 58, 23, 44, 29, 52, 16, 38, 25, 61, 34, 47, 21, 43, 18, 57, 28, 49]
    bars_html = "".join(
        [f"<div class='wave-bar' style='height:{h}px;'></div>" for h in bars]
    )

    st.markdown(f"""
    <div class="hero-container">
        <div class="mini-label">Silver Wave Dashboard</div>
        <div class="hero-title">AI Cover Detection System</div>
        <div class="hero-subtitle">
            업로드한 음원의 보컬 패턴을 분석하여 AI 커버곡 여부를 식별합니다.
            오디오 딥페이크 탐지 기반으로 결과를 시각화하고, 의심 구간과 분석 결과를 직관적으로 제공합니다.
        </div>
        <div class="wave-wrap">
            <div class="wave-line">
                {bars_html}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# -----------------------------
# 기능 카드
# -----------------------------
def render_feature_cards():
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="glass-card">
            <div class="mini-label">Step 01</div>
            <div class="card-title">Upload Audio</div>
            <div class="card-text">
                mp3 또는 wav 형식의 노래 파일을 업로드하여 분석을 시작합니다.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="glass-card">
            <div class="mini-label">Step 02</div>
            <div class="card-title">Analyze Voice Pattern</div>
            <div class="card-text">
                모델이 오디오를 전처리하고 구간별 보컬 패턴을 분석합니다.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="glass-card">
            <div class="mini-label">Step 03</div>
            <div class="card-title">Detect AI Cover</div>
            <div class="card-text">
                최종 판별 결과와 AI 가능성 점수, 의심 구간 정보를 제공합니다.
            </div>
        </div>
        """, unsafe_allow_html=True)


# -----------------------------
# 메인
# -----------------------------
load_css()
render_hero()
render_feature_cards()

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown('<div class="section-title">Upload Track</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "음원 파일을 업로드하세요",
    type=["wav", "mp3"]
)

if uploaded_file is not None:
    st.audio(uploaded_file)

    col_btn1, col_btn2, _ = st.columns([1, 1, 4])
    with col_btn1:
        analyze = st.button("Analyze Audio")
    with col_btn2:
        st.button("Clear")

    if analyze:
        with st.spinner("오디오를 분석하는 중입니다..."):
            result = fake_predict()

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<div class="section-title">Detection Result</div>', unsafe_allow_html=True)

        left, right = st.columns([1.2, 1])

        with left:
            st.markdown(f"""
            <div class="result-box">
                <div class="result-title">Final Detection</div>
                <div class="result-main">{result['label']}</div>
                <div class="result-score">AI 가능성 {result['score']}%</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

            st.markdown(f"""
            <div class="glass-card">
                <div class="mini-label">Summary</div>
                <div class="card-title">Analysis Overview</div>
                <div class="card-text">{result['summary']}</div>
            </div>
            """, unsafe_allow_html=True)

        with right:
            st.markdown("""
            <div class="glass-card">
                <div class="mini-label">Suspicious Segments</div>
                <div class="card-title">Highlighted Sections</div>
            """, unsafe_allow_html=True)

            for seg in result["segments"]:
                st.markdown(f"""
                <div class="segment-card">
                    <div class="segment-time">{seg['time']}</div>
                    <div class="segment-score">AI Score: {seg['score']:.2f}</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="glass-card">
            <div class="mini-label">Note</div>
            <div class="card-title">Notice</div>
            <div class="card-text">
                본 결과는 AI 보컬 탐지 모델 기반의 참고용 분석 결과이며,
                저작권 침해 여부에 대한 법적 판단을 대신하지 않습니다.
            </div>
        </div>
        """, unsafe_allow_html=True)

else:
    st.markdown("""
    <div class="glass-card" style="margin-top: 0.6rem;">
        <div class="mini-label">Ready</div>
        <div class="card-title">No Audio Uploaded</div>
        <div class="card-text">
            분석할 음원 파일을 업로드하면 결과 화면이 표시됩니다.
        </div>
    </div>
    """, unsafe_allow_html=True)
