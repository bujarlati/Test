"""Generate complete fixed-slot monster sprite sheets.

This is a recovery generator for monster sheets whose source art was not a
valid fixed-grid animation sheet. It favors complete, readable silhouettes over
fancy frame detail so the browser renderer never shows clipped body fragments.
"""

from __future__ import annotations

import math
from pathlib import Path

from generate_pixel_assets import Image, rgba


ROOT = Path(__file__).resolve().parents[1]
MONSTER_ROOT = ROOT / "web" / "assets" / "pixel" / "v1" / "monsters"

COMMON_ACTIONS = {
    "idle": 0,
    "walk": 1,
    "attack": 2,
    "hurt": 3,
    "death": 4,
}

COMMON_PALETTES = {
    "forest_slime": ("#2f6f54", "#75d39f", "#f0ffe0"),
    "thorn_boar": ("#573622", "#b56a36", "#9fd067"),
    "moss_imp": ("#2f3f2b", "#6f8f44", "#e6d28a"),
    "wild_mushroom": ("#4b332a", "#9d6a44", "#c4b56b"),
    "bark_guard": ("#3e3325", "#8b6847", "#d9b45f"),
    "cave_bat": ("#26384a", "#6c839c", "#b9d6ee"),
    "crystal_lurker": ("#243845", "#6fb4ce", "#b7f3ff"),
    "stone_crawler": ("#263141", "#526d8c", "#91bde8"),
    "cloud_wisp": ("#41556b", "#9db6d4", "#eff8ff"),
    "storm_harpy": ("#203345", "#4f7da3", "#bce8ff"),
    "sun_mote": ("#5b3216", "#ff9d2f", "#fff36a"),
    "rust_guard": ("#3d3333", "#8a6f66", "#ffc36d"),
    "hollow_knight": ("#202431", "#7a8198", "#d9e2ff"),
    "cursed_squire": ("#302936", "#856f98", "#e5d4ff"),
}

BOSS_PALETTES = {
    "cave_warden": ("#322b36", "#8b768e", "#d987ff"),
    "tempest_seraph": ("#263548", "#6f91bd", "#d8f4ff"),
    "throne_keeper": ("#3b3432", "#8e7b6e", "#f0c47a"),
}


def shadow(frame: Image, cx: int, cy: int, rx: int, ry: int) -> None:
    return


def triangle(frame: Image, x: int, y: int, width: int, height: int, color: tuple[int, int, int, int]) -> None:
    frame.poly([(x, y), (x - width // 2, y + height), (x + width // 2, y + height)], color)


def action_offsets(index: int, action: str, size: int) -> tuple[int, int, int]:
    phase = index / 8 * math.tau
    bob = 0
    lean = 0
    if action == "walk":
        lean = round(math.sin(phase) * (1 if size == 64 else 2))
    elif action == "attack":
        lean = round(math.sin(min(index, 5) / 5 * math.pi) * (2 if size == 64 else 6))
    elif action == "hurt":
        lean = -2 if index % 2 else 2
    elif action == "death":
        lean = min(index, 7) * (1 if size == 64 else 2)
        bob = 8 if size == 64 else 16
    return bob, lean, -lean


def alpha_bbox(frame: Image) -> tuple[int, int, int, int] | None:
    min_x = frame.width
    min_y = frame.height
    max_x = -1
    max_y = -1
    for y in range(frame.height):
        for x in range(frame.width):
            if frame.pixels[(y * frame.width + x) * 4 + 3] <= 8:
                continue
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            max_x = max(max_x, x)
            max_y = max(max_y, y)
    if max_x < 0:
        return None
    return min_x, min_y, max_x, max_y


def keep_inside_slot(frame: Image, margin: int = 3) -> Image:
    bbox = alpha_bbox(frame)
    if bbox is None:
        return frame
    min_x, min_y, max_x, max_y = bbox
    dx = 0
    dy = 0
    if min_x < margin:
        dx = margin - min_x
    elif max_x > frame.width - margin - 1:
        dx = frame.width - margin - 1 - max_x
    if min_y < margin:
        dy = margin - min_y
    elif max_y > frame.height - margin - 1:
        dy = frame.height - margin - 1 - max_y
    if dx == 0 and dy == 0:
        return frame

    shifted = Image(frame.width, frame.height)
    for y in range(frame.height):
        for x in range(frame.width):
            index = (y * frame.width + x) * 4
            color = tuple(frame.pixels[index:index + 4])
            if color[3]:
                shifted.pixel(x + dx, y + dy, color)  # type: ignore[arg-type]
    return shifted


def draw_quadruped(frame: Image, key: str, i: int, action: str) -> None:
    dark, body, accent = COMMON_PALETTES[key]
    bob, lean, _ = action_offsets(i, action, 64)
    ground = 59
    y = bob
    shadow(frame, 33, ground + 1, 24, 5)
    frame.ellipse(34 + lean, 39 + y, 24, 13, rgba(dark))
    frame.ellipse(36 + lean, 37 + y, 22, 11, rgba(body))
    frame.ellipse(51 + lean, 34 + y, 9, 8, rgba(body))
    frame.ellipse(53 + lean, 33 + y, 7, 6, rgba(dark, 80))
    frame.rect(52 + lean, 32 + y, 4, 3, rgba(accent))
    for leg_x in (20, 30, 43, 53):
        step = round(math.sin(i / 8 * math.tau + leg_x) * 2) if action == "walk" else 0
        frame.line(leg_x + lean, 46 + y, leg_x - 2 + lean, 57 + step, rgba(dark), 4)
        frame.line(leg_x + lean, 47 + y, leg_x - 1 + lean, 57 + step, rgba(body), 2)
    if key == "thorn_boar":
        triangle(frame, 43 + lean, 21 + y, 9, 14, rgba(accent))
        triangle(frame, 29 + lean, 22 + y, 8, 12, rgba(accent))
        frame.line(58 + lean, 35 + y, 63 + lean, 31 + y, rgba("#f4e1a1"), 2)
    elif key == "forest_slime":
        for sx, sy in ((22, 23), (33, 21), (45, 23)):
            frame.ellipse(sx + lean, sy + y, 6, 5, rgba("#526f45"))
    else:
        frame.line(14 + lean, 37 + y, 5 + lean, 32 + y, rgba(accent), 3)


def draw_biped(frame: Image, key: str, i: int, action: str) -> None:
    dark, body, accent = COMMON_PALETTES[key]
    bob, lean, _ = action_offsets(i, action, 64)
    ground = 59
    shadow(frame, 32, ground + 1, 18, 4)
    frame.line(26 + lean, 40 + bob, 22 + lean, 57, rgba(dark), 4)
    frame.line(38 + lean, 40 + bob, 43 + lean, 57, rgba(dark), 4)
    frame.ellipse(32 + lean, 35 + bob, 18, 18, rgba(dark))
    frame.ellipse(32 + lean, 34 + bob, 15, 16, rgba(body))
    frame.ellipse(32 + lean, 20 + bob, 12, 11, rgba(dark))
    frame.ellipse(33 + lean, 20 + bob, 9, 9, rgba(body))
    frame.rect(36 + lean, 18 + bob, 4, 3, rgba(accent))
    frame.line(45 + lean, 35 + bob, 58 + lean, 28 + bob, rgba(accent), 3 if action == "attack" else 2)
    if "knight" in key or "squire" in key or "guard" in key:
        frame.rect(20 + lean, 28 + bob, 7, 19, rgba(dark))
        frame.line(45 + lean, 36 + bob, 59 + lean, 46 + bob, rgba("#d4c6a4"), 2)
    if "imp" in key:
        triangle(frame, 23 + lean, 10 + bob, 9, 12, rgba(accent))
        triangle(frame, 43 + lean, 10 + bob, 9, 12, rgba(accent))


def draw_mushroom(frame: Image, i: int, action: str) -> None:
    dark, stem, cap = COMMON_PALETTES["wild_mushroom"]
    bob, lean, _ = action_offsets(i, action, 64)
    shadow(frame, 32, 60, 19, 4)
    frame.rect(25 + lean, 33 + bob, 16, 24, rgba(dark))
    frame.rect(27 + lean, 31 + bob, 12, 25, rgba(stem))
    frame.ellipse(32 + lean, 25 + bob, 26, 14, rgba(dark))
    frame.ellipse(32 + lean, 24 + bob, 23, 12, rgba(cap))
    frame.rect(38 + lean, 31 + bob, 4, 3, rgba("#2b1d16"))
    for x, y in ((23, 21), (33, 16), (42, 24)):
        frame.ellipse(x + lean, y + bob, 3, 2, rgba("#f7e7b4"))
    if action == "attack":
        frame.ellipse(49 + lean, 39 + bob, 8, 5, rgba("#9fff4f", 150))


def draw_flying(frame: Image, key: str, i: int, action: str) -> None:
    dark, body, accent = COMMON_PALETTES[key]
    _bob, lean, _ = action_offsets(i, action, 64)
    cy = 35
    shadow(frame, 32, 60, 16, 3)
    frame.ellipse(32 + lean, cy, 13, 12, rgba(dark))
    frame.ellipse(34 + lean, cy - 1, 10, 9, rgba(body))
    frame.rect(38 + lean, cy - 3, 4, 3, rgba(accent))
    wing = 13
    frame.poly([(23 + lean, cy), (5 + lean, cy - wing), (13 + lean, cy + 12)], rgba(body))
    frame.poly([(41 + lean, cy), (59 + lean, cy - wing), (52 + lean, cy + 12)], rgba(body))
    if "mote" in key:
        frame.ellipse(32 + lean, cy, 14, 14, rgba("#ffb23f"))
        frame.ellipse(32 + lean, cy, 8, 8, rgba(accent))
    elif "wisp" in key:
        frame.line(24 + lean, cy + 10, 10 + lean, cy + 18, rgba(accent), 2)
    elif "harpy" in key:
        frame.line(35 + lean, cy + 8, 44 + lean, cy + 22, rgba(dark), 3)


def draw_common(frame: Image, key: str, i: int, action: str) -> None:
    if key == "wild_mushroom":
        draw_mushroom(frame, i, action)
    elif key in {"moss_imp", "bark_guard", "rust_guard", "hollow_knight", "cursed_squire"}:
        draw_biped(frame, key, i, action)
    elif key in {"cave_bat", "cloud_wisp", "storm_harpy", "sun_mote"}:
        draw_flying(frame, key, i, action)
    else:
        draw_quadruped(frame, key, i, action)


def draw_boss(frame: Image, key: str, i: int, action: str) -> None:
    dark, body, accent = BOSS_PALETTES[key]
    bob, lean, _ = action_offsets(i, action, 128)
    shadow(frame, 64, 120, 42, 8)
    frame.line(45 + lean, 76 + bob, 34 + lean, 118, rgba(dark), 9)
    frame.line(81 + lean, 76 + bob, 96 + lean, 118, rgba(dark), 9)
    frame.ellipse(64 + lean, 67 + bob, 35, 39, rgba(dark))
    frame.ellipse(66 + lean, 65 + bob, 30, 35, rgba(body))
    frame.ellipse(68 + lean, 30 + bob, 24, 22, rgba(dark))
    frame.ellipse(70 + lean, 30 + bob, 19, 17, rgba(body))
    frame.rect(78 + lean, 27 + bob, 7, 5, rgba(accent))
    frame.line(42 + lean, 31 + bob, 24 + lean, 15 + bob, rgba(accent), 5)
    frame.line(91 + lean, 31 + bob, 112 + lean, 14 + bob, rgba(accent), 5)
    frame.line(37 + lean, 62 + bob, 13 + lean, 82 + bob, rgba(dark), 8)
    frame.line(89 + lean, 62 + bob, 116 + lean, 78 + bob, rgba(dark), 8)
    if action == "attack":
        frame.line(82 + lean, 48 + bob, 120 + lean, 38 + bob, rgba(accent), 7)
    if key == "tempest_seraph":
        frame.poly([(43 + lean, 54 + bob), (8 + lean, 27 + bob), (22 + lean, 86 + bob)], rgba("#5f7da8"))
        frame.poly([(82 + lean, 54 + bob), (120 + lean, 28 + bob), (103 + lean, 88 + bob)], rgba("#5f7da8"))
    elif key == "cave_warden":
        for x, y in ((48, 22), (63, 16), (80, 22)):
            frame.poly([(x + lean, y + bob), (x - 6 + lean, y + 20 + bob), (x + 7 + lean, y + 20 + bob)], rgba(accent))
    else:
        frame.rect(26 + lean, 48 + bob, 16, 35, rgba("#5c5048"))
        frame.rect(88 + lean, 48 + bob, 16, 35, rgba("#5c5048"))


def write_sheet(path: Path, key: str, size: int, boss: bool = False) -> None:
    sheet = Image(size * 8, size * 5)
    for action, row in COMMON_ACTIONS.items():
        for i in range(8):
            frame = Image(size, size)
            if boss:
                draw_boss(frame, key, i, action)
            else:
                draw_common(frame, key, i, action)
            frame = keep_inside_slot(frame)
            sheet.paste(frame, i * size, row * size)
    sheet.save_png(path)


def main() -> None:
    for key in COMMON_PALETTES:
        write_sheet(MONSTER_ROOT / "common" / f"{key}.png", key, 64)
    for key in BOSS_PALETTES:
        write_sheet(MONSTER_ROOT / "bosses" / f"{key}.png", key, 128, boss=True)


if __name__ == "__main__":
    main()
