"""Local JSON persistence for the idle forest prototype."""

from __future__ import annotations

from collections import deque
import json
from pathlib import Path
from typing import Any

from .engine import GameEngine
from .market import Market, MarketListing
from .models import Equipment, EquipmentSlot, Event, Hero, Monster, Rarity, RiftRun, Talent, TalentTier


SAVE_VERSION = 1


def engine_to_save(engine: GameEngine) -> dict[str, Any]:
    return {
        "rng_state": engine.rng.getstate(),
        "tick": engine.tick,
        "time_seconds": engine.time_seconds,
        "hero": hero_to_save(engine.hero),
        "active_monster": monster_to_save(engine.active_monster),
        "mode": engine.mode,
        "forest_depth": engine.forest_depth,
        "unlocked_rift_floor": engine.unlocked_rift_floor,
        "active_rift": rift_to_save(engine.active_rift),
        "treasure_mimics_defeated": engine.treasure_mimics_defeated,
        "market": market_to_save(engine.market),
        "events": [event.to_dict() for event in engine.events],
        "decorations": engine.decorations,
        "rift_decorations": engine.rift_decorations,
        "hero_attack_timer": engine._hero_attack_timer,
        "monster_attack_timer": engine._monster_attack_timer,
        "hero_heal_bank": engine._hero_heal_bank,
        "revive_remaining": engine._revive_remaining,
        "next_encounter_x": engine._next_encounter_x,
        "next_decoration_index": engine._next_decoration_index,
        "next_rift_decoration_index": engine._next_rift_decoration_index,
    }


def engine_from_save(data: dict[str, Any]) -> GameEngine:
    engine = GameEngine(seed=11)
    engine.rng.setstate(_tuple_state(data["rng_state"]))
    engine.tick = int(data["tick"])
    engine.time_seconds = float(data["time_seconds"])
    engine.hero = hero_from_save(data["hero"])
    engine.active_monster = monster_from_save(data.get("active_monster"))
    engine.mode = str(data.get("mode", "forest"))
    engine.forest_depth = int(data.get("forest_depth", 1))
    engine.unlocked_rift_floor = int(data.get("unlocked_rift_floor", 1))
    engine.active_rift = rift_from_save(data.get("active_rift"))
    engine.treasure_mimics_defeated = int(data.get("treasure_mimics_defeated", 0))
    engine.market = market_from_save(data.get("market", {}))
    engine.events = deque(
        [event_from_save(event) for event in data.get("events", [])],
        maxlen=80,
    )
    engine.decorations = list(data.get("decorations", []))
    engine.rift_decorations = list(data.get("rift_decorations", []))
    engine._hero_attack_timer = float(data.get("hero_attack_timer", 0.0))
    engine._monster_attack_timer = float(data.get("monster_attack_timer", 0.0))
    engine._hero_heal_bank = float(data.get("hero_heal_bank", 0.0))
    engine._revive_remaining = float(data.get("revive_remaining", 0.0))
    engine._next_encounter_x = float(data.get("next_encounter_x", engine.hero.x + 300))
    engine._next_decoration_index = int(data.get("next_decoration_index", 0))
    engine._next_rift_decoration_index = int(data.get("next_rift_decoration_index", 0))
    return engine


def hero_to_save(hero: Hero) -> dict[str, Any]:
    return {
        "id": hero.id,
        "name": hero.name,
        "gender": hero.gender,
        "level": hero.level,
        "exp": hero.exp,
        "base_attack": hero.base_attack,
        "base_defense": hero.base_defense,
        "base_max_hp": hero.base_max_hp,
        "base_attack_speed": hero.base_attack_speed,
        "base_hp_regen": hero.base_hp_regen,
        "base_attack_range": hero.base_attack_range,
        "hp": hero.hp,
        "gold": hero.gold,
        "x": hero.x,
        "y": hero.y,
        "speed": hero.speed,
        "talent_scrolls": hero.talent_scrolls,
        "talents": [talent.to_dict() for talent in hero.talents],
        "inventory": [equipment_to_save(item) for item in hero.inventory],
        "equipped": {slot.value: equipment_to_save(item) for slot, item in hero.equipped.items()},
    }


def hero_from_save(data: dict[str, Any]) -> Hero:
    hero = Hero(
        id=str(data["id"]),
        name=str(data["name"]),
        gender=str(data.get("gender", "male")),
        level=int(data.get("level", 1)),
        exp=int(data.get("exp", 0)),
        base_attack=int(data.get("base_attack", 8)),
        base_defense=int(data.get("base_defense", 2)),
        base_max_hp=int(data.get("base_max_hp", 80)),
        base_attack_speed=float(data.get("base_attack_speed", 1.0)),
        base_hp_regen=float(data.get("base_hp_regen", 2.0)),
        base_attack_range=float(data.get("base_attack_range", 68.0)),
        hp=int(data.get("hp", 80)),
        gold=int(data.get("gold", 0)),
        x=float(data.get("x", 0.0)),
        y=float(data.get("y", 220.0)),
        speed=float(data.get("speed", 38.0)),
        talent_scrolls=int(data.get("talent_scrolls", 0)),
    )
    hero.talents = [talent_from_save(talent) for talent in data.get("talents", [])]
    hero.inventory = [equipment_from_save(item) for item in data.get("inventory", [])]
    hero.equipped = {
        EquipmentSlot(slot): equipment_from_save(item)
        for slot, item in data.get("equipped", {}).items()
    }
    return hero


def equipment_to_save(item: Equipment) -> dict[str, Any]:
    return {
        "id": item.id,
        "name": item.name,
        "slot": item.slot.value,
        "rarity": item.rarity.value,
        "level": item.level,
        "attack": item.attack,
        "defense": item.defense,
        "max_hp": item.max_hp,
        "attack_speed": item.attack_speed,
        "hp_regen": item.hp_regen,
        "attack_range": item.attack_range,
        "weapon_type": item.weapon_type,
        "owner_id": item.owner_id,
        "tradable": item.tradable,
        "special": item.special,
        "set_id": item.set_id,
        "set_name": item.set_name,
        "set_piece": item.set_piece,
        "set_bonus": item.set_bonus,
    }


def equipment_from_save(data: dict[str, Any]) -> Equipment:
    return Equipment(
        id=str(data["id"]),
        name=str(data["name"]),
        slot=EquipmentSlot(str(data["slot"])),
        rarity=Rarity(str(data["rarity"])),
        level=int(data["level"]),
        attack=int(data.get("attack", 0)),
        defense=int(data.get("defense", 0)),
        max_hp=int(data.get("max_hp", 0)),
        attack_speed=float(data.get("attack_speed", 0.0)),
        hp_regen=float(data.get("hp_regen", 0.0)),
        attack_range=float(data.get("attack_range", 0.0)),
        weapon_type=data.get("weapon_type"),
        owner_id=data.get("owner_id"),
        tradable=bool(data.get("tradable", True)),
        special=bool(data.get("special", False)),
        set_id=data.get("set_id"),
        set_name=data.get("set_name"),
        set_piece=data.get("set_piece"),
        set_bonus=dict(data.get("set_bonus", {})),
    )


def talent_from_save(data: dict[str, Any]) -> Talent:
    return Talent(
        id=str(data["id"]),
        name=str(data["name"]),
        tier=TalentTier(str(data["tier"])),
        effects={str(key): float(value) for key, value in data.get("effects", {}).items()},
        description=str(data.get("description", "")),
    )


def monster_to_save(monster: Monster | None) -> dict[str, Any] | None:
    if monster is None:
        return None
    return {
        "id": monster.id,
        "kind": monster.kind,
        "level": monster.level,
        "max_hp": monster.max_hp,
        "hp": monster.hp,
        "attack": monster.attack,
        "defense": monster.defense,
        "exp_reward": monster.exp_reward,
        "gold_reward": monster.gold_reward,
        "x": monster.x,
        "y": monster.y,
        "role": monster.role,
        "theme": monster.theme,
        "threat": monster.threat,
    }


def monster_from_save(data: dict[str, Any] | None) -> Monster | None:
    if data is None:
        return None
    return Monster(
        id=str(data["id"]),
        kind=str(data["kind"]),
        level=int(data["level"]),
        max_hp=int(data["max_hp"]),
        hp=int(data["hp"]),
        attack=int(data["attack"]),
        defense=int(data["defense"]),
        exp_reward=int(data["exp_reward"]),
        gold_reward=int(data["gold_reward"]),
        x=float(data["x"]),
        y=float(data["y"]),
        role=str(data.get("role", "minion")),
        theme=str(data.get("theme", "forest")),
        threat=float(data.get("threat", 1.0)),
    )


def rift_to_save(rift: RiftRun | None) -> dict[str, Any] | None:
    if rift is None:
        return None
    return rift.to_dict() | {"origin_x": rift.origin_x}


def rift_from_save(data: dict[str, Any] | None) -> RiftRun | None:
    if data is None:
        return None
    return RiftRun(
        floor=int(data["floor"]),
        theme=str(data["theme"]),
        minions_required=int(data["minions_required"]),
        started_tick=int(data["started_tick"]),
        origin_x=float(data.get("origin_x", 0.0)),
        minions_defeated=int(data.get("minions_defeated", 0)),
        state=str(data.get("state", "minions")),
        completed_tick=data.get("completed_tick"),
    )


def market_to_save(market: Market) -> dict[str, Any]:
    return {"listings": [listing.to_dict() for listing in market.all_listings()]}


def market_from_save(data: dict[str, Any]) -> Market:
    market = Market()
    market._listings = {
        str(listing["id"]): MarketListing(
            id=str(listing["id"]),
            item=equipment_from_save(listing["item"]),
            seller_id=str(listing["seller_id"]),
            price=int(listing["price"]),
            created_tick=int(listing["created_tick"]),
            active=bool(listing.get("active", True)),
            buyer_id=listing.get("buyer_id"),
            sold_tick=listing.get("sold_tick"),
        )
        for listing in data.get("listings", [])
    }
    return market


def event_from_save(data: dict[str, Any]) -> Event:
    return Event(
        tick=int(data["tick"]),
        kind=str(data["kind"]),
        message=str(data["message"]),
        data=dict(data.get("data", {})),
    )


class SaveStore:
    def __init__(self, path: Path) -> None:
        self.path = path

    def save(self, profile: dict[str, Any], engine: GameEngine) -> None:
        payload = {
            "version": SAVE_VERSION,
            "profile": profile,
            "engine": engine_to_save(engine),
        }
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary_path = self.path.with_suffix(f"{self.path.suffix}.tmp")
        temporary_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        temporary_path.replace(self.path)

    def load(self) -> dict[str, Any] | None:
        if not self.path.exists():
            return None
        payload = json.loads(self.path.read_text(encoding="utf-8"))
        if int(payload.get("version", 0)) != SAVE_VERSION:
            raise ValueError("unsupported save version")
        return {
            "profile": dict(payload.get("profile", {})),
            "engine": engine_from_save(payload["engine"]),
        }

    def delete(self) -> None:
        self.path.unlink(missing_ok=True)


def _tuple_state(value: Any) -> Any:
    if isinstance(value, list):
        return tuple(_tuple_state(item) for item in value)
    return value
