"""
Aggregated trend report generator.

Produces community-level summaries — never individual user profiles.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class SubredditTrend:
    subreddit: str
    period: str  # e.g. "2026-W14"
    total_posts: int
    total_comments: int
    avg_sentiment: float  # -1.0 (neg) to 1.0 (pos)
    positive_ratio: float  # 0.0 to 1.0
    negative_ratio: float
    top_topics: list[str]


def render_markdown(trends: list[SubredditTrend]) -> str:
    """Render a list of subreddit trends as a markdown report."""
    lines = [
        "# Reddit Comment Trend Report",
        f"\nGenerated: {datetime.utcnow().isoformat()}Z\n",
        "## Summary\n",
        "| Subreddit | Posts | Comments | Avg Sentiment | Positive % | Negative % |",
        "|-----------|-------|----------|---------------|------------|------------|",
    ]
    for t in trends:
        lines.append(
            f"| r/{t.subreddit} | {t.total_posts} | {t.total_comments} | "
            f"{t.avg_sentiment:+.2f} | {t.positive_ratio*100:.1f}% | "
            f"{t.negative_ratio*100:.1f}% |"
        )

    lines.append("\n## Top Topics by Subreddit\n")
    for t in trends:
        lines.append(f"### r/{t.subreddit}")
        if t.top_topics:
            for topic in t.top_topics:
                lines.append(f"- {topic}")
        else:
            lines.append("_No topics detected_")
        lines.append("")

    return "\n".join(lines)
