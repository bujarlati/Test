"""Tiny stdlib HTTP API for the idle forest prototype.

This is intentionally dependency-free. Replace it with FastAPI or Flask once
accounts, persistence, and production deployment are needed.
"""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import random
import uuid
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from idle_forest import GameEngine
from idle_forest.models import Talent
from idle_forest.persistence import MAX_CHARACTERS_PER_ACCOUNT, SaveStore, SQLiteSaveStore
from idle_forest.talents import TALENT_CATALOG, TALENT_TIER_CONFIG, roll_starting_talents


WEB_ROOT = Path(__file__).with_name("web")
DATABASE_PATH = Path(os.environ.get("IDLE_FOREST_DB_PATH", Path(__file__).with_name("data") / "idle_forest.db"))
LEGACY_SAVE_PATH = Path(os.environ.get("IDLE_FOREST_SAVE_PATH", Path(__file__).with_name("data") / "savegame.json"))
SAVE_STORE = SQLiteSaveStore(DATABASE_PATH, legacy_store=SaveStore(LEGACY_SAVE_PATH))


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

    def to_save(self) -> dict[str, Any]:
        return {
            "draft": self.draft,
            "confirmed": self.confirmed,
        }

    def load_save(self, data: dict[str, Any]) -> None:
        self.draft = data.get("draft")
        self.confirmed = data.get("confirmed")

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


class RuntimeState:
    def __init__(self, profile: ProfileSession, engine: GameEngine) -> None:
        self.profile = profile
        self.engine = engine


PROFILE = ProfileSession(seed=11)
CHARACTER_RUNTIMES: dict[str, RuntimeState] = {}
CREATION_DRAFTS: dict[str, ProfileSession] = {}


def _engine_from_profile(profile: ProfileSession, hero_id: str = "player_1") -> GameEngine:
    if profile.confirmed is None:
        return GameEngine(seed=11, hero_id=hero_id)
    talent_ids = [str(talent["id"]) for talent in profile.confirmed["talents"]]
    return GameEngine(
        seed=11,
        hero_id=hero_id,
        hero_name=str(profile.confirmed["name"]),
        hero_gender=str(profile.confirmed["gender"]),
        starting_talents=profile.talents_from_ids(talent_ids),
    )


def _load_engine() -> GameEngine:
    try:
        loaded = SAVE_STORE.load()
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        _safe_print(f"Could not load savegame: {exc}")
        return _engine_from_profile(PROFILE)
    if loaded is None:
        return _engine_from_profile(PROFILE)
    PROFILE.load_save(loaded["profile"])
    return loaded["engine"]


def _save_game() -> None:
    SAVE_STORE.save(PROFILE.to_save(), ENGINE)


ENGINE = _load_engine()


def _runtime_for_character(character_id: str) -> RuntimeState:
    if character_id not in CHARACTER_RUNTIMES:
        loaded = SAVE_STORE.load_character(character_id)
        profile = ProfileSession(seed=11)
        profile.load_save(loaded["profile"])
        CHARACTER_RUNTIMES[character_id] = RuntimeState(profile=profile, engine=loaded["engine"])
    return CHARACTER_RUNTIMES[character_id]


def _save_character_runtime(character_id: str, runtime: RuntimeState) -> None:
    SAVE_STORE.save_character(character_id, runtime.profile.to_save(), runtime.engine)


def _new_character_id() -> str:
    return f"hero_{uuid.uuid4().hex[:20]}"


def _account_payload(session: dict[str, Any]) -> dict[str, Any]:
    return {
        "authenticated": True,
        "account": {
            "account_id": session["account_id"],
            "username": session["username"],
        },
        "characters": SAVE_STORE.list_characters(session["account_id"]),
        "active_character_id": session.get("active_character_id"),
        "max_characters": MAX_CHARACTERS_PER_ACCOUNT,
    }


def _login_response(login_result: dict[str, Any]) -> dict[str, Any]:
    session = SAVE_STORE.resolve_session(login_result["session_token"])
    return _account_payload(session) | {"session_token": login_result["session_token"]}


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
        if path == "/account":
            token = self._session_token()
            if token is None:
                self._send_json({"authenticated": False, "max_characters": MAX_CHARACTERS_PER_ACCOUNT})
                return
            try:
                self._send_json(_account_payload(SAVE_STORE.resolve_session(token)))
            except ValueError:
                self._send_json({"authenticated": False, "max_characters": MAX_CHARACTERS_PER_ACCOUNT})
            return
        if path == "/snapshot":
            active = self._active_runtime_or_none()
            self._send_json(active[2].engine.snapshot() if active is not None else ENGINE.snapshot())
            return
        if path == "/profile":
            active = self._active_runtime_or_none()
            if active is not None:
                self._send_json(active[2].profile.to_dict())
                return
            self._send_json(PROFILE.to_dict())
            return
        if path == "/market":
            active = self._active_runtime_or_none()
            self._send_json(active[2].engine.market.to_dict() if active is not None else ENGINE.market.to_dict())
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
            if path == "/account/register":
                account = SAVE_STORE.create_account(
                    username=str(payload.get("username", "")),
                    password=str(payload.get("password", "")),
                )
                migrated = SAVE_STORE.migrate_local_character_to_account(account["account_id"])
                session = SAVE_STORE.login_account(
                    username=str(payload.get("username", "")),
                    password=str(payload.get("password", "")),
                )
                if migrated is not None:
                    session = SAVE_STORE.set_active_character(
                        session["session_token"],
                        migrated["character_id"],
                    )
                self._send_json(
                    _login_response(session)
                    | {
                        "migrated_character": migrated,
                    }
                )
                return
            if path == "/account/login":
                session = SAVE_STORE.login_account(
                    username=str(payload.get("username", "")),
                    password=str(payload.get("password", "")),
                )
                self._send_json(_login_response(session))
                return
            if path == "/account/logout":
                self._send_json({"ok": True})
                return
            if path == "/characters/select":
                session = SAVE_STORE.set_active_character(
                    self._require_session()["session_token"],
                    str(payload["character_id"]),
                )
                runtime = _runtime_for_character(str(payload["character_id"]))
                self._send_json(_account_payload(session) | {"snapshot": runtime.engine.snapshot()})
                return
            if path == "/characters/delete":
                session = self._require_session()
                character_id = str(payload["character_id"])
                SAVE_STORE.delete_character(session["account_id"], character_id)
                CHARACTER_RUNTIMES.pop(character_id, None)
                refreshed = SAVE_STORE.resolve_session(session["session_token"])
                self._send_json(_account_payload(refreshed))
                return
            if path == "/reset":
                active = self._active_runtime_or_none()
                if active is not None:
                    _, character_id, runtime = active
                    runtime.engine = _engine_from_profile(runtime.profile, hero_id=character_id)
                    snapshot = runtime.engine.snapshot()
                    _save_character_runtime(character_id, runtime)
                    self._send_json(snapshot)
                    return
                ENGINE = _engine_from_profile(PROFILE)
                snapshot = ENGINE.snapshot()
                _save_game()
                self._send_json(snapshot)
                return
            if path == "/profile/roll":
                session = self._session_or_none()
                if session is not None:
                    draft = CREATION_DRAFTS.setdefault(
                        session["session_token"],
                        ProfileSession(seed=11),
                    )
                    result = draft.roll(
                        name=str(payload.get("name", "")),
                        gender=str(payload.get("gender", "")),
                    )
                    self._send_json(result)
                    return
                result = PROFILE.roll(name=str(payload.get("name", "")), gender=str(payload.get("gender", "")))
                _save_game()
                self._send_json(result)
                return
            if path == "/profile/confirm":
                talent_ids = payload.get("talent_ids")
                if talent_ids is not None and not isinstance(talent_ids, list):
                    raise ValueError("talent_ids must be a list")
                session = self._session_or_none()
                if session is not None:
                    draft = CREATION_DRAFTS.get(session["session_token"], ProfileSession(seed=11))
                    draft.confirm(
                        name=str(payload.get("name", "")) if "name" in payload else None,
                        gender=str(payload.get("gender", "")) if "gender" in payload else None,
                        talent_ids=[str(talent_id) for talent_id in talent_ids] if talent_ids is not None else None,
                    )
                    character_id = _new_character_id()
                    engine = _engine_from_profile(draft, hero_id=character_id)
                    character = SAVE_STORE.create_character(session["account_id"], draft.to_save(), engine)
                    session = SAVE_STORE.set_active_character(session["session_token"], character_id)
                    runtime = RuntimeState(profile=draft, engine=engine)
                    CHARACTER_RUNTIMES[character_id] = runtime
                    CREATION_DRAFTS.pop(session["session_token"], None)
                    self._send_json(
                        _account_payload(session)
                        | {
                            "profile": draft.to_dict(),
                            "snapshot": engine.snapshot(),
                            "character": character,
                        }
                    )
                    return
                PROFILE.confirm(
                    name=str(payload.get("name", "")) if "name" in payload else None,
                    gender=str(payload.get("gender", "")) if "gender" in payload else None,
                    talent_ids=[str(talent_id) for talent_id in talent_ids] if talent_ids is not None else None,
                )
                ENGINE = _engine_from_profile(PROFILE)
                snapshot = ENGINE.snapshot()
                _save_game()
                self._send_json({"profile": PROFILE.to_dict(), "snapshot": snapshot})
                return
            if path == "/profile/clear":
                session = self._session_or_none()
                if session is not None:
                    CREATION_DRAFTS.pop(session["session_token"], None)
                    self._send_json(_account_payload(session))
                    return
                PROFILE.clear()
                ENGINE = _engine_from_profile(PROFILE)
                SAVE_STORE.delete()
                self._send_json({"profile": PROFILE.to_dict(), "snapshot": ENGINE.snapshot()})
                return
            if path == "/tick":
                active = self._active_runtime_or_none()
                if active is not None:
                    _, character_id, runtime = active
                    seconds = float(payload.get("seconds", 1))
                    snapshot = runtime.engine.advance(seconds)
                    _save_character_runtime(character_id, runtime)
                    self._send_json(snapshot)
                    return
                seconds = float(payload.get("seconds", 1))
                snapshot = ENGINE.advance(seconds)
                _save_game()
                self._send_json(snapshot)
                return
            if path == "/rift/enter":
                active = self._active_runtime_or_none()
                if active is not None:
                    _, character_id, runtime = active
                    floor = payload.get("floor")
                    rift = runtime.engine.enter_rift(int(floor) if floor is not None else None)
                    snapshot = runtime.engine.snapshot()
                    _save_character_runtime(character_id, runtime)
                    self._send_json({"rift": rift.to_dict(), "snapshot": snapshot})
                    return
                floor = payload.get("floor")
                rift = ENGINE.enter_rift(int(floor) if floor is not None else None)
                snapshot = ENGINE.snapshot()
                _save_game()
                self._send_json({"rift": rift.to_dict(), "snapshot": snapshot})
                return
            if path == "/rift/leave":
                active = self._active_runtime_or_none()
                if active is not None:
                    _, character_id, runtime = active
                    runtime.engine.leave_rift()
                    snapshot = runtime.engine.snapshot()
                    _save_character_runtime(character_id, runtime)
                    self._send_json(snapshot)
                    return
                ENGINE.leave_rift()
                snapshot = ENGINE.snapshot()
                _save_game()
                self._send_json(snapshot)
                return
            if path == "/forest/deepen":
                active = self._active_runtime_or_none()
                if active is not None:
                    _, character_id, runtime = active
                    snapshot = runtime.engine.deepen_forest()
                    _save_character_runtime(character_id, runtime)
                    self._send_json(snapshot)
                    return
                snapshot = ENGINE.deepen_forest()
                _save_game()
                self._send_json(snapshot)
                return
            if path == "/forest/retreat":
                active = self._active_runtime_or_none()
                if active is not None:
                    _, character_id, runtime = active
                    snapshot = runtime.engine.retreat_forest()
                    _save_character_runtime(character_id, runtime)
                    self._send_json(snapshot)
                    return
                snapshot = ENGINE.retreat_forest()
                _save_game()
                self._send_json(snapshot)
                return
            if path == "/equip-best":
                active = self._active_runtime_or_none()
                if active is not None:
                    _, character_id, runtime = active
                    equipped = runtime.engine.equip_best_items()
                    snapshot = runtime.engine.snapshot()
                    _save_character_runtime(character_id, runtime)
                    self._send_json(
                        {
                            "equipped": [item.to_dict() for item in equipped],
                            "snapshot": snapshot,
                        }
                    )
                    return
                equipped = ENGINE.equip_best_items()
                snapshot = ENGINE.snapshot()
                _save_game()
                self._send_json(
                    {
                        "equipped": [item.to_dict() for item in equipped],
                        "snapshot": snapshot,
                    }
                )
                return
            if path == "/equip-item":
                active = self._active_runtime_or_none()
                engine = active[2].engine if active is not None else ENGINE
                item = engine.equip_item(item_id=str(payload["item_id"]))
                snapshot = engine.snapshot()
                if active is not None:
                    _save_character_runtime(active[1], active[2])
                else:
                    _save_game()
                self._send_json({"item": item.to_dict(), "snapshot": snapshot})
                return
            if path == "/talent/evolve":
                active = self._active_runtime_or_none()
                engine = active[2].engine if active is not None else ENGINE
                result = engine.evolve_talent(talent_id=str(payload["talent_id"]))
                snapshot = engine.snapshot()
                if active is not None:
                    _save_character_runtime(active[1], active[2])
                else:
                    _save_game()
                self._send_json({"talent": result, "snapshot": snapshot})
                return
            if path == "/market/list":
                active = self._active_runtime_or_none()
                engine = active[2].engine if active is not None else ENGINE
                listing = engine.list_item(
                    item_id=str(payload["item_id"]),
                    price=int(payload["price"]),
                )
                snapshot = engine.snapshot()
                if active is not None:
                    _save_character_runtime(active[1], active[2])
                else:
                    _save_game()
                self._send_json({"listing": listing.to_dict(), "snapshot": snapshot})
                return
            if path == "/market/buy":
                active = self._active_runtime_or_none()
                engine = active[2].engine if active is not None else ENGINE
                item = engine.buy_listing(
                    listing_id=str(payload["listing_id"]),
                    buyer_id=str(payload.get("buyer_id", engine.hero.id)),
                )
                snapshot = engine.snapshot()
                if active is not None:
                    _save_character_runtime(active[1], active[2])
                else:
                    _save_game()
                self._send_json({"item": item.to_dict(), "snapshot": snapshot})
                return
        except PermissionError as exc:
            self._send_json({"error": str(exc)}, status=HTTPStatus.UNAUTHORIZED)
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

    def _session_token(self) -> str | None:
        token = str(self.headers.get("X-Session-Token", "")).strip()
        return token or None

    def _session_or_none(self) -> dict[str, Any] | None:
        token = self._session_token()
        if token is None:
            return None
        try:
            return SAVE_STORE.resolve_session(token)
        except ValueError:
            return None

    def _require_session(self) -> dict[str, Any]:
        token = self._session_token()
        if token is None:
            raise PermissionError("login required")
        try:
            return SAVE_STORE.resolve_session(token)
        except ValueError as exc:
            raise PermissionError(str(exc)) from exc

    def _active_runtime_or_none(self) -> tuple[dict[str, Any], str, RuntimeState] | None:
        session = self._session_or_none()
        if session is None:
            return None
        character_id = session.get("active_character_id")
        if not character_id:
            raise ValueError("select a character")
        return session, str(character_id), _runtime_for_character(str(character_id))

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
        self.send_header("Access-Control-Allow-Headers", "Content-Type, X-Session-Token")


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
