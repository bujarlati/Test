"""Data models used by the idle forest engine."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class Rarity(str, Enum):
    WHITE = "white"
    GREEN = "green"
    BLUE = "blue"
    PURPLE = "purple"
    GOLD = "gold"
    RED = "red"


class EquipmentSlot(str, Enum):
    WEAPON = "weapon"
    HELMET = "helmet"
    ARMOR = "armor"
    BOOTS = "boots"
    RING = "ring"


class TalentTier(str, Enum):
    COMMON = "common"
    UNCOMMON = "uncommon"
    EXCELLENT = "excellent"
    RARE = "rare"
    TRANSCENDENT = "transcendent"
    MYTHIC = "mythic"


@dataclass(frozen=True)
class Talent:
    id: str
    name: str
    tier: TalentTier
    effects: dict[str, float]
    description: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "tier": self.tier.value,
            "effects": self.effects,
            "description": self.description,
        }


@dataclass
class Equipment:
    id: str
    name: str
    slot: EquipmentSlot
    rarity: Rarity
    level: int
    attack: int = 0
    defense: int = 0
    max_hp: int = 0
    owner_id: str | None = None
    tradable: bool = True
    special: bool = False
    set_id: str | None = None
    set_name: str | None = None
    set_piece: str | None = None
    set_bonus: dict[str, Any] = field(default_factory=dict)

    @property
    def score(self) -> int:
        special_bonus = 12 if self.special else 0
        return self.attack * 4 + self.defense * 3 + self.max_hp + self.level * 2 + special_bonus

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "slot": self.slot.value,
            "rarity": self.rarity.value,
            "level": self.level,
            "attack": self.attack,
            "defense": self.defense,
            "max_hp": self.max_hp,
            "owner_id": self.owner_id,
            "tradable": self.tradable,
            "score": self.score,
            "special": self.special,
            "set_id": self.set_id,
            "set_name": self.set_name,
            "set_piece": self.set_piece,
            "set_bonus": self.set_bonus,
        }


@dataclass
class Hero:
    id: str
    name: str
    level: int = 1
    exp: int = 0
    base_attack: int = 8
    base_defense: int = 2
    base_max_hp: int = 80
    hp: int = 80
    gold: int = 0
    x: float = 0.0
    y: float = 220.0
    speed: float = 38.0
    talent_scrolls: int = 0
    talents: list[Talent] = field(default_factory=list)
    inventory: list[Equipment] = field(default_factory=list)
    equipped: dict[EquipmentSlot, Equipment] = field(default_factory=dict)

    @property
    def attack_power(self) -> int:
        base = (
            self.base_attack
            + sum(item.attack for item in self.equipped.values())
            + sum(bonus["attack"] for bonus in self.active_set_bonuses().values())
        )
        return max(1, int(base * (1 + self.talent_pct("attack_pct") + self.talent_pct("all_stats_pct"))))

    @property
    def defense_power(self) -> int:
        base = (
            self.base_defense
            + sum(item.defense for item in self.equipped.values())
            + sum(bonus["defense"] for bonus in self.active_set_bonuses().values())
        )
        return max(0, int(base * (1 + self.talent_pct("defense_pct") + self.talent_pct("all_stats_pct"))))

    @property
    def max_hp(self) -> int:
        base = (
            self.base_max_hp
            + sum(item.max_hp for item in self.equipped.values())
            + sum(bonus["max_hp"] for bonus in self.active_set_bonuses().values())
        )
        return max(1, int(base * (1 + self.talent_pct("max_hp_pct") + self.talent_pct("all_stats_pct"))))

    @property
    def move_speed(self) -> float:
        return self.speed * (1 + self.talent_pct("move_speed_pct"))

    @property
    def drop_rate_bonus(self) -> float:
        return self.talent_pct("drop_rate_pct")

    @property
    def rift_drop_rate_bonus(self) -> float:
        return self.talent_pct("rift_drop_rate_pct")

    @property
    def treasure_mimic_chance_bonus(self) -> float:
        return self.talent_pct("treasure_mimic_chance_pct")

    @property
    def gold_bonus_pct(self) -> float:
        return self.talent_pct("gold_pct")

    @property
    def exp_bonus_pct(self) -> float:
        return self.talent_pct("exp_pct")

    @property
    def exp_to_next_level(self) -> int:
        return 60 + self.level * 35

    def heal(self, amount: int) -> None:
        self.hp = min(self.max_hp, self.hp + amount)

    def gain_exp(self, amount: int) -> list[int]:
        gained_levels: list[int] = []
        self.exp += amount
        while self.exp >= self.exp_to_next_level:
            self.exp -= self.exp_to_next_level
            self.level += 1
            self.base_attack += 2
            self.base_defense += 1
            self.base_max_hp += 10
            self.hp = self.max_hp
            gained_levels.append(self.level)
        return gained_levels

    def talent_effect_totals(self) -> dict[str, float]:
        totals: dict[str, float] = {}
        for talent in self.talents:
            for key, value in talent.effects.items():
                totals[key] = totals.get(key, 0.0) + value
        return totals

    def talent_pct(self, key: str) -> float:
        return self.talent_effect_totals().get(key, 0.0)

    def active_set_bonuses(self) -> dict[str, dict[str, Any]]:
        grouped: dict[str, list[Equipment]] = {}
        for item in self.equipped.values():
            if item.special and item.set_id:
                grouped.setdefault(item.set_id, []).append(item)

        active: dict[str, dict[str, Any]] = {}
        for set_id, items in grouped.items():
            first = items[0]
            required = int(first.set_bonus.get("pieces_required", 2))
            if len(items) < required:
                continue
            active[set_id] = {
                "set_id": set_id,
                "set_name": first.set_name,
                "pieces": len(items),
                "pieces_required": required,
                "attack": max(int(item.set_bonus.get("attack", 0)) for item in items),
                "defense": max(int(item.set_bonus.get("defense", 0)) for item in items),
                "max_hp": max(int(item.set_bonus.get("max_hp", 0)) for item in items),
            }
        return active

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "level": self.level,
            "exp": self.exp,
            "exp_to_next_level": self.exp_to_next_level,
            "hp": self.hp,
            "max_hp": self.max_hp,
            "attack": self.attack_power,
            "defense": self.defense_power,
            "gold": self.gold,
            "position": {"x": round(self.x, 2), "y": round(self.y, 2)},
            "speed": round(self.move_speed, 2),
            "talent_scrolls": self.talent_scrolls,
            "talents": [talent.to_dict() for talent in self.talents],
            "talent_effects": self.talent_effect_totals(),
            "inventory": [item.to_dict() for item in self.inventory],
            "equipped": {
                slot.value: item.to_dict() for slot, item in self.equipped.items()
            },
            "set_bonuses": list(self.active_set_bonuses().values()),
        }


@dataclass
class Monster:
    id: str
    kind: str
    level: int
    max_hp: int
    hp: int
    attack: int
    defense: int
    exp_reward: int
    gold_reward: int
    x: float
    y: float
    role: str = "minion"
    theme: str = "forest"

    @property
    def is_alive(self) -> bool:
        return self.hp > 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "kind": self.kind,
            "level": self.level,
            "hp": self.hp,
            "max_hp": self.max_hp,
            "attack": self.attack,
            "defense": self.defense,
            "exp_reward": self.exp_reward,
            "gold_reward": self.gold_reward,
            "position": {"x": round(self.x, 2), "y": round(self.y, 2)},
            "role": self.role,
            "theme": self.theme,
        }


@dataclass
class RiftRun:
    floor: int
    theme: str
    minions_required: int
    started_tick: int
    origin_x: float
    minions_defeated: int = 0
    state: str = "minions"
    completed_tick: int | None = None

    @property
    def is_boss_phase(self) -> bool:
        return self.state == "boss"

    @property
    def is_complete(self) -> bool:
        return self.state == "complete"

    @property
    def progress_text(self) -> str:
        if self.state == "complete":
            return "complete"
        if self.state == "boss":
            return "boss"
        return f"{self.minions_defeated}/{self.minions_required}"

    def to_dict(self) -> dict[str, Any]:
        return {
            "active": not self.is_complete,
            "floor": self.floor,
            "theme": self.theme,
            "state": self.state,
            "minions_required": self.minions_required,
            "minions_defeated": self.minions_defeated,
            "started_tick": self.started_tick,
            "completed_tick": self.completed_tick,
            "progress_text": self.progress_text,
        }


@dataclass
class Event:
    tick: int
    kind: str
    message: str
    data: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "tick": self.tick,
            "kind": self.kind,
            "message": self.message,
            "data": self.data,
        }
