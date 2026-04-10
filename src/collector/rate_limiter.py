"""
Token bucket rate limiter for Reddit API calls.

Stays well below Reddit's official 100 req/min limit by defaulting to 60 rpm,
with additional per-request delay as a safety buffer.
"""
from __future__ import annotations

import threading
import time
from dataclasses import dataclass


@dataclass
class RateLimitConfig:
    requests_per_minute: int = 60
    request_delay_seconds: float = 1.5
    max_backoff_seconds: float = 60.0


class TokenBucketLimiter:
    """Thread-safe token bucket limiter."""

    def __init__(self, config: RateLimitConfig) -> None:
        self._config = config
        self._capacity = config.requests_per_minute
        self._tokens = float(config.requests_per_minute)
        self._refill_rate = config.requests_per_minute / 60.0  # tokens per second
        self._last_refill = time.monotonic()
        self._lock = threading.Lock()

    def acquire(self) -> None:
        """Block until a token is available, then consume it."""
        with self._lock:
            self._refill()
            while self._tokens < 1.0:
                wait = (1.0 - self._tokens) / self._refill_rate
                time.sleep(wait)
                self._refill()
            self._tokens -= 1.0

        # Additional safety buffer between requests
        if self._config.request_delay_seconds > 0:
            time.sleep(self._config.request_delay_seconds)

    def _refill(self) -> None:
        now = time.monotonic()
        elapsed = now - self._last_refill
        self._tokens = min(self._capacity, self._tokens + elapsed * self._refill_rate)
        self._last_refill = now


def backoff_seconds(attempt: int, retry_after: float | None = None) -> float:
    """Exponential backoff with optional Retry-After override."""
    if retry_after is not None and retry_after > 0:
        return min(retry_after, 60.0)
    return min(2**attempt, 60.0)
