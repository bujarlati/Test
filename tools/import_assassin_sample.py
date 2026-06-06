"""Import a generated 3x8 assassin sprite preview into a game sprite sheet.

The source is expected to be a three-row, eight-column image:
row 0 idle, row 1 walk/run, row 2 empty-hand blade attack motion.
The output is a transparent 128px-frame sheet matching the frontend action rows.
"""

from __future__ import annotations

import argparse
import statistics
import struct
import sys
import zlib
from collections import deque
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from generate_pixel_assets import HERO_ACTIONS, Image


Color = tuple[int, int, int, int]


def paeth(a: int, b: int, c: int) -> int:
    p = a + b - c
    pa = abs(p - a)
    pb = abs(p - b)
    pc = abs(p - c)
    if pa <= pb and pa <= pc:
        return a
    if pb <= pc:
        return b
    return c


def read_png(path: Path) -> tuple[int, int, bytearray]:
    data = path.read_bytes()
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError(f"{path} is not a PNG")
    offset = 8
    width = height = 0
    color_type = 0
    idat = bytearray()
    while offset < len(data):
        length = struct.unpack(">I", data[offset:offset + 4])[0]
        kind = data[offset + 4:offset + 8]
        payload = data[offset + 8:offset + 8 + length]
        offset += 12 + length
        if kind == b"IHDR":
            width, height, bit_depth, color_type, _compression, _filter, interlace = struct.unpack(
                ">IIBBBBB", payload
            )
            if bit_depth != 8 or color_type not in (2, 6) or interlace != 0:
                raise ValueError("only non-interlaced 8-bit RGB/RGBA PNG files are supported")
        elif kind == b"IDAT":
            idat.extend(payload)
        elif kind == b"IEND":
            break

    channels = 4 if color_type == 6 else 3
    bpp = channels
    stride = width * channels
    raw = zlib.decompress(bytes(idat))
    rows: list[bytearray] = []
    cursor = 0
    previous = bytearray(stride)
    for _y in range(height):
        filter_type = raw[cursor]
        cursor += 1
        current = bytearray(raw[cursor:cursor + stride])
        cursor += stride
        for index in range(stride):
            left = current[index - bpp] if index >= bpp else 0
            up = previous[index]
            up_left = previous[index - bpp] if index >= bpp else 0
            if filter_type == 1:
                current[index] = (current[index] + left) & 0xFF
            elif filter_type == 2:
                current[index] = (current[index] + up) & 0xFF
            elif filter_type == 3:
                current[index] = (current[index] + ((left + up) // 2)) & 0xFF
            elif filter_type == 4:
                current[index] = (current[index] + paeth(left, up, up_left)) & 0xFF
            elif filter_type != 0:
                raise ValueError(f"unsupported PNG filter {filter_type}")
        rows.append(current)
        previous = current

    rgba = bytearray(width * height * 4)
    for y, row in enumerate(rows):
        for x in range(width):
            src = x * channels
            dst = (y * width + x) * 4
            rgba[dst:dst + 3] = row[src:src + 3]
            rgba[dst + 3] = row[src + 3] if channels == 4 else 255
    return width, height, rgba


def pixel(pixels: bytearray, width: int, x: int, y: int) -> Color:
    index = (y * width + x) * 4
    return pixels[index], pixels[index + 1], pixels[index + 2], pixels[index + 3]


def color_distance(a: Color, b: Color) -> float:
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2) ** 0.5


def median_background(pixels: bytearray, width: int, x0: int, y0: int, x1: int, y1: int) -> Color:
    samples: list[Color] = []
    step_x = max(1, (x1 - x0) // 28)
    step_y = max(1, (y1 - y0) // 28)
    for x in range(x0, x1, step_x):
        samples.append(pixel(pixels, width, x, y0))
        samples.append(pixel(pixels, width, x, y1 - 1))
    for y in range(y0, y1, step_y):
        samples.append(pixel(pixels, width, x0, y))
        samples.append(pixel(pixels, width, x1 - 1, y))
    return (
        int(statistics.median(c[0] for c in samples)),
        int(statistics.median(c[1] for c in samples)),
        int(statistics.median(c[2] for c in samples)),
        255,
    )


def transparent_mask(
    pixels: bytearray,
    width: int,
    x0: int,
    y0: int,
    x1: int,
    y1: int,
    tolerance: float,
) -> list[list[bool]]:
    cell_w = x1 - x0
    cell_h = y1 - y0
    background = median_background(pixels, width, x0, y0, x1, y1)
    transparent = [[False for _x in range(cell_w)] for _y in range(cell_h)]
    visited = [[False for _x in range(cell_w)] for _y in range(cell_h)]
    queue: deque[tuple[int, int]] = deque()

    def is_background(cx: int, cy: int) -> bool:
        color = pixel(pixels, width, x0 + cx, y0 + cy)
        return color[3] == 0 or color_distance(color, background) <= tolerance

    for cx in range(cell_w):
        queue.append((cx, 0))
        queue.append((cx, cell_h - 1))
    for cy in range(cell_h):
        queue.append((0, cy))
        queue.append((cell_w - 1, cy))

    while queue:
        cx, cy = queue.popleft()
        if cx < 0 or cy < 0 or cx >= cell_w or cy >= cell_h or visited[cy][cx]:
            continue
        visited[cy][cx] = True
        if not is_background(cx, cy):
            continue
        transparent[cy][cx] = True
        queue.append((cx + 1, cy))
        queue.append((cx - 1, cy))
        queue.append((cx, cy + 1))
        queue.append((cx, cy - 1))
    return transparent


def frame_bbox(mask: list[list[bool]]) -> tuple[int, int, int, int] | None:
    xs: list[int] = []
    ys: list[int] = []
    for y, row in enumerate(mask):
        for x, transparent in enumerate(row):
            if not transparent:
                xs.append(x)
                ys.append(y)
    if not xs:
        return None
    return min(xs), min(ys), max(xs) + 1, max(ys) + 1


def keep_largest_component(mask: list[list[bool]]) -> list[list[bool]]:
    height = len(mask)
    width = len(mask[0]) if height else 0
    visited = [[False for _x in range(width)] for _y in range(height)]
    best: set[tuple[int, int]] = set()

    for y in range(height):
        for x in range(width):
            if mask[y][x] or visited[y][x]:
                continue
            component: set[tuple[int, int]] = set()
            queue: deque[tuple[int, int]] = deque([(x, y)])
            while queue:
                cx, cy = queue.popleft()
                if cx < 0 or cy < 0 or cx >= width or cy >= height:
                    continue
                if visited[cy][cx] or mask[cy][cx]:
                    continue
                visited[cy][cx] = True
                component.add((cx, cy))
                queue.append((cx + 1, cy))
                queue.append((cx - 1, cy))
                queue.append((cx, cy + 1))
                queue.append((cx, cy - 1))
            if len(component) > len(best):
                best = component

    if not best:
        return mask
    refined = [[True for _x in range(width)] for _y in range(height)]
    for x, y in best:
        refined[y][x] = False
    return refined


def paste_scaled_frame(
    sheet: Image,
    out_col: int,
    out_row: int,
    pixels: bytearray,
    source_width: int,
    source_x0: int,
    source_y0: int,
    mask: list[list[bool]],
    bbox: tuple[int, int, int, int],
    frame_size: int = 128,
) -> None:
    bx0, by0, bx1, by1 = bbox
    bbox_w = bx1 - bx0
    bbox_h = by1 - by0
    scale = min(116 / max(1, bbox_w), 116 / max(1, bbox_h))
    draw_w = max(1, round(bbox_w * scale))
    draw_h = max(1, round(bbox_h * scale))
    dest_x0 = out_col * frame_size + (frame_size - draw_w) // 2
    dest_y0 = out_row * frame_size + 121 - draw_h

    for dy in range(draw_h):
        sy = min(by1 - 1, by0 + int(dy / scale))
        for dx in range(draw_w):
            sx = min(bx1 - 1, bx0 + int(dx / scale))
            if mask[sy][sx]:
                continue
            color = pixel(pixels, source_width, source_x0 + sx, source_y0 + sy)
            if color[3] == 0:
                continue
            sheet.pixel(dest_x0 + dx, dest_y0 + dy, color)


def build_sheet(source: Path, output: Path, tolerance: float = 28.0) -> None:
    width, height, pixels = read_png(source)
    sheet = Image(128 * 8, 128 * len(HERO_ACTIONS))
    source_rows = {
        "idle": 0,
        "walk": 1,
        "attack_unarmed": 2,
        "attack_blade": 2,
        "attack_dual": 2,
        "attack_bow": 2,
        "attack_spear": 2,
        "attack_heavy": 2,
        "hurt": 2,
        "death": 2,
        "revive": 0,
    }

    for action, config in HERO_ACTIONS.items():
        src_row = source_rows[action]
        for col in range(8):
            x0 = round(col * width / 8)
            x1 = round((col + 1) * width / 8)
            y0 = round(src_row * height / 3)
            y1 = round((src_row + 1) * height / 3)
            mask = transparent_mask(pixels, width, x0, y0, x1, y1, tolerance)
            mask = keep_largest_component(mask)
            bbox = frame_bbox(mask)
            if bbox is None:
                continue
            paste_scaled_frame(sheet, col, config["row"], pixels, width, x0, y0, mask, bbox)

    sheet.save_png(output)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--tolerance", type=float, default=28.0)
    args = parser.parse_args()
    build_sheet(args.source, args.output, args.tolerance)


if __name__ == "__main__":
    main()
