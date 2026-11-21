"""SQLite song catalog helpers for the Hum-to-Song project."""

import sqlite3
from pathlib import Path

DEFAULT_DB_PATH = Path('songs.db')


def create_database(db_path=DEFAULT_DB_PATH):
    """Create the songs table if it does not already exist."""
    with sqlite3.connect(db_path) as connection:
        connection.execute('''
            CREATE TABLE IF NOT EXISTS songs (
                song_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                artist TEXT NOT NULL,
                source TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        ''')


def add_song(title, artist, source=None, db_path=DEFAULT_DB_PATH):
    """Insert a song and return its numeric ID."""
    if not title or not title.strip() or not artist or not artist.strip():
        raise ValueError('Title and artist are required.')
    create_database(db_path)
    with sqlite3.connect(db_path) as connection:
        cursor = connection.execute(
            'INSERT INTO songs (title, artist, source) VALUES (?, ?, ?)',
            (title.strip(), artist.strip(), source),
        )
        return cursor.lastrowid


def get_song(song_id, db_path=DEFAULT_DB_PATH):
    """Return one song as a dictionary, or None when not found."""
    create_database(db_path)
    with sqlite3.connect(db_path) as connection:
        connection.row_factory = sqlite3.Row
        row = connection.execute(
            'SELECT song_id, title, artist, source, created_at FROM songs WHERE song_id = ?',
            (song_id,),
        ).fetchone()
        return dict(row) if row else None


def list_songs(db_path=DEFAULT_DB_PATH):
    """Return all songs ordered by their IDs."""
    create_database(db_path)
    with sqlite3.connect(db_path) as connection:
        connection.row_factory = sqlite3.Row
        rows = connection.execute(
            'SELECT song_id, title, artist, source, created_at FROM songs ORDER BY song_id'
        ).fetchall()
        return [dict(row) for row in rows]
