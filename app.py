
"""Hum-to-Song Recognition Program - Sprint 2."""

import streamlit as st
from src.audio_processing import prepare_audio, AudioPreparationError

st.set_page_config(
    page_title="Hum-to-Song Recognition",
    page_icon="🎵",
    layout="centered"
)

TRANSLATIONS = {
    "English": {
        "title": "Hum-to-Song Recognition",
        "subtitle": "Sprint 2: Recording, Uploading, Submission, and Audio Preparation",
        "notice": "Song recognition is not implemented yet. This demo prepares audio for later analysis.",
        "source": "Choose an audio source",
        "record": "Record Humming",
        "upload": "Upload Audio",
        "submit": "Submit Audio for Processing",
        "success": "Audio submitted and prepared successfully.",
        "prepared": "Prepared Audio",
        "download": "Download Prepared WAV",
        "ready": "Ready for future noise reduction, pitch extraction, and song matching.",
        "language": "Language / 语言"
    },
    "中文": {
        "title": "哼唱歌曲识别",
        "subtitle": "Sprint 2：录音、上传、提交和音频预处理",
        "notice": "歌曲识别尚未实现。本程序用于准备后续分析所需的音频。",
        "source": "选择音频来源",
        "record": "录制哼唱",
        "upload": "上传音频",
        "submit": "提交音频进行处理",
        "success": "音频提交并处理成功。",
        "prepared": "处理后的音频",
        "download": "下载处理后的 WAV 文件",
        "ready": "音频已准备好，可用于后续降噪、音高提取和歌曲匹配。",
        "language": "Language / 语言"
    }
}

# Language selection
language = st.selectbox(
    "Language / 语言",
    ["English", "中文"],
    key="language_selector"
)

t = TRANSLATIONS[language]

# Main interface
st.title(t["title"])
st.caption(t["subtitle"])
st.info(t["notice"])

# Audio source selection
mode = st.radio(
    t["source"],
    [t["record"], t["upload"]],
    horizontal=True,
    key="audio_source"
)

selected = None
filename = None

if mode == t["record"]:
    selected = st.audio_input(
        t["record"],
        key="audio_recorder"
    )
    filename = "recording.wav"

else:
    selected = st.file_uploader(
        t["upload"],
        type=["wav", "flac", "ogg"],
        key="audio_uploader"
    )
    if selected is not None:
        filename = selected.name

# Audio preview
if selected is not None:
    st.audio(selected)

# Submit and process
if st.button(
    t["submit"],
    type="primary",
    disabled=selected is None,
    key="submit_audio"
):
    try:
        result = prepare_audio(
            filename,
            selected.getvalue()
        )

    except AudioPreparationError as exc:
        st.error(str(exc))

    else:
        st.session_state["processed_audio"] = result.wav_bytes
        st.session_state["processed_metadata"] = (
            result.sample_rate,
            result.duration_seconds
        )
        st.success(t["success"])

# Display processed audio
if "processed_audio" in st.session_state:
    sample_rate, duration = st.session_state["processed_metadata"]

    st.subheader(t["prepared"])

    st.write(
        f"Mono WAV | {sample_rate:,} Hz | {duration:.2f} s"
    )

    st.audio(
        st.session_state["processed_audio"],
        format="audio/wav"
    )

    st.download_button(
        t["download"],
        st.session_state["processed_audio"],
        file_name="prepared_humming.wav",
        mime="audio/wav"
    )

    st.caption(t["ready"])
