"""
Curriculum ordering and state tracking.

Phase 1 — Hall of Fame (~109 episodes): highest-signal content first
Phase 2 — Executive Tools: executive-specific development
Phase 3 — Manager Tools Basics: fill foundational gaps

State is stored in state.json next to this file.
"""

import json
import os
from dataclasses import dataclass
from typing import Optional

from feeds import Episode, PHASE_LABELS

STATE_PATH = os.path.join(os.path.dirname(__file__), "state.json")

# Ordered list of (feed_key, phase_number) pairs defining the curriculum
PHASE_ORDER = ["hof", "exec", "basics"]


@dataclass
class CurriculumPosition:
    day: int
    phase_key: str
    episode_index: int
    episode: Episode
    phase_label: str
    index_in_phase: int       # 1-based
    total_in_phase: int


def load_state() -> dict:
    if os.path.exists(STATE_PATH):
        with open(STATE_PATH) as f:
            return json.load(f)
    return {"day": 1, "phase_key": "hof", "episode_index": 0}


def save_state(state: dict) -> None:
    with open(STATE_PATH, "w") as f:
        json.dump(state, f, indent=2)


def get_position(feeds: dict[str, list[Episode]], state: Optional[dict] = None) -> Optional[CurriculumPosition]:
    if state is None:
        state = load_state()

    phase_key = state.get("phase_key", "hof")
    episode_index = state.get("episode_index", 0)
    day = state.get("day", 1)

    # Walk phases until we find an episode at the current index
    for key in PHASE_ORDER:
        if key != phase_key:
            continue
        episodes = feeds.get(key, [])
        if episode_index < len(episodes):
            return CurriculumPosition(
                day=day,
                phase_key=key,
                episode_index=episode_index,
                episode=episodes[episode_index],
                phase_label=PHASE_LABELS[key],
                index_in_phase=episode_index + 1,
                total_in_phase=len(episodes),
            )
        # This phase is exhausted — advance to next
        phase_key = _next_phase(key)
        episode_index = 0
        if phase_key is None:
            return None  # All phases complete

    return None


def advance(feeds: dict[str, list[Episode]]) -> None:
    state = load_state()
    phase_key = state.get("phase_key", "hof")
    episode_index = state.get("episode_index", 0)
    day = state.get("day", 1)

    episode_index += 1
    episodes = feeds.get(phase_key, [])

    if episode_index >= len(episodes):
        next_key = _next_phase(phase_key)
        if next_key:
            phase_key = next_key
            episode_index = 0
        else:
            # Curriculum complete — stay at last position
            episode_index = len(episodes) - 1

    save_state({"day": day + 1, "phase_key": phase_key, "episode_index": episode_index})


def _next_phase(current: str) -> Optional[str]:
    idx = PHASE_ORDER.index(current)
    if idx + 1 < len(PHASE_ORDER):
        return PHASE_ORDER[idx + 1]
    return None


def reset(phase_key: str = "hof", episode_index: int = 0, day: int = 1) -> None:
    save_state({"day": day, "phase_key": phase_key, "episode_index": episode_index})
