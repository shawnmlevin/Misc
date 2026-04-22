import feedparser
from datetime import datetime, timezone
from typing import Dict, List, TypedDict


class Episode(TypedDict):
    title: str
    summary: str
    link: str
    published: str


FEEDS = {
    "hof": "https://www.manager-tools.com/podcasts/important-topic-feeds/hall-fame-feed",
    "exec": "https://www.manager-tools.com/executive-tools-podcasts",
    "basics": "https://www.manager-tools.com/podcasts/basics-rss.xml",
}

PHASE_LABELS = {
    "hof": "Manager Tools Hall of Fame",
    "exec": "Executive Tools",
    "basics": "Manager Tools Basics",
}


def _entry_date(entry) -> datetime:
    if getattr(entry, "published_parsed", None):
        return datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
    return datetime(1970, 1, 1, tzinfo=timezone.utc)


def fetch_feed(url: str) -> List[Episode]:
    parsed = feedparser.parse(url)
    entries_with_dates = [
        (_entry_date(e), e) for e in parsed.entries
    ]
    entries_with_dates.sort(key=lambda x: x[0])  # oldest-first

    episodes = []
    for _, entry in entries_with_dates:
        summary = getattr(entry, "summary", None) or getattr(entry, "description", "")
        episodes.append(Episode(
            title=entry.get("title", "Untitled"),
            summary=summary,
            link=entry.get("link", ""),
            published=entry.get("published", ""),
        ))
    return episodes


def get_all_feeds() -> Dict[str, List[Episode]]:
    result = {}
    for key, url in FEEDS.items():
        try:
            result[key] = fetch_feed(url)
        except Exception as e:
            print(f"Warning: could not fetch {key} feed ({url}): {e}")
            result[key] = []
    return result
