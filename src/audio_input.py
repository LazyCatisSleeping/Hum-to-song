"""Streamlit recording/upload widgets; UI only, no signal processing."""
from dataclasses import dataclass
import streamlit as st

@dataclass(frozen=True)
class SelectedAudio:
    filename: str
    content: bytes


def choose_audio(labels: dict[str, str]) -> SelectedAudio | None:
    """Return the current user's WAV recording or uploaded audio, if present."""
    # Stable internal values allow switching languages without switching workflows.
    choice = st.radio(
        labels["source"],
        ["record", "upload"],
        format_func=lambda item: labels[item],
        horizontal=True,
        key="audio_source",
    )
    if choice == "record":
        selected = st.audio_input(labels["record"], key="audio_recorder")
        filename = "recording.wav"
    else:
        selected = st.file_uploader(
            labels["upload"], type=["wav", "flac", "ogg"], key="audio_uploader"
        )
        filename = selected.name if selected is not None else ""
    if selected is None:
        return None
    st.audio(selected)
    return SelectedAudio(filename=filename, content=selected.getvalue())
