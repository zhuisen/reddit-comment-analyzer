"""
Reddit API client wrapper.

Uses PRAW (official Python Reddit API Wrapper) for OAuth2 authentication.
All requests are read-only and rate-limited.
"""
from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from typing import Iterator

from .rate_limiter import RateLimitConfig, TokenBucketLimiter

logger = logging.getLogger(__name__)


@dataclass
class CommentRecord:
    """A single collected comment (sans PII by default)."""

    comment_id: str
    post_id: str
    subreddit: str
    score: int
    created_utc: float
    body: str
    depth: int
    author_hash: str | None = None  # Optional anonymized author


class RedditClient:
    """
    Read-only Reddit client with built-in rate limiting.

    Requires environment variables:
      - REDDIT_CLIENT_ID
      - REDDIT_CLIENT_SECRET
      - REDDIT_USER_AGENT
    """

    def __init__(self, rate_limit: RateLimitConfig | None = None) -> None:
        self._limiter = TokenBucketLimiter(rate_limit or RateLimitConfig())
        self._reddit = self._build_reddit()

    def _build_reddit(self):
        """
        Build PRAW Reddit instance in read-only mode.

        Note: praw is a runtime dependency. Import is deferred so the rest of
        the codebase can be imported without praw installed (e.g. for testing).
        """
        try:
            import praw  # type: ignore
        except ImportError as e:
            raise RuntimeError(
                "praw is required. Install via: pip install -r requirements.txt"
            ) from e

        client_id = os.environ.get("REDDIT_CLIENT_ID")
        client_secret = os.environ.get("REDDIT_CLIENT_SECRET")
        user_agent = os.environ.get("REDDIT_USER_AGENT")

        if not all([client_id, client_secret, user_agent]):
            raise RuntimeError(
                "Missing Reddit credentials. Copy .env.example to .env and fill in."
            )

        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
        )
        reddit.read_only = True
        return reddit

    def iter_subreddit_comments(
        self,
        subreddit_name: str,
        category: str = "hot",
        max_posts: int = 50,
        comment_depth: int = 3,
        min_post_score: int = 5,
    ) -> Iterator[CommentRecord]:
        """
        Yield comments from a subreddit's recent posts.

        Rate-limited automatically. Read-only.
        """
        subreddit = self._reddit.subreddit(subreddit_name)
        posts_method = {
            "hot": subreddit.hot,
            "new": subreddit.new,
            "top": subreddit.top,
        }.get(category, subreddit.hot)

        post_count = 0
        for post in posts_method(limit=max_posts):
            self._limiter.acquire()

            if post.score < min_post_score:
                continue
            if post.stickied or post.removed_by_category:
                continue

            post_count += 1
            logger.info("Processing post %s (%d/%d)", post.id, post_count, max_posts)

            try:
                post.comments.replace_more(limit=0)
            except Exception as e:
                logger.warning("Failed to expand comments for %s: %s", post.id, e)
                continue

            for comment in post.comments.list():
                if getattr(comment, "depth", 0) > comment_depth:
                    continue
                if not getattr(comment, "body", None):
                    continue
                if comment.body in ("[deleted]", "[removed]"):
                    continue

                yield CommentRecord(
                    comment_id=comment.id,
                    post_id=post.id,
                    subreddit=subreddit_name,
                    score=comment.score,
                    created_utc=comment.created_utc,
                    body=comment.body,
                    depth=getattr(comment, "depth", 0),
                )
