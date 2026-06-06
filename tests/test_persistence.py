from __future__ import annotations

from contextlib import closing
import tempfile
from pathlib import Path
import sqlite3
import unittest

from idle_forest import GameEngine
from idle_forest.content import generate_equipment
from idle_forest.persistence import SaveStore, SQLiteSaveStore
from idle_forest.talents import TALENT_CATALOG
from idle_forest.models import TalentTier


class PersistenceTests(unittest.TestCase):
    def test_save_store_restores_engine_progress_and_market_history(self) -> None:
        talents = TALENT_CATALOG[TalentTier.COMMON][:3]
        engine = GameEngine(
            seed=44,
            hero_name="Astra",
            hero_gender="female",
            starting_talents=talents,
            starter_gold=500,
        )
        engine.advance(3)
        engine.deepen_forest()
        loot = generate_equipment(level=4, rng=engine.rng)
        loot.owner_id = engine.hero.id
        engine.hero.inventory.append(loot)
        listing = engine.list_item(loot.id, price=77)
        engine.buy_listing(listing.id, buyer_id="player_2")

        with tempfile.TemporaryDirectory() as directory:
            store = SaveStore(Path(directory) / "savegame.json")
            store.save(
                profile={
                    "confirmed": {
                        "name": "Astra",
                        "gender": "female",
                        "talents": [talent.to_dict() for talent in talents],
                    },
                    "draft": None,
                },
                engine=engine,
            )

            loaded = store.load()

        self.assertIsNotNone(loaded)
        assert loaded is not None
        restored = loaded["engine"]
        self.assertEqual(restored.hero.name, "Astra")
        self.assertEqual(restored.hero.gender, "female")
        self.assertEqual(restored.hero.gold, engine.hero.gold)
        self.assertEqual(restored.forest_depth, 2)
        self.assertEqual(restored.tick, engine.tick)
        self.assertEqual(restored.hero.equipped.keys(), engine.hero.equipped.keys())
        self.assertEqual(
            [talent.id for talent in restored.hero.talents],
            [talent.id for talent in talents],
        )
        restored_listing = restored.market.get_listing(listing.id)
        self.assertFalse(restored_listing.active)
        self.assertEqual(restored_listing.buyer_id, "player_2")

    def test_sqlite_store_restores_engine_and_mirrors_trade_tables(self) -> None:
        talents = TALENT_CATALOG[TalentTier.COMMON][:3]
        engine = GameEngine(
            seed=45,
            hero_name="Broker",
            hero_gender="male",
            starting_talents=talents,
            starter_gold=300,
        )
        item = generate_equipment(level=5, rng=engine.rng)
        item.owner_id = engine.hero.id
        engine.hero.inventory.append(item)
        listing = engine.list_item(item.id, price=123)
        engine.buy_listing(listing.id, buyer_id="friend_hero")

        with tempfile.TemporaryDirectory() as directory:
            db_path = Path(directory) / "idle_forest.db"
            store = SQLiteSaveStore(db_path)
            store.save(profile=self._profile("Broker", "male", talents), engine=engine)

            loaded = store.load()

            with closing(sqlite3.connect(db_path)) as connection:
                character = connection.execute(
                    "SELECT name, gender, level, gold FROM characters WHERE hero_id = ?",
                    (engine.hero.id,),
                ).fetchone()
                market_row = connection.execute(
                    "SELECT seller_id, buyer_id, price, active FROM market_listings WHERE listing_id = ?",
                    (listing.id,),
                ).fetchone()
                item_row = connection.execute(
                    "SELECT owner_id, location FROM item_instances WHERE item_id = ?",
                    (item.id,),
                ).fetchone()
                ledger_count = connection.execute(
                    "SELECT COUNT(*) FROM gold_ledger WHERE hero_id = ?",
                    (engine.hero.id,),
                ).fetchone()[0]

        self.assertIsNotNone(loaded)
        assert loaded is not None
        restored = loaded["engine"]
        self.assertEqual(restored.hero.name, "Broker")
        self.assertEqual(restored.hero.gold, engine.hero.gold)
        self.assertEqual(character, ("Broker", "male", engine.hero.level, engine.hero.gold))
        self.assertEqual(market_row, (engine.hero.id, "friend_hero", 123, 0))
        self.assertEqual(item_row, ("friend_hero", "market"))
        self.assertGreaterEqual(ledger_count, 1)

    def test_sqlite_store_migrates_legacy_json_save(self) -> None:
        talents = TALENT_CATALOG[TalentTier.COMMON][:3]
        engine = GameEngine(
            seed=46,
            hero_name="LegacyHero",
            hero_gender="female",
            starting_talents=talents,
            starter_gold=444,
        )
        engine.advance(2)

        with tempfile.TemporaryDirectory() as directory:
            legacy_path = Path(directory) / "savegame.json"
            db_path = Path(directory) / "idle_forest.db"
            legacy = SaveStore(legacy_path)
            legacy.save(profile=self._profile("LegacyHero", "female", talents), engine=engine)

            store = SQLiteSaveStore(db_path, legacy_store=legacy)
            loaded = store.load()

            with closing(sqlite3.connect(db_path)) as connection:
                row = connection.execute(
                    "SELECT name, gender, gold FROM characters WHERE hero_id = ?",
                    (engine.hero.id,),
                ).fetchone()

        self.assertIsNotNone(loaded)
        assert loaded is not None
        self.assertEqual(loaded["engine"].hero.name, "LegacyHero")
        self.assertEqual(loaded["engine"].tick, engine.tick)
        self.assertEqual(row, ("LegacyHero", "female", engine.hero.gold))

    def test_sqlite_load_without_save_does_not_create_database(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            db_path = Path(directory) / "idle_forest.db"
            store = SQLiteSaveStore(db_path)

            loaded = store.load()

            self.assertIsNone(loaded)
            self.assertFalse(db_path.exists())

    def test_account_characters_are_limited_to_three_and_delete_releases_slot(self) -> None:
        talents = TALENT_CATALOG[TalentTier.COMMON][:3]
        with tempfile.TemporaryDirectory() as directory:
            db_path = Path(directory) / "idle_forest.db"
            store = SQLiteSaveStore(db_path)
            account = store.create_account("runner", "forest-pass")

            created = []
            for index in range(3):
                engine = GameEngine(
                    seed=60 + index,
                    hero_id=f"runner_{index}",
                    hero_name=f"Runner {index}",
                    hero_gender="female" if index == 1 else "male",
                    starting_talents=talents,
                )
                created.append(
                    store.create_character(
                        account_id=account["account_id"],
                        profile=self._profile(engine.hero.name, engine.hero.gender, talents),
                        engine=engine,
                    )
                )

            with self.assertRaises(ValueError):
                store.create_character(
                    account_id=account["account_id"],
                    profile=self._profile("Fourth", "male", talents),
                    engine=GameEngine(
                        seed=63,
                        hero_id="runner_3",
                        hero_name="Fourth",
                        starting_talents=talents,
                    ),
                )

            store.delete_character(account["account_id"], created[1]["character_id"])
            replacement = store.create_character(
                account_id=account["account_id"],
                profile=self._profile("Replacement", "female", talents),
                engine=GameEngine(
                    seed=64,
                    hero_id="runner_replacement",
                    hero_name="Replacement",
                    hero_gender="female",
                    starting_talents=talents,
                ),
            )
            characters = store.list_characters(account["account_id"])

        self.assertEqual([character["slot_index"] for character in created], [0, 1, 2])
        self.assertEqual(replacement["slot_index"], 1)
        self.assertEqual(len(characters), 3)
        self.assertNotIn(created[1]["character_id"], [character["character_id"] for character in characters])

    def test_account_login_and_character_load_use_session_token(self) -> None:
        talents = TALENT_CATALOG[TalentTier.COMMON][:3]
        with tempfile.TemporaryDirectory() as directory:
            db_path = Path(directory) / "idle_forest.db"
            store = SQLiteSaveStore(db_path)
            account = store.create_account("astra", "blade-pass")
            engine = GameEngine(
                seed=65,
                hero_id="astra_main",
                hero_name="Astra",
                hero_gender="female",
                starting_talents=talents,
                starter_gold=777,
            )
            character = store.create_character(
                account_id=account["account_id"],
                profile=self._profile("Astra", "female", talents),
                engine=engine,
            )

            session = store.login_account("astra", "blade-pass")
            store.set_active_character(session["session_token"], character["character_id"])
            resolved = store.resolve_session(session["session_token"])
            loaded = store.load_character(character["character_id"])

        self.assertEqual(resolved["account_id"], account["account_id"])
        self.assertEqual(resolved["active_character_id"], character["character_id"])
        self.assertEqual(loaded["engine"].hero.name, "Astra")
        self.assertEqual(loaded["engine"].hero.gold, 777)
        self.assertEqual(loaded["profile"]["confirmed"]["gender"], "female")

    def _profile(self, name: str, gender: str, talents: list) -> dict:
        return {
            "confirmed": {
                "name": name,
                "gender": gender,
                "talents": [talent.to_dict() for talent in talents],
            },
            "draft": None,
        }


if __name__ == "__main__":
    unittest.main()
