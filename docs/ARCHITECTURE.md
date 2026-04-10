# Architecture

## Overview

Reddit Comment Analyzer is a local-first pipeline with four stages:

```
  Reddit API          Local Pipeline                    Output
┌────────────┐    ┌──────────────────────────┐    ┌──────────────┐
│            │    │                          │    │              │
│  r/sub1    │───▶│  Collector ──▶ Analyzer  │───▶│  SQLite DB   │
│  r/sub2    │    │      │            │      │    │      │       │
│  r/sub3    │    │      ▼            ▼      │    │      ▼       │
│            │    │  Rate Limit   Sentiment  │    │   Reports    │
└────────────┘    │   + Retry      + Topic   │    │ (Markdown)   │
                  └──────────────────────────┘    └──────────────┘
```

## Components

### 1. Collector (`src/collector/`)

Responsible for fetching data from Reddit's API.

- **`reddit_client.py`** — Thin wrapper around PRAW with OAuth2
- **`rate_limiter.py`** — Token bucket limiter (60 req/min default)

**Design decisions:**
- Uses PRAW for battle-tested OAuth handling
- Never retries on 403/401 (respects account restrictions)
- Exponential backoff on 429 and 5xx
- Honors `Retry-After` header

### 2. Analyzer (`src/analyzer/`)

Runs NLP on collected comments. All inference is **local** — no external API calls.

- **`sentiment.py`** — Sentiment classification (DistilBERT fine-tuned on SST-2)
- Future: topic clustering, entity extraction

**Design decisions:**
- Models loaded from Hugging Face once, then cached locally
- Batch inference for efficiency (16 comments per batch)
- No data leaves the machine — strict privacy boundary

### 3. Storage (`src/storage/`)

Local SQLite persistence layer.

- **`database.py`** — SQLAlchemy ORM models

**Schema (simplified):**

```sql
subreddits (id, name, first_seen, last_scanned)
posts (id, subreddit_id, score, created_utc, category)
comments (id, post_id, score, created_utc, sentiment_score, topic_cluster)
-- Note: no username storage by default (privacy config)
```

**Design decisions:**
- Optional username anonymization at write time
- Retention policy auto-purges old data
- No raw comment text stored if `hash_comment_bodies: true`

### 4. Reports (`src/reports/`)

Generates aggregated trend reports.

- **`trends.py`** — Time-series trend aggregation

**Output format:**
- Markdown by default
- Community-level aggregates only (never per-user)
- Exportable to CSV/JSON for further analysis

## Data Flow

1. **Config load** → read `config.yaml`, validate target subreddits
2. **Authenticate** → OAuth2 with Reddit via PRAW
3. **Collect** → fetch posts from each subreddit, rate-limited
4. **Expand comments** → traverse comment tree to configured depth
5. **Filter** → skip deleted/low-score/short-length content
6. **Analyze** → batch sentiment inference on comment bodies
7. **Store** → write aggregated records to SQLite (with anonymization)
8. **Report** → generate trend markdown on demand

## Rate Limiting Strategy

```python
# Token bucket: 60 tokens, refill 1/second
# Reddit allows 100/min; we stay at 60/min as safety buffer
# Additional 1.5s sleep between requests
# On 429: exponential backoff (1s → 2s → 4s → 8s → give up)
```

## Error Handling

| Error | Action |
|-------|--------|
| 401 Unauthorized | Halt, alert user to re-auth |
| 403 Forbidden | Log, skip resource, continue |
| 429 Rate Limited | Exponential backoff, respect Retry-After |
| 5xx Server Error | Retry up to 3 times with backoff |
| Network timeout | Retry once, then skip |

## Testing

Unit tests mock the Reddit API to avoid test-run rate limit usage.
Integration tests use recorded API responses (VCR.py pattern).
