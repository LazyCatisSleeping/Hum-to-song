from io import BytesIO
import numpy as np
import pytest
import soundfile as sf
from src.audio_processing import (
    AudioPreparationError,
    MAX_DURATION_SECONDS,
    MAX_FILE_SIZE_BYTES,
    TARGET_SAMPLE_RATE,
    prepare_audio,
)


def audio_bytes(rate=44100, seconds=1.0, channels=2, amplitude=0.3, audio_format="WAV"):
    t = np.arange(int(rate * seconds)) / rate
    wave = (amplitude * np.sin(2 * np.pi * 440 * t)).astype('float32')
    sound = np.column_stack([wave] * channels)
    buffer = BytesIO()
    sf.write(buffer, sound, rate, format=audio_format)
    return buffer.getvalue()


@pytest.mark.parametrize("audio_format", ["WAV", "FLAC", "OGG"])
def test_prepare_resamples_and_downmixes(audio_format):
    result = prepare_audio(
        f"humming.{audio_format.lower()}", audio_bytes(audio_format=audio_format)
    )
    output = sf.info(BytesIO(result.wav_bytes))
    assert output.format == "WAV"
    assert output.subtype == "PCM_16"
    assert output.samplerate == TARGET_SAMPLE_RATE
    assert output.channels == 1
    assert output.frames == TARGET_SAMPLE_RATE


def test_truncates_long_recording():
    result = prepare_audio('humming.wav', audio_bytes(rate=8000, seconds=31, channels=1))
    assert result.duration_seconds == MAX_DURATION_SECONDS
    assert result.samples == MAX_DURATION_SECONDS * TARGET_SAMPLE_RATE


def test_rejects_unsupported_format():
    with pytest.raises(AudioPreparationError, match='WAV'):
        prepare_audio('song.mp3', b'test')


def test_rejects_empty_file():
    with pytest.raises(AudioPreparationError, match='empty'):
        prepare_audio('song.wav', b'')


def test_rejects_file_larger_than_limit():
    with pytest.raises(AudioPreparationError, match="15 MB"):
        prepare_audio("song.wav", b"\0" * (MAX_FILE_SIZE_BYTES + 1))


def test_rejects_silence():
    with pytest.raises(AudioPreparationError, match='silent'):
        prepare_audio('song.wav', audio_bytes(amplitude=0))


def test_rejects_invalid_data():
    with pytest.raises(AudioPreparationError, match='decode'):
        prepare_audio('song.wav', b'not a wave')
