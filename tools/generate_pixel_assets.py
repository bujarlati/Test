"""Generate first-pass pixel art sprite sheets with stdlib-only PNG writing."""

from __future__ import annotations

import json
import math
import struct
import zlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSET_ROOT = ROOT / "web" / "assets" / "pixel" / "v1"


Color = tuple[int, int, int, int]


def rgba(hex_color: str, alpha: int = 255) -> Color:
    text = hex_color.lstrip("#")
    return int(text[0:2], 16), int(text[2:4], 16), int(text[4:6], 16), alpha


class Image:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.pixels = bytearray(width * height * 4)

    def pixel(self, x: int, y: int, color: Color) -> None:
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return
        r, g, b, a = color
        index = (y * self.width + x) * 4
        if a >= 255:
            self.pixels[index:index + 4] = bytes((r, g, b, a))
            return
        base_a = self.pixels[index + 3]
        out_a = a + base_a * (255 - a) // 255
        if out_a <= 0:
            return
        for offset, value in enumerate((r, g, b)):
            base = self.pixels[index + offset]
            self.pixels[index + offset] = (value * a + base * base_a * (255 - a) // 255) // out_a
        self.pixels[index + 3] = out_a

    def rect(self, x: int, y: int, width: int, height: int, color: Color) -> None:
        for py in range(y, y + height):
            for px in range(x, x + width):
                self.pixel(px, py, color)

    def ellipse(self, cx: int, cy: int, rx: int, ry: int, color: Color) -> None:
        if rx <= 0 or ry <= 0:
            return
        for py in range(cy - ry, cy + ry + 1):
            for px in range(cx - rx, cx + rx + 1):
                dx = (px - cx) / rx
                dy = (py - cy) / ry
                if dx * dx + dy * dy <= 1:
                    self.pixel(px, py, color)

    def line(self, x1: int, y1: int, x2: int, y2: int, color: Color, thickness: int = 1) -> None:
        steps = max(abs(x2 - x1), abs(y2 - y1), 1)
        radius = max(0, thickness // 2)
        for step in range(steps + 1):
            t = step / steps
            x = round(x1 + (x2 - x1) * t)
            y = round(y1 + (y2 - y1) * t)
            self.ellipse(x, y, radius, radius, color)

    def poly(self, points: list[tuple[int, int]], color: Color) -> None:
        if len(points) < 3:
            return
        ys = [point[1] for point in points]
        for y in range(min(ys), max(ys) + 1):
            nodes: list[int] = []
            j = len(points) - 1
            for i, point in enumerate(points):
                xi, yi = point
                xj, yj = points[j]
                if (yi < y <= yj) or (yj < y <= yi):
                    nodes.append(round(xi + (y - yi) / (yj - yi) * (xj - xi)))
                j = i
            nodes.sort()
            for start, end in zip(nodes[0::2], nodes[1::2]):
                for x in range(start, end + 1):
                    self.pixel(x, y, color)

    def paste(self, other: "Image", x: int, y: int) -> None:
        for py in range(other.height):
            for px in range(other.width):
                index = (py * other.width + px) * 4
                color = tuple(other.pixels[index:index + 4])
                if color[3]:
                    self.pixel(x + px, y + py, color)  # type: ignore[arg-type]

    def save_png(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        rows = []
        stride = self.width * 4
        for y in range(self.height):
            rows.append(b"\x00" + bytes(self.pixels[y * stride:(y + 1) * stride]))
        raw = b"".join(rows)

        def chunk(kind: bytes, data: bytes) -> bytes:
            return (
                struct.pack(">I", len(data))
                + kind
                + data
                + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
            )

        payload = (
            b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", struct.pack(">IIBBBBB", self.width, self.height, 8, 6, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(raw, level=9))
            + chunk(b"IEND", b"")
        )
        path.write_bytes(payload)


HERO_ACTIONS = {
    "idle": {"row": 0, "frames": 8, "frameMs": 120},
    "walk": {"row": 1, "frames": 8, "frameMs": 82},
    "attack_unarmed": {"row": 2, "frames": 8, "frameMs": 68},
    "attack_blade": {"row": 3, "frames": 8, "frameMs": 64},
    "attack_dual": {"row": 4, "frames": 8, "frameMs": 60},
    "attack_bow": {"row": 5, "frames": 8, "frameMs": 76},
    "attack_spear": {"row": 6, "frames": 8, "frameMs": 72},
    "attack_heavy": {"row": 7, "frames": 8, "frameMs": 82},
    "hurt": {"row": 8, "frames": 4, "frameMs": 90},
    "death": {"row": 9, "frames": 8, "frameMs": 110},
    "revive": {"row": 10, "frames": 8, "frameMs": 95},
}

MONSTER_ACTIONS = {
    "idle": {"row": 0, "frames": 8, "frameMs": 120},
    "walk": {"row": 1, "frames": 8, "frameMs": 92},
    "attack": {"row": 2, "frames": 8, "frameMs": 76},
    "hurt": {"row": 3, "frames": 4, "frameMs": 90},
    "death": {"row": 4, "frames": 8, "frameMs": 110},
}


def draw_shadow(frame: Image, cx: int, y: int, rx: int, ry: int) -> None:
    frame.ellipse(cx, y, rx, ry, rgba("#111815", 82))


def draw_hero_frame(frame: Image, frame_index: int, action: str, female: bool) -> None:
    skin = rgba("#d99b71")
    skin_shadow = rgba("#9b654d")
    outline = rgba("#101416")
    cloth = rgba("#202b34") if not female else rgba("#2b2636")
    leather = rgba("#293948") if not female else rgba("#42324f")
    leather_hi = rgba("#3e6374") if not female else rgba("#6e4f7a")
    accent = rgba("#60c8d8") if not female else rgba("#a879ff")
    trousers = rgba("#1d2529")
    boot = rgba("#141112")
    hood = rgba("#181f28")
    hood_hi = rgba("#2d4050")
    hair = rgba("#39291f") if not female else rgba("#6d3a54")
    hair_hi = rgba("#755739") if not female else rgba("#b56386")
    eye = rgba("#111414")
    eye_glint = rgba("#d7fff4")
    phase = frame_index / 8 * math.tau
    ground = 84
    breath = round(math.sin(phase) * 1)
    stride = round(math.sin(phase) * 5)
    counter = round(math.sin(phase + math.pi) * 5)
    attacking = action.startswith("attack_")
    attack_curve = [0, 3, 9, 15, 18, 10, 4, 0][frame_index]
    lean = 0
    if attacking:
        lean = round(attack_curve / 5)
    if action == "hurt":
        lean = -5
    if action == "death":
        draw_shadow(frame, 48, ground + 2, 28, 5)
        frame.rect(24, 67, 46, 11, outline)
        frame.rect(27, 64, 40, 13, leather)
        frame.rect(56, 55, 19, 16, outline)
        frame.ellipse(65, 61, 9, 8, skin)
        frame.rect(32, 74, 24, 5, boot)
        frame.rect(52, 78, 26, 5, boot)
        frame.rect(30, 62, 18, 4, accent)
        return

    draw_shadow(frame, 48, ground + 2, 23, 5)
    hip_y = 64 + breath
    torso_y = 45 + breath
    head_y = 29 + breath

    if action == "walk":
        left_foot = (37 + stride, ground)
        right_foot = (58 + counter, ground)
        left_knee = (40 + stride // 2, 74)
        right_knee = (56 + counter // 2, 74)
    elif attacking:
        left_foot = (35 - attack_curve // 7, ground)
        right_foot = (59 + attack_curve // 5, ground)
        left_knee = (40, 74)
        right_knee = (56 + attack_curve // 7, 74)
    else:
        left_foot = (38, ground)
        right_foot = (58, ground)
        left_knee = (40, 74)
        right_knee = (56, 74)

    frame.line(45, hip_y, left_knee[0], left_knee[1], outline, 6)
    frame.line(53, hip_y, right_knee[0], right_knee[1], outline, 6)
    frame.line(left_knee[0], left_knee[1], left_foot[0], left_foot[1], trousers, 5)
    frame.line(right_knee[0], right_knee[1], right_foot[0], right_foot[1], trousers, 5)
    frame.rect(left_foot[0] - 6, left_foot[1] - 3, 13, 5, boot)
    frame.rect(right_foot[0] - 6, right_foot[1] - 3, 13, 5, boot)

    frame.poly(
        [
            (35 + lean, torso_y - 2),
            (61 + lean, torso_y - 1),
            (58 + lean, torso_y + 25),
            (38 + lean, torso_y + 25),
        ],
        outline,
    )
    frame.poly(
        [
            (38 + lean, torso_y),
            (58 + lean, torso_y),
            (56 + lean, torso_y + 23),
            (40 + lean, torso_y + 23),
        ],
        leather,
    )
    frame.rect(39 + lean, torso_y + 3, 18, 4, leather_hi)
    frame.line(40 + lean, torso_y + 9, 55 + lean, torso_y + 20, accent, 2)
    frame.rect(35 + lean, torso_y + 23, 26, 5, cloth)
    frame.rect(58 + lean, torso_y + 5, 4, 20, hood_hi)

    left_shoulder = (38 + lean, torso_y + 8)
    right_shoulder = (59 + lean, torso_y + 8)
    left_hand = (31 + lean - (stride // 3 if action == "walk" else 0), torso_y + 16)
    right_hand = (63 + lean + (stride // 3 if action == "walk" else 0), torso_y + 14)

    if action == "attack_unarmed":
        right_hand = (66 + lean + attack_curve, torso_y + 12 - attack_curve // 6)
        left_hand = (34 + lean, torso_y + 11)
    elif action == "attack_blade":
        right_hand = (63 + lean + attack_curve, torso_y + 9 - attack_curve // 5)
        left_hand = (33 + lean, torso_y + 17)
    elif action == "attack_dual":
        right_hand = (61 + lean + attack_curve, torso_y + 8 - attack_curve // 5)
        left_hand = (35 + lean + attack_curve // 2, torso_y + 20 + attack_curve // 9)
    elif action == "attack_bow":
        right_hand = (39 + lean - attack_curve // 5, torso_y + 5)
        left_hand = (65 + lean + attack_curve // 3, torso_y + 7)
    elif action == "attack_spear":
        right_hand = (54 + lean + attack_curve // 2, torso_y + 13)
        left_hand = (72 + lean + attack_curve, torso_y + 8 - attack_curve // 8)
    elif action == "attack_heavy":
        right_hand = (56 + lean + attack_curve // 2, torso_y - 4 + attack_curve // 5)
        left_hand = (43 + lean + attack_curve // 3, torso_y - 3 + attack_curve // 5)

    frame.line(left_shoulder[0], left_shoulder[1], left_hand[0], left_hand[1], outline, 5)
    frame.line(right_shoulder[0], right_shoulder[1], right_hand[0], right_hand[1], outline, 5)
    frame.line(left_shoulder[0], left_shoulder[1], left_hand[0], left_hand[1], skin_shadow, 3)
    frame.line(right_shoulder[0], right_shoulder[1], right_hand[0], right_hand[1], skin_shadow, 3)
    frame.ellipse(left_hand[0], left_hand[1], 3, 3, skin)
    frame.ellipse(right_hand[0], right_hand[1], 3, 3, skin)

    if female:
        frame.rect(35 + lean, head_y - 10, 27, 29, outline)
        frame.rect(37 + lean, head_y - 8, 23, 27, hair)
        frame.rect(40 + lean, head_y - 8, 15, 3, hair_hi)

    frame.ellipse(49 + lean, head_y - 1, 15, 15, outline)
    frame.ellipse(49 + lean, head_y - 1, 13, 13, hood)
    frame.ellipse(51 + lean, head_y + 2, 9, 10, skin)
    frame.rect(39 + lean, head_y - 12, 21, 8, hood_hi)
    frame.rect(43 + lean, head_y - 9, 13, 3, hair)
    if female:
        frame.rect(42 + lean, head_y - 8, 10, 2, hair_hi)
    frame.pixel(55 + lean, head_y + 1, eye)
    frame.pixel(56 + lean, head_y + 1, eye)
    frame.pixel(55 + lean, head_y, eye_glint)
    frame.rect(56 + lean, head_y + 7, 4, 1, skin_shadow)
    if action == "revive":
        glow = rgba("#ffdc7d", 118 + frame_index * 10)
        frame.ellipse(48, 58, 28 + frame_index % 3, 34 + frame_index % 3, glow)


def hero_sheet(path: Path, female: bool) -> None:
    sheet = Image(96 * 8, 96 * len(HERO_ACTIONS))
    for action, config in HERO_ACTIONS.items():
        for frame_index in range(8):
            frame = Image(96, 96)
            draw_hero_frame(frame, frame_index, action, female)
            sheet.paste(frame, frame_index * 96, config["row"] * 96)
    sheet.save_png(path)


def draw_slime(frame: Image, i: int, action: str) -> None:
    ground = 58
    bounce = round(math.sin(i / 8 * math.tau) * 3)
    if action == "attack":
        bounce -= min(i, 4)
    if action == "death":
        bounce = 9
    draw_shadow(frame, 32, ground + 1, 22, 5)
    frame.ellipse(32, 39 + bounce, 23, 17, rgba("#18201c"))
    frame.ellipse(32, 38 + bounce, 21, 15, rgba("#5db7a3"))
    frame.ellipse(25, 34 + bounce, 5, 4, rgba("#b9ffe4"))
    frame.ellipse(41, 34 + bounce, 5, 4, rgba("#b9ffe4"))
    frame.pixel(27, 34 + bounce, rgba("#141817"))
    frame.pixel(43, 34 + bounce, rgba("#141817"))
    frame.rect(27, 45 + bounce, 13, 2, rgba("#276a5c"))


def draw_thorn(frame: Image, i: int, action: str) -> None:
    ground = 59
    bob = round(math.sin(i / 8 * math.tau) * 2)
    if action == "attack":
        bob -= min(i, 3)
    draw_shadow(frame, 32, ground + 1, 22, 5)
    frame.line(16, 28 + bob, 24, 42 + bob, rgba("#1d3928"), 4)
    frame.line(49, 25 + bob, 41, 42 + bob, rgba("#1d3928"), 4)
    frame.ellipse(33, 39 + bob, 22, 17, rgba("#151c18"))
    frame.ellipse(33, 38 + bob, 20, 15, rgba("#4d6f35"))
    frame.rect(22, 45 + bob, 24, 10, rgba("#26381f"))
    frame.rect(23, 35 + bob, 5, 4, rgba("#ffca55"))
    frame.rect(40, 35 + bob, 5, 4, rgba("#ffca55"))
    for x in (21, 31, 43):
        frame.poly([(x, 25 + bob), (x + 5, 34 + bob), (x - 5, 34 + bob)], rgba("#9bbf66"))


def draw_imp(frame: Image, i: int, action: str) -> None:
    ground = 59
    hop = round(math.sin(i / 8 * math.tau) * 4)
    if action == "attack":
        hop -= min(i, 4)
    draw_shadow(frame, 32, ground + 1, 19, 4)
    frame.line(25, 42 + hop, 19, 56, rgba("#29161a"), 4)
    frame.line(39, 42 + hop, 45, 56, rgba("#29161a"), 4)
    frame.ellipse(32, 35 + hop, 19, 20, rgba("#211218"))
    frame.ellipse(32, 34 + hop, 17, 18, rgba("#8f3544"))
    frame.poly([(21, 22 + hop), (27, 32 + hop), (17, 32 + hop)], rgba("#f3d49b"))
    frame.poly([(43, 22 + hop), (37, 32 + hop), (47, 32 + hop)], rgba("#f3d49b"))
    frame.rect(24, 33 + hop, 6, 4, rgba("#ffdc7d"))
    frame.rect(37, 33 + hop, 6, 4, rgba("#ffdc7d"))
    frame.line(44, 39 + hop, 56, 34 + hop, rgba("#f3d49b"), 2)


def draw_boss(frame: Image, i: int, action: str) -> None:
    ground = 116
    sway = round(math.sin(i / 8 * math.tau) * 3)
    if action == "attack":
        sway += min(i, 4) * 2
    draw_shadow(frame, 64, ground + 2, 42, 8)
    frame.line(42, 76, 30 + sway, 112, rgba("#1b241b"), 9)
    frame.line(82, 76, 96 + sway, 112, rgba("#1b241b"), 9)
    frame.rect(39 + sway, 36, 50, 61, rgba("#1a2119"))
    frame.rect(43 + sway, 38, 42, 57, rgba("#4e3a25"))
    frame.rect(46 + sway, 48, 36, 15, rgba("#2f8052"))
    frame.ellipse(64 + sway, 41, 31, 25, rgba("#171b1c"))
    frame.ellipse(64 + sway, 40, 28, 22, rgba("#6d4b2c"))
    frame.line(39 + sway, 29, 22 + sway, 13, rgba("#332418"), 5)
    frame.line(88 + sway, 29, 108 + sway, 12, rgba("#332418"), 5)
    frame.rect(51 + sway, 38, 7, 5, rgba("#ffca55"))
    frame.rect(73 + sway, 38, 7, 5, rgba("#ffca55"))
    frame.line(30 + sway, 65, 12 + sway, 85, rgba("#332418"), 8)
    frame.line(90 + sway, 63, 116 + sway, 78, rgba("#332418"), 8)
    for x, y in ((51, 21), (75, 18), (62, 16)):
        frame.ellipse(x + sway, y, 5, 5, rgba("#5fd18b"))


def monster_sheet(path: Path, kind: str, size: int) -> None:
    sheet = Image(size * 8, size * 5)
    for action, config in MONSTER_ACTIONS.items():
        for frame_index in range(8):
            frame = Image(size, size)
            if kind == "slime":
                draw_slime(frame, frame_index, action)
            elif kind == "thorn":
                draw_thorn(frame, frame_index, action)
            elif kind == "imp":
                draw_imp(frame, frame_index, action)
            else:
                draw_boss(frame, frame_index, action)
            sheet.paste(frame, frame_index * size, config["row"] * size)
    sheet.save_png(path)


def write_manifest() -> None:
    manifest = {
        "version": "pixel-v1",
        "tileSize": 32,
        "heroes": {
            "male_base": {
                "image": "/web/assets/pixel/v1/heroes/male/base.png",
                "frameWidth": 96,
                "frameHeight": 96,
                "drawWidth": 88,
                "drawHeight": 88,
                "anchors": {
                    "feet": [48, 84],
                    "mainHand": [62, 50],
                    "offHand": [36, 51],
                    "head": [49, 29],
                    "torso": [48, 50],
                },
                "animations": HERO_ACTIONS,
            },
            "female_base": {
                "image": "/web/assets/pixel/v1/heroes/female/base.png",
                "frameWidth": 96,
                "frameHeight": 96,
                "drawWidth": 88,
                "drawHeight": 88,
                "anchors": {
                    "feet": [48, 84],
                    "mainHand": [62, 50],
                    "offHand": [36, 51],
                    "head": [49, 29],
                    "torso": [48, 50],
                },
                "animations": HERO_ACTIONS,
            },
        },
        "equipment": {},
        "monsters": {
            "slime": {
                "image": "/web/assets/pixel/v1/monsters/common/slime.png",
                "frameWidth": 64,
                "frameHeight": 64,
                "drawWidth": 70,
                "drawHeight": 70,
                "animations": MONSTER_ACTIONS,
            },
            "thorn": {
                "image": "/web/assets/pixel/v1/monsters/common/thorn.png",
                "frameWidth": 64,
                "frameHeight": 64,
                "drawWidth": 72,
                "drawHeight": 72,
                "animations": MONSTER_ACTIONS,
            },
            "imp": {
                "image": "/web/assets/pixel/v1/monsters/common/imp.png",
                "frameWidth": 64,
                "frameHeight": 64,
                "drawWidth": 70,
                "drawHeight": 70,
                "animations": MONSTER_ACTIONS,
            },
            "forest_boss": {
                "image": "/web/assets/pixel/v1/monsters/bosses/forest_boss.png",
                "frameWidth": 128,
                "frameHeight": 128,
                "drawWidth": 126,
                "drawHeight": 126,
                "animations": MONSTER_ACTIONS,
            },
        },
        "maps": {},
        "effects": {},
    }
    path = ASSET_ROOT / "manifests" / "assets.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")


def write_prompt_notes() -> None:
    text = """# Pixel Asset Prompt Notes

These first-pass assets are generated locally with `tools/generate_pixel_assets.py`.
They establish the file layout, frame sizes, animation rows, and anchors that future
Pixellab exports should follow.

Recommended Pixellab prompt base:

```text
dark fantasy pixel art side-view game sprite, clean readable silhouette, upper-left
warm rim light, transparent background, sprite sheet, no text, no UI frame, no watermark
```

Hero export target:

- 96x96 frame size
- 8 columns
- rows: idle, walk, attack_unarmed, attack_blade, attack_dual, attack_bow,
  attack_spear, attack_heavy, hurt, death, revive
- base hero frames must keep both hands empty; weapons are separate overlays attached
  by per-frame hand anchors in the frontend

Monster export target:

- common monsters: 64x64 frame size
- boss monsters: 128x128 frame size
- 8 columns
- rows: idle, walk, attack, hurt, death
"""
    (ASSET_ROOT / "PROMPTS.md").write_text(text, encoding="utf-8")


def main() -> None:
    hero_sheet(ASSET_ROOT / "heroes" / "male" / "base.png", female=False)
    hero_sheet(ASSET_ROOT / "heroes" / "female" / "base.png", female=True)
    monster_sheet(ASSET_ROOT / "monsters" / "common" / "slime.png", "slime", 64)
    monster_sheet(ASSET_ROOT / "monsters" / "common" / "thorn.png", "thorn", 64)
    monster_sheet(ASSET_ROOT / "monsters" / "common" / "imp.png", "imp", 64)
    monster_sheet(ASSET_ROOT / "monsters" / "bosses" / "forest_boss.png", "boss", 128)
    write_manifest()
    write_prompt_notes()


if __name__ == "__main__":
    main()
