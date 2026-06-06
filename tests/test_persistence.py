from __future__ import annotations

import tempfile
from pathlib import Path
import unittest

from idle_forest import GameEngine
from idle_forest.content import generate_equipment
from idle_forest.persistence import SaveStore
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


if __name__ == "__main__":
    unittest.main()
