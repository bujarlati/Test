"""Tiny stdlib HTTP API for the idle forest prototype.

This is intentionally dependency-free. Replace it with FastAPI or Flask once
accounts, persistence, and production deployment are needed.
"""

from __future__ import annotations

import argparse
import json
import mimetypes
import random
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from idle_forest import GameEngine
from idle_forest.models import Talent
from idle_forest.talents import TALENT_CATALOG, TALENT_TIER_CONFIG, roll_starting_talents


WEB_ROOT = Path(__file__).with_name("web")


def _safe_print(message: str) -> None:
    try:
        print(message)
    except (AttributeError, OSError):
        pass


def _talent_by_id() -> dict[str, Talent]:
    return {
        talent.id: talent
        for talents in TALENT_CATALOG.values()
        for talent in talents
    }


class ProfileSession:
    """In-memory profile draft for the local prototype."""

    def __init__(self, seed: int | None = None) -> None:
        self.rng = random.Random(seed)
        self.draft: dict[str, Any] | None = None
        self.confirmed: dict[str, Any] | None = None

    def roll(self, name: str, gender: str) -> dict[str, Any]:
        clean_name = self._clean_name(name)
        clean_gender = self._clean_gender(gender)
        if (
            self.draft is None
            or self.draft["name"] != clean_name
            or self.draft["gender"] != clean_gender
        ):
            self.draft = {
                "name": clean_name,
                "gender": clean_gender,
                "rolls_used": 0,
                "talents": [],
            }
        if int(self.draft["rolls_used"]) >= 3:
            raise ValueError("no talent rolls remaining")

        talents = roll_starting_talents(self.rng, 3)
        self.draft["rolls_used"] = int(self.draft["rolls_used"]) + 1
        self.draft["talents"] = [talent.to_dict() for talent in talents]
        return self._draft_response()

    def confirm(
        self,
        name: str | None = None,
        gender: str | None = None,
        talent_ids: list[str] | None = None,
    ) -> dict[str, Any]:
        if talent_ids is None:
            if self.draft is None or not self.draft.get("talents"):
                raise ValueError("roll talents before confirming")
            talent_ids = [str(talent["id"]) for talent in self.draft["talents"]]
        talents = self.talents_from_ids(talent_ids)
        if len(talents) != 3:
            raise ValueError("character requires exactly three talents")

        clean_name = self._clean_name(name or (self.draft or {}).get("name", ""))
        clean_gender = self._clean_gender(gender or (self.draft or {}).get("gender", "male"))
        self.confirmed = {
            "name": clean_name,
            "gender": clean_gender,
            "talents": [talent.to_dict() for talent in talents],
        }
        return self.confirmed

    def clear(self) -> None:
        self.draft = None
        self.confirmed = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "confirmed": self.confirmed is not None,
            "character": self.confirmed,
            "draft": self._draft_response() if self.draft is not None else None,
        }

    def talents_from_ids(self, talent_ids: list[str]) -> list[Talent]:
        lookup = _talent_by_id()
        talents: list[Talent] = []
        seen: set[str] = set()
        for talent_id in talent_ids:
            if talent_id in seen:
                raise ValueError("duplicate talent selected")
            seen.add(talent_id)
            try:
                talents.append(lookup[talent_id])
            except KeyError as exc:
                raise ValueError(f"unknown talent: {talent_id}") from exc
        return talents

    def _draft_response(self) -> dict[str, Any]:
        if self.draft is None:
            raise ValueError("no active draft")
        rolls_used = int(self.draft["rolls_used"])
        return {
            "name": self.draft["name"],
            "gender": self.draft["gender"],
            "rolls_used": rolls_used,
            "rolls_remaining": max(0, 3 - rolls_used),
            "talents": self.draft["talents"],
        }

    def _clean_name(self, name: str) -> str:
        clean = str(name).strip()
        if not clean:
            raise ValueError("character name is required")
        if len(clean) > 24:
            raise ValueError("character name is too long")
        return clean

    def _clean_gender(self, gender: str) -> str:
        clean = str(gender).strip().lower()
        if clean not in {"male", "female"}:
            raise ValueError("gender must be male or female")
        return clean


PROFILE = ProfileSession(seed=11)


def _engine_from_profile() -> GameEngine:
    if PROFILE.confirmed is None:
        return GameEngine(seed=11)
    talent_ids = [str(talent["id"]) for talent in PROFILE.confirmed["talents"]]
    return GameEngine(
        seed=11,
        hero_name=str(PROFILE.confirmed["name"]),
        hero_gender=str(PROFILE.confirmed["gender"]),
        starting_talents=PROFILE.talents_from_ids(talent_ids),
    )


ENGINE = _engine_from_profile()


class IdleForestHandler(BaseHTTPRequestHandler):
    server_version = "IdleForest/0.1"

    def do_GET(self) -> None:
        path = self._route_path()
        if path in {"", "/"}:
            self._send_static(WEB_ROOT / "index.html")
            return
        if path.startswith("/web/"):
            self._send_static(WEB_ROOT / path.removeprefix("/web/"))
            return
        if path == "/snapshot":
            self._send_json(ENGINE.snapshot())
            return
        if path == "/profile":
            self._send_json(PROFILE.to_dict())
            return
        if path == "/market":
            self._send_json(ENGINE.market.to_dict())
            return
        if path == "/talents":
            self._send_json(
                {
                    "tiers": [
                        {
                            "id": tier.value,
                            "label": TALENT_TIER_CONFIG[tier].label,
                            "count": len(talents),
                            "talents": [talent.to_dict() for talent in talents],
                        }
                        for tier, talents in TALENT_CATALOG.items()
                    ]
                }
            )
            return
        self._send_json({"error": "not found"}, status=HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:
        global ENGINE
        path = self._route_path()
        try:
            payload = self._read_json()
            if path == "/reset":
                ENGINE = _engine_from_profile()
                self._send_json(ENGINE.snapshot())
                return
            if path == "/profile/roll":
                self._send_json(PROFILE.roll(
                    name=str(payload.get("name", "")),
                    gender=str(payload.get("gender", "")),
                ))
                return
            if path == "/profile/confirm":
                talent_ids = payload.get("talent_ids")
                if talent_ids is not None and not isinstance(talent_ids, list):
                    raise ValueError("talent_ids must be a list")
                PROFILE.confirm(
                    name=str(payload.get("name", "")) if "name" in payload else None,
                    gender=str(payload.get("gender", "")) if "gender" in payload else None,
                    talent_ids=[str(talent_id) for talent_id in talent_ids] if talent_ids is not None else None,
                )
                ENGINE = _engine_from_profile()
                self._send_json({"profile": PROFILE.to_dict(), "snapshot": ENGINE.snapshot()})
                return
            if path == "/profile/clear":
                PROFILE.clear()
                ENGINE = _engine_from_profile()
                self._send_json({"profile": PROFILE.to_dict(), "snapshot": ENGINE.snapshot()})
                return
            if path == "/tick":
                seconds = float(payload.get("seconds", 1))
                self._send_json(ENGINE.advance(seconds))
                return
            if path == "/rift/enter":
                floor = payload.get("floor")
                rift = ENGINE.enter_rift(int(floor) if floor is not None else None)
                self._send_json({"rift": rift.to_dict(), "snapshot": ENGINE.snapshot()})
                return
            if path == "/rift/leave":
                ENGINE.leave_rift()
                self._send_json(ENGINE.snapshot())
                return
            if path == "/forest/deepen":
                self._send_json(ENGINE.deepen_forest())
                return
            if path == "/forest/retreat":
                self._send_json(ENGINE.retreat_forest())
                return
            if path == "/equip-best":
                equipped = ENGINE.equip_best_items()
                self._send_json(
                    {
                        "equipped": [item.to_dict() for item in equipped],
                        "snapshot": ENGINE.snapshot(),
                    }
                )
                return
            if path == "/equip-item":
                item = ENGINE.equip_item(item_id=str(payload["item_id"]))
                self._send_json({"item": item.to_dict(), "snapshot": ENGINE.snapshot()})
                return
            if path == "/talent/evolve":
                result = ENGINE.evolve_talent(talent_id=str(payload["talent_id"]))
                self._send_json({"talent": result, "snapshot": ENGINE.snapshot()})
                return
            if path == "/market/list":
                listing = ENGINE.list_item(
                    item_id=str(payload["item_id"]),
                    price=int(payload["price"]),
                )
                self._send_json({"listing": listing.to_dict(), "snapshot": ENGINE.snapshot()})
                return
            if path == "/market/buy":
                item = ENGINE.buy_listing(
                    listing_id=str(payload["listing_id"]),
                    buyer_id=str(payload.get("buyer_id", ENGINE.hero.id)),
                )
                self._send_json({"item": item.to_dict(), "snapshot": ENGINE.snapshot()})
                return
        except (KeyError, ValueError) as exc:
            self._send_json({"error": str(exc)}, status=HTTPStatus.BAD_REQUEST)
            return

        self._send_json({"error": "not found"}, status=HTTPStatus.NOT_FOUND)

    def do_OPTIONS(self) -> None:
        self.send_response(HTTPStatus.NO_CONTENT)
        self._send_cors_headers()
        self.end_headers()

    def log_message(self, format: str, *args: Any) -> None:
        return

    def _read_json(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0"))
        if length == 0:
            return {}
        raw = self.rfile.read(length).decode("utf-8")
        return json.loads(raw)

    def _route_path(self) -> str:
        return urlparse(self.path).path

    def _send_json(self, data: dict[str, Any], status: HTTPStatus = HTTPStatus.OK) -> None:
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self._send_cors_headers()
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_static(self, requested_path: Path) -> None:
        try:
            resolved_root = WEB_ROOT.resolve()
            resolved_path = requested_path.resolve()
        except FileNotFoundError:
            self._send_json({"error": "not found"}, status=HTTPStatus.NOT_FOUND)
            return

        if resolved_root not in resolved_path.parents and resolved_path != resolved_root:
            self._send_json({"error": "not found"}, status=HTTPStatus.NOT_FOUND)
            return
        if not resolved_path.is_file():
            self._send_json({"error": "not found"}, status=HTTPStatus.NOT_FOUND)
            return

        content_type = mimetypes.guess_type(resolved_path.name)[0] or "application/octet-stream"
        body = resolved_path.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self._send_cors_headers()
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_cors_headers(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Idle Forest HTTP demo.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    server = ThreadingHTTPServer((args.host, args.port), IdleForestHandler)
    _safe_print(f"Idle Forest running at http://{args.host}:{args.port}")
    _safe_print("Open / for the web prototype, or call GET /snapshot and POST /tick.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        _safe_print("\nStopping server.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
