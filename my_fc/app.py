# app.py
import io
import os
import subprocess
import traceback
import wave
import numpy as np
import torch
import torch.nn.functional as F
import torchaudio
from flask import Flask, request, jsonify
from transformers import RobertaTokenizer, Wav2Vec2FeatureExtractor

# 导入你的模型定义（根据实际情况修改）
from utils.context_model import rob_d2v_cme_context
from utils.cross_attn_encoder import CMELayer, BertConfig  # 如果使用 cme 模型

# ---------- 配置 ----------
SAMPLE_RATE = 16000
AUDIO_MAX_LEN = 96000
TEXT_MAX_LEN = 96
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
FFMPEG_BIN = os.environ.get("FFMPEG_PATH", "ffmpeg")

# 模型配置（必须与训练时一致）
class Config:
    dropout = 0.1
    n_classes = 3
    num_hidden_layers = 5

# ---------- 全局加载模型（服务启动时加载一次）----------
print("🔄 加载 tokenizer 和特征提取器...")
tokenizer = RobertaTokenizer.from_pretrained("./models/roberta-large", local_files_only=True)
feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained(
    "./models/facebook_data2vec-audio-large-960h", local_files_only=True
)

print("🔄 加载模型权重...")
model = rob_d2v_cme_context(Config()).to(DEVICE)
model.load_state_dict(torch.load("./checkpoint/best_model.pth", map_location=DEVICE))
model.eval()
print("✅ 模型加载完成！")

# ---------- 预处理函数 ----------
def _decode_wav_bytes(wav_bytes):
    with wave.open(io.BytesIO(wav_bytes), 'rb') as wf:
        channels = wf.getnchannels()
        sample_width = wf.getsampwidth()
        sr = wf.getframerate()
        frame_count = wf.getnframes()
        raw = wf.readframes(frame_count)

    if sample_width == 1:
        arr = np.frombuffer(raw, dtype=np.uint8).astype(np.float32)
        arr = (arr - 128.0) / 128.0
    elif sample_width == 2:
        arr = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
    elif sample_width == 4:
        arr = np.frombuffer(raw, dtype=np.int32).astype(np.float32) / 2147483648.0
    else:
        raise ValueError(f"Unsupported sample width: {sample_width}")

    if channels > 1:
        arr = arr.reshape(-1, channels).mean(axis=1)

    audio = torch.from_numpy(arr)
    return audio, sr


def load_audio_from_bytes(bytes_data):
    # 1) 先按标准 WAV 解析（最快且无额外依赖）
    try:
        audio, sr = _decode_wav_bytes(bytes_data)
    except wave.Error:
        # 2) 非 WAV 时，尝试通过 ffmpeg 管道转为 WAV
        try:
            proc = subprocess.run(
                [
                    FFMPEG_BIN,
                    '-hide_banner',
                    '-loglevel', 'error',
                    '-i', 'pipe:0',
                    '-f', 'wav',
                    '-ac', '1',
                    '-ar', str(SAMPLE_RATE),
                    'pipe:1'
                ],
                input=bytes_data,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True
            )
            audio, sr = _decode_wav_bytes(proc.stdout)
        except Exception as e:
            raise RuntimeError(
                "Unsupported audio format and ffmpeg decode failed. "
                "Please ensure ffmpeg is installed and available in PATH, "
                "or upload WAV audio."
            ) from e

    if sr != SAMPLE_RATE:
        resampler = torchaudio.transforms.Resample(sr, SAMPLE_RATE)
        audio = resampler(audio)
    return audio

def preprocess_audio(waveform):
    features = feature_extractor(
        waveform.numpy(), sampling_rate=SAMPLE_RATE,
        max_length=AUDIO_MAX_LEN, truncation=True, padding="max_length",
        return_attention_mask=True
    )
    return torch.tensor(features["input_values"][0]), torch.tensor(features["attention_mask"][0])

def preprocess_text(text):
    enc = tokenizer(text, max_length=TEXT_MAX_LEN, padding="max_length",
                    truncation=True, return_attention_mask=True)
    return torch.tensor(enc["input_ids"]), torch.tensor(enc["attention_mask"])

# ---------- Flask 应用 ----------
app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # 解析 multipart/form-data
        text = request.form.get('text', '')
        text_context = request.form.get('text_context', '')
        audio_file = request.files.get('audio')
        if not text or not audio_file:
            return jsonify({"error": "Missing text or audio"}), 400

        # 主音频
        wav_main = load_audio_from_bytes(audio_file.read())
        audio_val, audio_mask = preprocess_audio(wav_main)

        # 上下文音频（多个，自动拼接）
        ctx_files = request.files.getlist('audio_context')
        wavs = [load_audio_from_bytes(f.read()) for f in ctx_files if f.filename]
        if wavs:
            wav_concat = torch.cat(wavs, dim=0)
            audio_ctx_val, audio_ctx_mask = preprocess_audio(wav_concat)
        else:
            # 没有上下文音频时，退化为使用主音频，避免全零上下文导致模型内部出现 NaN
            audio_ctx_val = audio_val.clone()
            audio_ctx_mask = audio_mask.clone()

        # 文本
        text_ids, text_mask = preprocess_text(text)
        ctx_ids, ctx_mask = preprocess_text(text_context) if text_context else preprocess_text("")

        # 推理
        with torch.no_grad():
            outputs = model(
                text_inputs=text_ids.unsqueeze(0).to(DEVICE),
                text_mask=text_mask.unsqueeze(0).to(DEVICE),
                text_context_inputs=ctx_ids.unsqueeze(0).to(DEVICE),
                text_context_mask=ctx_mask.unsqueeze(0).to(DEVICE),
                audio_inputs=audio_val.unsqueeze(0).to(DEVICE),
                audio_mask=audio_mask.unsqueeze(0).to(DEVICE),
                audio_context_inputs=audio_ctx_val.unsqueeze(0).to(DEVICE),
                audio_context_mask=audio_ctx_mask.unsqueeze(0).to(DEVICE)
            )

        # 兼容二分类/多分类输出：当输出不是标量时返回向量与预测类别
        m_logits = outputs["M"].detach().cpu().squeeze(0)
        t_logits = outputs["T"].detach().cpu().squeeze(0)
        a_logits = outputs["A"].detach().cpu().squeeze(0)

        if m_logits.numel() == 1:
            return jsonify({
                "prediction": float(m_logits.item()),
                "text_score": float(t_logits.item()),
                "audio_score": float(a_logits.item())
            })

        m_probs = F.softmax(m_logits, dim=-1)
        t_probs = F.softmax(t_logits, dim=-1)
        a_probs = F.softmax(a_logits, dim=-1)

        return jsonify({
            "prediction": int(torch.argmax(m_probs).item()) + 1,
            "logits": {
                "M": m_logits.tolist(),
                "T": t_logits.tolist(),
                "A": a_logits.tolist()
            },
            "probabilities": {
                "M": m_probs.tolist(),
                "T": t_probs.tolist(),
                "A": a_probs.tolist()
            }
        })
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)