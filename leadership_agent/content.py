"""
Generates bite-sized leadership briefs using the Claude API.

Uses prompt caching on the system prompt to minimize API cost across daily runs.
"""

import json
import anthropic
from dataclasses import dataclass
from feeds import Episode


SYSTEM_PROMPT = """You are a senior executive coach who synthesizes leadership podcast content into concise, actionable daily briefs for an executive or senior leader. Your writing is direct, practical, and free of corporate jargon.

When given a podcast episode title and its description, you produce a structured brief in JSON. The brief should feel like a trusted colleague distilling the most important insight, not a book report.

Always return valid JSON with exactly this structure:
{
  "summary": "2-3 sentence synthesis of the core concept and why it matters for executives",
  "takeaways": [
    "First key takeaway — specific and actionable",
    "Second key takeaway — specific and actionable",
    "Third key takeaway — specific and actionable"
  ],
  "action_item": "One concrete thing the reader can do today or this week to apply the concept"
}"""


@dataclass
class Brief:
    summary: str
    takeaways: list[str]
    action_item: str


def generate_brief(episode: Episode, phase_label: str, api_key: str) -> Brief:
    client = anthropic.Anthropic(api_key=api_key)

    user_content = f"""Podcast series: {phase_label}
Episode title: {episode['title']}

Official description:
{episode['summary'] or '(No description available)'}

Generate a leadership brief for this episode."""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=600,
        system=[
            {
                "type": "text",
                "text": SYSTEM_PROMPT,
                # Cache the system prompt — it never changes between runs
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[{"role": "user", "content": user_content}],
    )

    raw = response.content[0].text.strip()

    # Strip markdown code fences if Claude wraps the JSON
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()

    data = json.loads(raw)
    return Brief(
        summary=data["summary"],
        takeaways=data["takeaways"],
        action_item=data["action_item"],
    )
