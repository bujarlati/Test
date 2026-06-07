"""Generate a clean long-haired female assassin sprite sheet.

The v3 sheet is drawn directly instead of reshaping the male sheet. It favors
stable feet, readable long hair, and complete lower-body silhouettes so the
runtime animation stays smooth and does not inherit cutout artifacts.
"""

from __future__ import annotations

import math
from pathlib import Path

from generate_pixel_assets import HERO_ACTIONS, Image, rgba


ROOT = Path(__file__).resolve().parents[1]
ASSET_ROOT = ROOT / "web" / "assets" / "pixel" / "v1"
FRAME_SIZE = 128
FRAME_COLUMNS = 16


FEMALE_ACTIONS = {
    "idle": {"row": 0, "frames": 16, "frameMs": 58},
    "walk": {"row": 1, "frames": 16, "frameMs": 44},
    "attack_unarmed": {"row": 2, "frames": 16, "frameMs": 42},
    "attack_blade": {"row": 3, "frames": 16, "frameMs": 40},
    "attack_dual": {"row": 4, "frames": 16, "frameMs": 38},
    "attack_bow": {"row": 5, "frames": 16, "frameMs": 48},
    "attack_spear": {"row": 6, "frames": 16, "frameMs": 46},
    "attack_heavy": {"row": 7, "frames": 16, "frameMs": 52},
    "hurt": {"row": 8, "frames": 8, "frameMs": 70},
    "death": {"row": 9, "frames": 16, "frameMs": 70},
    "revive": {"row": 10, "frames": 16, "frameMs": 58},
}


def phase(frame_index: int) -> float:
    return frame_index / FRAME_COLUMNS * math.tau


def draw_boot(frame: Image, hip: tuple[int, int], knee: tuple[int, int], foot: tuple[int, int], highlight: bool) -> None:
    frame.line(hip[0], hip[1], knee[0], knee[1], rgba("#171822"), 6)
    frame.line(knee[0], knee[1], foot[0], foot[1] - 3, rgba("#11131a"), 6)
    frame.line(knee[0] + 1, knee[1], foot[0] + 1, foot[1] - 5, rgba("#2c2339"), 2)
    frame.line(foot[0] - 6, foot[1], foot[0] + 7, foot[1], rgba("#0b0d12"), 4)
    if highlight:
        frame.line(hip[0] + 1, hip[1] + 3, knee[0] + 2, knee[1] - 1, rgba("#65527f"), 1)


def draw_arm(frame: Image, shoulder: tuple[int, int], elbow: tuple[int, int], hand: tuple[int, int], front: bool) -> None:
    base = rgba("#171822") if front else rgba("#10131b")
    edge = rgba("#51446b") if front else rgba("#342c49")
    frame.line(shoulder[0], shoulder[1], elbow[0], elbow[1], base, 5)
    frame.line(elbow[0], elbow[1], hand[0], hand[1], base, 4)
    frame.line(shoulder[0], shoulder[1], elbow[0], elbow[1], edge, 1)
    frame.ellipse(hand[0], hand[1], 3, 3, rgba("#f0a46f"))


def draw_hair(frame: Image, x: int, y: int, motion: float, action: str) -> None:
    sway = math.sin(motion) * 4
    lift = -4 if action.startswith("attack") else 0
    frame.poly(
        [
            (x - 8, y - 31),
            (x - 28 + round(sway), y - 8 + lift),
            (x - 33 + round(sway * 0.7), y + 28),
            (x - 20 + round(sway * 0.4), y + 39),
            (x - 5, y + 5),
        ],
        rgba("#251732", 235),
    )
    frame.line(x - 10, y - 22, x - 29 + round(sway), y + 20, rgba("#765092", 225), 3)
    frame.line(x - 2, y - 25, x - 16 + round(sway * 0.6), y + 10, rgba("#d9a8ec", 190), 1)


def draw_frame(sheet: Image, action: str, frame_index: int) -> None:
    config = FEMALE_ACTIONS[action]
    cell = Image(FRAME_SIZE, FRAME_SIZE)
    p = phase(frame_index)
    walk = action == "walk"
    attack = action.startswith("attack")
    hurt = action == "hurt"
    death = action == "death"
    revive = action == "revive"
    bottom = 121
    cx = 64

    if death:
        fall = min(1.0, frame_index / 10)
        cx -= round(fall * 16)
        body_y = 76 + round(fall * 22)
    elif revive:
        rise = min(1.0, frame_index / 12)
        body_y = 86 - round(rise * 17)
    else:
        body_y = 66 + round(math.sin(p) * (1 if walk else 0.6))

    stride = math.sin(p) if walk else 0
    counter = math.sin(p + math.pi) if walk else 0
    attack_curve = math.sin(min(1, frame_index / max(1, FEMALE_ACTIONS[action]["frames"] - 1)) * math.pi)
    lean = round((attack_curve * 8 if attack else 0) - (5 if hurt else 0))

    head = (cx + lean, body_y - 32)
    neck = (cx + lean, body_y - 17)
    left_hip = (cx - 8 + lean, body_y + 20)
    right_hip = (cx + 8 + lean, body_y + 20)
    left_knee = (cx - 12 + lean + round(stride * 8), body_y + 43)
    right_knee = (cx + 12 + lean + round(counter * 8), body_y + 43)
    left_foot = (cx - 12 + lean + round(stride * 12), bottom)
    right_foot = (cx + 12 + lean + round(counter * 12), bottom)

    draw_hair(cell, head[0], head[1], p, action)
    cell.poly([(cx - 27 + lean, body_y - 8), (cx - 13 + lean, bottom - 6), (cx + 2 + lean, body_y + 7)], rgba("#0d1018", 215))
    cell.poly([(cx - 18 + lean, body_y - 12), (cx + 23 + lean, body_y - 10), (cx + 11 + lean, body_y + 33), (cx - 11 + lean, body_y + 34)], rgba("#141723"))
    cell.poly([(cx - 8 + lean, body_y - 11), (cx + 12 + lean, body_y - 9), (cx + 7 + lean, body_y + 28), (cx - 7 + lean, body_y + 29)], rgba("#222033"))
    cell.line(cx - 10 + lean, body_y + 3, cx + 15 + lean, body_y + 5, rgba("#a05ddd"), 2)
    cell.line(cx - 8 + lean, body_y + 8, cx - 18 + lean + round(math.sin(p) * 3), body_y + 32, rgba("#7f4bbd"), 2)

    cell.ellipse(head[0], head[1], 13, 14, rgba("#171a24"))
    cell.poly([(head[0] - 13, head[1] - 2), (head[0] + 7, head[1] - 14), (head[0] + 17, head[1] - 3), (head[0] + 9, head[1] + 6)], rgba("#202333"))
    cell.ellipse(head[0] + 4, head[1] + 1, 7, 8, rgba("#f2a56f"))
    cell.rect(head[0] + 6, head[1] - 2, 2, 2, rgba("#12141b"))
    cell.line(head[0] - 3, head[1] - 8, head[0] + 10, head[1] - 9, rgba("#d7a5ec"), 1)

    left_shoulder = (cx - 15 + lean, body_y - 7)
    right_shoulder = (cx + 15 + lean, body_y - 7)
    if attack:
        reach = round(attack_curve * 24)
        right_hand = (cx + 31 + lean + reach, body_y - 4 - round(attack_curve * 9))
        left_hand = (cx - 19 + lean + round(attack_curve * 7), body_y + 9)
    elif hurt:
        right_hand = (cx + 10 + lean, body_y + 13)
        left_hand = (cx - 30 + lean, body_y + 3)
    else:
        right_hand = (cx + 24 + lean + round(stride * 5), body_y + 16)
        left_hand = (cx - 25 + lean + round(counter * 5), body_y + 14)
    draw_arm(cell, left_shoulder, (left_hand[0] + 4, left_hand[1] - 9), left_hand, False)
    draw_arm(cell, right_shoulder, (right_hand[0] - 5, right_hand[1] - 9), right_hand, True)

    draw_boot(cell, right_hip, right_knee, right_foot, True)
    draw_boot(cell, left_hip, left_knee, left_foot, False)
    cell.line(cx - 13 + lean, body_y + 24, cx + 14 + lean, body_y + 24, rgba("#0b0d12"), 4)
    cell.line(cx - 12 + lean, body_y + 22, cx + 12 + lean, body_y + 23, rgba("#7f4bbd"), 1)

    sheet.paste(cell, frame_index * FRAME_SIZE, config["row"] * FRAME_SIZE)


def main() -> None:
    sheet = Image(FRAME_SIZE * FRAME_COLUMNS, FRAME_SIZE * len(HERO_ACTIONS))
    for action, config in HERO_ACTIONS.items():
        frames = FEMALE_ACTIONS[action]["frames"]
        for frame_index in range(frames):
            draw_frame(sheet, action, frame_index)
    sheet.save_png(ASSET_ROOT / "heroes" / "female" / "assassin_sample.png")


if __name__ == "__main__":
    main()
