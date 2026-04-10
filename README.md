# Reddit Comment Analyzer

A lightweight Python tool for collecting and analyzing public Reddit comment sentiment and discussion trends.

## Purpose

This tool helps Redditors and community moderators understand discussion patterns by:

- **Sentiment Analysis** - Analyze public comment sentiment to identify community concerns and trending topics
- **Trend Detection** - Track discussion trends across subreddits over time
- **Aggregated Insights** - Generate community-level summaries (no individual user tracking)

## How It Works

1. Collect public comments via Reddit's official API (OAuth2, read-only)
2. Run sentiment/NLP analysis using local AI models
3. Store aggregated results in a local SQLite database
4. Output trend reports and visualizations

## Tech Stack

- **Language**: Python 3.11+
- **Reddit Access**: Official Reddit API (OAuth2, read-only)
- **NLP/AI**: Local inference (no data sent to third parties)
- **Storage**: SQLite (local only)

## Data & Privacy

- Read-only access to **public** comments only
- No personal data collection or individual user tracking
- All data stored locally, never redistributed or sold
- Compliant with Reddit's [Responsible Builder Policy](https://support.reddithelp.com/hc/en-us/articles/42728983564564-Responsible-Builder-Policy)

## Target Subreddits

Public subreddits related to market research and product discussions, including:
- r/singapore
- r/technology
- r/SaaS
- r/datascience

## Status

Under development. Pending Reddit API access approval.

## License

MIT
