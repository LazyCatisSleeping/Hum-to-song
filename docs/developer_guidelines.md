# Hum-to-Song Developer Guidelines

## Set up the project

Install [Git](https://git-scm.com/downloads) and [Python 3.12](https://www.python.org/downloads/). Clone the repository and open the project folder in VS Code.

```bash
git clone https://github.com/LazyCatisSleeping/Hum-to-song.git
cd Hum-to-song
```

If you are reviewing a pull request, switch to its branch before you run these commands. Run them from the project folder. The requirements file installs the app libraries and pytest. Python includes SQLite.

**Windows PowerShell**

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m streamlit run app.py
```

**macOS or Linux**

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pytest -q
.venv/bin/python -m streamlit run app.py
```

To test in a browser, open the Local URL from the terminal and try the steps in the [User Manual](user_manual.md).

## Find the code

| File or folder | Purpose |
| --- | --- |
| [`app.py`](../app.py) | Streamlit entry point. It defines the current English and Chinese labels, inputs, and result display. |
| [`src/audio_processing.py`](../src/audio_processing.py) | Checks input, then trims, mixes, and resamples it to produce a WAV file. |
| [`src/audio_input.py`](../src/audio_input.py), [`src/translations.py`](../src/translations.py) | UI helpers from the recording and upload pull request. The current entry point defines its own widgets and labels. |
| [`src/database.py`](../src/database.py) | Standalone SQLite catalog for song titles, artists, and optional sources. |
| [`tests/`](../tests/) | Automated checks for audio preparation, the SQLite catalog, and the Streamlit page. |
| [`requirements.txt`](../requirements.txt), [`tests.yml`](../.github/workflows/tests.yml) | Python packages and the GitHub Actions test workflow. |

`app.py` passes a filename and audio bytes to `prepare_audio`. The function validates the input and returns PCM-16 WAV bytes at 22,050 Hz with one channel. The page shows an error message when `prepare_audio` raises `AudioPreparationError`.

The song catalog can create a database, add a song, find a song by ID, and list songs in ID order. It stores the default `songs.db` file in the current working directory. Pass a temporary path in tests. The current Streamlit path prepares audio without calling the catalog. [Database design](database_design.md)

## Add and run a test

1. Find the test file for the behavior you changed. Use `tests/test_audio_processing.py` for audio, `tests/test_database.py` for the catalog, and `tests/test_app.py` for the page.
2. Add a function whose name starts with `test_`. Set up one input, run the function, and use `assert` to check the result. Use generated audio or a temporary database so another developer can run the test with a clean checkout.
3. Run the new case first, then run the full suite. If you changed a widget or page text, try the browser steps and check both languages.

For example, add this case to `tests/test_database.py` to check that song names are saved without extra spaces. That file already imports `add_song` and `get_song`. Pytest gives `tmp_path` its own temporary folder for the test.

```python
def test_song_names_are_trimmed(tmp_path):
    db_path = tmp_path / "songs.db"
    song_id = add_song("  Sample Song  ", "  Sample Artist  ", db_path=db_path)
    song = get_song(song_id, db_path=db_path)
    assert song["title"] == "Sample Song"
    assert song["artist"] == "Sample Artist"
```

With the virtual environment active, run these commands. You can also use the virtual environment's Python path from the setup section in place of `python`.

```bash
python -m pytest tests/test_database.py::test_song_names_are_trimmed -q
python -m pytest -q
```

## Check the build history

GitHub Actions installs the requirements and runs `python -m pytest -q` on Ubuntu with Python 3.12. The workflow runs when a pull request opens or receives a new commit, and when a commit reaches `main` or a `peer-review/` branch. [Workflow file](../.github/workflows/tests.yml)

Open the repository's **Actions** tab to see its run history. Select a **Tests** run and open the **pytest** job. Check the branch or pull request and the commit shown on the run page. The pytest step shows the test count or names and errors for failed tests. You can also reach the run from the pull request's **Checks** tab. [GitHub Actions run history](https://github.com/LazyCatisSleeping/Hum-to-song/actions)

## Share a change

Start from the current `main` and create a branch for your work. Check the diff and run the tests before opening a pull request. Include what changed, how you tested it, and any open problems. Keep credentials, local databases, and personal audio out of commits. Ask a teammate to review and check the Actions result before merging.
