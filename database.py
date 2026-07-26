"""Small SQLite layer for Google Play reviews."""

import sqlite3
from datetime import datetime, timezone
from pathlib import Path


DATABASE_PATH = Path("data/reviews.sqlite3")


def connect():
    """Open the database and create the review table if needed."""
    DATABASE_PATH.parent.mkdir(exist_ok=True)
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA journal_mode = DELETE")
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS reviews (
            app_id TEXT NOT NULL,
            app_name TEXT NOT NULL,
            review_id TEXT NOT NULL,
            user_name TEXT,
            content TEXT,
            score INTEGER,
            thumbs_up INTEGER,
            app_version TEXT,
            reviewed_at TEXT,
            reply_content TEXT,
            replied_at TEXT,
            scraped_at TEXT NOT NULL,
            PRIMARY KEY (app_id, review_id)
        )
        """
    )
    connection.execute(
        "CREATE INDEX IF NOT EXISTS reviews_by_date ON reviews(reviewed_at)"
    )
    return connection


def newest_review_date(connection, app_id):
    """Return the newest stored review date for one app."""
    row = connection.execute(
        "SELECT MAX(reviewed_at) AS newest FROM reviews WHERE app_id = ?",
        (app_id,),
    ).fetchone()
    return row["newest"]


def save_reviews(connection, app_name, app_id, reviews):
    """Insert one downloaded page and return the number of new rows."""
    scraped_at = datetime.now(timezone.utc).isoformat()
    before = connection.total_changes
    rows = [
        (
            app_id,
            app_name,
            review["reviewId"],
            review.get("userName"),
            review.get("content"),
            review.get("score"),
            review.get("thumbsUpCount"),
            review.get("reviewCreatedVersion"),
            _date(review.get("at")),
            review.get("replyContent"),
            _date(review.get("repliedAt")),
            scraped_at,
        )
        for review in reviews
        if review.get("reviewId")
    ]
    connection.executemany(
        """
        INSERT OR IGNORE INTO reviews (
            app_id, app_name, review_id, user_name, content, score,
            thumbs_up, app_version, reviewed_at, reply_content,
            replied_at, scraped_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        rows,
    )
    connection.commit()
    return connection.total_changes - before


def count_reviews(connection, app_id=None):
    """Count all reviews, or reviews belonging to one app."""
    if app_id:
        row = connection.execute(
            "SELECT COUNT(*) AS total FROM reviews WHERE app_id = ?",
            (app_id,),
        ).fetchone()
    else:
        row = connection.execute(
            "SELECT COUNT(*) AS total FROM reviews"
        ).fetchone()
    return row["total"]


def read_reviews(connection, app_id=None):
    """Read reviews newest-first for later analysis or export."""
    if app_id:
        return connection.execute(
            "SELECT * FROM reviews WHERE app_id = ? ORDER BY reviewed_at DESC",
            (app_id,),
        ).fetchall()
    return connection.execute(
        "SELECT * FROM reviews ORDER BY reviewed_at DESC"
    ).fetchall()


def _date(value):
    return value.isoformat() if value else None
