"""Sprint 2 audio preparation pipeline."""
from dataclasses import dataclass
from io import BytesIO
import numpy as np
import soundfile as sf
import librosa

TARGET_SAMPLE_RATE = 22050
MAX_DURATION_SECONDS = 30
MAX_FILE_SIZE_BYTES = 15 * 1024 * 1024
SUPPORTED_EXTENSIONS = {"wav", "flac", "ogg"}

class AudioPreparationError(ValueError):
    """Invalid or unsupported submitted audio."""

@dataclass(frozen=True)
class PreparedAudio:
    wav_bytes: bytes
    sample_rate: int
    duration_seconds: float
    samples: int


def prepare_audio(filename: str, raw_bytes: bytes) -> PreparedAudio:
    """Decode, mix to mono, trim to at most 30 seconds and resample to 22.05 kHz."""
    ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
    if ext not in SUPPORTED_EXTENSIONS:
        raise AudioPreparationError('Please upload WAV, FLAC, or OGG audio.')
    if not raw_bytes:
        raise AudioPreparationError('The selected file is empty.')
    if len(raw_bytes) > MAX_FILE_SIZE_BYTES:
        raise AudioPreparationError('Audio file exceeds 15 MB.')
    try:
        audio, sample_rate = sf.read(BytesIO(raw_bytes), dtype='float32', always_2d=True)
    except (sf.LibsndfileError, RuntimeError, ValueError) as exc:
        raise AudioPreparationError('Cannot decode this audio file.') from exc
    if sample_rate <= 0 or audio.size == 0:
        raise AudioPreparationError('Audio contains no usable samples.')
    # Avoid processing arbitrarily long recordings. The first 30 seconds are used.
    audio = audio[: int(sample_rate * MAX_DURATION_SECONDS)]
    mono = np.mean(audio, axis=1, dtype=np.float32)
    if not np.all(np.isfinite(mono)):
        raise AudioPreparationError('Audio contains invalid samples.')
    if np.max(np.abs(mono)) < 1e-5:
        raise AudioPreparationError('Audio is silent. Please record a melody.')
    if sample_rate != TARGET_SAMPLE_RATE:
        mono = librosa.resample(mono, orig_sr=sample_rate, target_sr=TARGET_SAMPLE_RATE)
    # Do not apply noise reduction or extract pitch: those are future stories.
    mono = np.clip(mono, -1.0, 1.0)
    buffer = BytesIO()
    sf.write(buffer, mono, TARGET_SAMPLE_RATE, format='WAV', subtype='PCM_16')
    return PreparedAudio(buffer.getvalue(), TARGET_SAMPLE_RATE,
                         len(mono) / TARGET_SAMPLE_RATE, len(mono))
