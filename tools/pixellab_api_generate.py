"""Small Pixellab v2 API helper for local asset generation.

Set PIXELLAB_API_KEY in the environment before running. Generated files are
written locally and should be inspected before copying into web/assets.
"""

from __future__ import annotations

import argparse
import base64
import http.client
import json
import os
import socket
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


BASE_URL = os.environ.get("PIXELLAB_BASE_URL", "https://api.pixellab.ai/v2").rstrip("/")
ROOT = Path(__file__).resolve().parents[1]
REQUEST_TIMEOUT = float(os.environ.get("PIXELLAB_REQUEST_TIMEOUT", "300"))
REQUEST_RETRIES = int(os.environ.get("PIXELLAB_REQUEST_RETRIES", "3"))


class PixellabError(RuntimeError):
    pass


def load_local_env() -> None:
    env_path = ROOT / ".env"
    if not env_path.exists():
        return
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def require_token() -> str:
    load_local_env()
    token = os.environ.get("PIXELLAB_API_KEY", "").strip()
    if not token:
        raise PixellabError("PIXELLAB_API_KEY is not set")
    return token


def request_json(method: str, path: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    token = require_token()
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    for attempt in range(1, REQUEST_RETRIES + 1):
        request = urllib.request.Request(
            f"{BASE_URL}{path}",
            data=body,
            method=method,
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT) as response:
                raw = response.read().decode("utf-8")
                return json.loads(raw) if raw else {}
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise PixellabError(f"Pixellab API error {exc.code}: {detail}") from exc
        except (
            TimeoutError,
            ConnectionResetError,
            socket.timeout,
            urllib.error.URLError,
            http.client.RemoteDisconnected,
            http.client.IncompleteRead,
        ) as exc:
            if attempt >= REQUEST_RETRIES:
                raise PixellabError(f"Pixellab API connection failed after {attempt} attempts: {exc}") from exc
            time.sleep(2 * attempt)
    raise PixellabError("Pixellab API request failed")


def request_binary(url: str) -> bytes:
    token = os.environ.get("PIXELLAB_API_KEY", "").strip()
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    for attempt in range(1, REQUEST_RETRIES + 1):
        request = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT) as response:
                return response.read()
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise PixellabError(f"download error {exc.code}: {detail}") from exc
        except (
            TimeoutError,
            ConnectionResetError,
            socket.timeout,
            urllib.error.URLError,
            http.client.RemoteDisconnected,
            http.client.IncompleteRead,
        ) as exc:
            if attempt >= REQUEST_RETRIES:
                raise PixellabError(f"download failed after {attempt} attempts: {exc}") from exc
            time.sleep(2 * attempt)
    raise PixellabError("download failed")


def read_image_base64(path: Path) -> str:
    data = path.read_bytes()
    mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    return f"data:{mime};base64,{base64.b64encode(data).decode('ascii')}"


def read_image_base64_data(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("ascii")


def decode_base64_image(value: str) -> bytes:
    if "," in value and value.lstrip().startswith("data:"):
        value = value.split(",", 1)[1]
    return base64.b64decode(value)


def find_base64_images(value: Any) -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        if isinstance(value.get("base64"), str):
            found.append(value["base64"])
        for child in value.values():
            found.extend(find_base64_images(child))
    elif isinstance(value, list):
        for child in value:
            found.extend(find_base64_images(child))
    return found


def find_image_urls(value: Any) -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        for child in value.values():
            found.extend(find_image_urls(child))
    elif isinstance(value, list):
        for child in value:
            found.extend(find_image_urls(child))
    elif isinstance(value, str):
        lowered = value.lower()
        if lowered.startswith("http") and any(token in lowered for token in (".png", ".jpg", ".jpeg", ".webp")):
            found.append(value)
    return found


def write_images(response: dict[str, Any], out_dir: Path, prefix: str) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    for index, image in enumerate(find_base64_images(response), start=1):
        path = out_dir / f"{prefix}_{index:02d}.png"
        path.write_bytes(decode_base64_image(image))
        paths.append(path)
    return paths


def download_image_urls(response: dict[str, Any], out_dir: Path, prefix: str) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    seen: set[str] = set()
    for index, url in enumerate(find_image_urls(response), start=1):
        if url in seen:
            continue
        seen.add(url)
        suffix = Path(url.split("?", 1)[0]).suffix or ".png"
        path = out_dir / f"{prefix}_{index:02d}{suffix}"
        path.write_bytes(request_binary(url))
        paths.append(path)
    return paths


def poll_job(job_id: str, interval: float, timeout: float) -> dict[str, Any]:
    started = time.monotonic()
    while True:
        status = request_json("GET", f"/background-jobs/{job_id}")
        state = status.get("status")
        print(f"job {job_id}: {state}", file=sys.stderr)
        if state == "completed":
            return status
        if state == "failed":
            raise PixellabError(json.dumps(status.get("last_response"), ensure_ascii=False))
        if time.monotonic() - started > timeout:
            raise PixellabError(f"Timed out waiting for Pixellab job {job_id}")
        time.sleep(interval)


def poll_object(object_id: str, interval: float, timeout: float) -> dict[str, Any]:
    started = time.monotonic()
    running = {"queued", "pending", "processing", "running"}
    while True:
        status = request_json("GET", f"/objects/{object_id}")
        state = status.get("status")
        print(f"object {object_id}: {state}", file=sys.stderr)
        if state not in running:
            if state == "failed":
                raise PixellabError(json.dumps(status, ensure_ascii=False))
            return status
        if time.monotonic() - started > timeout:
            raise PixellabError(f"Timed out waiting for Pixellab object {object_id}")
        time.sleep(interval)


def add_common_image_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--width", type=int, default=128)
    parser.add_argument("--height", type=int, default=128)
    parser.add_argument("--seed", type=int)
    parser.add_argument("--no-background", action="store_true")
    parser.add_argument("--view", choices=["side", "low top-down", "high top-down"])
    parser.add_argument(
        "--direction",
        choices=[
            "north",
            "north-east",
            "east",
            "south-east",
            "south",
            "south-west",
            "west",
            "north-west",
        ],
    )
    parser.add_argument(
        "--outline",
        choices=["single color black outline", "single color outline", "selective outline", "lineless"],
    )
    parser.add_argument("--detail", choices=["low detail", "medium detail", "highly detailed"])


def image_payload(args: argparse.Namespace) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "description": args.prompt,
        "image_size": {"width": args.width, "height": args.height},
    }
    for name in ("seed", "view", "direction", "outline", "detail"):
        value = getattr(args, name, None)
        if value is not None:
            payload[name] = value
    if args.no_background:
        payload["no_background"] = True
    return payload


def cmd_balance(_: argparse.Namespace) -> None:
    print(json.dumps(request_json("GET", "/balance"), ensure_ascii=False, indent=2))


def cmd_image(args: argparse.Namespace) -> None:
    endpoint = "/create-image-pixflux" if args.model == "pixflux" else "/create-image-pixen"
    response = request_json("POST", endpoint, image_payload(args))
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    images = find_base64_images(response)
    if not images:
        raise PixellabError("No image found in Pixellab response")
    out.write_bytes(decode_base64_image(images[0]))
    print(out)


def cmd_pro_image(args: argparse.Namespace) -> None:
    response = request_json("POST", "/generate-image-v2", image_payload(args))
    job_id = response["background_job_id"]
    status = poll_job(job_id, args.poll_interval, args.timeout)
    paths = write_images(status.get("last_response") or status, Path(args.out_dir), "image")
    print(json.dumps({"job_id": job_id, "saved": [str(path) for path in paths]}, ensure_ascii=False, indent=2))


def cmd_animate(args: argparse.Namespace) -> None:
    payload: dict[str, Any] = {
        "first_frame": {"base64": read_image_base64(Path(args.first_frame))},
        "action": args.action,
        "frame_count": args.frame_count,
    }
    if args.seed is not None:
        payload["seed"] = args.seed
    if args.no_background:
        payload["no_background"] = True
    response = request_json("POST", "/animate-with-text-v3", payload)
    job_id = response["background_job_id"]
    status = poll_job(job_id, args.poll_interval, args.timeout)
    paths = write_images(status.get("last_response") or status, Path(args.out_dir), "frame")
    print(json.dumps({"job_id": job_id, "saved": [str(path) for path in paths]}, ensure_ascii=False, indent=2))


def read_skeleton_keypoints(path: Path) -> list[Any]:
    def normalize_keypoints(value: Any) -> Any:
        if isinstance(value, list):
            normalized = [normalize_keypoints(child) for child in value]
            for point in normalized:
                if isinstance(point, dict) and isinstance(point.get("z_index"), float):
                    point["z_index"] = round(point["z_index"])
            return normalized
        if isinstance(value, dict):
            normalized = {key: normalize_keypoints(child) for key, child in value.items()}
            if isinstance(normalized.get("z_index"), float):
                normalized["z_index"] = round(normalized["z_index"])
            return normalized
        return value

    if path.is_dir():
        keypoints: list[Any] = []
        for child in sorted(path.glob("*.json")):
            data = json.loads(child.read_text(encoding="utf-8"))
            keypoints.append(normalize_keypoints(data.get("keypoints") or data.get("skeleton_keypoints") or data))
        if not keypoints:
            raise PixellabError(f"No skeleton JSON files found in {path}")
        return keypoints
    data = json.loads(path.read_text(encoding="utf-8"))
    return normalize_keypoints(data.get("keypoints") or data.get("skeleton_keypoints") or data)


def cmd_animate_skeleton(args: argparse.Namespace) -> None:
    reference_path = Path(args.reference_image)
    payload: dict[str, Any] = {
        "image_size": {"width": args.width, "height": args.height},
        "reference_image": {
            "type": "base64",
            "base64": read_image_base64_data(reference_path),
            "format": reference_path.suffix.lower().lstrip(".") or "png",
        },
        "skeleton_keypoints": read_skeleton_keypoints(Path(args.skeleton)),
    }
    for name in ("seed", "view", "direction"):
        value = getattr(args, name, None)
        if value is not None:
            payload[name] = value
    if args.no_background:
        payload["no_background"] = True
    response = request_json("POST", "/animate-with-skeleton", payload)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "response.json").write_text(json.dumps(response, ensure_ascii=False, indent=2), encoding="utf-8")
    paths = write_images(response, out_dir, "frame")
    if not paths:
        paths = download_image_urls(response, out_dir, "frame")
    print(json.dumps({"metadata": str(out_dir / "response.json"), "saved": [str(path) for path in paths]}, ensure_ascii=False, indent=2))


def cmd_estimate_skeleton(args: argparse.Namespace) -> None:
    image_path = Path(args.image)
    payload = {
        "image": {
            "type": "base64",
            "base64": read_image_base64_data(image_path),
            "format": image_path.suffix.lower().lstrip(".") or "png",
        }
    }
    response = request_json("POST", "/estimate-skeleton", payload)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(response, ensure_ascii=False, indent=2), encoding="utf-8")
    keypoints = response.get("keypoints") or response.get("skeleton_keypoints") or []
    print(json.dumps({"out": str(out), "keypoints": len(keypoints)}, ensure_ascii=False, indent=2))


def cmd_character(args: argparse.Namespace) -> None:
    payload: dict[str, Any] = {
        "description": args.prompt,
        "image_size": {"width": args.width, "height": args.height},
        "view": args.view,
        "template_id": args.template_id,
    }
    if args.reference_image:
        payload["reference_image"] = {"base64": read_image_base64(Path(args.reference_image))}
    for name in ("seed", "outline", "detail"):
        value = getattr(args, name, None)
        if value is not None:
            payload[name] = value
    if args.no_background:
        payload["no_background"] = True
    response = request_json("POST", "/create-character-v3", payload)
    job_id = response["background_job_id"]
    status = poll_job(job_id, args.poll_interval, args.timeout)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "job.json").write_text(json.dumps(status, ensure_ascii=False, indent=2), encoding="utf-8")
    paths = write_images(status.get("last_response") or status, out_dir, "character")
    print(
        json.dumps(
            {
                "job_id": job_id,
                "character_id": response.get("character_id"),
                "metadata": str(out_dir / "job.json"),
                "saved": [str(path) for path in paths],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


def cmd_map_object(args: argparse.Namespace) -> None:
    payload: dict[str, Any] = {
        "description": args.prompt,
        "image_size": {"width": args.width, "height": args.height},
    }
    for name in ("seed", "view", "outline", "detail", "shading"):
        value = getattr(args, name, None)
        if value is not None:
            payload[name] = value
    response = request_json("POST", "/map-objects", payload)
    job_id = response["background_job_id"]
    status = poll_job(job_id, args.poll_interval, args.timeout)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "job.json").write_text(json.dumps(status, ensure_ascii=False, indent=2), encoding="utf-8")
    saved = write_images(status.get("last_response") or status, out_dir, "map_object")
    if response.get("object_id"):
        object_detail = request_json("GET", f"/objects/{response['object_id']}")
        (out_dir / "object.json").write_text(json.dumps(object_detail, ensure_ascii=False, indent=2), encoding="utf-8")
        saved.extend(download_image_urls(object_detail, out_dir, "object_url"))
    print(
        json.dumps(
            {
                "job_id": job_id,
                "object_id": response.get("object_id"),
                "metadata": str(out_dir),
                "saved": [str(path) for path in saved],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


def cmd_object(args: argparse.Namespace) -> None:
    view = args.view
    if args.directions == 8 and view == "sidescroller":
        view = "side"
    if args.directions == 1 and view in {"side", "low top-down", "high top-down"}:
        view = "sidescroller" if view == "side" else "top-down"
    payload: dict[str, Any] = {
        "description": args.prompt,
        "size": args.size,
        "view": view,
    }
    if args.reference_image:
        payload["reference_image"] = {"base64": read_image_base64(Path(args.reference_image))}
    if args.style_image:
        key = "style_image" if args.directions == 8 else "style_images"
        payload[key] = {"base64": read_image_base64(Path(args.style_image))} if args.directions == 8 else [
            {"base64": read_image_base64(Path(args.style_image))}
        ]
    endpoint = "/create-8-direction-object" if args.directions == 8 else "/create-1-direction-object"
    response = request_json("POST", endpoint, payload)
    object_id = response["object_id"]
    detail = poll_object(object_id, args.poll_interval, args.timeout)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "object.json").write_text(json.dumps(detail, ensure_ascii=False, indent=2), encoding="utf-8")
    saved = write_images(detail, out_dir, "object")
    saved.extend(download_image_urls(detail, out_dir, "object_url"))
    print(
        json.dumps(
            {
                "background_job_id": response.get("background_job_id"),
                "object_id": object_id,
                "metadata": str(out_dir / "object.json"),
                "saved": [str(path) for path in saved],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate game pixel assets through Pixellab v2 API")
    subparsers = parser.add_subparsers(required=True)

    balance = subparsers.add_parser("balance", help="Check Pixellab account balance")
    balance.set_defaults(func=cmd_balance)

    image = subparsers.add_parser("image", help="Generate one synchronous image")
    add_common_image_args(image)
    image.add_argument("--model", choices=["pixflux", "pixen"], default="pixflux")
    image.add_argument("--out", required=True)
    image.set_defaults(func=cmd_image)

    pro_image = subparsers.add_parser("pro-image", help="Generate async Pro image candidates")
    add_common_image_args(pro_image)
    pro_image.add_argument("--out-dir", required=True)
    pro_image.add_argument("--poll-interval", type=float, default=5)
    pro_image.add_argument("--timeout", type=float, default=300)
    pro_image.set_defaults(func=cmd_pro_image)

    animate = subparsers.add_parser("animate", help="Animate a first frame with text")
    animate.add_argument("--first-frame", required=True)
    animate.add_argument("--action", required=True)
    animate.add_argument("--frame-count", type=int, choices=[4, 6, 8, 10, 12, 14, 16], default=8)
    animate.add_argument("--seed", type=int)
    animate.add_argument("--no-background", action="store_true")
    animate.add_argument("--out-dir", required=True)
    animate.add_argument("--poll-interval", type=float, default=5)
    animate.add_argument("--timeout", type=float, default=300)
    animate.set_defaults(func=cmd_animate)

    animate_skeleton = subparsers.add_parser("animate-skeleton", help="Animate a character from Pixellab skeleton keypoints")
    animate_skeleton.add_argument("--reference-image", required=True)
    animate_skeleton.add_argument("--skeleton", required=True, help="Skeleton JSON file or directory of frame JSON files")
    animate_skeleton.add_argument("--width", type=int, default=128)
    animate_skeleton.add_argument("--height", type=int, default=128)
    animate_skeleton.add_argument("--view", choices=["side", "low top-down", "high top-down"])
    animate_skeleton.add_argument(
        "--direction",
        choices=[
            "north",
            "north-east",
            "east",
            "south-east",
            "south",
            "south-west",
            "west",
            "north-west",
        ],
    )
    animate_skeleton.add_argument("--seed", type=int)
    animate_skeleton.add_argument("--no-background", action="store_true")
    animate_skeleton.add_argument("--out-dir", required=True)
    animate_skeleton.set_defaults(func=cmd_animate_skeleton)

    skeleton = subparsers.add_parser("estimate-skeleton", help="Estimate skeleton keypoints for a character image")
    skeleton.add_argument("--image", required=True)
    skeleton.add_argument("--out", required=True)
    skeleton.set_defaults(func=cmd_estimate_skeleton)

    character = subparsers.add_parser("character-v3", help="Create a v3 character and poll the job")
    add_common_image_args(character)
    character.add_argument("--reference-image")
    character.add_argument("--template-id", default="mannequin")
    character.add_argument("--out-dir", required=True)
    character.add_argument("--poll-interval", type=float, default=5)
    character.add_argument("--timeout", type=float, default=360)
    character.set_defaults(func=cmd_character)

    map_object = subparsers.add_parser("map-object", help="Create a transparent map/item object")
    map_object.add_argument("--prompt", required=True)
    map_object.add_argument("--width", type=int, default=128)
    map_object.add_argument("--height", type=int, default=128)
    map_object.add_argument("--seed", type=int)
    map_object.add_argument("--view", choices=["side", "low top-down", "high top-down"], default="side")
    map_object.add_argument("--outline", choices=["single color outline", "selective outline", "lineless"])
    map_object.add_argument("--detail", choices=["low detail", "medium detail", "high detail"])
    map_object.add_argument(
        "--shading",
        choices=["flat shading", "basic shading", "medium shading", "detailed shading"],
    )
    map_object.add_argument("--out-dir", required=True)
    map_object.add_argument("--poll-interval", type=float, default=5)
    map_object.add_argument("--timeout", type=float, default=180)
    map_object.set_defaults(func=cmd_map_object)

    obj = subparsers.add_parser("object", help="Create a Pixellab object through the object pipeline")
    obj.add_argument("--prompt", required=True)
    obj.add_argument("--directions", type=int, choices=[1, 8], default=1)
    obj.add_argument("--size", type=int, default=64)
    obj.add_argument("--view", choices=["top-down", "sidescroller", "low top-down", "high top-down", "side"], default="sidescroller")
    obj.add_argument("--reference-image")
    obj.add_argument("--style-image")
    obj.add_argument("--out-dir", required=True)
    obj.add_argument("--poll-interval", type=float, default=5)
    obj.add_argument("--timeout", type=float, default=300)
    obj.set_defaults(func=cmd_object)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        args.func(args)
    except PixellabError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
