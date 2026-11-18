# Team Upload Guide

This repository starts with empty directories. Each teammate should commit only the files they actually create, revise, or test.

## Planned responsibilities

- Wayne: `README.md`, `docs/requirements.md`
- Lily: `src/audio_input.py`, `src/translations.py`
- Cary: `app.py`, `src/audio_processing.py`, `tests/test_audio_processing.py`, plus integration
- Marlon: `src/database.py`, `docs/database_design.md`, `tests/test_database.py` (planned foundation; not completed song matching)

## Workflow

1. Create the GitHub repository and upload this starter as the first commit.
2. Invite the other contributors.
3. Each teammate clones the repository and creates a feature branch.
4. Add or revise the assigned files, test them, commit under their own verified Git identity, and push.
5. Open a pull request and merge reviewed changes into `main`.
6. After all required files and `requirements.txt` are present, create a virtual environment, install dependencies, and run `python -m streamlit run app.py`.

This starter cannot run until application code is added. The placeholders (.gitkeep) can be removed once their directories contain tracked files. Do not add prewritten code under someone's name as proof that they authored it.
