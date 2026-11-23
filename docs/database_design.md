# Database Design — Hum-to-Song

## Purpose

This SQLite module stores basic information about songs. It does **not** recognize humming or match melodies. It is separate from the existing Streamlit audio preparation flow.

## Songs table

| Column | SQLite type | Meaning |
| --- | --- | --- |
| `song_id` | INTEGER PRIMARY KEY AUTOINCREMENT | Unique song identifier |
| `title` | TEXT NOT NULL | Song title |
| `artist` | TEXT NOT NULL | Song artist |
| `source` | TEXT | Optional source of catalog entry |
| `created_at` | TEXT NOT NULL | Creation timestamp (SQLite `CURRENT_TIMESTAMP`) |

## Python functions

- `create_database(db_path)`: Creates the table if needed.
- `add_song(title, artist, source, db_path)`: Adds a song and returns its ID.
- `get_song(song_id, db_path)`: Finds a song by ID, or returns `None`.
- `list_songs(db_path)`: Returns all stored songs.

The default database filename is `songs.db` relative to the working directory. SQL query parameters (`?`) are used for user-provided values.

## Tests

From the project root, run `python -m pytest tests/test_database.py -v`. Tests use temporary database files through pytest's `tmp_path` fixture and do not modify the default database.

## Current integration status

This module is standalone and is not called from `app.py`. No melody features, matching algorithm, or song-recognition results are implemented here.
