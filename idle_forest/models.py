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
    RAINBOW = "rainbow"


class EquipmentSlot(str, Enum):
    WEAPON = "weapon"
    HELMET = "helmet"
    ARMOR = "armor"
    BOOTS = "boots"
    RING = "ring"


RARITY_APPEARANCE: dict[Rarity, dict[str, str]] = {
    Rarity.WHITE: {"primary": "#d8dde4", "accent": "#8f9aa4", "glow": "#d8dde4"},
    Rarity.GREEN: {"primary": "#5fd18b", "accent": "#2f8f5c", "glow": "#36b37e"},
    Rarity.BLUE: {"primary": "#68b7ff", "accent": "#2b78c2", "glow": "#2684ff"},
    Rarity.PURPLE: {"primary": "#b779ff", "accent": "#7543bd", "glow": "#9b5cff"},
    Rarity.GOLD: {"primary": "#ffdc7d", "accent": "#b98221", "glow": "#ffca55"},
    Rarity.RED: {"primary": "#ff7a7c", "accent": "#9e2e3a", "glow": "#ff4d4f"},
    Rarity.RAINBOW: {"primary": "#8effff", "accent": "#ff78e6", "glow": "#fff36a"},
}

SLOT_ICON_SHAPES: dict[EquipmentSlot, str] = {
    EquipmentSlot.WEAPON: "slash",
    EquipmentSlot.HELMET: "crest",
    EquipmentSlot.ARMOR: "chest",
    EquipmentSlot.BOOTS: "step",
    EquipmentSlot.RING: "pet",
}


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
    attack_speed: float = 0.0
    hp_regen: float = 0.0
    attack_range: float = 0.0
    weapon_type: str | None = None
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
        speed_bonus = int(self.attack_speed * 30)
        regen_bonus = int(self.hp_regen * 4)
        range_bonus = int(self.attack_range * 0.08)
        return (
            self.attack * 4
            + self.defense * 3
            + self.max_hp
            + self.level * 2
            + speed_bonus
            + regen_bonus
            + range_bonus
            + special_bonus
        )

    def appearance(self) -> dict[str, Any]:
        palette = dict(RARITY_APPEARANCE[self.rarity])
        model = self.slot.value
        accent = self.set_id or self.rarity.value

        if self.slot == EquipmentSlot.WEAPON:
            model = self.weapon_type or "blade"
            if self.id.startswith("starter_wooden_sword"):
                model = "wooden_blade"
                palette = {
                    "primary": "#d2a15f",
                    "accent": "#7a4b2a",
                    "glow": "#d8dde4",
                }
                accent = "starter"
        elif self.slot == EquipmentSlot.HELMET:
            model = "crown_helm" if self.rarity in {Rarity.GOLD, Rarity.RED, Rarity.RAINBOW} else "visor_helm"
        elif self.slot == EquipmentSlot.ARMOR:
            model = "plate_mail" if self.rarity in {Rarity.PURPLE, Rarity.GOLD, Rarity.RED, Rarity.RAINBOW} else "leather_mail"
        elif self.slot == EquipmentSlot.BOOTS:
            model = "winged_boots" if self.attack_speed > 0 or self.hp_regen > 0.18 else "travel_boots"
        elif self.slot == EquipmentSlot.RING:
            model = {
                Rarity.WHITE: "sprout_pet",
                Rarity.GREEN: "leaf_pet",
                Rarity.BLUE: "moon_cat_pet",
                Rarity.PURPLE: "star_bunny_pet",
                Rarity.GOLD: "spark_fox_pet",
                Rarity.RED: "ember_fox_pet",
                Rarity.RAINBOW: "ember_fox_pet",
            }[self.rarity]

        return {
            "slot": self.slot.value,
            "model": model,
            "palette": palette,
            "accent": accent,
            "aura": self.special or self.rarity in {Rarity.PURPLE, Rarity.GOLD, Rarity.RED, Rarity.RAINBOW},
            "icon_shape": SLOT_ICON_SHAPES[self.slot],
        }

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
            "attack_speed": round(self.attack_speed, 2),
            "hp_regen": round(self.hp_regen, 2),
            "attack_range": round(self.attack_range, 2),
            "weapon_type": self.weapon_type,
            "owner_id": self.owner_id,
            "tradable": self.tradable,
            "score": self.score,
            "special": self.special,
            "set_id": self.set_id,
            "set_name": self.set_name,
            "set_piece": self.set_piece,
            "set_bonus": self.set_bonus,
            "appearance": self.appearance(),
        }


@dataclass
class Hero:
    id: str
    name: str
    gender: str = "male"
    level: int = 1
    exp: int = 0
    base_attack: int = 8
    base_defense: int = 2
    base_max_hp: int = 80
    base_attack_speed: float = 1.0
    base_hp_regen: float = 2.0
    base_attack_range: float = 68.0
    hp: int = 80
    gold: int = 0
    x: float = 0.0
    y: float = 220.0
    speed: float = 38.0
    talent_scrolls: int = 0
    donations: int = 0
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
    def attack_speed(self) -> float:
        equipment_bonus = sum(item.attack_speed for item in self.equipped.values())
        return max(0.2, self.base_attack_speed + equipment_bonus)

    @property
    def attack_interval(self) -> float:
        return 1.0 / self.attack_speed

    @property
    def hp_regen(self) -> float:
        equipment_bonus = sum(item.hp_regen for item in self.equipped.values())
        return max(0.0, self.base_hp_regen + equipment_bonus)

    @property
    def attack_range(self) -> float:
        equipment_bonus = sum(item.attack_range for item in self.equipped.values())
        return max(self.base_attack_range, self.base_attack_range + equipment_bonus)

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

    @property
    def can_expand_talent_with_donations(self) -> bool:
        return bool(self.talents) and self.donations >= 5 and all(
            talent.tier == TalentTier.MYTHIC for talent in self.talents
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "level": self.level,
            "exp": self.exp,
            "exp_to_next_level": self.exp_to_next_level,
            "exp_progress": round(self.exp / max(1, self.exp_to_next_level), 4),
            "hp": self.hp,
            "max_hp": self.max_hp,
            "attack": self.attack_power,
            "defense": self.defense_power,
            "attack_speed": round(self.attack_speed, 2),
            "attack_interval": round(self.attack_interval, 2),
            "attack_range": round(self.attack_range, 2),
            "hp_regen": round(self.hp_regen, 2),
            "gold": self.gold,
            "position": {"x": round(self.x, 2), "y": round(self.y, 2)},
            "speed": round(self.move_speed, 2),
            "talent_scrolls": self.talent_scrolls,
            "donations": self.donations,
            "can_expand_talent": self.can_expand_talent_with_donations,
            "talents": [talent.to_dict() for talent in self.talents],
            "talent_effects": self.talent_effect_totals(),
            "inventory": [item.to_dict() for item in self.inventory],
            "equipped": {
                slot.value: item.to_dict() for slot, item in self.equipped.items()
            },
            "equipment_slots": [
                {
                    "slot": slot.value,
                    "item": self.equipped[slot].to_dict() if slot in self.equipped else None,
                }
                for slot in EquipmentSlot
            ],
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
    threat: float = 1.0

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
            "threat": round(self.threat, 2),
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
