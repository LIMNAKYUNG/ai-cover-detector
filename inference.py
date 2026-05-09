import io
import numpy as np
import torch
import torch.nn.functional as F
import torchaudio
import streamlit as st
from huggingface_hub import hf_hub_download
from model import Wav2Vec2Model

REPO_ID    = "eunei/ai-cover-detector-singgraph"
MODEL_FILE = "best.pth"
SR         = 16000
CUT        = 64600    # 학습 시 사용한 샘플 수
THRESHOLD  = 0.5


@st.cache_resource(show_spinner="모델 가중치 로딩 중...")
def load_model():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    weight_path = hf_hub_download(repo_id=REPO_ID, filename=MODEL_FILE)

    class _Args: pass
    model = Wav2Vec2Model(_Args(), device)
    model.load_state_dict(torch.load(weight_path, map_location=device))
    model.eval().to(device)
    return model, device


def load_and_clip(file_bytes: bytes):
    waveform, sr = torchaudio.load(io.BytesIO(file_bytes))

    # 모노 변환
    if waveform.shape[0] > 1:
        waveform = waveform.mean(dim=0, keepdim=True)

    # 16kHz 리샘플
    wav = torchaudio.transforms.Resample(sr, SR)(waveform)  # (1, N)
    wav_np = wav.squeeze(0).numpy()

    # 정규화
    max_abs = np.max(np.abs(wav_np))
    if max_abs > 0:
        wav_np = wav_np / max_abs

    total = wav_np.shape[0]
    clips, timestamps = [], []

    for start in range(0, total, CUT):
        end = start + CUT
        if end > total:
            # 마지막 클립: 패딩
            chunk = wav_np[start:]
            if len(chunk) == 0:
                break
            repeats = int(CUT / len(chunk)) + 1
            chunk = np.tile(chunk, repeats)[:CUT]
        else:
            chunk = wav_np[start:end]

        clips.append(chunk)
        t_s = start // SR
        t_e = t_s + int(CUT / SR)
        timestamps.append(f"{t_s//60:02d}:{t_s%60:02d} ~ {t_e//60:02d}:{t_e%60:02d}")

    return clips, timestamps


def run_inference(uploaded_file) -> dict:
    model, device = load_model()
    clips, timestamps = load_and_clip(uploaded_file.read())

    if not clips:
        return {"label":"분석 불가","score":0,
                "summary":"음원이 너무 짧습니다.","segments":[]}

    scores, suspicious = [], []

    with torch.no_grad():
        for chunk, ts in zip(clips, timestamps):
            # 학습과 동일: x와 x2 모두 같은 16kHz 입력
            x = torch.tensor(chunk, dtype=torch.float32).unsqueeze(0).to(device)  # (1, 64600)
            logits = model(x, x)  # x2도 동일하게
            prob = F.softmax(logits, dim=-1)[0, 1].item()
            scores.append(prob)
            if prob >= THRESHOLD:
                suspicious.append({"time": ts, "score": round(prob, 2)})

    top_k      = max(1, len(scores) // 3)
    song_score = float(np.mean(sorted(scores, reverse=True)[:top_k]))
    song_pct   = round(song_score * 100)
    is_ai      = song_score >= THRESHOLD

    return {
        "label":    "AI 커버곡 가능성 높음" if is_ai else "AI 커버곡 가능성 낮음",
        "score":    song_pct,
        "summary":  (f"분석된 {len(clips)}개 구간 중 {len(suspicious)}개 구간에서 AI 보컬 패턴이 감지되었습니다."
                     if suspicious else
                     f"분석된 {len(clips)}개 구간 모두에서 AI 보컬 패턴이 감지되지 않았습니다."),
        "segments": suspicious[:5],
    }
