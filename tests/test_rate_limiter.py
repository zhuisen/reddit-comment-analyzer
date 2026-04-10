"""Tests for the token bucket rate limiter."""
from __future__ import annotations

import time

from src.collector.rate_limiter import (
    RateLimitConfig,
    TokenBucketLimiter,
    backoff_seconds,
)


def test_rate_limiter_allows_initial_burst() -> None:
    config = RateLimitConfig(requests_per_minute=60, request_delay_seconds=0)
    limiter = TokenBucketLimiter(config)

    # First request should be immediate
    start = time.monotonic()
    limiter.acquire()
    elapsed = time.monotonic() - start
    assert elapsed < 0.1


def test_backoff_honors_retry_after() -> None:
    assert backoff_seconds(0, retry_after=5.0) == 5.0
    assert backoff_seconds(10, retry_after=3.0) == 3.0


def test_backoff_exponential_without_retry_after() -> None:
    assert backoff_seconds(0) == 1.0
    assert backoff_seconds(1) == 2.0
    assert backoff_seconds(2) == 4.0
    # Capped at 60
    assert backoff_seconds(10) == 60.0
