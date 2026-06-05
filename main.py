"""Command-line demo for the idle forest engine."""

from __future__ import annotations

import argparse
import json

from idle_forest import GameEngine


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Idle Forest prototype.")
    parser.add_argument("--ticks", type=int, default=30, help="Seconds to simulate.")
    parser.add_argument("--seed", type=int, default=7, help="Random seed for repeatable demos.")
    parser.add_argument("--json", action="store_true", help="Print the final snapshot as JSON.")
    parser.add_argument(
        "--auto-equip",
        action="store_true",
        help="Automatically equip stronger items after each second.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    engine = GameEngine(seed=args.seed)
    last_event_count = 0

    for second in range(1, args.ticks + 1):
        snapshot = engine.advance(1)
        if args.auto_equip:
            engine.equip_best_items()
            snapshot = engine.snapshot()

        new_events = snapshot["events"][last_event_count:]
        last_event_count = len(snapshot["events"])
        important = [event for event in new_events if event["kind"] in {"monster_kill", "loot", "level_up"}]
        monster = snapshot["monster"]
        monster_text = "none" if monster is None else f"{monster['kind']}({monster['hp']}/{monster['max_hp']})"
        print(
            f"[{second:03d}s] x={snapshot['hero']['position']['x']:>6} "
            f"lv={snapshot['hero']['level']} hp={snapshot['hero']['hp']}/{snapshot['hero']['max_hp']} "
            f"atk={snapshot['hero']['attack']} def={snapshot['hero']['defense']} "
            f"gold={snapshot['hero']['gold']} monster={monster_text}"
        )
        for event in important:
            print(f"  - {event['message']}")

    if args.json:
        print(json.dumps(engine.snapshot(), indent=2))


if __name__ == "__main__":
    main()
