# Hum-to-Song Recognition — Sprint 2

Team 1 — Escape From DDL | CPS 4301 Software Engineering

**Members:** Weiying (Wayne) Chen, Xinyue (Lily) Feng, Caiyue (Cary) Wang, Marlon Cedeno.

This repository is an audio-input proof of concept, **not a complete song-recognition application**.

## User stories covered

| Story | Feature | Demonstration |
| --- | --- | --- |
| US-01 | Record Humming | Use the browser microphone, grant permission, and record a WAV clip |
| US-02 | Upload Audio | Upload a WAV, FLAC, or OGG file |
| US-03 | Submit Audio for Recognition | Press Submit to pass the selected audio into the processing workflow |
| US-04 | Prepare Audio | Decode, downmix to mono, cap at 30 seconds, resample to 22,050 Hz, and produce PCM-16 WAV |

US-05 (noise reduction), US-06 (pitch extraction), US-07 (melodic pattern), US-08–US-10 (song retrieval/matching/ranking), and US-11 (recognition results) are **not implemented**.

## Run locally

Python 3.10–3.12 recommended.

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Open the local URL shown in the terminal (normally http://localhost:8501). Microphone permission is required for recording. Use the upload option if browser recording is unavailable.

## Test

```bash
python -m pytest -q
```

## Manual acceptance checks

1. Open the app and record a short hum. Submit it; a prepared playable/downloadable WAV appears (US-01, US-03, US-04).
2. Upload a valid WAV/FLAC/OGG, submit it, and verify conversion metadata (US-02, US-03, US-04).
3. Upload an empty, invalid, or silent file; verify a clear error.
4. Upload a 31-second sample; verify output is at most 30 seconds.
5. Verify output is mono, 22,050 Hz, 16-bit PCM WAV.

## Limitations

- Supports WAV, FLAC, OGG uploads; not MP3/M4A.
- Uses the first 30 seconds of audio; no cloud storage or song database.
- Only Sprint 2's audio submission and preparation handoff is demonstrated. Recognition is a future sprint.

## Credits and contributions

All four members are listed as project team members. GitHub commit authorship is recorded per actual author and is **not automatically shared**. Each member should make their own commits or use a truthful `Co-authored-by` trailer for genuine jointly authored changes.
