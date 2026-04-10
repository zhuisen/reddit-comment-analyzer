"""
Local SQLite persistence using SQLAlchemy.

Schema favors aggregated metrics over per-user profiling.
By default, author usernames are not stored.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class StorageConfig:
    database_path: str = "./data/analysis.db"
    retention_days: int = 90
    anonymize_authors: bool = True
    hash_comment_bodies: bool = False


def hash_author(username: str | None, salt: str = "reddit-analyzer-v1") -> str | None:
    """One-way hash of a username. Used when anonymize_authors is True."""
    if not username:
        return None
    return hashlib.sha256(f"{salt}:{username}".encode()).hexdigest()[:16]


# SQL schema (applied via SQLAlchemy or raw SQL on init)
SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS subreddits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    first_seen TEXT NOT NULL,
    last_scanned TEXT
);

CREATE TABLE IF NOT EXISTS posts (
    id TEXT PRIMARY KEY,
    subreddit_id INTEGER NOT NULL REFERENCES subreddits(id),
    score INTEGER NOT NULL,
    num_comments INTEGER NOT NULL,
    created_utc REAL NOT NULL,
    category TEXT,
    collected_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS comments (
    id TEXT PRIMARY KEY,
    post_id TEXT NOT NULL REFERENCES posts(id),
    score INTEGER NOT NULL,
    created_utc REAL NOT NULL,
    depth INTEGER NOT NULL DEFAULT 0,
    author_hash TEXT,           -- nullable; hashed if anonymize_authors
    body TEXT,                  -- nullable; omitted if hash_comment_bodies
    sentiment_label TEXT,
    sentiment_score REAL,
    topic_cluster INTEGER,
    collected_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_comments_post ON comments(post_id);
CREATE INDEX IF NOT EXISTS idx_comments_sentiment ON comments(sentiment_label);
CREATE INDEX IF NOT EXISTS idx_posts_subreddit ON posts(subreddit_id);
"""


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()
