"""Tiny stdlib HTTP API for the idle forest prototype.

This is intentionally dependency-free. Replace it with FastAPI or Flask once
accounts, persistence, and production deployment are needed.
"""

from __future__ import annotations

import argparse
import json
import mimetypes
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from idle_forest import GameEngine
from idle_forest.talents import TALENT_CATALOG, TALENT_TIER_CONFIG


ENGINE = GameEngine(seed=11)
WEB_ROOT = Path(__file__).with_name("web")


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
                ENGINE = GameEngine(seed=11)
                self._send_json(ENGINE.snapshot())
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
    print(f"Idle Forest running at http://{args.host}:{args.port}")
    print("Open / for the web prototype, or call GET /snapshot and POST /tick.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
