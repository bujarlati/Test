from __future__ import annotations

import http.client
import importlib
import json
import os
from http.server import ThreadingHTTPServer
from pathlib import Path
import sys
import tempfile
import threading
import unittest

from idle_forest import GameEngine
from idle_forest.content import generate_equipment
from idle_forest.models import TalentTier
from idle_forest.talents import TALENT_CATALOG


class ServerAccountTests(unittest.TestCase):
    def setUp(self) -> None:
        self._old_db_path = os.environ.get("IDLE_FOREST_DB_PATH")
        self._old_save_path = os.environ.get("IDLE_FOREST_SAVE_PATH")
        self._directory = tempfile.TemporaryDirectory()
        root = Path(self._directory.name)
        os.environ["IDLE_FOREST_DB_PATH"] = str(root / "idle_forest.db")
        os.environ["IDLE_FOREST_SAVE_PATH"] = str(root / "savegame.json")
        sys.modules.pop("server", None)
        self.server_module = importlib.import_module("server")
        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), self.server_module.IdleForestHandler)
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()
        self.port = self.httpd.server_address[1]

    def tearDown(self) -> None:
        self.httpd.shutdown()
        self.httpd.server_close()
        self.thread.join(timeout=2)
        self._directory.cleanup()
        if self._old_db_path is None:
            os.environ.pop("IDLE_FOREST_DB_PATH", None)
        else:
            os.environ["IDLE_FOREST_DB_PATH"] = self._old_db_path
        if self._old_save_path is None:
            os.environ.pop("IDLE_FOREST_SAVE_PATH", None)
        else:
            os.environ["IDLE_FOREST_SAVE_PATH"] = self._old_save_path
        sys.modules.pop("server", None)

    def test_account_can_create_select_and_delete_character(self) -> None:
        registered = self._post("/account/register", {"username": "runner", "password": "forest-pass"})
        token = registered["session_token"]

        rolled = self._post(
            "/profile/roll",
            {"name": "Astra", "gender": "female"},
            token=token,
        )
        confirmed = self._post(
            "/profile/confirm",
            {
                "name": "Astra",
                "gender": "female",
                "talent_ids": [talent["id"] for talent in rolled["talents"]],
            },
            token=token,
        )
        account = self._get("/account", token=token)
        character_id = confirmed["character"]["character_id"]
        selected = self._post("/characters/select", {"character_id": character_id}, token=token)
        deleted = self._post("/characters/delete", {"character_id": character_id}, token=token)

        self.assertEqual(confirmed["snapshot"]["hero"]["name"], "Astra")
        self.assertEqual(confirmed["snapshot"]["hero"]["gender"], "female")
        self.assertEqual(len(account["characters"]), 1)
        self.assertEqual(account["active_character_id"], character_id)
        self.assertEqual(selected["active_character_id"], character_id)
        self.assertEqual(deleted["characters"], [])
        self.assertIsNone(deleted["active_character_id"])

    def test_account_can_create_multiple_characters_without_save_id_collisions(self) -> None:
        registered = self._post("/account/register", {"username": "party", "password": "forest-pass"})
        token = registered["session_token"]

        first = self._create_character(token, "First", "male")
        second = self._create_character(token, "Second", "female")
        account = self._get("/account", token=token)

        self.assertNotEqual(first["character"]["character_id"], second["character"]["character_id"])
        self.assertEqual(len(account["characters"]), 2)
        self.assertEqual([character["slot_index"] for character in account["characters"]], [0, 1])

    def test_first_talent_rolls_are_not_reused_between_accounts(self) -> None:
        first = self._post("/account/register", {"username": "storm", "password": "forest-pass"})
        second = self._post("/account/register", {"username": "ember", "password": "forest-pass"})

        first_roll = self._post(
            "/profile/roll",
            {"name": "Astra", "gender": "female"},
            token=first["session_token"],
        )
        second_roll = self._post(
            "/profile/roll",
            {"name": "Borin", "gender": "male"},
            token=second["session_token"],
        )

        self.assertNotEqual(
            [talent["id"] for talent in first_roll["talents"]],
            [talent["id"] for talent in second_roll["talents"]],
        )

    def test_market_listing_is_visible_and_buyable_by_another_account(self) -> None:
        seller = self._post("/account/register", {"username": "seller", "password": "forest-pass"})
        buyer = self._post("/account/register", {"username": "buyer", "password": "forest-pass"})
        seller_character = self._create_character(seller["session_token"], "Seller", "male")
        buyer_character = self._create_character(buyer["session_token"], "Buyer", "female")
        seller_id = seller_character["character"]["character_id"]

        runtime = self.server_module.CHARACTER_RUNTIMES[seller_id]
        item = generate_equipment(level=3, rng=runtime.engine.rng)
        item.owner_id = seller_id
        runtime.engine.hero.inventory.append(item)

        listed = self._post(
            "/market/list",
            {"item_id": item.id, "price": 25},
            token=seller["session_token"],
        )
        buyer_before = self._get("/snapshot", token=buyer["session_token"])
        bought = self._post(
            "/market/buy",
            {"listing_id": listed["listing"]["id"]},
            token=buyer["session_token"],
        )
        buyer_after = bought["snapshot"]
        seller_after = self._get("/snapshot", token=seller["session_token"])

        self.assertEqual(buyer_character["character"]["character_id"], buyer_after["hero"]["id"])
        self.assertIn(
            listed["listing"]["id"],
            [listing["id"] for listing in buyer_before["market"]["active"]],
        )
        self.assertIn(item.id, [inventory_item["id"] for inventory_item in buyer_after["hero"]["inventory"]])
        self.assertNotIn(
            listed["listing"]["id"],
            [listing["id"] for listing in buyer_after["market"]["active"]],
        )
        self.assertEqual(seller_after["hero"]["gold"], seller_character["snapshot"]["hero"]["gold"] + 25)

    def test_market_listing_can_be_canceled_by_seller(self) -> None:
        seller = self._post("/account/register", {"username": "cancel", "password": "forest-pass"})
        seller_character = self._create_character(seller["session_token"], "Seller", "male")
        seller_id = seller_character["character"]["character_id"]

        runtime = self.server_module.CHARACTER_RUNTIMES[seller_id]
        item = generate_equipment(level=4, rng=runtime.engine.rng)
        item.owner_id = seller_id
        runtime.engine.hero.inventory.append(item)

        listed = self._post(
            "/market/list",
            {"item_id": item.id, "price": 31},
            token=seller["session_token"],
        )
        canceled = self._post(
            "/market/cancel",
            {"listing_id": listed["listing"]["id"]},
            token=seller["session_token"],
        )
        snapshot = canceled["snapshot"]

        self.assertEqual(canceled["item"]["id"], item.id)
        self.assertIn(item.id, [inventory_item["id"] for inventory_item in snapshot["hero"]["inventory"]])
        self.assertNotIn(
            listed["listing"]["id"],
            [listing["id"] for listing in snapshot["market"]["active"]],
        )

    def test_market_listing_cannot_be_canceled_by_other_account(self) -> None:
        seller = self._post("/account/register", {"username": "seller2", "password": "forest-pass"})
        buyer = self._post("/account/register", {"username": "buyer2", "password": "forest-pass"})
        seller_character = self._create_character(seller["session_token"], "Seller", "male")
        self._create_character(buyer["session_token"], "Buyer", "female")
        seller_id = seller_character["character"]["character_id"]

        runtime = self.server_module.CHARACTER_RUNTIMES[seller_id]
        item = generate_equipment(level=4, rng=runtime.engine.rng)
        item.owner_id = seller_id
        runtime.engine.hero.inventory.append(item)

        listed = self._post(
            "/market/list",
            {"item_id": item.id, "price": 31},
            token=seller["session_token"],
        )
        error = self._post_error(
            "/market/cancel",
            {"listing_id": listed["listing"]["id"]},
            token=buyer["session_token"],
        )
        seller_after = self._get("/snapshot", token=seller["session_token"])

        self.assertEqual(error["status"], 401)
        self.assertIn("seller", error["body"]["error"])
        self.assertIn(
            listed["listing"]["id"],
            [listing["id"] for listing in seller_after["market"]["active"]],
        )

    def test_register_migrates_existing_local_save_into_first_character(self) -> None:
        talents = TALENT_CATALOG[TalentTier.COMMON][:3]
        engine = GameEngine(
            seed=70,
            hero_name="Legacy",
            hero_gender="female",
            starting_talents=talents,
            starter_gold=555,
        )
        self.server_module.SAVE_STORE.save(
            profile={
                "confirmed": {
                    "name": "Legacy",
                    "gender": "female",
                    "talents": [talent.to_dict() for talent in talents],
                },
                "draft": None,
            },
            engine=engine,
        )

        registered = self._post("/account/register", {"username": "legacy", "password": "forest-pass"})
        snapshot = self._get("/snapshot", token=registered["session_token"])

        self.assertEqual(len(registered["characters"]), 1)
        self.assertEqual(registered["active_character_id"], registered["characters"][0]["character_id"])
        self.assertEqual(snapshot["hero"]["name"], "Legacy")
        self.assertEqual(snapshot["hero"]["gold"], 555)

    def test_json_response_ignores_client_disconnect_during_write(self) -> None:
        handler = object.__new__(self.server_module.IdleForestHandler)
        calls: list[tuple] = []

        class AbortedWriter:
            def write(self, body: bytes) -> None:
                raise ConnectionAbortedError("client closed")

        handler.wfile = AbortedWriter()
        handler.send_response = lambda status: calls.append(("response", status))
        handler.send_header = lambda name, value: calls.append(("header", name, value))
        handler.end_headers = lambda: calls.append(("end",))
        handler._send_cors_headers = lambda: calls.append(("cors",))

        handler._send_json({"ok": True})

        self.assertIn(("response", self.server_module.HTTPStatus.OK), calls)

    def test_tick_endpoint_throttles_character_saves_between_autosave_windows(self) -> None:
        registered = self._post("/account/register", {"username": "autosave", "password": "forest-pass"})
        token = registered["session_token"]
        self._create_character(token, "Saver", "female")
        save_calls: list[float] = []
        original_save = self.server_module._save_character_runtime

        def spy_save(character_id: str, runtime) -> None:
            save_calls.append(runtime.engine.time_seconds)
            original_save(character_id, runtime)

        self.server_module._save_character_runtime = spy_save
        try:
            for _ in range(3):
                self._post("/tick", {"seconds": 0.25}, token=token)
        finally:
            self.server_module._save_character_runtime = original_save

        self.assertEqual(save_calls, [])

    def test_auto_rift_endpoint_toggles_active_character_rift_loop(self) -> None:
        registered = self._post("/account/register", {"username": "autorift", "password": "forest-pass"})
        token = registered["session_token"]
        self._create_character(token, "Looper", "female")

        enabled = self._post("/rift/auto", {"enabled": True}, token=token)

        self.assertTrue(enabled["snapshot"]["rift"]["auto"])
        self.assertTrue(enabled["snapshot"]["rift"]["active"])
        self.assertEqual(enabled["snapshot"]["mode"], "rift")

        disabled = self._post("/rift/auto", {"enabled": False}, token=token)

        self.assertFalse(disabled["snapshot"]["rift"]["auto"])

    def _get(self, path: str, token: str | None = None) -> dict:
        return self._request("GET", path, None, token)

    def _post(self, path: str, body: dict, token: str | None = None) -> dict:
        return self._request("POST", path, body, token)

    def _post_error(self, path: str, body: dict, token: str | None = None) -> dict:
        return self._request("POST", path, body, token, allow_error=True)

    def _create_character(self, token: str, name: str, gender: str) -> dict:
        rolled = self._post("/profile/roll", {"name": name, "gender": gender}, token=token)
        return self._post(
            "/profile/confirm",
            {
                "name": name,
                "gender": gender,
                "talent_ids": [talent["id"] for talent in rolled["talents"]],
            },
            token=token,
        )

    def _request(
        self,
        method: str,
        path: str,
        body: dict | None,
        token: str | None,
        allow_error: bool = False,
    ) -> dict:
        payload = json.dumps(body).encode("utf-8") if body is not None else None
        headers = {"Content-Type": "application/json"}
        if token is not None:
            headers["X-Session-Token"] = token
        connection = http.client.HTTPConnection("127.0.0.1", self.port, timeout=5)
        try:
            connection.request(method, path, body=payload, headers=headers)
            response = connection.getresponse()
            data = json.loads(response.read().decode("utf-8"))
        finally:
            connection.close()
        if allow_error:
            return {"status": response.status, "body": data}
        if response.status >= 400:
            self.fail(f"{method} {path} failed with {response.status}: {data}")
        return data


if __name__ == "__main__":
    unittest.main()
