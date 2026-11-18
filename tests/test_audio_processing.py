from io import BytesIO
import numpy as np
import pytest
import soundfile as sf
from src.audio_processing import (
    AudioPreparationError, prepare_audio, TARGET_SAMPLE_RATE, MAX_DURATION_SECONDS
)


def wave_bytes(rate=44100, seconds=1.0, channels=2, amplitude=0.3):
    t = np.arange(int(rate * seconds)) / rate
    wave = (amplitude * np.sin(2 * np.pi * 440 * t)).astype('float32')
    sound = np.column_stack([wave] * channels)
    buffer = BytesIO()
    sf.write(buffer, sound, rate, format='WAV')
    return buffer.getvalue()


def test_prepare_resamples_and_downmixes():
    result = prepare_audio('humming.wav', wave_bytes())
    output, rate = sf.read(BytesIO(result.wav_bytes))
    assert rate == TARGET_SAMPLE_RATE
    assert output.ndim == 1
    assert len(output) == TARGET_SAMPLE_RATE


def test_truncates_long_recording():
    result = prepare_audio('humming.wav', wave_bytes(rate=8000, seconds=31, channels=1))
    assert result.duration_seconds <= MAX_DURATION_SECONDS + 1 / TARGET_SAMPLE_RATE


def test_rejects_unsupported_format():
    with pytest.raises(AudioPreparationError, match='WAV'):
        prepare_audio('song.mp3', b'test')


def test_rejects_empty_file():
    with pytest.raises(AudioPreparationError, match='empty'):
        prepare_audio('song.wav', b'')


def test_rejects_silence():
    with pytest.raises(AudioPreparationError, match='silent'):
        prepare_audio('song.wav', wave_bytes(amplitude=0))


def test_rejects_invalid_data():
    with pytest.raises(AudioPreparationError, match='decode'):
        prepare_audio('song.wav', b'not a wave')
