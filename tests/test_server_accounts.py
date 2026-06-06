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

    def _get(self, path: str, token: str | None = None) -> dict:
        return self._request("GET", path, None, token)

    def _post(self, path: str, body: dict, token: str | None = None) -> dict:
        return self._request("POST", path, body, token)

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

    def _request(self, method: str, path: str, body: dict | None, token: str | None) -> dict:
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
        if response.status >= 400:
            self.fail(f"{method} {path} failed with {response.status}: {data}")
        return data


if __name__ == "__main__":
    unittest.main()
