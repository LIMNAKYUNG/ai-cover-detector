import streamlit as st

st.set_page_config(
    page_title="AI Cover Detection System",
    page_icon="🎵",
    layout="wide",
)

# -----------------------------
# 스타일 / 애니메이션
# -----------------------------
def load_css():
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(180deg, #0B0B0D 0%, #111318 100%);
        color: #F3F4F6;
        font-family: 'Inter', sans-serif;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 3rem;
        padding-right: 3rem;
    }

    @keyframes backgroundGlow {
        0%   { transform: translateX(-10px) translateY(0px); opacity: 0.18; }
        50%  { transform: translateX(10px) translateY(-6px); opacity: 0.28; }
        100% { transform: translateX(-10px) translateY(0px); opacity: 0.18; }
    }

    @keyframes wavePulse {
        0%   { transform: scaleY(0.55); opacity: 0.55; }
        50%  { transform: scaleY(1.15); opacity: 1; }
        100% { transform: scaleY(0.55); opacity: 0.55; }
    }

    @keyframes fadeSlideUp {
        0% {
            opacity: 0;
            transform: translateY(18px);
        }
        100% {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes shimmer {
        0%   { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }

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
        animation: fadeSlideUp 0.9s ease-out;
    }

    .hero-container::before {
        content: "";
        position: absolute;
        top: -40%;
        right: -10%;
        width: 320px;
        height: 320px;
        background: radial-gradient(circle, rgba(143,168,201,0.22), transparent 65%);
        filter: blur(20px);
        animation: backgroundGlow 6s ease-in-out infinite;
        pointer-events: none;
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

    .wave-wrap {
        margin-top: 1rem;
        opacity: 0.65;
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
        transform-origin: bottom center;
        animation: wavePulse 1.8s ease-in-out infinite;
    }

    .glass-card {
        background: linear-gradient(180deg, rgba(21,23,28,0.95), rgba(17,19,24,0.95));
        border: 1px solid rgba(192, 196, 204, 0.16);
        border-radius: 22px;
        padding: 1.4rem 1.4rem;
        box-shadow: 0 10px 24px rgba(0,0,0,0.28);
        height: 100%;
        animation: fadeSlideUp 0.8s ease-out;
        transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
    }

    .glass-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 16px 30px rgba(0,0,0,0.35);
        border-color: rgba(143,168,201,0.32);
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

    .result-box {
        position: relative;
        overflow: hidden;
        background: linear-gradient(180deg, rgba(16,18,22,1), rgba(20,23,29,1));
        border: 1px solid rgba(192, 196, 204, 0.18);
        border-radius: 24px;
        padding: 1.8rem;
        box-shadow: 0 12px 28px rgba(0,0,0,0.3);
        animation: fadeSlideUp 0.9s ease-out;
    }

    .result-box::before {
        content: "";
        position: absolute;
        inset: 0;
        background: linear-gradient(
            110deg,
            transparent 20%,
            rgba(255,255,255,0.06) 45%,
            transparent 70%
        );
        background-size: 200% 100%;
        animation: shimmer 4s linear infinite;
        pointer-events: none;
    }

    .result-title {
        font-size: 1rem;
        color: #C0C4CC;
        margin-bottom: 0.6rem;
        position: relative;
        z-index: 1;
    }

    .result-main {
        font-size: 2rem;
        font-weight: 800;
        color: #F8F9FA;
        margin-bottom: 0.4rem;
        position: relative;
        z-index: 1;
    }

    .result-score {
        font-size: 1rem;
        color: #8FA8C9;
        font-weight: 700;
        position: relative;
        z-index: 1;
    }

    .segment-card {
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(192, 196, 204, 0.14);
        border-radius: 16px;
        padding: 0.9rem 1rem;
        margin-bottom: 0.8rem;
        animation: fadeSlideUp 0.8s ease-out;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }

    .segment-card:hover {
        transform: translateX(4px);
        border-color: rgba(143,168,201,0.28);
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

    [data-testid="stFileUploader"] {
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(192, 196, 204, 0.18);
        border-radius: 18px;
        padding: 1rem;
        animation: fadeSlideUp 0.9s ease-out;
    }

    [data-testid="stFileUploader"] section {
        border: 1px dashed rgba(192, 196, 204, 0.35) !important;
        border-radius: 16px !important;
        background: rgba(255,255,255,0.01);
    }

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
        transform: translateY(-2px) scale(1.01);
        filter: brightness(1.05);
    }

    .section-title {
        font-size: 1.5rem;
        font-weight: 800;
        color: #F3F4F6;
        margin-top: 0.6rem;
        margin-bottom: 1rem;
        animation: fadeSlideUp 0.7s ease-out;
    }

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

    bars_html = ""
    for i, h in enumerate(bars):
        delay = round(i * 0.08, 2)
        duration = 1.6 + (i % 4) * 0.25
        bars_html += (
            f'<div class="wave-bar" '
            f'style="height:{h}px; animation-delay:{delay}s; animation-duration:{duration}s;">'
            f'</div>'
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
# ✅ 수정: 각 카드를 컬럼 안에서 개별 st.markdown()으로 렌더링하면
#    Streamlit이 HTML을 컬럼 밖으로 밀어내는 문제가 생길 수 있음.
#    세 카드를 단일 HTML 블록으로 조립 후 컬럼 없이 flex로 배치하도록 변경.
# -----------------------------
def render_feature_cards():
    st.markdown("""
    <div style="display: flex; gap: 1.2rem; margin-bottom: 0.4rem;">
        <div class="glass-card" style="flex: 1;">
            <div class="mini-label">Step 01</div>
            <div class="card-title">Upload Audio</div>
            <div class="card-text">
                mp3 또는 wav 형식의 노래 파일을 업로드하여 분석을 시작합니다.
            </div>
        </div>
        <div class="glass-card" style="flex: 1;">
            <div class="mini-label">Step 02</div>
            <div class="card-title">Analyze Voice Pattern</div>
            <div class="card-text">
                모델이 오디오를 전처리하고 구간별 보컬 패턴을 분석합니다.
            </div>
        </div>
        <div class="glass-card" style="flex: 1;">
            <div class="mini-label">Step 03</div>
            <div class="card-title">Detect AI Cover</div>
            <div class="card-text">
                최종 판별 결과와 AI 가능성 점수, 의심 구간 정보를 제공합니다.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# -----------------------------
# 메인 렌더링
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
        clear = st.button("Clear")

    if analyze:
        st.markdown("""
        <div class="glass-card" style="margin-top: 1rem; margin-bottom: 1rem;">
            <div class="mini-label">Processing</div>
            <div class="card-title">Analyzing Audio Track</div>
            <div class="card-text">
                보컬 패턴을 분석하고 AI 커버곡 여부를 판별하는 중입니다...
            </div>
            <div class="wave-wrap">
                <div class="wave-line">
                    <div class="wave-bar" style="height:18px; animation-delay:0s;"></div>
                    <div class="wave-bar" style="height:35px; animation-delay:0.1s;"></div>
                    <div class="wave-bar" style="height:22px; animation-delay:0.2s;"></div>
                    <div class="wave-bar" style="height:48px; animation-delay:0.3s;"></div>
                    <div class="wave-bar" style="height:28px; animation-delay:0.4s;"></div>
                    <div class="wave-bar" style="height:42px; animation-delay:0.5s;"></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

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
            # ✅ 수정: glass-card 열기 → 루프로 segment-card 추가 → glass-card 닫기를
            #    각각 별도 st.markdown()으로 호출하면 Streamlit이 독립 블록으로 처리해
            #    열린 태그가 화면에 그대로 노출됨.
            #    segment HTML을 루프에서 문자열로 조립한 뒤 단일 st.markdown()으로 렌더링.
            segments_html = ""
            for seg in result["segments"]:
                segments_html += f"""
                <div class="segment-card">
                    <div class="segment-time">{seg['time']}</div>
                    <div class="segment-score">AI Score: {seg['score']:.2f}</div>
                </div>
                """

            st.markdown(f"""
            <div class="glass-card">
                <div class="mini-label">Suspicious Segments</div>
                <div class="card-title">Highlighted Sections</div>
                {segments_html}
            </div>
            """, unsafe_allow_html=True)

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
