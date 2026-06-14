"""Regenerate monster sheets from Pixellab seed frames and animations.

The Pixellab API can drift away from strict sprite grids, so this script keeps
raw generations in artifacts and imports only normalized fixed-slot sheets into
the game asset directory.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import shutil
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from generate_pixel_assets import Image
from import_assassin_sample import read_png
from pixellab_api_generate import (
    PixellabError,
    decode_base64_image,
    find_base64_images,
    poll_job,
    request_json,
)


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = ROOT / "artifacts" / "pixellab" / "api" / "monsters" / "regenerated"
ASSET_ROOT = ROOT / "web" / "assets" / "pixel" / "v1"
MANIFEST_PATH = ASSET_ROOT / "manifests" / "assets.json"
ACTIONS = ("idle", "walk", "attack", "hurt", "death")


@dataclass(frozen=True)
class MonsterSpec:
    key: str
    description: str
    boss: bool = False

    @property
    def slot_size(self) -> int:
        return 128 if self.boss else 64

    @property
    def seed_size(self) -> int:
        return 256 if self.boss else 128

    @property
    def asset_path(self) -> Path:
        family = "bosses" if self.boss else "common"
        return ASSET_ROOT / "monsters" / family / f"{self.key}.png"


MONSTERS = [
    MonsterSpec("forest_slime", "low crawling amber gelatin slime, transparent ooze body, glowing green leaf core inside, no legs, splash lunge attack"),
    MonsterSpec("thorn_boar", "quadruped horned forest boar, bramble armor, mossy tusks, animal body, weighty charge attack"),
    MonsterSpec("moss_imp", "small moss goblin predator, branch horns, hunched biped body, claw swipe attack"),
    MonsterSpec("wild_mushroom", "squat fungal crawler, huge plated mushroom cap, short stem legs, spore burst attack"),
    MonsterSpec("bark_guard", "wooden bark guardian beast, root limbs, tree trunk torso, heavy slam attack"),
    MonsterSpec("cave_bat", "cavern bat creature, wide wings, hooked claws, no humanoid armor, diving bite attack"),
    MonsterSpec("crystal_lurker", "low crystal panther lizard, four legs, glowing jaw, shard pounce attack"),
    MonsterSpec("stone_crawler", "armored stone insect crawler, many legs, mandibles, snap attack"),
    MonsterSpec("cloud_wisp", "floating cloud spirit beast, soft vapor body, curling tail, wind pulse attack"),
    MonsterSpec("storm_harpy", "storm feather raptor harpy, bird monster body, talons, slash attack"),
    MonsterSpec("sun_mote", "bright solar floating creature, round glowing core with flame fins, flare burst attack"),
    MonsterSpec("rust_guard", "rusted castle armor beast, animated empty armor body, broken halberd arm, chop attack"),
    MonsterSpec("hollow_knight", "hollow cursed knight creature, oversized helm, empty shadow body, sword lunge attack"),
    MonsterSpec("cursed_squire", "small cursed shield squire construct, squat armor body, shield bash attack"),
    MonsterSpec("cave_warden", "massive crystal-jawed cave apex monster, quadruped body, crystal spike burst attack", True),
    MonsterSpec("tempest_seraph", "huge storm wing apex beast, lightning feather wings, non-human monster body, dive and wing sweep attack", True),
    MonsterSpec("throne_keeper", "cursed throne guardian titan, royal plate monster body, giant blade smash and shield crush attack", True),
]

ACTION_PROMPTS = {
    "idle": "subtle breathing idle loop, same monster, stable feet, no camera movement, full body remains visible",
    "walk": "smooth in-place side-view walk loop, same monster, stable body scale, no travel across frame, full body remains visible",
    "attack": "clear side-view attack animation, same monster, strike forward then recover, full body remains visible",
    "hurt": "brief recoil hurt animation, same monster, full body remains visible",
    "death": "collapse or dissolve death animation, same monster, full body remains visible",
}


def alpha_bbox(pixels: bytearray, width: int, height: int) -> tuple[int, int, int, int] | None:
    min_x = width
    min_y = height
    max_x = -1
    max_y = -1
    for y in range(height):
        for x in range(width):
            if pixels[(y * width + x) * 4 + 3] <= 8:
                continue
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            max_x = max(max_x, x)
            max_y = max(max_y, y)
    if max_x < 0:
        return None
    return min_x, min_y, max_x, max_y


def frame_alpha_bbox(frame: Image) -> tuple[int, int, int, int] | None:
    return alpha_bbox(frame.pixels, frame.width, frame.height)


def visible_area(pixels: bytearray) -> int:
    return sum(1 for index in range(3, len(pixels), 4) if pixels[index] > 8)


def body_anchor_bbox(pixels: bytearray, width: int, height: int) -> tuple[int, int, int, int] | None:
    body = bytearray(pixels)
    for index in range(0, len(body), 4):
        alpha = body[index + 3]
        if alpha <= 8:
            continue
        r, g, b = body[index], body[index + 1], body[index + 2]
        brightness = (r + g + b) / 3
        saturation = max(r, g, b) - min(r, g, b)
        if brightness > 225 or (brightness > 185 and saturation > 85):
            body[index + 3] = 0
    return alpha_bbox(body, width, height)


def image_from_png(path: Path) -> Image:
    width, height, pixels = read_png(path)
    image = Image(width, height)
    image.pixels[:] = pixels
    return remove_edge_background(image)


def color_distance(a: tuple[int, int, int, int], b: tuple[int, int, int, int]) -> float:
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2) ** 0.5


def pixel_at(image: Image, x: int, y: int) -> tuple[int, int, int, int]:
    index = (y * image.width + x) * 4
    return tuple(image.pixels[index:index + 4])  # type: ignore[return-value]


def remove_edge_background(image: Image, tolerance: float = 34.0) -> Image:
    corners = [
        pixel_at(image, 0, 0),
        pixel_at(image, image.width - 1, 0),
        pixel_at(image, 0, image.height - 1),
        pixel_at(image, image.width - 1, image.height - 1),
    ]
    background = tuple(sorted(color[index] for color in corners)[len(corners) // 2] for index in range(4))
    if background[3] <= 8:
        return image

    cleaned = Image(image.width, image.height)
    cleaned.pixels[:] = image.pixels
    visited = bytearray(image.width * image.height)
    queue = [(0, 0), (image.width - 1, 0), (0, image.height - 1), (image.width - 1, image.height - 1)]
    while queue:
        x, y = queue.pop()
        if x < 0 or y < 0 or x >= image.width or y >= image.height:
            continue
        offset = y * image.width + x
        if visited[offset]:
            continue
        visited[offset] = 1
        color = pixel_at(cleaned, x, y)
        if color[3] <= 8 or color_distance(color, background) > tolerance:
            continue
        index = offset * 4
        cleaned.pixels[index + 3] = 0
        queue.extend(((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))
    return cleaned


def clean_png_in_place(path: Path) -> None:
    image = image_from_png(path)
    image.save_png(path)


def crop_frame(image: Image, bbox: tuple[int, int, int, int]) -> Image:
    x0, y0, x1, y1 = bbox
    out = Image(x1 - x0 + 1, y1 - y0 + 1)
    for y in range(out.height):
        for x in range(out.width):
            src = ((y0 + y) * image.width + x0 + x) * 4
            color = tuple(image.pixels[src:src + 4])
            if color[3]:
                out.pixel(x, y, color)  # type: ignore[arg-type]
    return out


def paste_scaled(sheet: Image, frame: Image, slot_x: int, slot_y: int, scale: float, slot_size: int) -> None:
    bbox = frame_alpha_bbox(frame)
    if bbox is None:
        return
    cropped = crop_frame(frame, bbox)
    draw_w = max(1, round(cropped.width * scale))
    draw_h = max(1, round(cropped.height * scale))
    dest_x = slot_x + (slot_size - draw_w) // 2
    dest_y = slot_y + slot_size - 4 - draw_h
    for y in range(draw_h):
        sy = min(cropped.height - 1, int(y / scale))
        for x in range(draw_w):
            sx = min(cropped.width - 1, int(x / scale))
            src = (sy * cropped.width + sx) * 4
            color = tuple(cropped.pixels[src:src + 4])
            if color[3] > 8:
                sheet.pixel(dest_x + x, dest_y + y, color)  # type: ignore[arg-type]


def split_strip(path: Path, expected: int) -> list[Image]:
    image = image_from_png(path)
    width, height, pixels = image.width, image.height, image.pixels
    frames: list[Image] = []
    if width >= height * 2:
        for index in range(expected):
            x0 = round(index * width / expected)
            x1 = round((index + 1) * width / expected)
            frame = Image(x1 - x0, height)
            for y in range(height):
                for x in range(frame.width):
                    src = (y * width + x0 + x) * 4
                    color = tuple(pixels[src:src + 4])
                    if color[3]:
                        frame.pixel(x, y, color)  # type: ignore[arg-type]
            frames.append(frame)
    return frames


def load_action_frames(action_dir: Path, expected: int = 8) -> list[Image]:
    files = sorted(path for path in action_dir.glob("*.png") if path.name != "seed.png")
    if len(files) == 1:
        strip = split_strip(files[0], expected)
        if len(strip) >= expected:
            return strip[:expected]
    return [image_from_png(path) for path in files[:expected]]


def save_response_images(response: dict[str, Any], out_dir: Path, prefix: str) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for index, data in enumerate(find_base64_images(response), start=1):
        path = out_dir / f"{prefix}_{index:02d}.png"
        path.write_bytes(decode_base64_image(data))
        paths.append(path)
    return paths


def create_seed(spec: MonsterSpec, out_dir: Path, seed: int | None, force: bool) -> Path:
    seed_path = out_dir / "seed.png"
    if seed_path.exists() and not force:
        return seed_path
    prompt = (
        "dark fantasy pixel art side-view Monster Hunter inspired game monster, "
        f"{spec.description}, facing right, full body centered, transparent background, "
        "no text, no scenery, complete silhouette with head feet tail fully visible, "
        "production game sprite, readable at small scale"
    )
    payload: dict[str, Any] = {
        "description": prompt,
        "image_size": {"width": spec.seed_size, "height": spec.seed_size},
        "no_background": True,
        "view": "side",
        "direction": "east",
        "outline": "single color outline",
        "detail": "medium detail",
    }
    if seed is not None:
        payload["seed"] = seed
    response = request_json("POST", "/create-image-pixflux", payload)
    paths = save_response_images(response, out_dir, "seed_raw")
    if not paths:
        raise PixellabError(f"No seed image returned for {spec.key}")
    shutil.copyfile(paths[0], seed_path)
    clean_png_in_place(seed_path)
    return seed_path


def create_action_frames(spec: MonsterSpec, seed_path: Path, action: str, out_dir: Path, seed: int | None, force: bool) -> None:
    existing = sorted(out_dir.glob("*.png"))
    if len(existing) >= 8 and not force:
        return
    if force and out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    prompt = (
        f"{ACTION_PROMPTS[action]}, dark fantasy pixel art, side-view facing right, "
        f"Monster Hunter inspired {spec.description}, transparent background, no scenery, no text"
    )
    payload: dict[str, Any] = {
        "first_frame": {
            "base64": "data:image/png;base64," + __import__("base64").b64encode(seed_path.read_bytes()).decode("ascii")
        },
        "action": prompt,
        "frame_count": 8,
        "no_background": True,
    }
    if seed is not None:
        payload["seed"] = seed
    response = None
    for attempt in range(1, 7):
        try:
            response = request_json("POST", "/animate-with-text-v3", payload)
            break
        except PixellabError as exc:
            if "429" not in str(exc) or attempt >= 6:
                raise
            wait = 20 * attempt
            print(f"{spec.key} {action}: Pixellab concurrency limit, retrying in {wait}s", file=sys.stderr)
            time.sleep(wait)
    if response is None:
        raise PixellabError(f"Could not submit {action} animation for {spec.key}")
    job_id = response["background_job_id"]
    status = poll_job(job_id, 5, 900 if spec.boss else 360)
    (out_dir / "job.json").write_text(json.dumps(status, ensure_ascii=False, indent=2), encoding="utf-8")
    paths = save_response_images(status.get("last_response") or status, out_dir, "frame")
    if not paths:
        raise PixellabError(f"No {action} frames returned for {spec.key}")


def validate_seed(path: Path, spec: MonsterSpec) -> None:
    clean_png_in_place(path)
    width, height, pixels = read_png(path)
    bbox = alpha_bbox(pixels, width, height)
    if bbox is None:
        raise ValueError(f"{spec.key} seed is empty")
    min_visible = 700 if spec.boss else 220
    if visible_area(pixels) < min_visible:
        raise ValueError(f"{spec.key} seed is too sparse")
    x0, y0, x1, y1 = bbox
    if x0 <= 1 or y0 <= 1 or x1 >= width - 2 or y1 >= height - 2:
        raise ValueError(f"{spec.key} seed touches edge: {bbox}")


def build_sheet(spec: MonsterSpec, source_dir: Path, output_path: Path) -> None:
    frames_by_action: dict[str, list[Image]] = {}
    all_bboxes: list[tuple[int, int, int, int]] = []
    for action in ACTIONS:
        frames = load_action_frames(source_dir / action)
        if len(frames) < 8:
            raise ValueError(f"{spec.key} {action} has {len(frames)} frames, expected 8")
        frames_by_action[action] = frames
        for frame in frames:
            bbox = frame_alpha_bbox(frame)
            if bbox is None:
                raise ValueError(f"{spec.key} {action} contains an empty frame")
            all_bboxes.append(bbox)

    max_w = max(x1 - x0 + 1 for x0, _y0, x1, _y1 in all_bboxes)
    max_h = max(y1 - y0 + 1 for _x0, y0, _x1, y1 in all_bboxes)
    slot = spec.slot_size
    scale = min((slot - 8) / max(1, max_w), (slot - 8) / max(1, max_h))
    sheet = Image(slot * 8, slot * len(ACTIONS))
    for row, action in enumerate(ACTIONS):
        for col, frame in enumerate(frames_by_action[action]):
            paste_scaled(sheet, frame, col * slot, row * slot, scale, slot)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save_png(output_path)


def validate_sheet(spec: MonsterSpec, path: Path) -> None:
    width, height, pixels = read_png(path)
    slot = spec.slot_size
    if (width, height) != (slot * 8, slot * 5):
        raise ValueError(f"{spec.key} sheet has wrong size: {width}x{height}")
    min_visible = 420 if spec.boss else 120
    for row, action in enumerate(ACTIONS):
        bottoms: list[int] = []
        centers: list[float] = []
        for col in range(8):
            frame = bytearray(slot * slot * 4)
            for y in range(slot):
                src = ((row * slot + y) * width + col * slot) * 4
                dst = y * slot * 4
                frame[dst:dst + slot * 4] = pixels[src:src + slot * 4]
            bbox = alpha_bbox(frame, slot, slot)
            anchor = body_anchor_bbox(frame, slot, slot) or bbox
            if bbox is None:
                raise ValueError(f"{spec.key} {action} frame {col + 1} is empty")
            area = visible_area(frame)
            if area < min_visible:
                raise ValueError(f"{spec.key} {action} frame {col + 1} is too sparse: {area}")
            x0, y0, x1, y1 = bbox
            if x0 < 2 or y0 < 2 or x1 > slot - 2 or y1 > slot - 2:
                raise ValueError(f"{spec.key} {action} frame {col + 1} touches edge: {bbox}")
            ax0, _ay0, ax1, ay1 = anchor
            bottoms.append(ay1)
            centers.append((ax0 + ax1) / 2)
        allowed_bottom_drift = 4 if action in {"hurt", "death"} else 1
        if max(bottoms) - min(bottoms) > allowed_bottom_drift:
            raise ValueError(f"{spec.key} {action} bottom anchor drifts")
        if max(centers) - min(centers) > (6 if spec.boss else 4):
            raise ValueError(f"{spec.key} {action} horizontal anchor drifts")


def update_manifest(specs: list[MonsterSpec]) -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    for spec in specs:
        record = manifest["monsters"][spec.key]
        record["source"] = "pixellab"
    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def run(specs: list[MonsterSpec], *, force: bool, seed: int | None, import_only: bool, workers: int) -> None:
    imported: list[MonsterSpec] = []
    for index, spec in enumerate(specs, start=1):
        print(f"[{index}/{len(specs)}] {spec.key}")
        work_dir = ARTIFACT_ROOT / spec.key
        work_dir.mkdir(parents=True, exist_ok=True)
        seed_path = work_dir / "seed.png"
        if not import_only:
            seed_path = create_seed(spec, work_dir, None if seed is None else seed + index, force)
            validate_seed(seed_path, spec)
            with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, workers)) as executor:
                futures = [
                    executor.submit(
                        create_action_frames,
                        spec,
                        seed_path,
                        action,
                        work_dir / action,
                        None if seed is None else seed + index * 100 + action_index,
                        force,
                    )
                    for action_index, action in enumerate(ACTIONS, start=1)
                ]
                for future in concurrent.futures.as_completed(futures):
                    future.result()
        if not seed_path.exists():
            raise ValueError(f"{spec.key} seed is missing; cannot import")
        build_sheet(spec, work_dir, spec.asset_path)
        validate_sheet(spec, spec.asset_path)
        imported.append(spec)
    update_manifest(imported)


def selected_specs(names: list[str]) -> list[MonsterSpec]:
    if not names:
        return MONSTERS
    by_key = {spec.key: spec for spec in MONSTERS}
    missing = [name for name in names if name not in by_key]
    if missing:
        raise ValueError(f"Unknown monster keys: {', '.join(missing)}")
    return [by_key[name] for name in names]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--monster", action="append", default=[], help="Regenerate/import one monster key; repeatable")
    parser.add_argument("--force", action="store_true", help="Regenerate existing Pixellab outputs")
    parser.add_argument("--seed", type=int, default=9100)
    parser.add_argument("--import-only", action="store_true", help="Skip Pixellab calls and import existing artifact frames")
    parser.add_argument("--workers", type=int, default=2, help="Concurrent Pixellab action jobs per monster")
    args = parser.parse_args()
    try:
        run(selected_specs(args.monster), force=args.force, seed=args.seed, import_only=args.import_only, workers=args.workers)
    except (PixellabError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
