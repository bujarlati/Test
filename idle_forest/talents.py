# -*- coding: utf-8 -*-
"""Talent catalog generation and rolls."""

from __future__ import annotations

import random
from dataclasses import dataclass

from .models import Talent, TalentTier


@dataclass(frozen=True)
class TalentTierConfig:
    label: str
    weight: int
    power: float


TALENT_TIER_CONFIG: dict[TalentTier, TalentTierConfig] = {
    TalentTier.COMMON: TalentTierConfig("普通", 6200, 1.00),
    TalentTier.UNCOMMON: TalentTierConfig("优良", 2500, 1.45),
    TalentTier.EXCELLENT: TalentTierConfig("卓越", 900, 2.05),
    TalentTier.RARE: TalentTierConfig("罕见", 320, 2.85),
    TalentTier.TRANSCENDENT: TalentTierConfig("超凡", 70, 4.05),
    TalentTier.MYTHIC: TalentTierConfig("绝世", 10, 5.80),
}

TALENT_TIER_ORDER: tuple[TalentTier, ...] = (
    TalentTier.COMMON,
    TalentTier.UNCOMMON,
    TalentTier.EXCELLENT,
    TalentTier.RARE,
    TalentTier.TRANSCENDENT,
    TalentTier.MYTHIC,
)

TALENT_PREFIXES: dict[TalentTier, tuple[str, ...]] = {
    TalentTier.COMMON: (
        "粗砺",
        "晨露",
        "林风",
        "土纹",
        "旅人",
        "铁叶",
        "旧誓",
        "萤火",
        "苔痕",
        "木心",
        "灰羽",
        "浅泉",
        "草蛇",
        "石芽",
        "微光",
    ),
    TalentTier.UNCOMMON: (
        "青岚",
        "银叶",
        "赤炉",
        "星尘",
        "潮汐",
        "霜枝",
        "迅影",
        "坚盾",
        "猎月",
        "灵泉",
        "松歌",
        "云径",
        "烁金",
        "远山",
        "鸣雷",
    ),
    TalentTier.EXCELLENT: (
        "苍穹",
        "曜石",
        "龙鳞",
        "秘银",
        "幽篁",
        "星火",
        "月蚀",
        "风暴",
        "圣泉",
        "裂岩",
        "霜狼",
        "金枝",
        "灵鹿",
        "荒歌",
        "逐日",
    ),
    TalentTier.RARE: (
        "王庭",
        "深渊",
        "神木",
        "天火",
        "黑曜",
        "星界",
        "古龙",
        "不灭",
        "回响",
        "命轮",
        "暮色",
        "赤冕",
        "白塔",
        "永夜",
        "破晓",
    ),
    TalentTier.TRANSCENDENT: (
        "太初",
        "万象",
        "虚空",
        "无垢",
        "天启",
        "星律",
        "圣痕",
        "龙皇",
        "神谕",
        "魂渊",
        "寰宇",
        "轮回",
        "炽天",
        "玄冥",
        "不朽",
    ),
    TalentTier.MYTHIC: (
        "绝世",
        "创世",
        "终焉",
        "无上",
        "命运",
        "永恒",
        "诸神",
        "太虚",
        "鸿蒙",
        "星海",
        "天命",
        "神座",
        "九曜",
        "万古",
        "归墟",
    ),
}

TALENT_ARCHETYPES: tuple[dict[str, object], ...] = (
    {
        "id": "rock_defense",
        "name": "坚如磐石",
        "effect": "defense_pct",
        "base": 0.10,
        "description": "防御力提升 {value}%。",
    },
    {
        "id": "battle_heart",
        "name": "战意涌动",
        "effect": "attack_pct",
        "base": 0.08,
        "description": "攻击力提升 {value}%。",
    },
    {
        "id": "living_vigor",
        "name": "生生不息",
        "effect": "max_hp_pct",
        "base": 0.10,
        "description": "生命上限提升 {value}%。",
    },
    {
        "id": "swift_step",
        "name": "疾风步",
        "effect": "move_speed_pct",
        "base": 0.07,
        "description": "移动速度提升 {value}%。",
    },
    {
        "id": "treasure_sense",
        "name": "寻宝直觉",
        "effect": "drop_rate_pct",
        "base": 0.045,
        "description": "装备掉宝率提升 {value}%。",
    },
    {
        "id": "golden_touch",
        "name": "聚财手",
        "effect": "gold_pct",
        "base": 0.10,
        "description": "金币获取提升 {value}%。",
    },
    {
        "id": "clear_mind",
        "name": "悟性通明",
        "effect": "exp_pct",
        "base": 0.08,
        "description": "经验获取提升 {value}%。",
    },
    {
        "id": "mimic_scent",
        "name": "宝箱嗅觉",
        "effect": "treasure_mimic_chance_pct",
        "base": 0.018,
        "description": "宝箱怪遭遇率提升 {value}%。",
    },
    {
        "id": "rift_grace",
        "name": "秘境眷顾",
        "effect": "rift_drop_rate_pct",
        "base": 0.055,
        "description": "秘境掉宝率提升 {value}%。",
    },
    {
        "id": "chosen_one",
        "name": "天命加身",
        "effect": "all_stats_pct",
        "base": 0.035,
        "description": "攻击、防御、生命提升 {value}%。",
    },
)


def build_talent_catalog() -> dict[TalentTier, list[Talent]]:
    catalog: dict[TalentTier, list[Talent]] = {}
    for tier in TALENT_TIER_ORDER:
        config = TALENT_TIER_CONFIG[tier]
        talents: list[Talent] = []
        for prefix_index, prefix in enumerate(TALENT_PREFIXES[tier], start=1):
            for archetype_index, archetype in enumerate(TALENT_ARCHETYPES, start=1):
                value = round(float(archetype["base"]) * config.power, 4)
                display_value = round(value * 100, 1)
                talent_id = f"{tier.value}_{prefix_index:02d}_{archetype['id']}_{archetype_index:02d}"
                name = f"{prefix}{archetype['name']}"
                talents.append(
                    Talent(
                        id=talent_id,
                        name=name,
                        tier=tier,
                        effects={str(archetype["effect"]): value},
                        description=str(archetype["description"]).format(value=display_value),
                    )
                )
        catalog[tier] = talents
    return catalog


TALENT_CATALOG = build_talent_catalog()


def roll_talent_tier(rng: random.Random) -> TalentTier:
    total = sum(TALENT_TIER_CONFIG[tier].weight for tier in TALENT_TIER_ORDER)
    pick = rng.randint(1, total)
    current = 0
    for tier in TALENT_TIER_ORDER:
        current += TALENT_TIER_CONFIG[tier].weight
        if pick <= current:
            return tier
    return TalentTier.COMMON


def roll_talent(rng: random.Random, tier: TalentTier | None = None) -> Talent:
    selected_tier = tier or roll_talent_tier(rng)
    return rng.choice(TALENT_CATALOG[selected_tier])


def roll_starting_talents(rng: random.Random, count: int = 3) -> list[Talent]:
    talents: list[Talent] = []
    seen: set[str] = set()
    while len(talents) < count:
        talent = roll_talent(rng)
        if talent.id in seen:
            continue
        seen.add(talent.id)
        talents.append(talent)
    return talents


def next_tier(tier: TalentTier) -> TalentTier | None:
    index = TALENT_TIER_ORDER.index(tier)
    if index >= len(TALENT_TIER_ORDER) - 1:
        return None
    return TALENT_TIER_ORDER[index + 1]


def evolve_talent_roll(talent: Talent, rng: random.Random) -> Talent:
    target_tier = next_tier(talent.tier)
    if target_tier is None:
        raise ValueError("mythic talent cannot evolve")
    return roll_talent(rng, target_tier)
