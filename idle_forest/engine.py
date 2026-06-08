"""Idle world loop and game actions."""

from __future__ import annotations

import random
from collections import deque
from typing import Any

from .config import (
    ENCOUNTER_MAX_DISTANCE,
    ENCOUNTER_MIN_DISTANCE,
    HERO_DEATH_GOLD_LOSS_MAX_PCT,
    HERO_DEATH_GOLD_LOSS_MIN_PCT,
    HERO_ATTACK_RANGE,
    HERO_ATTACK_SPEED,
    HERO_GROUND_Y,
    HERO_HP_REGEN,
    HERO_REVIVE_SECONDS,
    HERO_START_X,
    HERO_WALK_SPEED,
    MONSTER_APPROACH_DISTANCE,
    MONSTER_ATTACK_INTERVAL,
    RIFT_BOSS_DROP_BONUS,
    RIFT_DROP_BONUS_PER_FLOOR,
    RIFT_MINION_DROP_BONUS,
    RIFT_MINIONS_BASE,
    RIFT_MINIONS_MAX,
    SCENE_CHUNK_WIDTH,
    TALENT_SCROLL_DROP_CHANCE,
    TREASURE_MIMIC_CHANCE,
    TREASURE_MIMIC_PITY_THRESHOLD,
)
from .content import (
    RIFT_THEMES,
    SYSTEM_SHOP_DONATION_COST,
    SYSTEM_SHOP_DONATION_SKU,
    SYSTEM_SHOP_RAINBOW_COSTS,
    create_decoration,
    create_monster,
    create_rift_decoration,
    create_rift_monster,
    create_starter_weapon,
    create_treasure_mimic,
    generate_equipment,
    generate_special_set_equipment,
    generate_system_shop_equipment,
    maybe_drop_equipment,
    system_shop_catalog,
)
from .market import Market, MarketListing
from .models import Equipment, EquipmentSlot, Event, Hero, Monster, Rarity, RiftRun, Talent, TalentTier
from .talents import (
    TALENT_CATALOG,
    TALENT_TIER_CONFIG,
    evolve_talent_roll,
    roll_starting_talents,
)


class GameEngine:
    """A small deterministic-ish idle game engine.

    The engine does not know about a renderer. It exposes a JSON-friendly
    snapshot with enough scene information for a 2D client to draw.
    """

    def __init__(
        self,
        seed: int | None = None,
        hero_id: str = "player_1",
        hero_name: str = "Forest Runner",
        hero_gender: str = "male",
        starting_talents: list[Talent] | None = None,
        starter_gold: int = 80,
    ) -> None:
        self.rng = random.Random(seed)
        self.tick = 0
        self.time_seconds = 0.0
        self.hero = Hero(
            id=hero_id,
            name=hero_name,
            gender=hero_gender,
            x=HERO_START_X,
            y=HERO_GROUND_Y,
            speed=HERO_WALK_SPEED,
            base_attack_speed=HERO_ATTACK_SPEED,
            base_attack_range=HERO_ATTACK_RANGE,
            base_hp_regen=HERO_HP_REGEN,
            gold=starter_gold,
        )
        self.hero.talents = list(starting_talents) if starting_talents is not None else roll_starting_talents(self.rng, 3)
        self.hero.equipped[EquipmentSlot.WEAPON] = create_starter_weapon(self.hero.id)
        self.active_monster: Monster | None = None
        self.mode = "forest"
        self.forest_depth = 1
        self.unlocked_rift_floor = 1
        self.active_rift: RiftRun | None = None
        self.treasure_mimics_defeated = 0
        self.market = Market()
        self.events: deque[Event] = deque(maxlen=80)
        self.decorations: list[dict[str, object]] = []
        self.rift_decorations: list[dict[str, object]] = []
        self._hero_attack_timer = 0.0
        self._monster_attack_timer = 0.0
        self._hero_heal_bank = 0.0
        self._revive_remaining = 0.0
        self._next_encounter_x = self._roll_next_encounter_x(self.hero.x)
        self._next_decoration_index = 0
        self._next_rift_decoration_index = 0
        self._ensure_scenery_until(700)
        self._seed_market()
        self._add_event("spawn", "Hero entered the forest.", hero_id=self.hero.id)
        for talent in self.hero.talents:
            self._add_event(
                "talent_roll",
                f"Rolled talent {talent.name}.",
                talent_id=talent.id,
                tier=talent.tier.value,
                effects=talent.effects,
            )

    def advance(self, seconds: float = 1.0) -> dict[str, Any]:
        if seconds <= 0:
            raise ValueError("seconds must be greater than zero")

        steps = max(1, int(seconds / 0.25))
        dt = seconds / steps
        for _ in range(steps):
            self._advance_step(dt)
        return self.snapshot()

    def equip_item(self, item_id: str) -> Equipment:
        for index, item in enumerate(self.hero.inventory):
            if item.id != item_id:
                continue

            previous = self.hero.equipped.get(item.slot)
            self.hero.equipped[item.slot] = item
            self.hero.inventory.pop(index)
            if previous is not None:
                self.hero.inventory.append(previous)
            self.hero.hp = min(self.hero.hp + item.max_hp, self.hero.max_hp)
            self._add_event(
                "equip",
                f"Equipped {item.name}.",
                item_id=item.id,
                slot=item.slot.value,
            )
            return item
        raise KeyError(f"item not found in inventory: {item_id}")

    def enter_rift(self, floor: int | None = None) -> RiftRun:
        if self.active_rift is not None and not self.active_rift.is_complete:
            raise ValueError("already in rift")

        target_floor = floor or self.unlocked_rift_floor
        if target_floor < 1:
            raise ValueError("rift floor must be at least 1")
        if target_floor > self.unlocked_rift_floor:
            raise ValueError("rift floor is locked")

        theme = self.rng.choice(RIFT_THEMES)
        minions_required = min(RIFT_MINIONS_MAX, RIFT_MINIONS_BASE + target_floor // 2)
        self.active_rift = RiftRun(
            floor=target_floor,
            theme=theme,
            minions_required=minions_required,
            started_tick=self.tick,
            origin_x=self.hero.x,
        )
        self.mode = "rift"
        self.active_monster = None
        self.hero.x = 0.0
        self.hero.y = HERO_GROUND_Y
        self.hero.heal(max(10, self.hero.max_hp // 4))
        self._hero_attack_timer = 0.0
        self._monster_attack_timer = 0.0
        self._next_encounter_x = self.rng.uniform(42.0, 72.0)
        self.rift_decorations = []
        self._next_rift_decoration_index = 0
        self._ensure_rift_scenery_until(760)
        self._add_event(
            "rift_enter",
            f"Entered floor {target_floor} {theme} rift.",
            floor=target_floor,
            theme=theme,
            minions_required=minions_required,
        )
        return self.active_rift

    def leave_rift(self) -> None:
        if self.active_rift is None:
            return
        floor = self.active_rift.floor
        self._return_to_forest(self.active_rift.origin_x)
        self._add_event("rift_leave", f"Left floor {floor} rift.", floor=floor)

    def deepen_forest(self) -> dict[str, Any]:
        if self.mode == "rift" and self.active_rift is not None:
            raise ValueError("cannot deepen forest while in rift")

        self.forest_depth += 1
        self.mode = "forest"
        self.active_monster = None
        self.hero.x = 0.0
        self.hero.y = HERO_GROUND_Y
        self.hero.heal(max(6, self.hero.max_hp // 8))
        self._hero_attack_timer = 0.0
        self._monster_attack_timer = 0.0
        self._revive_remaining = 0.0
        self._next_encounter_x = self._roll_next_encounter_x(self.hero.x)
        self.decorations = []
        self._next_decoration_index = 0
        self._ensure_scenery_until(900)
        self._add_event(
            "forest_deepen",
            f"Hero pushed into forest depth {self.forest_depth}.",
            depth=self.forest_depth,
            monster_level_bonus=self._forest_level_bonus(),
        )
        return self.snapshot()

    def retreat_forest(self) -> dict[str, Any]:
        if self.mode == "rift" and self.active_rift is not None:
            raise ValueError("cannot retreat forest while in rift")

        self.forest_depth = max(1, self.forest_depth - 1)
        self.mode = "forest"
        self.active_monster = None
        self.hero.x = 0.0
        self.hero.y = HERO_GROUND_Y
        self.hero.heal(max(10, self.hero.max_hp // 5))
        self._hero_attack_timer = 0.0
        self._monster_attack_timer = 0.0
        self._revive_remaining = 0.0
        self._next_encounter_x = self._roll_next_encounter_x(self.hero.x)
        self.decorations = []
        self._next_decoration_index = 0
        self._ensure_scenery_until(900)
        self._add_event(
            "forest_retreat",
            f"Hero retreated to forest depth {self.forest_depth}.",
            depth=self.forest_depth,
            monster_level_bonus=self._forest_level_bonus(),
        )
        return self.snapshot()

    def evolve_talent(self, talent_id: str) -> dict[str, Any]:
        if self.hero.talent_scrolls <= 0:
            raise ValueError("not enough talent evolution scrolls")

        for index, talent in enumerate(self.hero.talents):
            if talent.id != talent_id:
                continue
            evolved = evolve_talent_roll(talent, self.rng)
            self.hero.talent_scrolls -= 1
            self.hero.talents[index] = evolved
            self.hero.hp = min(self.hero.hp, self.hero.max_hp)
            self._add_event(
                "talent_evolve",
                f"Evolved {talent.name} into {evolved.name}.",
                old_talent_id=talent.id,
                old_tier=talent.tier.value,
                new_talent_id=evolved.id,
                new_tier=evolved.tier.value,
            )
            return {
                "old": talent.to_dict(),
                "new": evolved.to_dict(),
            }
        raise KeyError(f"talent not found: {talent_id}")

    def equip_best_items(self) -> list[Equipment]:
        equipped: list[Equipment] = []
        candidates = sorted(self.hero.inventory, key=lambda item: item.score, reverse=True)
        for item in list(candidates):
            current = self.hero.equipped.get(item.slot)
            if current is None or item.score > current.score:
                equipped.append(self.equip_item(item.id))
        return equipped

    def list_item(self, item_id: str, price: int) -> MarketListing:
        for index, item in enumerate(self.hero.inventory):
            if item.id != item_id:
                continue
            listing = self.market.create_listing(item, self.hero.id, price, self.tick)
            self.hero.inventory.pop(index)
            self._add_event(
                "market_list",
                f"Listed {item.name} for {price} gold.",
                listing_id=listing.id,
                item_id=item.id,
                price=price,
            )
            return listing
        raise KeyError(f"item not found in inventory: {item_id}")

    def buy_listing(self, listing_id: str, buyer_id: str) -> Equipment:
        listing = self.market.get_listing(listing_id)
        buyer_is_hero = buyer_id == self.hero.id
        seller_is_hero = listing.seller_id == self.hero.id
        if buyer_is_hero and self.hero.gold < listing.price:
            raise ValueError("not enough gold")

        item = self.market.buy(listing_id, buyer_id, self.tick)
        if buyer_is_hero:
            self.hero.gold -= listing.price
            self.hero.inventory.append(item)
        if seller_is_hero:
            self.hero.gold += listing.price
        self._add_event(
            "market_buy",
            f"{buyer_id} bought {item.name}.",
            listing_id=listing_id,
            item_id=item.id,
            buyer_id=buyer_id,
        )
        return item

    def cancel_listing(self, listing_id: str) -> Equipment:
        item = self.market.cancel(listing_id, self.hero.id, self.tick)
        self.hero.inventory.append(item)
        self._add_event(
            "market_cancel",
            f"Canceled listing for {item.name}.",
            listing_id=listing_id,
            item_id=item.id,
        )
        return item

    def buy_system_shop_item(self, sku: str) -> dict[str, Any]:
        if sku == SYSTEM_SHOP_DONATION_SKU:
            if self.hero.gold < SYSTEM_SHOP_DONATION_COST:
                raise ValueError("not enough gold")
            self.hero.gold -= SYSTEM_SHOP_DONATION_COST
            self.hero.donations += 1
            self._add_event(
                "system_shop_buy",
                "Bought a donation sigil.",
                sku=sku,
                price=SYSTEM_SHOP_DONATION_COST,
                donations=self.hero.donations,
            )
            return {
                "purchase": {
                    "sku": sku,
                    "kind": "donation",
                    "price": SYSTEM_SHOP_DONATION_COST,
                    "donations": self.hero.donations,
                }
            }

        if sku not in SYSTEM_SHOP_RAINBOW_COSTS:
            raise KeyError(f"unknown system shop sku: {sku}")
        price = SYSTEM_SHOP_RAINBOW_COSTS[sku]
        if self.hero.gold < price:
            raise ValueError("not enough gold")
        self.hero.gold -= price
        item = generate_system_shop_equipment(sku, self.hero.level, self.rng, owner_id=self.hero.id)
        self.hero.inventory.append(item)
        self._add_event(
            "system_shop_buy",
            f"Bought {item.name}.",
            sku=sku,
            item_id=item.id,
            price=price,
        )
        return {"purchase": {"sku": sku, "kind": "equipment", "price": price, "item": item.to_dict()}}

    def recycle_item(self, item_id: str) -> dict[str, Any]:
        for index, item in enumerate(self.hero.inventory):
            if item.id != item_id:
                continue
            self.hero.inventory.pop(index)
            value = item.score
            self.hero.gold += value
            self._add_event(
                "equipment_recycle",
                f"Recycled {item.name} for {value} gold.",
                item_id=item.id,
                gold=value,
            )
            return {"item": item.to_dict(), "gold": value}
        raise KeyError(f"item not found in inventory: {item_id}")

    def recycle_all_inventory(self) -> dict[str, Any]:
        items = list(self.hero.inventory)
        self.hero.inventory.clear()
        value = sum(item.score for item in items)
        self.hero.gold += value
        self._add_event(
            "equipment_recycle_all",
            f"Recycled {len(items)} items for {value} gold.",
            count=len(items),
            gold=value,
        )
        return {"items": [item.to_dict() for item in items], "count": len(items), "gold": value}

    def sell_own_listing_to_system(self, listing_id: str) -> dict[str, Any]:
        listing = self.market.get_listing(listing_id)
        if not listing.active:
            raise ValueError("listing is not active")
        if listing.seller_id != self.hero.id:
            raise PermissionError("cannot sell another player's listing")
        item = listing.item
        value = item.score
        listing.active = False
        listing.buyer_id = "system_shop"
        listing.sold_tick = self.tick
        item.owner_id = "system_shop"
        self.hero.gold += value
        self._add_event(
            "market_sell_system",
            f"Sold {item.name} to the system for {value} gold.",
            listing_id=listing_id,
            item_id=item.id,
            gold=value,
        )
        return {"listing": listing.to_dict(), "item": item.to_dict(), "gold": value}

    def donate_for_talent(self) -> dict[str, Any]:
        if self.hero.donations < 5:
            raise ValueError("not enough donations")
        if not self.hero.talents or any(talent.tier != TalentTier.MYTHIC for talent in self.hero.talents):
            raise ValueError("all current talents must be mythic")

        owned_ids = {talent.id for talent in self.hero.talents}
        candidates = [talent for talent in TALENT_CATALOG[TalentTier.COMMON] if talent.id not in owned_ids]
        if not candidates:
            candidates = list(TALENT_CATALOG[TalentTier.COMMON])
        talent = self.rng.choice(candidates)
        self.hero.donations -= 5
        self.hero.talents.append(talent)
        self._add_event(
            "talent_expand",
            f"Unlocked extra talent {talent.name}.",
            talent_id=talent.id,
            tier=talent.tier.value,
            spent=5,
        )
        return {"spent": 5, "talent": talent.to_dict(), "donations": self.hero.donations}

    def snapshot(self) -> dict[str, Any]:
        camera_x = max(0.0, self.hero.x - 180.0)
        if self.mode == "rift" and self.active_rift is not None:
            self._ensure_rift_scenery_until(camera_x + 900)
            nearby_decorations = [
                decor
                for decor in self.rift_decorations
                if camera_x - 120 <= float(decor["x"]) <= camera_x + 980
            ]
            biome = self.active_rift.theme
        else:
            self._ensure_scenery_until(camera_x + 900)
            nearby_decorations = [
                decor
                for decor in self.decorations
                if camera_x - 120 <= float(decor["x"]) <= camera_x + 980
            ]
            biome = "deep_forest" if self.forest_depth > 1 else "forest"
        hero_weapon = self.hero.equipped.get(EquipmentSlot.WEAPON)
        hero_snapshot = self.hero.to_dict()
        hero_snapshot.update(
            {
                "reviving": self._revive_remaining > 0,
                "revive_remaining": round(self._revive_remaining, 2),
                "revive_duration": HERO_REVIVE_SECONDS,
            }
        )
        hero_state = "walk"
        if self._revive_remaining > 0:
            hero_state = "reviving"
        elif self.active_monster is not None:
            distance = self.active_monster.x - self.hero.x
            hero_state = "combat" if distance <= self.hero.attack_range else "approach"
        entities: list[dict[str, Any]] = [
            {
                "id": self.hero.id,
                "type": "hero",
                "name": self.hero.name,
                "gender": self.hero.gender,
                "position": {"x": round(self.hero.x, 2), "y": round(self.hero.y, 2)},
                "facing": "right",
                "state": hero_state,
                "hp": self.hero.hp,
                "max_hp": self.hero.max_hp,
                "reviving": self._revive_remaining > 0,
                "revive_remaining": round(self._revive_remaining, 2),
                "attack_range": round(self.hero.attack_range, 2),
                "attack_speed": round(self.hero.attack_speed, 2),
                "hp_regen": round(self.hero.hp_regen, 2),
                "weapon": hero_weapon.to_dict() if hero_weapon is not None else None,
                "equipped": hero_snapshot["equipped"],
                "talents": hero_snapshot["talents"],
                "talent_effects": hero_snapshot["talent_effects"],
            }
        ]
        if self.active_monster is not None:
            entities.append(
                {
                    "id": self.active_monster.id,
                    "type": "monster",
                    "name": self.active_monster.kind,
                    "position": {
                        "x": round(self.active_monster.x, 2),
                        "y": round(self.active_monster.y, 2),
                    },
                    "facing": "left",
                    "state": "waiting" if self._revive_remaining > 0 else "combat",
                    "hp": self.active_monster.hp,
                    "max_hp": self.active_monster.max_hp,
                    "role": self.active_monster.role,
                    "theme": self.active_monster.theme,
                    "threat": round(self.active_monster.threat, 2),
                    "level": self.active_monster.level,
                }
            )

        return {
            "time": {"tick": self.tick, "seconds": round(self.time_seconds, 2)},
            "mode": self.mode,
            "hero": hero_snapshot,
            "monster": self.active_monster.to_dict()
            if self.active_monster is not None
            else None,
            "scene": {
                "biome": biome,
                "mode": self.mode,
                "forest_depth": self.forest_depth,
                "camera": {"x": round(camera_x, 2), "y": 0},
                "ground_y": HERO_GROUND_Y,
                "next_encounter_x": round(self._next_encounter_x, 2),
                "decorations": nearby_decorations,
                "entities": entities,
            },
            "rift": self._rift_snapshot(),
            "forest": self._forest_snapshot(),
            "treasure": self._treasure_snapshot(),
            "talent": self._talent_snapshot(),
            "system_shop": self._system_shop_snapshot(),
            "market": self.market.to_dict(),
            "events": [event.to_dict() for event in self.events],
        }

    def _advance_step(self, dt: float) -> None:
        self.time_seconds += dt
        self.tick += 1

        if self._revive_remaining > 0:
            self._advance_revive(dt)
            return

        if self.active_monster is None:
            if self.mode == "rift" and self.active_rift is not None:
                self._advance_rift_travel(dt)
            else:
                self._advance_forest_travel(dt)
            return

        self._advance_combat(dt)

    def _advance_forest_travel(self, dt: float) -> None:
        self.hero.x += self.hero.move_speed * dt
        self._heal_hero_over_time(self.hero.hp_regen, dt)
        if self.hero.x >= self._next_encounter_x:
            self._spawn_monster()

    def _advance_rift_travel(self, dt: float) -> None:
        self.hero.x += self.hero.move_speed * dt
        self._heal_hero_over_time(self.hero.hp_regen * 0.5, dt)
        if self.hero.x >= self._next_encounter_x:
            self._spawn_rift_monster()

    def _advance_combat(self, dt: float) -> None:
        if self.hero.hp <= 0 or self._revive_remaining > 0:
            return
        distance = self.active_monster.x - self.hero.x
        attack_range = self.hero.attack_range
        if distance > attack_range:
            move_distance = min(distance - attack_range, self.hero.move_speed * dt)
            self.hero.x += move_distance
            self._heal_hero_over_time(self.hero.hp_regen, dt)
            distance = self.active_monster.x - self.hero.x
        if distance > attack_range:
            return

        self._hero_attack_timer += dt
        self._monster_attack_timer += dt
        if self._hero_attack_timer >= self.hero.attack_interval:
            self._hero_attack_timer = 0.0
            self._hero_attack()

        if self.active_monster is not None and self._monster_attack_timer >= MONSTER_ATTACK_INTERVAL:
            self._monster_attack_timer = 0.0
            self._monster_attack()

    def _spawn_monster(self) -> None:
        level = max(1, self.hero.level + int(self.hero.x / 450) + self._forest_level_bonus())
        mimic_chance = min(0.35, TREASURE_MIMIC_CHANCE + self.hero.treasure_mimic_chance_bonus)
        mimic = self.rng.random() < mimic_chance
        if mimic:
            self.active_monster = create_treasure_mimic(
                level=level,
                x=self.hero.x + MONSTER_APPROACH_DISTANCE,
                y=HERO_GROUND_Y,
                rng=self.rng,
            )
        else:
            self.active_monster = create_monster(
                level=level,
                x=self.hero.x + MONSTER_APPROACH_DISTANCE,
                y=HERO_GROUND_Y,
                rng=self.rng,
                forest_depth=self.forest_depth,
            )
        self._hero_attack_timer = 0.0
        self._monster_attack_timer = 0.0
        if mimic:
            self._add_event(
                "treasure_mimic_spawn",
                "A treasure mimic sprang from the undergrowth.",
                monster_id=self.active_monster.id,
                level=level,
                pity=self.treasure_mimics_defeated,
                pity_threshold=TREASURE_MIMIC_PITY_THRESHOLD,
                chance=round(mimic_chance, 4),
            )
            return
        self._add_event(
            "monster_spawn",
            f"A {self.active_monster.kind} appeared.",
            monster_id=self.active_monster.id,
            level=level,
        )

    def _spawn_rift_monster(self) -> None:
        if self.active_rift is None:
            return
        boss = self.active_rift.minions_defeated >= self.active_rift.minions_required
        if boss:
            self.active_rift.state = "boss"
        self.active_monster = create_rift_monster(
            floor=self.active_rift.floor,
            theme=self.active_rift.theme,
            x=self.hero.x + MONSTER_APPROACH_DISTANCE,
            y=HERO_GROUND_Y,
            rng=self.rng,
            boss=boss,
        )
        self._hero_attack_timer = 0.0
        self._monster_attack_timer = 0.0
        event_kind = "rift_boss_spawn" if boss else "rift_monster_spawn"
        label = "Boss" if boss else "Monster"
        self._add_event(
            event_kind,
            f"{label} {self.active_monster.kind} appeared in the rift.",
            monster_id=self.active_monster.id,
            floor=self.active_rift.floor,
            theme=self.active_rift.theme,
            role=self.active_monster.role,
        )

    def _hero_attack(self) -> None:
        if self.active_monster is None:
            return

        damage = max(
            1,
            self.hero.attack_power
            + self.rng.randint(0, max(1, self.hero.level))
            - self.active_monster.defense,
        )
        self.active_monster.hp = max(0, self.active_monster.hp - damage)
        self._add_event(
            "hero_attack",
            f"Hero hit {self.active_monster.kind} for {damage}.",
            monster_id=self.active_monster.id,
            damage=damage,
            monster_hp=self.active_monster.hp,
        )
        if not self.active_monster.is_alive:
            self._kill_monster(self.active_monster)

    def _monster_attack(self) -> None:
        if self.active_monster is None:
            return
        damage = max(
            1,
            self.active_monster.attack
            + self.rng.randint(0, max(1, self.active_monster.level))
            - self.hero.defense_power,
        )
        self.hero.hp = max(0, self.hero.hp - damage)
        self._add_event(
            "monster_attack",
            f"{self.active_monster.kind} hit hero for {damage}.",
            monster_id=self.active_monster.id,
            damage=damage,
            hero_hp=self.hero.hp,
        )
        if self.hero.hp <= 0:
            self._hero_defeated()

    def _kill_monster(self, monster: Monster) -> None:
        if self.mode == "rift" and self.active_rift is not None:
            self._kill_rift_monster(monster)
            return
        if monster.role == "treasure_mimic":
            self._kill_treasure_mimic(monster)
            return

        self._grant_kill_rewards(monster, "monster_kill", f"Defeated {monster.kind}.")
        item = maybe_drop_equipment(
            monster.level,
            self.rng,
            chance_bonus=self.hero.drop_rate_bonus,
        )
        self._add_loot_event(item)
        self.active_monster = None
        self._next_encounter_x = self._roll_next_encounter_x(self.hero.x)

    def _kill_treasure_mimic(self, monster: Monster) -> None:
        self._grant_kill_rewards(
            monster,
            "treasure_mimic_kill",
            "Cracked open a treasure mimic.",
            pity_before=self.treasure_mimics_defeated,
            pity_threshold=TREASURE_MIMIC_PITY_THRESHOLD,
        )
        self.treasure_mimics_defeated += 1

        special_item = generate_special_set_equipment(monster.level, self.rng)
        self._add_loot_event(
            special_item,
            "special_loot",
            pity=self.treasure_mimics_defeated,
            pity_threshold=TREASURE_MIMIC_PITY_THRESHOLD,
        )

        if self.treasure_mimics_defeated >= TREASURE_MIMIC_PITY_THRESHOLD:
            guaranteed = generate_special_set_equipment(
                monster.level + 1,
                self.rng,
                rarity=Rarity.RED,
            )
            self._add_loot_event(
                guaranteed,
                "pity_special_loot",
                guaranteed_red=True,
                pity=TREASURE_MIMIC_PITY_THRESHOLD,
                pity_threshold=TREASURE_MIMIC_PITY_THRESHOLD,
            )
            self._add_event(
                "treasure_pity",
                "Pity triggered: an extra red special set item dropped.",
                item_id=guaranteed.id,
                set_name=guaranteed.set_name,
            )
            self.treasure_mimics_defeated = 0

        self.active_monster = None
        self._next_encounter_x = self._roll_next_encounter_x(self.hero.x)

    def _kill_rift_monster(self, monster: Monster) -> None:
        if self.active_rift is None:
            return
        boss = monster.role == "boss"
        event_kind = "rift_boss_kill" if boss else "rift_monster_kill"
        self._grant_kill_rewards(
            monster,
            event_kind,
            f"Defeated {monster.kind} in floor {self.active_rift.floor}.",
            floor=self.active_rift.floor,
            theme=self.active_rift.theme,
            role=monster.role,
        )

        floor_bonus = self.active_rift.floor * RIFT_DROP_BONUS_PER_FLOOR
        chance_bonus = floor_bonus + (RIFT_BOSS_DROP_BONUS if boss else RIFT_MINION_DROP_BONUS)
        chance_bonus += self.hero.drop_rate_bonus + self.hero.rift_drop_rate_bonus
        drop_level = monster.level + (1 if boss else 0)
        item = maybe_drop_equipment(drop_level, self.rng, chance_bonus=chance_bonus)
        self._add_loot_event(
            item,
            "rift_loot",
            floor=self.active_rift.floor,
            theme=self.active_rift.theme,
            boss=boss,
        )

        if boss:
            self._complete_rift()
            return

        self.active_rift.minions_defeated += 1
        if self.active_rift.minions_defeated >= self.active_rift.minions_required:
            self.active_rift.state = "boss"
            self._next_encounter_x = self.hero.x + self.rng.uniform(65.0, 95.0)
        else:
            self._next_encounter_x = self.hero.x + self.rng.uniform(42.0, 80.0)
        self.active_monster = None

    def _grant_kill_rewards(
        self,
        monster: Monster,
        event_kind: str,
        message: str,
        **extra: Any,
    ) -> None:
        gold_reward = max(0, int(monster.gold_reward * (1 + self.hero.gold_bonus_pct)))
        exp_reward = max(0, int(monster.exp_reward * (1 + self.hero.exp_bonus_pct)))
        self.hero.gold += gold_reward
        levels = self.hero.gain_exp(exp_reward)
        self._add_event(
            event_kind,
            message,
            monster_id=monster.id,
            exp=exp_reward,
            gold=gold_reward,
            **extra,
        )
        for level in levels:
            self._add_event("level_up", f"Hero reached level {level}.", level=level)
        self._maybe_drop_talent_scroll(monster)

    def _maybe_drop_talent_scroll(self, monster: Monster) -> None:
        chance = TALENT_SCROLL_DROP_CHANCE + self.hero.drop_rate_bonus * 0.4
        if monster.role == "treasure_mimic":
            chance += 0.16
        elif monster.role == "boss":
            chance += 0.12
        chance = min(0.7, chance)
        if self.rng.random() >= chance:
            return
        self.hero.talent_scrolls += 1
        self._add_event(
            "talent_scroll_drop",
            "Found a talent evolution scroll.",
            scrolls=self.hero.talent_scrolls,
            chance=round(chance, 4),
            monster_id=monster.id,
        )

    def _add_loot_event(
        self,
        item: Equipment | None,
        event_kind: str = "loot",
        **extra: Any,
    ) -> None:
        if item is not None:
            item.owner_id = self.hero.id
            self.hero.inventory.append(item)
            self._add_event(
                event_kind,
                f"Found {item.name}.",
                item_id=item.id,
                item_name=item.name,
                item_appearance=item.appearance(),
                rarity=item.rarity.value,
                slot=item.slot.value,
                special=item.special,
                set_id=item.set_id,
                set_name=item.set_name,
                set_piece=item.set_piece,
                **extra,
            )

    def _complete_rift(self) -> None:
        if self.active_rift is None:
            return
        floor = self.active_rift.floor
        theme = self.active_rift.theme
        self.active_rift.state = "complete"
        self.active_rift.completed_tick = self.tick
        self.unlocked_rift_floor = max(self.unlocked_rift_floor, floor + 1)
        self._add_event(
            "rift_complete",
            f"Cleared floor {floor} {theme} rift. Floor {self.unlocked_rift_floor} unlocked.",
            floor=floor,
            theme=theme,
            unlocked_floor=self.unlocked_rift_floor,
        )
        origin_x = self.active_rift.origin_x
        self._return_to_forest(origin_x)

    def _hero_defeated(self) -> None:
        if self._revive_remaining > 0:
            return

        monster_id = self.active_monster.id if self.active_monster else None
        self.hero.hp = 0
        self._apply_death_gold_penalty(monster_id)
        self._revive_remaining = HERO_REVIVE_SECONDS
        self._hero_attack_timer = 0.0
        self._monster_attack_timer = 0.0
        self._add_event(
            "hero_defeat",
            "Hero fell and is waiting to revive.",
            monster_id=monster_id,
            revive_seconds=HERO_REVIVE_SECONDS,
        )

    def _apply_death_gold_penalty(self, monster_id: str | None) -> None:
        gold_before = self.hero.gold
        if gold_before <= 0:
            return
        loss_pct = self.rng.uniform(HERO_DEATH_GOLD_LOSS_MIN_PCT, HERO_DEATH_GOLD_LOSS_MAX_PCT)
        gold_lost = min(gold_before, max(1, int(round(gold_before * loss_pct))))
        self.hero.gold = max(0, gold_before - gold_lost)
        self._add_event(
            "gold_loss",
            f"Death penalty: lost {gold_lost} gold.",
            monster_id=monster_id,
            gold_lost=gold_lost,
            gold_before=gold_before,
            gold_after=self.hero.gold,
            loss_pct=round(loss_pct, 4),
        )

    def _advance_revive(self, dt: float) -> None:
        self._revive_remaining = max(0.0, self._revive_remaining - dt)
        if self._revive_remaining > 0:
            return
        self.hero.hp = self.hero.max_hp
        self._hero_attack_timer = 0.0
        self._monster_attack_timer = 0.0
        monster_id = self.active_monster.id if self.active_monster else None
        self._add_event(
            "hero_revive",
            "Hero revived and rejoined the fight.",
            monster_id=monster_id,
        )

    def _return_to_forest(self, origin_x: float) -> None:
        self.mode = "forest"
        self.active_monster = None
        self.active_rift = None
        self.hero.x = origin_x
        self.hero.y = HERO_GROUND_Y
        self._hero_attack_timer = 0.0
        self._monster_attack_timer = 0.0
        self._revive_remaining = 0.0
        self._next_encounter_x = self._roll_next_encounter_x(self.hero.x)

    def _heal_hero_over_time(self, rate: float, dt: float) -> None:
        if self.hero.hp >= self.hero.max_hp or rate <= 0:
            self._hero_heal_bank = 0.0
            return
        self._hero_heal_bank += rate * dt
        amount = int(self._hero_heal_bank)
        if amount <= 0:
            return
        self._hero_heal_bank -= amount
        self.hero.heal(amount)

    def _roll_next_encounter_x(self, current_x: float) -> float:
        distance_scale = max(0.62, 1.0 - (self.forest_depth - 1) * 0.08)
        return current_x + self.rng.uniform(
            ENCOUNTER_MIN_DISTANCE * distance_scale,
            ENCOUNTER_MAX_DISTANCE * distance_scale,
        )

    def _ensure_scenery_until(self, target_x: float) -> None:
        while self._next_decoration_index * SCENE_CHUNK_WIDTH < target_x:
            x = self._next_decoration_index * SCENE_CHUNK_WIDTH
            self.decorations.append(
                create_decoration(
                    self._next_decoration_index,
                    x,
                    self.rng,
                    forest_depth=self.forest_depth,
                )
            )
            if self.forest_depth > 1:
                self.decorations.append(
                    create_decoration(
                        self._next_decoration_index + 10_000,
                        x + SCENE_CHUNK_WIDTH * 0.48,
                        self.rng,
                        forest_depth=self.forest_depth,
                    )
                )
            self._next_decoration_index += 1

    def _ensure_rift_scenery_until(self, target_x: float) -> None:
        if self.active_rift is None:
            return
        while self._next_rift_decoration_index * SCENE_CHUNK_WIDTH < target_x:
            x = self._next_rift_decoration_index * SCENE_CHUNK_WIDTH
            self.rift_decorations.append(
                create_rift_decoration(
                    self.active_rift.theme,
                    self._next_rift_decoration_index,
                    x,
                    self.rng,
                )
            )
            self._next_rift_decoration_index += 1

    def _seed_market(self) -> None:
        sellers = ("npc_blacksmith", "npc_ranger", "npc_collector")
        for index, seller_id in enumerate(sellers):
            item = generate_equipment(level=index + 1, rng=self.rng)
            item.owner_id = seller_id
            price = max(18, item.score * 2 + index * 8)
            self.market.create_listing(item, seller_id, price, self.tick)

    def _forest_level_bonus(self) -> int:
        return max(0, (self.forest_depth - 1) * 3)

    def _recommended_forest_power(self) -> int:
        depth_bonus = max(0, self.forest_depth - 1)
        return 135 + depth_bonus * 72 + self._forest_level_bonus() * 10

    def _forest_snapshot(self) -> dict[str, Any]:
        return {
            "depth": self.forest_depth,
            "biome": "deep_forest" if self.forest_depth > 1 else "forest",
            "monster_level_bonus": self._forest_level_bonus(),
            "threat": round(1.0 + max(0, self.forest_depth - 1) * 0.32, 2),
            "recommended_power": self._recommended_forest_power(),
            "hero_power": self._hero_power(),
        }

    def _rift_snapshot(self) -> dict[str, Any]:
        recommended_power = self._recommended_rift_power(self.unlocked_rift_floor)
        base = {
            "active": False,
            "unlocked_floor": self.unlocked_rift_floor,
            "recommended_power": recommended_power,
            "hero_power": self._hero_power(),
            "available_themes": list(RIFT_THEMES),
        }
        if self.active_rift is None:
            return base
        active = self.active_rift.to_dict()
        active.update(
            {
                "unlocked_floor": self.unlocked_rift_floor,
                "recommended_power": self._recommended_rift_power(self.active_rift.floor),
                "hero_power": self._hero_power(),
                "available_themes": list(RIFT_THEMES),
            }
        )
        return active

    def _hero_power(self) -> int:
        return self.hero.attack_power * 5 + self.hero.defense_power * 4 + self.hero.max_hp

    def _recommended_rift_power(self, floor: int) -> int:
        return 125 + floor * 34

    def _treasure_snapshot(self) -> dict[str, Any]:
        return {
            "mimic_chance": TREASURE_MIMIC_CHANCE,
            "mimics_defeated_since_red": self.treasure_mimics_defeated,
            "pity_threshold": TREASURE_MIMIC_PITY_THRESHOLD,
            "pity_remaining": TREASURE_MIMIC_PITY_THRESHOLD - self.treasure_mimics_defeated,
            "pity_progress": self.treasure_mimics_defeated / TREASURE_MIMIC_PITY_THRESHOLD,
        }

    def _talent_snapshot(self) -> dict[str, Any]:
        return {
            "tiers": [
                {
                    "id": tier.value,
                    "label": config.label,
                    "count": len(TALENT_CATALOG[tier]),
                    "weight": config.weight,
                }
                for tier, config in TALENT_TIER_CONFIG.items()
            ],
            "total_catalog_count": sum(len(talents) for talents in TALENT_CATALOG.values()),
            "donation_cost": 5,
            "donations": self.hero.donations,
            "can_expand": self.hero.can_expand_talent_with_donations,
        }

    def _system_shop_snapshot(self) -> dict[str, Any]:
        items = []
        for entry in system_shop_catalog(self.hero.level):
            price = int(entry["price"])
            items.append(entry | {"affordable": self.hero.gold >= price})
        return {"items": items}

    def _add_event(self, kind: str, message: str, **data: Any) -> None:
        self.events.append(Event(self.tick, kind, message, data))
