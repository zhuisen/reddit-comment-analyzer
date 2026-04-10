# Privacy Policy

This document describes how Reddit Comment Analyzer handles data.

## TL;DR

- **Local-only**: Everything runs on the operator's own machine
- **Public data only**: No private content, no DMs
- **Aggregated**: Reports show community trends, not individual profiles
- **No sharing**: Data is never sold, shared, or sent to third parties

## What Data We Access

Through Reddit's official API, this tool reads:

- Public post titles, bodies, scores, timestamps, and subreddit
- Public comment bodies, scores, timestamps, and reply structure
- Subreddit metadata (name, subscriber count, description)

## What Data We Do NOT Access

- Private messages
- Chat conversations
- Deleted or removed content
- User email addresses
- Payment or premium account information
- Any data behind authentication walls (other than public read-only API)

## How Data Is Stored

- **Location**: Local SQLite database on the operator's machine
- **Encryption**: Filesystem-level encryption recommended for sensitive deployments
- **Format**: Normalized schema with optional username anonymization
- **Access**: Only the local operator can access the database

## How Data Is Used

Stored data is used **only** for:

1. Generating aggregated sentiment trend reports
2. Identifying trending topics at the subreddit level
3. Personal research and community insights

Stored data is **never** used for:

- Individual user targeting or profiling
- Building datasets for ML training
- Commercial resale
- Advertising or marketing to Reddit users

## Data Sharing

**We do not share, sell, or redistribute any data.** All analysis results stay local unless the operator explicitly chooses to export a report.

## Data Retention

- Default: 90 days, then auto-purged
- Configurable via `config.yaml`
- Operator can manually purge at any time

## User Rights

If you are a Redditor and you would like your data removed from this tool's local database:

1. Open a GitHub issue with your username
2. We will purge all matching records within 7 days
3. No verification beyond username is required — we err on the side of deletion

## Third-Party Services

This tool does **not** use any third-party cloud services. Specifically:

- **No** OpenAI / Anthropic / Google / third-party LLM APIs
- **No** cloud sentiment analysis services
- **No** analytics trackers
- **No** telemetry

All NLP processing happens on-device using open-source models from Hugging Face, downloaded once and run locally.

## Compliance

This tool is designed to comply with:

- Reddit API Terms of Use
- Reddit User Agreement & Privacy Policy
- GDPR (EU) and PDPA (Singapore)
- Responsible Builder Policy

## Contact

For privacy concerns, open an issue on the GitHub repository.
