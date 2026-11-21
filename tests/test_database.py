"""Tests use temporary SQLite files, not the team's real database."""

import sqlite3
import pytest

from src.database import add_song, create_database, get_song, list_songs


def test_create_database_creates_songs_table(tmp_path):
    db_path = tmp_path / 'test_songs.db'
    create_database(db_path)
    with sqlite3.connect(db_path) as connection:
        table = connection.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='songs'"
        ).fetchone()
    assert table == ('songs',)


def test_create_database_can_run_twice(tmp_path):
    db_path = tmp_path / 'test_songs.db'
    create_database(db_path)
    create_database(db_path)
    assert db_path.exists()


def test_add_and_get_song(tmp_path):
    db_path = tmp_path / 'test_songs.db'
    song_id = add_song('Test Song', 'Test Artist', 'manual', db_path)
    song = get_song(song_id, db_path)
    assert song['title'] == 'Test Song'
    assert song['artist'] == 'Test Artist'
    assert song['source'] == 'manual'


def test_list_songs(tmp_path):
    db_path = tmp_path / 'test_songs.db'
    add_song('First', 'Artist A', db_path=db_path)
    add_song('Second', 'Artist B', db_path=db_path)
    assert [song['title'] for song in list_songs(db_path)] == ['First', 'Second']


def test_missing_song_returns_none(tmp_path):
    assert get_song(999, tmp_path / 'test_songs.db') is None


def test_rejects_blank_title(tmp_path):
    with pytest.raises(ValueError, match='required'):
        add_song(' ', 'Artist', db_path=tmp_path / 'test_songs.db')
