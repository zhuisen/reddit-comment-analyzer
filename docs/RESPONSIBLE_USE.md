# Responsible Use Policy

This project is built with respect for Reddit, its users, and its community guidelines. This document outlines our commitments.

## Our Commitments

### 1. Official API Only

We use Reddit's **official OAuth2 API** exclusively. This tool will never:

- Scrape Reddit's HTML pages
- Circumvent rate limits or bot detection
- Use unofficial or reverse-engineered endpoints
- Share or reuse API credentials

### 2. Read-Only Operation

This tool is strictly **read-only**. It will never:

- Post comments or submissions
- Vote on posts or comments
- Send private messages
- Modify or delete content
- Impersonate users

### 3. Rate Limit Respect

We operate well below Reddit's published limits:

| Metric | Reddit Limit | Our Target |
|--------|--------------|------------|
| Requests per minute | 100 | ≤60 |
| Typical load | — | ~10 req/min |
| Backoff strategy | — | Exponential + Retry-After |

All requests include a descriptive User-Agent as required by Reddit's API guidelines.

### 4. Public Data Only

We only access **public** data:

- Public subreddit posts and comments
- Public user profile pages (aggregated metrics only)

We do **not** access:

- Private messages or chats
- Deleted or removed content
- NSFW-only content (unless explicitly relevant to research and approved)
- Private or banned subreddits

### 5. Privacy & Anonymization

- Aggregated community metrics only — no individual user profiling
- Usernames are hashed or stripped by default in storage
- No data is sold, shared, or redistributed
- All processing happens **locally** on the operator's machine
- No data is sent to third-party services or cloud APIs

### 6. Data Retention & Deletion

- Default retention: 90 days, configurable
- If a Redditor requests their data be removed, it will be purged immediately
- No persistent user profiles are built
- Deleted-upstream content is honored and removed from local storage

### 7. Compliance

This tool is designed to comply with:

- [Reddit API Terms of Use](https://www.redditinc.com/policies/data-api-terms)
- [Reddit User Agreement](https://www.redditinc.com/policies/user-agreement)
- [Responsible Builder Policy](https://support.reddithelp.com/hc/en-us/articles/42728983564564-Responsible-Builder-Policy)
- GDPR / PDPA (for applicable users)

## Scope Limitations

This tool will **not** be used for:

- Commercial resale of Reddit data
- Political targeting or microtargeting
- Automated content moderation without human review
- Training large language models on Reddit content
- Surveillance of individual users
- Any use that violates Reddit's content policy

## Reporting Issues

If you believe this tool is being misused or violates Reddit's policies, please open an issue on the GitHub repository.
