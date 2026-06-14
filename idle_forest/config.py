"""Shared balance values for the idle forest prototype."""

from __future__ import annotations

from dataclasses import dataclass

from .models import Rarity


@dataclass(frozen=True)
class RarityConfig:
    label: str
    color: str
    weight: int
    power_multiplier: float
    min_level_bonus: int = 0


RARITY_CONFIG: dict[Rarity, RarityConfig] = {
    Rarity.WHITE: RarityConfig("White", "#d8dde4", 7000, 1.00),
    Rarity.GREEN: RarityConfig("Green", "#36b37e", 2200, 1.18),
    Rarity.BLUE: RarityConfig("Blue", "#2684ff", 650, 1.45),
    Rarity.PURPLE: RarityConfig("Purple", "#9b5cff", 130, 1.85, 1),
    Rarity.GOLD: RarityConfig("Gold", "#ffab00", 18, 2.45, 2),
    Rarity.RED: RarityConfig("Red", "#ff4d4f", 2, 3.30, 3),
    Rarity.RAINBOW: RarityConfig("Rainbow", "#8effff", 0, 4.65, 5),
}

RARITY_ORDER: tuple[Rarity, ...] = (
    Rarity.WHITE,
    Rarity.GREEN,
    Rarity.BLUE,
    Rarity.PURPLE,
    Rarity.GOLD,
    Rarity.RED,
    Rarity.RAINBOW,
)

HERO_START_X = 0.0
HERO_GROUND_Y = 220.0
HERO_WALK_SPEED = 38.0
HERO_COMBAT_WALK_SPEED = 10.0
HERO_ATTACK_INTERVAL = 1.0
HERO_ATTACK_SPEED = 1.0
HERO_ATTACK_RANGE = 68.0
HERO_HP_REGEN = 2.0
HERO_REVIVE_SECONDS = 3.0
HERO_DEATH_GOLD_LOSS_MIN_PCT = 0.20
HERO_DEATH_GOLD_LOSS_MAX_PCT = 0.50
MONSTER_ATTACK_INTERVAL = 1.35
MELEE_RANGE = 24.0
MONSTER_APPROACH_DISTANCE = 840.0
RIFT_MONSTER_APPROACH_DISTANCE = MONSTER_APPROACH_DISTANCE
BASE_DROP_CHANCE = 0.42
ENCOUNTER_MIN_DISTANCE = 70.0
ENCOUNTER_MAX_DISTANCE = 130.0
SCENE_CHUNK_WIDTH = 80.0
RIFT_MINIONS_BASE = 2
RIFT_MINIONS_MAX = 7
RIFT_MINION_DROP_BONUS = 0.08
RIFT_BOSS_DROP_BONUS = 0.34
RIFT_DROP_BONUS_PER_FLOOR = 0.025
TREASURE_MIMIC_CHANCE = 0.055
TREASURE_MIMIC_PITY_THRESHOLD = 8
TALENT_SCROLL_DROP_CHANCE = 0.045
