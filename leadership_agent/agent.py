#!/usr/bin/env python3
"""
Leadership Daily Brief Agent

Fetches today's Manager Tools / Executive Tools episode from the curriculum,
generates a bite-sized brief with Claude, and emails it via Gmail.

Usage:
  python agent.py              # normal daily run
  python agent.py --dry-run    # print email to stdout, don't send, don't advance
  python agent.py --test       # send a real email for Day 1, don't advance state
  python agent.py --status     # print current position and exit
  python agent.py --reset      # reset curriculum back to Day 1, Phase 1
"""

import argparse
import sys

from config import load_config
from feeds import get_all_feeds, PHASE_LABELS
from curriculum import get_position, advance, reset
from content import generate_brief
from emailer import send, build_subject, build_body


def main() -> None:
    parser = argparse.ArgumentParser(description="Leadership Daily Brief Agent")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--dry-run", action="store_true", help="Print email to stdout, skip send and state advance")
    group.add_argument("--test", action="store_true", help="Send a real email for Day 1 without advancing state")
    group.add_argument("--status", action="store_true", help="Print current curriculum position and exit")
    group.add_argument("--reset", action="store_true", help="Reset curriculum to Day 1, Phase 1 (Hall of Fame)")
    args = parser.parse_args()

    if args.reset:
        reset()
        print("Curriculum reset to Day 1 — Manager Tools Hall of Fame, Episode 1.")
        return

    cfg = load_config()

    print("Fetching feeds...", flush=True)
    feeds = get_all_feeds()

    if args.status:
        _print_status(feeds)
        return

    # For --test, temporarily use a state pointing to Day 1
    state_override = {"day": 1, "phase_key": "hof", "episode_index": 0} if args.test else None
    pos = get_position(feeds, state=state_override)

    if pos is None:
        print("Curriculum complete! All episodes have been delivered.")
        sys.exit(0)

    print(f"Day {pos.day}: {pos.phase_label} — {pos.episode['title']}", flush=True)
    print("Generating brief with Claude...", flush=True)

    brief = generate_brief(pos.episode, pos.phase_label, cfg.anthropic_api_key)

    # Look up tomorrow's episode title for the preview
    tomorrow_state = {"day": pos.day + 1, "phase_key": pos.phase_key, "episode_index": pos.episode_index + 1}
    tomorrow_pos = get_position(feeds, state=tomorrow_state)
    tomorrow_title = tomorrow_pos.episode["title"] if tomorrow_pos else None

    if args.dry_run:
        subject = build_subject(pos)
        body = build_body(pos, brief, tomorrow_title)
        print(f"\nSubject: {subject}\n")
        print(body)
        return

    print(f"Sending to {cfg.to_email}...", flush=True)
    send(
        gmail_address=cfg.gmail_address,
        gmail_app_password=cfg.gmail_app_password,
        to_email=cfg.to_email,
        pos=pos,
        brief=brief,
        tomorrow_title=tomorrow_title,
    )
    print("Sent.")

    if not args.test:
        advance(feeds)
        print(f"State advanced to Day {pos.day + 1}.")


def _print_status(feeds: dict) -> None:
    from curriculum import load_state
    state = load_state()
    pos = get_position(feeds, state=state)
    if pos is None:
        print("Curriculum complete — all episodes delivered.")
        return

    print(f"Day:     {pos.day}")
    print(f"Phase:   {pos.phase_label}")
    print(f"Episode: {pos.episode['title']}")
    print(f"Progress in phase: {pos.index_in_phase}/{pos.total_in_phase}")
    for key, episodes in feeds.items():
        print(f"  {PHASE_LABELS[key]}: {len(episodes)} episodes loaded")


if __name__ == "__main__":
    main()
