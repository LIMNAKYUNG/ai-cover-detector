import streamlit as st

st.title("AI 커버곡 판별 시스템")
st.write("음원 파일을 업로드하면 AI 커버곡 여부를 분석합니다.")

uploaded_file = st.file_uploader("음원 파일 업로드", type=["wav", "mp3"])

if uploaded_file is not None:
    st.audio(uploaded_file)
    st.success("파일 업로드 완료")
