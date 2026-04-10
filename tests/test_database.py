"""Tests for the storage layer."""
from __future__ import annotations

from src.storage.database import hash_author


def test_hash_author_is_deterministic() -> None:
    h1 = hash_author("alice")
    h2 = hash_author("alice")
    assert h1 == h2


def test_hash_author_differs_by_username() -> None:
    assert hash_author("alice") != hash_author("bob")


def test_hash_author_none_for_empty() -> None:
    assert hash_author(None) is None
    assert hash_author("") is None


def test_hash_author_length() -> None:
    h = hash_author("charlie")
    assert h is not None
    assert len(h) == 16
