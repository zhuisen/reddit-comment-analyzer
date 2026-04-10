# Reddit Comment Analyzer

A lightweight, privacy-respecting Python tool for analyzing public Reddit comment sentiment and discussion trends. Designed for community moderators and researchers who want to understand what topics matter most to their subreddit members.

## Purpose

This tool helps Redditors and community moderators better understand their communities by answering questions like:

- **What topics are trending** in our subreddit this week?
- **How does community sentiment** shift around specific issues?
- **Which discussions** generate the most engagement?
- **What concerns** are members raising that moderators should know about?

All analysis is performed on **public** comment data using Reddit's **official OAuth2 API** in read-only mode.

## How It Works

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Reddit API │ ──▶ │   Collect   │ ──▶ │   Analyze   │ ──▶ │   Report    │
│  (OAuth2)   │     │ (rate-lim.) │     │ (local NLP) │     │  (SQLite)   │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
     read-only         batch mode         on-device          local only
```

1. **Collect** — Fetch public comments from target subreddits via Reddit's official API
2. **Analyze** — Run sentiment analysis and topic clustering using local NLP models
3. **Aggregate** — Compute community-level metrics (never individual user profiling)
4. **Report** — Generate trend summaries stored in a local SQLite database

## Key Design Principles

### Respect for Reddit & Its Users

- **Official API only** — OAuth2 authentication, no scraping, no API abuse
- **Read-only access** — Never posts, votes, or modifies content
- **Rate limit compliant** — Stays well under 100 requests/minute (typically <10 req/min)
- **Public data only** — No private messages, no NSFW targeting, no deleted content recovery
- **Aggregated analytics** — Reports show community trends, not individual user tracking

### Privacy-First Architecture

- **Local-only processing** — NLP runs on-device, no data sent to third-party APIs
- **No redistribution** — Data is never shared, sold, or published
- **No persistent user profiles** — Only aggregated subreddit-level statistics stored
- **Deletable on request** — If a Redditor requests removal, their data is purged

## Tech Stack

| Component | Choice | Why |
|-----------|--------|-----|
| Language | Python 3.11+ | Ubiquitous, strong NLP ecosystem |
| Reddit Access | `praw` (official wrapper) | Battle-tested OAuth2 handling |
| Sentiment NLP | Local transformer model | No third-party data sharing |
| Storage | SQLite | Local-first, no cloud dependencies |
| Rate Limiting | Built-in throttle + backoff | Respects Reddit's limits |

## Project Structure

```
reddit-comment-analyzer/
├── src/
│   ├── collector/          # Reddit API client with rate limiting
│   │   ├── __init__.py
│   │   ├── reddit_client.py
│   │   └── rate_limiter.py
│   ├── analyzer/           # NLP & sentiment analysis
│   │   ├── __init__.py
│   │   └── sentiment.py
│   ├── storage/            # Local SQLite persistence
│   │   ├── __init__.py
│   │   └── database.py
│   └── reports/            # Aggregated trend reports
│       ├── __init__.py
│       └── trends.py
├── config/
│   └── config.example.yaml
├── docs/
│   ├── ARCHITECTURE.md
│   ├── RESPONSIBLE_USE.md
│   └── PRIVACY.md
├── tests/
├── .env.example
├── requirements.txt
├── LICENSE
└── README.md
```

## Installation

```bash
git clone https://github.com/zhuisen/reddit-comment-analyzer.git
cd reddit-comment-analyzer
pip install -r requirements.txt
cp .env.example .env  # Fill in your Reddit API credentials
cp config/config.example.yaml config/config.yaml
```

## Configuration

See `config/config.example.yaml` for all options. Minimum setup:

```yaml
reddit:
  user_agent: "script:reddit-comment-analyzer:v0.1.0 (by /u/yourname)"
  rate_limit_rpm: 60  # Well below Reddit's 100/min limit

collection:
  subreddits:
    - singapore
    - technology
  categories: [hot, new]
  max_posts_per_run: 50
  comment_depth: 3

analysis:
  sentiment_model: "distilbert-base-uncased-finetuned-sst-2-english"
  batch_size: 16

storage:
  database_path: "./data/analysis.db"
```

## Target Subreddits

Public subreddits related to market research, product discussions, and local community topics:

- r/singapore
- r/technology
- r/SaaS
- r/datascience
- r/smallbusiness

Read-only access to public comments only. No private or NSFW content.

## Responsible Use

This tool is built to comply with:

- [Reddit's API Terms of Use](https://www.redditinc.com/policies/data-api-terms)
- [Responsible Builder Policy](https://support.reddithelp.com/hc/en-us/articles/42728983564564-Responsible-Builder-Policy)
- [Reddit's User Agreement](https://www.redditinc.com/policies/user-agreement)

See [docs/RESPONSIBLE_USE.md](docs/RESPONSIBLE_USE.md) for our commitments and [docs/PRIVACY.md](docs/PRIVACY.md) for the full privacy policy.

## Status

**Under development** — Pending Reddit API access approval.

Development roadmap:
- [x] Project scaffold and architecture
- [ ] Reddit API client with rate limiting
- [ ] Sentiment analysis pipeline
- [ ] Trend aggregation reports
- [ ] CLI interface
- [ ] Unit tests

## Contributing

This is currently a personal research project. Issues and suggestions welcome.

## License

MIT — see [LICENSE](LICENSE)
