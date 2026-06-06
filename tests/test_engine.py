from __future__ import annotations

import importlib
import os
import sys
import tempfile
from pathlib import Path
import unittest

from idle_forest import GameEngine
from idle_forest.config import (
    HERO_REVIVE_SECONDS,
    MONSTER_APPROACH_DISTANCE,
    TREASURE_MIMIC_PITY_THRESHOLD,
)
from idle_forest.content import create_treasure_mimic, generate_equipment
from idle_forest.models import Equipment, EquipmentSlot, Monster, Rarity, TalentTier
from idle_forest.talents import TALENT_CATALOG


class GameEngineTests(unittest.TestCase):
    def test_new_hero_starts_with_equipped_wooden_sword(self) -> None:
        engine = GameEngine(seed=30)
        snapshot = engine.snapshot()

        weapon = snapshot["hero"]["equipped"].get("weapon")
        self.assertIsNotNone(weapon)
        assert weapon is not None
        self.assertEqual(weapon["name"], "Starter Wooden Sword")
        self.assertEqual(weapon["weapon_type"], "blade")
        self.assertFalse(weapon["tradable"])
        self.assertEqual(snapshot["scene"]["entities"][0]["weapon"]["id"], weapon["id"])

    def test_equipment_snapshot_includes_visual_appearance(self) -> None:
        engine = GameEngine(seed=33)
        snapshot = engine.snapshot()
        weapon = snapshot["hero"]["equipped"]["weapon"]
        hero_entity = snapshot["scene"]["entities"][0]

        self.assertIn("appearance", weapon)
        self.assertEqual(weapon["appearance"]["slot"], "weapon")
        self.assertEqual(weapon["appearance"]["model"], "wooden_blade")
        self.assertIn("palette", weapon["appearance"])
        self.assertIn("primary", weapon["appearance"]["palette"])
        self.assertIn("accent", weapon["appearance"]["palette"])
        self.assertIn("glow", weapon["appearance"]["palette"])
        self.assertEqual(
            hero_entity["equipped"]["weapon"]["appearance"]["model"],
            weapon["appearance"]["model"],
        )
        self.assertEqual(
            [talent["id"] for talent in hero_entity["talents"]],
            [talent["id"] for talent in snapshot["hero"]["talents"]],
        )
        self.assertEqual(hero_entity["talent_effects"], snapshot["hero"]["talent_effects"])

    def test_loot_event_exposes_item_name_and_appearance_for_scene_popups(self) -> None:
        engine = GameEngine(seed=34)
        item = Equipment(
            id="drop_yitian",
            name="Yitian Sword",
            slot=EquipmentSlot.WEAPON,
            rarity=Rarity.GOLD,
            level=8,
            attack=42,
            weapon_type="blade",
        )

        engine._add_loot_event(item)

        loot_event = [
            event
            for event in engine.snapshot()["events"]
            if event["data"].get("item_id") == "drop_yitian"
        ][-1]
        self.assertEqual(loot_event["data"]["item_name"], "Yitian Sword")
        self.assertEqual(loot_event["data"]["item_appearance"]["slot"], "weapon")
        self.assertEqual(loot_event["data"]["item_appearance"]["palette"]["glow"], "#ffca55")

    def test_hero_revives_in_place_and_keeps_current_monster(self) -> None:
        engine = GameEngine(seed=31)
        engine.hero.talents = []
        engine.hero.base_defense = 0
        engine.hero.hp = 5
        engine.hero.x = 120.0
        monster = Monster(
            id="test_brute",
            kind="test_brute",
            level=1,
            max_hp=80,
            hp=37,
            attack=20,
            defense=0,
            exp_reward=0,
            gold_reward=0,
            x=engine.hero.x + 20,
            y=engine.hero.y,
        )
        engine.active_monster = monster

        engine._monster_attack()
        defeated_snapshot = engine.snapshot()

        self.assertEqual(engine.hero.hp, 0)
        self.assertEqual(engine.hero.x, 120.0)
        self.assertIs(engine.active_monster, monster)
        self.assertEqual(engine.active_monster.hp, 37)
        self.assertTrue(defeated_snapshot["hero"]["reviving"])
        self.assertEqual(defeated_snapshot["scene"]["entities"][0]["state"], "reviving")

        engine.advance(HERO_REVIVE_SECONDS - 0.25)
        self.assertEqual(engine.hero.hp, 0)
        self.assertIs(engine.active_monster, monster)

        revived_snapshot = engine.advance(0.25)
        self.assertEqual(engine.hero.hp, engine.hero.max_hp)
        self.assertIs(engine.active_monster, monster)
        self.assertFalse(revived_snapshot["hero"]["reviving"])
        self.assertEqual(revived_snapshot["monster"]["id"], "test_brute")

    def test_snapshot_exposes_experience_progress_and_equipment_slots(self) -> None:
        engine = GameEngine(seed=32)
        snapshot = engine.snapshot()
        hero = snapshot["hero"]

        self.assertIn("exp_progress", hero)
        self.assertEqual(hero["exp_progress"], 0)
        self.assertIn("equipment_slots", hero)
        slots = {slot["slot"]: slot for slot in hero["equipment_slots"]}
        self.assertEqual(set(slots), {"weapon", "helmet", "armor", "boots", "ring"})
        self.assertIsNotNone(slots["weapon"]["item"])
        self.assertIsNone(slots["helmet"]["item"])

    def test_hero_progresses_and_snapshot_has_scene_entities(self) -> None:
        engine = GameEngine(seed=1)
        snapshot = engine.advance(10)

        self.assertGreater(snapshot["hero"]["position"]["x"], 0)
        self.assertEqual(snapshot["scene"]["biome"], "forest")
        self.assertGreaterEqual(len(snapshot["scene"]["entities"]), 1)
        self.assertGreater(len(snapshot["scene"]["decorations"]), 0)
        self.assertEqual(len(snapshot["hero"]["talents"]), 3)

    def test_move_speed_reaches_next_forest_encounter_faster(self) -> None:
        slow = GameEngine(seed=101)
        fast = GameEngine(seed=101)

        slow.hero.speed = 25.0
        fast.hero.speed = 75.0
        slow._next_encounter_x = 140.0
        fast._next_encounter_x = 140.0

        slow.advance(2.0)
        fast.advance(2.0)

        self.assertIsNone(slow.active_monster)
        self.assertIsNotNone(fast.active_monster)

    def test_combat_can_award_gold_or_loot(self) -> None:
        engine = GameEngine(seed=2)
        snapshot = engine.advance(90)

        kill_events = [event for event in snapshot["events"] if event["kind"] == "monster_kill"]
        self.assertGreater(len(kill_events), 0)
        self.assertGreaterEqual(snapshot["hero"]["gold"], 0)

    def test_monster_spawns_ahead_beyond_attack_range(self) -> None:
        engine = GameEngine(seed=21)

        engine._spawn_monster()

        self.assertIsNotNone(engine.active_monster)
        assert engine.active_monster is not None
        distance = engine.active_monster.x - engine.hero.x
        self.assertGreaterEqual(MONSTER_APPROACH_DISTANCE, 800.0)
        self.assertGreaterEqual(distance, 800.0)

    def test_deepen_forest_increases_difficulty_and_changes_scene(self) -> None:
        engine = GameEngine(seed=35)
        first = engine.snapshot()

        second = engine.deepen_forest()
        engine._spawn_monster()
        assert engine.active_monster is not None

        self.assertEqual(first["forest"]["depth"], 1)
        self.assertEqual(second["forest"]["depth"], 2)
        self.assertEqual(second["scene"]["biome"], "deep_forest")
        self.assertEqual(engine.active_monster.theme, "deep_forest")
        self.assertGreaterEqual(engine.active_monster.level, engine.hero.level + 3)
        self.assertIn("threat", engine.active_monster.to_dict())
        self.assertGreater(engine.active_monster.to_dict()["threat"], 1.0)

    def test_forest_recommended_power_scales_and_can_retreat(self) -> None:
        engine = GameEngine(seed=36)
        first = engine.snapshot()

        second = engine.deepen_forest()
        third = engine.deepen_forest()
        retreated = engine.retreat_forest()
        shallow = engine.retreat_forest()
        still_shallow = engine.retreat_forest()

        self.assertEqual(first["forest"]["depth"], 1)
        self.assertEqual(second["forest"]["depth"], 2)
        self.assertEqual(third["forest"]["depth"], 3)
        self.assertGreater(second["forest"]["recommended_power"], first["forest"]["recommended_power"])
        self.assertGreater(third["forest"]["recommended_power"], second["forest"]["recommended_power"])
        self.assertEqual(retreated["forest"]["depth"], 2)
        self.assertLess(retreated["forest"]["recommended_power"], third["forest"]["recommended_power"])
        self.assertEqual(shallow["forest"]["depth"], 1)
        self.assertEqual(still_shallow["forest"]["depth"], 1)
        self.assertEqual(still_shallow["scene"]["biome"], "forest")

    def test_rift_monster_spawns_offscreen_ahead_of_hero(self) -> None:
        engine = GameEngine(seed=27)
        engine.enter_rift()

        engine._spawn_rift_monster()

        self.assertIsNotNone(engine.active_monster)
        assert engine.active_monster is not None
        distance = engine.active_monster.x - engine.hero.x
        self.assertGreaterEqual(distance, 800.0)

    def test_hero_waits_to_attack_until_inside_weapon_range(self) -> None:
        engine = GameEngine(seed=22)
        engine._spawn_monster()
        assert engine.active_monster is not None
        engine.active_monster.max_hp = 500
        engine.active_monster.hp = 500
        engine.active_monster.x = engine.hero.x + 140
        engine._hero_attack_timer = 999

        engine._advance_combat(0.25)

        self.assertEqual(engine.active_monster.hp, 500)

    def test_attack_speed_controls_attack_interval(self) -> None:
        engine = GameEngine(seed=23)
        engine.hero.equipped.clear()
        engine.hero.base_attack_speed = 2.0
        engine._spawn_monster()
        assert engine.active_monster is not None
        engine.active_monster.max_hp = 500
        engine.active_monster.hp = 500
        engine.active_monster.x = engine.hero.x + 10

        engine._advance_combat(0.49)
        self.assertEqual(engine.active_monster.hp, 500)

        engine._advance_combat(0.02)
        assert engine.active_monster is not None
        self.assertLess(engine.active_monster.hp, 500)

    def test_hp_regen_controls_travel_healing(self) -> None:
        engine = GameEngine(seed=24)
        engine.hero.base_max_hp = 100
        engine.hero.hp = 40
        engine.hero.base_hp_regen = 8.0
        engine._next_encounter_x = 9999

        engine.advance(1)

        self.assertEqual(engine.hero.hp, 48)

    def test_hp_regen_ticks_while_approaching_monster(self) -> None:
        engine = GameEngine(seed=102)
        engine.hero.hp = 20
        engine.hero.base_hp_regen = 12.0
        engine.active_monster = Monster(
            id="far_monster",
            kind="forest_slime",
            level=1,
            max_hp=200,
            hp=200,
            attack=1,
            defense=0,
            exp_reward=0,
            gold_reward=0,
            x=engine.hero.x + 220,
            y=engine.hero.y,
        )

        engine.advance(1.0)

        self.assertGreater(engine.hero.hp, 20)
        self.assertIsNotNone(engine.active_monster)

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

    def test_engine_accepts_character_name_gender_and_talents(self) -> None:
        talents = TALENT_CATALOG[TalentTier.COMMON][:3]

        engine = GameEngine(
            seed=25,
            hero_name="Astra",
            hero_gender="female",
            starting_talents=talents,
        )
        snapshot = engine.snapshot()

        self.assertEqual(snapshot["hero"]["name"], "Astra")
        self.assertEqual(snapshot["hero"]["gender"], "female")
        self.assertEqual(snapshot["scene"]["entities"][0]["gender"], "female")
        self.assertEqual(
            [talent["id"] for talent in snapshot["hero"]["talents"]],
            [talent.id for talent in talents],
        )

    def test_profile_rolls_are_limited_to_three(self) -> None:
        old_db_path = os.environ.get("IDLE_FOREST_DB_PATH")
        old_save_path = os.environ.get("IDLE_FOREST_SAVE_PATH")
        try:
            with tempfile.TemporaryDirectory() as directory:
                os.environ["IDLE_FOREST_DB_PATH"] = str(Path(directory) / "idle_forest.db")
                os.environ["IDLE_FOREST_SAVE_PATH"] = str(Path(directory) / "savegame.json")
                sys.modules.pop("server", None)
                ProfileSession = importlib.import_module("server").ProfileSession

                session = ProfileSession(seed=26)
                first = session.roll(name="Astra", gender="female")
                second = session.roll(name="Astra", gender="female")
                third = session.roll(name="Astra", gender="female")
        finally:
            if old_db_path is None:
                os.environ.pop("IDLE_FOREST_DB_PATH", None)
            else:
                os.environ["IDLE_FOREST_DB_PATH"] = old_db_path
            if old_save_path is None:
                os.environ.pop("IDLE_FOREST_SAVE_PATH", None)
            else:
                os.environ["IDLE_FOREST_SAVE_PATH"] = old_save_path
            sys.modules.pop("server", None)

        self.assertEqual(first["rolls_remaining"], 2)
        self.assertEqual(second["rolls_remaining"], 1)
        self.assertEqual(third["rolls_remaining"], 0)
        self.assertEqual(len(third["talents"]), 3)
        with self.assertRaises(ValueError):
            session.roll(name="Astra", gender="female")


if __name__ == "__main__":
    unittest.main()
