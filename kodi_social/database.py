import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / 'posts.db'

POSTS_DDL = """
CREATE TABLE IF NOT EXISTS posts (
    uid TEXT UNIQUE,
    title TEXT,
    date_published TEXT
)
"""

INSERT = """
INSERT INTO posts
VALUES (?, ?, ?)
"""

CHECK_EXISTS = "SELECT 1 FROM posts WHERE uid = ?"


class DatabaseCursor:

    def __init__(self, db_path: Path = DB_PATH, commit: bool = False):
        self._db_path = db_path
        self._connection = None
        self._commit = commit

    def __enter__(self):
        self._connection = sqlite3.connect(self._db_path)
        cursor = self._connection.cursor()
        return cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._connection is not None:
            if self._commit:
                self._connection.commit()
            self._connection.close()


def create_database() -> None:
    with DatabaseCursor() as cursor:
        cursor.execute(POSTS_DDL)


def post_exists(uid: str) -> bool:
    with DatabaseCursor() as cursor:
        cursor.execute(CHECK_EXISTS, [uid])
        result = cursor.fetchone()
        return bool(result and result[0])


def insert_posts(rows: list[tuple[str, str, str]]) -> None:
    with DatabaseCursor(commit=True) as cursor:
        cursor.executemany(INSERT, rows)
