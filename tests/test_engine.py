from __future__ import annotations

import unittest

from idle_forest import GameEngine
from idle_forest.config import TREASURE_MIMIC_PITY_THRESHOLD
from idle_forest.content import create_treasure_mimic, generate_equipment
from idle_forest.models import Equipment, EquipmentSlot, Rarity, TalentTier
from idle_forest.talents import TALENT_CATALOG


class GameEngineTests(unittest.TestCase):
    def test_hero_progresses_and_snapshot_has_scene_entities(self) -> None:
        engine = GameEngine(seed=1)
        snapshot = engine.advance(10)

        self.assertGreater(snapshot["hero"]["position"]["x"], 0)
        self.assertEqual(snapshot["scene"]["biome"], "forest")
        self.assertGreaterEqual(len(snapshot["scene"]["entities"]), 1)
        self.assertGreater(len(snapshot["scene"]["decorations"]), 0)
        self.assertEqual(len(snapshot["hero"]["talents"]), 3)

    def test_combat_can_award_gold_or_loot(self) -> None:
        engine = GameEngine(seed=2)
        snapshot = engine.advance(90)

        kill_events = [event for event in snapshot["events"] if event["kind"] == "monster_kill"]
        self.assertGreater(len(kill_events), 0)
        self.assertGreaterEqual(snapshot["hero"]["gold"], 0)

    def test_equip_best_uses_highest_score_for_slot(self) -> None:
        engine = GameEngine(seed=3)
        weak = generate_equipment(level=1, rng=engine.rng)
        strong = generate_equipment(level=8, rng=engine.rng)
        strong.slot = weak.slot
        strong.attack = weak.attack + 20
        strong.defense = weak.defense + 20
        strong.max_hp = weak.max_hp + 20
        engine.hero.inventory.extend([weak, strong])

        equipped = engine.equip_best_items()

        self.assertIn(strong, equipped)
        self.assertEqual(engine.hero.equipped[strong.slot].id, strong.id)

    def test_market_listing_removes_item_from_inventory_and_sells(self) -> None:
        engine = GameEngine(seed=4)
        start_gold = engine.hero.gold
        active_before = len(engine.market.active_listings())
        item = generate_equipment(level=2, rng=engine.rng)
        item.owner_id = engine.hero.id
        engine.hero.inventory.append(item)

        listing = engine.list_item(item.id, price=50)
        sold_item = engine.buy_listing(listing.id, buyer_id="player_2")

        self.assertEqual(sold_item.owner_id, "player_2")
        self.assertEqual(len(engine.hero.inventory), 0)
        self.assertEqual(engine.hero.gold, start_gold + 50)
        self.assertEqual(len(engine.market.active_listings()), active_before)

    def test_market_purchase_by_hero_costs_gold_and_adds_item(self) -> None:
        engine = GameEngine(seed=5, starter_gold=300)
        listing = next(
            listing
            for listing in engine.market.active_listings()
            if listing.seller_id != engine.hero.id
        )
        start_gold = engine.hero.gold

        bought_item = engine.buy_listing(listing.id, buyer_id=engine.hero.id)

        self.assertEqual(engine.hero.gold, start_gold - listing.price)
        self.assertEqual(bought_item.owner_id, engine.hero.id)
        self.assertIn(bought_item.id, [item.id for item in engine.hero.inventory])
        self.assertNotIn(listing.id, [item.id for item in engine.market.active_listings()])

    def test_market_purchase_fails_without_enough_gold(self) -> None:
        engine = GameEngine(seed=6, starter_gold=0)
        listing = next(
            listing
            for listing in engine.market.active_listings()
            if listing.seller_id != engine.hero.id
        )

        with self.assertRaises(ValueError):
            engine.buy_listing(listing.id, buyer_id=engine.hero.id)

    def test_enter_rift_changes_mode_and_randomizes_theme(self) -> None:
        engine = GameEngine(seed=7)

        rift = engine.enter_rift()
        snapshot = engine.snapshot()

        self.assertEqual(engine.mode, "rift")
        self.assertTrue(snapshot["rift"]["active"])
        self.assertEqual(snapshot["rift"]["floor"], 1)
        self.assertIn(rift.theme, snapshot["rift"]["available_themes"])
        self.assertEqual(snapshot["scene"]["biome"], rift.theme)
        self.assertGreater(snapshot["rift"]["minions_required"], 0)

    def test_rift_completion_unlocks_next_floor(self) -> None:
        engine = GameEngine(seed=8)
        weapon = Equipment(
            id="test_rift_weapon",
            name="Test Rift Axe",
            slot=EquipmentSlot.WEAPON,
            rarity=Rarity.RED,
            level=10,
            attack=60,
            owner_id=engine.hero.id,
        )
        armor = Equipment(
            id="test_rift_armor",
            name="Test Rift Guard",
            slot=EquipmentSlot.ARMOR,
            rarity=Rarity.RED,
            level=10,
            defense=30,
            max_hp=160,
            owner_id=engine.hero.id,
        )
        engine.hero.inventory.extend([weapon, armor])
        engine.equip_item(weapon.id)
        engine.equip_item(armor.id)

        engine.enter_rift()
        for _ in range(240):
            snapshot = engine.advance(1)
            if snapshot["mode"] == "forest":
                break

        self.assertEqual(engine.mode, "forest")
        self.assertEqual(engine.unlocked_rift_floor, 2)
        self.assertTrue(
            any(event["kind"] == "rift_complete" for event in engine.snapshot()["events"])
        )

    def test_treasure_mimic_drops_special_set_item(self) -> None:
        engine = GameEngine(seed=9)
        monster = create_treasure_mimic(level=1, x=engine.hero.x + 24, y=engine.hero.y, rng=engine.rng)
        engine.active_monster = monster

        engine._kill_monster(monster)

        special_items = [item for item in engine.hero.inventory if item.special]
        self.assertEqual(len(special_items), 1)
        self.assertIsNotNone(special_items[0].set_id)
        self.assertEqual(engine.treasure_mimics_defeated, 1)
        self.assertEqual(engine.snapshot()["treasure"]["mimics_defeated_since_red"], 1)

    def test_treasure_mimic_pity_grants_red_special_item_and_resets(self) -> None:
        engine = GameEngine(seed=10)

        for _ in range(TREASURE_MIMIC_PITY_THRESHOLD):
            monster = create_treasure_mimic(
                level=1,
                x=engine.hero.x + 24,
                y=engine.hero.y,
                rng=engine.rng,
            )
            engine.active_monster = monster
            engine._kill_monster(monster)

        red_specials = [
            item for item in engine.hero.inventory if item.special and item.rarity == Rarity.RED
        ]
        self.assertGreaterEqual(len(red_specials), 1)
        self.assertEqual(engine.treasure_mimics_defeated, 0)
        self.assertTrue(
            any(event["kind"] == "treasure_pity" for event in engine.snapshot()["events"])
        )

    def test_special_set_bonus_applies_when_two_pieces_equipped(self) -> None:
        engine = GameEngine(seed=11)
        engine.hero.talents = []
        first = Equipment(
            id="test_special_weapon",
            name="Test Hoard Fang",
            slot=EquipmentSlot.WEAPON,
            rarity=Rarity.PURPLE,
            level=3,
            attack=10,
            owner_id=engine.hero.id,
            special=True,
            set_id="test_set",
            set_name="Test Set",
            set_piece="Fang",
            set_bonus={"pieces_required": 2, "attack": 7, "defense": 4, "max_hp": 30},
        )
        second = Equipment(
            id="test_special_armor",
            name="Test Hoard Shell",
            slot=EquipmentSlot.ARMOR,
            rarity=Rarity.PURPLE,
            level=3,
            defense=8,
            max_hp=20,
            owner_id=engine.hero.id,
            special=True,
            set_id="test_set",
            set_name="Test Set",
            set_piece="Shell",
            set_bonus={"pieces_required": 2, "attack": 7, "defense": 4, "max_hp": 30},
        )
        engine.hero.inventory.extend([first, second])

        engine.equip_item(first.id)
        engine.equip_item(second.id)

        self.assertEqual(engine.hero.attack_power, engine.hero.base_attack + 10 + 7)
        self.assertEqual(engine.hero.defense_power, engine.hero.base_defense + 8 + 4)
        self.assertEqual(engine.hero.max_hp, engine.hero.base_max_hp + 20 + 30)
        self.assertEqual(len(engine.hero.to_dict()["set_bonuses"]), 1)

    def test_talent_catalog_has_150_per_tier(self) -> None:
        for tier in TalentTier:
            self.assertEqual(len(TALENT_CATALOG[tier]), 150)
        self.assertEqual(sum(len(talents) for talents in TALENT_CATALOG.values()), 900)

    def test_starting_talents_are_three_unique_rolls(self) -> None:
        engine = GameEngine(seed=12)
        talent_ids = [talent.id for talent in engine.hero.talents]

        self.assertEqual(len(talent_ids), 3)
        self.assertEqual(len(set(talent_ids)), 3)
        self.assertEqual(engine.snapshot()["talent"]["total_catalog_count"], 900)

    def test_evolve_talent_consumes_scroll_and_rolls_next_tier(self) -> None:
        engine = GameEngine(seed=13)
        engine.hero.talent_scrolls = 1
        engine.hero.talents[0] = TALENT_CATALOG[TalentTier.COMMON][0]

        result = engine.evolve_talent(engine.hero.talents[0].id)

        self.assertEqual(engine.hero.talent_scrolls, 0)
        self.assertEqual(result["old"]["tier"], TalentTier.COMMON.value)
        self.assertEqual(result["new"]["tier"], TalentTier.UNCOMMON.value)
        self.assertEqual(engine.hero.talents[0].tier, TalentTier.UNCOMMON)

    def test_mythic_talent_cannot_evolve(self) -> None:
        engine = GameEngine(seed=14)
        engine.hero.talent_scrolls = 1
        engine.hero.talents[0] = TALENT_CATALOG[TalentTier.MYTHIC][0]

        with self.assertRaises(ValueError):
            engine.evolve_talent(engine.hero.talents[0].id)


if __name__ == "__main__":
    unittest.main()
