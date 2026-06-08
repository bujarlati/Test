"""Content factories for monsters, equipment, and forest scenery."""

from __future__ import annotations

import random
from uuid import uuid4

from .config import BASE_DROP_CHANCE, RARITY_CONFIG, RARITY_ORDER
from .models import Equipment, EquipmentSlot, Monster, Rarity


MONSTER_KINDS = (
    "forest_slime",
    "thorn_boar",
    "moss_imp",
    "wild_mushroom",
    "bark_guard",
)

DEEP_FOREST_MONSTER_KINDS = (
    "shadow_slime",
    "bramble_wolf",
    "gloom_imp",
    "venom_mushroom",
    "ancient_bark_guard",
)

RIFT_THEMES = ("cave", "sky", "castle")

RIFT_MONSTERS: dict[str, tuple[str, ...]] = {
    "cave": ("cave_bat", "crystal_lurker", "stone_crawler"),
    "sky": ("cloud_wisp", "storm_harpy", "sun_mote"),
    "castle": ("rust_guard", "hollow_knight", "cursed_squire"),
}

RIFT_BOSSES: dict[str, str] = {
    "cave": "cave_warden",
    "sky": "tempest_seraph",
    "castle": "throne_keeper",
}

RIFT_DECORATIONS: dict[str, tuple[str, ...]] = {
    "cave": ("stalagmite", "crystal", "dark_column", "glow_mushroom"),
    "sky": ("cloud_bank", "floating_rock", "sun_ruin", "wind_banner"),
    "castle": ("arch", "banner", "broken_wall", "torch"),
}

SPECIAL_RARITY_WEIGHTS: dict[Rarity, int] = {
    Rarity.WHITE: 6000,
    Rarity.GREEN: 2550,
    Rarity.BLUE: 1000,
    Rarity.PURPLE: 360,
    Rarity.GOLD: 85,
    Rarity.RED: 5,
    Rarity.RAINBOW: 0,
}

SPECIAL_SET_DEFS: tuple[dict[str, str], ...] = (
    {
        "id": "hoardbound",
        "name": "Hoardbound",
        "prefix": "Hoardbound",
        "bonus_name": "Greed Engine",
    },
    {
        "id": "luckseeker",
        "name": "Luckseeker",
        "prefix": "Luckseeker",
        "bonus_name": "Fortune Pulse",
    },
    {
        "id": "mimicbane",
        "name": "Mimicbane",
        "prefix": "Mimicbane",
        "bonus_name": "Chestbreaker Oath",
    },
)

SLOT_NAME_PARTS: dict[EquipmentSlot, tuple[str, ...]] = {
    EquipmentSlot.WEAPON: ("Axe", "Blade", "Spear", "Hatchet"),
    EquipmentSlot.HELMET: ("Cap", "Helm", "Mask", "Crown"),
    EquipmentSlot.ARMOR: ("Coat", "Vest", "Mail", "Guard"),
    EquipmentSlot.BOOTS: ("Boots", "Greaves", "Steps", "Treads"),
    EquipmentSlot.RING: ("Ring", "Charm", "Loop", "Band"),
}

SPECIAL_SLOT_PIECES: dict[EquipmentSlot, str] = {
    EquipmentSlot.WEAPON: "Fang",
    EquipmentSlot.HELMET: "Visage",
    EquipmentSlot.ARMOR: "Carapace",
    EquipmentSlot.BOOTS: "Strides",
    EquipmentSlot.RING: "Seal",
}

RARITY_NAME_PREFIX: dict[Rarity, tuple[str, ...]] = {
    Rarity.WHITE: ("Plain", "Worn", "Simple"),
    Rarity.GREEN: ("Fresh", "Rooted", "Hunter's"),
    Rarity.BLUE: ("Moonlit", "River", "Runed"),
    Rarity.PURPLE: ("Elder", "Spirit", "Twilight"),
    Rarity.GOLD: ("Sunforged", "Royal", "Ancient"),
    Rarity.RED: ("Mythic", "Dragonbone", "Worldroot"),
    Rarity.RAINBOW: ("Prismatic", "Celestial", "Chromaforge"),
}

SYSTEM_SHOP_DONATION_SKU = "donation"
SYSTEM_SHOP_DONATION_COST = 25000
SYSTEM_SHOP_RAINBOW_COSTS: dict[str, int] = {
    "rainbow_weapon": 1200000,
    "rainbow_helmet": 900000,
    "rainbow_armor": 1100000,
    "rainbow_boots": 850000,
    "rainbow_ring": 950000,
}
SYSTEM_SHOP_RAINBOW_SLOTS: dict[str, EquipmentSlot] = {
    "rainbow_weapon": EquipmentSlot.WEAPON,
    "rainbow_helmet": EquipmentSlot.HELMET,
    "rainbow_armor": EquipmentSlot.ARMOR,
    "rainbow_boots": EquipmentSlot.BOOTS,
    "rainbow_ring": EquipmentSlot.RING,
}


def roll_rarity(rng: random.Random) -> Rarity:
    total = sum(RARITY_CONFIG[rarity].weight for rarity in RARITY_ORDER)
    pick = rng.randint(1, total)
    current = 0
    for rarity in RARITY_ORDER:
        current += RARITY_CONFIG[rarity].weight
        if pick <= current:
            return rarity
    return Rarity.WHITE


def roll_special_rarity(rng: random.Random) -> Rarity:
    total = sum(SPECIAL_RARITY_WEIGHTS.values())
    pick = rng.randint(1, total)
    current = 0
    for rarity in RARITY_ORDER:
        current += SPECIAL_RARITY_WEIGHTS[rarity]
        if pick <= current:
            return rarity
    return Rarity.WHITE


def create_monster(
    level: int,
    x: float,
    y: float,
    rng: random.Random,
    forest_depth: int = 1,
) -> Monster:
    deep = forest_depth > 1
    kind = rng.choice(DEEP_FOREST_MONSTER_KINDS if deep else MONSTER_KINDS)
    threat = 1.0 + max(0, forest_depth - 1) * 0.32
    scale = (1 + level * 0.18) * threat
    hp = int(rng.randint(26, 38) * scale)
    attack = int(rng.randint(4, 7) * scale)
    defense = int((rng.randint(0, 3) + level * 0.35) * threat)
    return Monster(
        id=f"monster_{uuid4().hex[:10]}",
        kind=kind,
        level=level,
        max_hp=hp,
        hp=hp,
        attack=attack,
        defense=defense,
        exp_reward=int((12 + level * 6) * threat),
        gold_reward=int((rng.randint(4, 8) + level * 2) * threat),
        x=x,
        y=y,
        theme="deep_forest" if deep else "forest",
        threat=threat,
    )


def create_treasure_mimic(level: int, x: float, y: float, rng: random.Random) -> Monster:
    scale = 1.18 + level * 0.2
    hp = int(rng.randint(38, 52) * scale)
    attack = int(rng.randint(5, 8) * (1 + level * 0.12))
    defense = int(rng.randint(1, 3) + level * 0.45)
    return Monster(
        id=f"monster_{uuid4().hex[:10]}",
        kind="treasure_mimic",
        level=level,
        max_hp=hp,
        hp=hp,
        attack=attack,
        defense=defense,
        exp_reward=18 + level * 8,
        gold_reward=rng.randint(12, 22) + level * 4,
        x=x,
        y=y,
        role="treasure_mimic",
        theme="forest",
    )


def create_rift_monster(
    floor: int,
    theme: str,
    x: float,
    y: float,
    rng: random.Random,
    boss: bool = False,
) -> Monster:
    level = max(1, floor + rng.randint(0, max(1, floor // 3)))
    if boss:
        kind = RIFT_BOSSES[theme]
        scale = 1.35 + floor * 0.22
        hp = int(rng.randint(54, 68) * scale)
        attack = int(rng.randint(7, 10) * (1 + floor * 0.15))
        defense = int(2 + floor * 0.75)
        role = "boss"
        exp_reward = 38 + floor * 18
        gold_reward = rng.randint(18, 28) + floor * 7
    else:
        kind = rng.choice(RIFT_MONSTERS[theme])
        scale = 0.92 + floor * 0.15
        hp = int(rng.randint(24, 36) * scale)
        attack = int(rng.randint(4, 7) * (1 + floor * 0.1))
        defense = int(rng.randint(0, 2) + floor * 0.35)
        role = "minion"
        exp_reward = 16 + floor * 8
        gold_reward = rng.randint(6, 10) + floor * 3

    return Monster(
        id=f"monster_{uuid4().hex[:10]}",
        kind=kind,
        level=level,
        max_hp=hp,
        hp=hp,
        attack=attack,
        defense=defense,
        exp_reward=exp_reward,
        gold_reward=gold_reward,
        x=x,
        y=y,
        role=role,
        theme=theme,
    )


def create_starter_weapon(owner_id: str) -> Equipment:
    return Equipment(
        id=f"starter_wooden_sword_{owner_id}",
        name="Starter Wooden Sword",
        slot=EquipmentSlot.WEAPON,
        rarity=Rarity.WHITE,
        level=1,
        attack=6,
        attack_speed=0.05,
        attack_range=4.0,
        weapon_type="blade",
        owner_id=owner_id,
        tradable=False,
    )


def generate_equipment(level: int, rng: random.Random) -> Equipment:
    rarity = roll_rarity(rng)
    config = RARITY_CONFIG[rarity]
    item_level = max(1, level + config.min_level_bonus + rng.randint(-1, 1))
    slot = rng.choice(tuple(EquipmentSlot))
    multiplier = config.power_multiplier
    base = max(1, item_level)

    attack = defense = max_hp = 0
    attack_speed = hp_regen = move_speed = attack_range = 0.0
    weapon_type = None
    if slot == EquipmentSlot.WEAPON:
        attack = int((5 + base * 2) * multiplier)
        weapon_type = rng.choice(("axe", "blade", "spear"))
        attack_range = {"axe": 8.0, "blade": 4.0, "spear": 18.0}[weapon_type]
        attack_speed = {"axe": 0.04, "blade": 0.18, "spear": 0.08}[weapon_type]
    elif slot == EquipmentSlot.HELMET:
        defense = int((2 + base) * multiplier)
        max_hp = int((5 + base * 2) * multiplier)
    elif slot == EquipmentSlot.ARMOR:
        defense = int((4 + base * 2) * multiplier)
        max_hp = int((10 + base * 3) * multiplier)
    elif slot == EquipmentSlot.BOOTS:
        defense = int((1 + base) * multiplier)
        max_hp = int((3 + base) * multiplier)
        hp_regen = round(0.35 * multiplier, 2)
        move_speed = round(0.045 * multiplier, 3)
    elif slot == EquipmentSlot.RING:
        attack = int((1 + base) * multiplier)
        max_hp = int((6 + base * 2) * multiplier)
        attack_speed = round(0.09 * multiplier, 2)

    prefix = rng.choice(RARITY_NAME_PREFIX[rarity])
    noun = rng.choice(SLOT_NAME_PARTS[slot])
    return Equipment(
        id=f"item_{uuid4().hex[:12]}",
        name=f"{prefix} {noun} Lv.{item_level}",
        slot=slot,
        rarity=rarity,
        level=item_level,
        attack=attack,
        defense=defense,
        max_hp=max_hp,
        attack_speed=attack_speed,
        hp_regen=hp_regen,
        move_speed=move_speed,
        attack_range=attack_range,
        weapon_type=weapon_type,
        tradable=True,
    )


def generate_special_set_equipment(
    level: int,
    rng: random.Random,
    rarity: Rarity | None = None,
) -> Equipment:
    rolled_rarity = rarity or roll_special_rarity(rng)
    config = RARITY_CONFIG[rolled_rarity]
    set_def = rng.choice(SPECIAL_SET_DEFS)
    slot = rng.choice(tuple(EquipmentSlot))
    item_level = max(1, level + config.min_level_bonus + rng.randint(0, 2))
    multiplier = config.power_multiplier * 1.12
    base = max(1, item_level)

    attack = defense = max_hp = 0
    attack_speed = hp_regen = move_speed = attack_range = 0.0
    weapon_type = None
    if slot == EquipmentSlot.WEAPON:
        attack = int((7 + base * 2.4) * multiplier)
        weapon_type = rng.choice(("axe", "blade", "spear"))
        attack_range = {"axe": 10.0, "blade": 6.0, "spear": 22.0}[weapon_type]
        attack_speed = {"axe": 0.06, "blade": 0.22, "spear": 0.1}[weapon_type]
    elif slot == EquipmentSlot.HELMET:
        defense = int((3 + base * 1.2) * multiplier)
        max_hp = int((7 + base * 2.4) * multiplier)
    elif slot == EquipmentSlot.ARMOR:
        defense = int((5 + base * 2.2) * multiplier)
        max_hp = int((14 + base * 3.5) * multiplier)
    elif slot == EquipmentSlot.BOOTS:
        defense = int((2 + base * 1.1) * multiplier)
        max_hp = int((6 + base * 1.8) * multiplier)
        hp_regen = round(0.48 * multiplier, 2)
        move_speed = round(0.065 * multiplier, 3)
    elif slot == EquipmentSlot.RING:
        attack = int((2 + base * 1.35) * multiplier)
        max_hp = int((10 + base * 2.4) * multiplier)
        attack_speed = round(0.12 * multiplier, 2)

    bonus_multiplier = config.power_multiplier
    set_bonus = {
        "name": set_def["bonus_name"],
        "pieces_required": 2,
        "attack": int((4 + base * 0.9) * bonus_multiplier),
        "defense": int((2 + base * 0.55) * bonus_multiplier),
        "max_hp": int((14 + base * 2.2) * bonus_multiplier),
    }
    piece = SPECIAL_SLOT_PIECES[slot]
    return Equipment(
        id=f"item_{uuid4().hex[:12]}",
        name=f"{set_def['prefix']} {piece} Lv.{item_level}",
        slot=slot,
        rarity=rolled_rarity,
        level=item_level,
        attack=attack,
        defense=defense,
        max_hp=max_hp,
        attack_speed=attack_speed,
        hp_regen=hp_regen,
        move_speed=move_speed,
        attack_range=attack_range,
        weapon_type=weapon_type,
        tradable=True,
        special=True,
        set_id=set_def["id"],
        set_name=set_def["name"],
        set_piece=piece,
        set_bonus=set_bonus,
    )


def system_shop_catalog(hero_level: int = 1) -> list[dict[str, object]]:
    item_level = max(20, hero_level + RARITY_CONFIG[Rarity.RAINBOW].min_level_bonus + 8)
    catalog: list[dict[str, object]] = [
        {
            "sku": SYSTEM_SHOP_DONATION_SKU,
            "name": "Donation Sigil",
            "kind": "donation",
            "price": SYSTEM_SHOP_DONATION_COST,
            "description": "A rare offering. Five can unlock another talent after every current talent becomes mythic.",
        }
    ]
    slot_names = {
        EquipmentSlot.WEAPON: "Prismatic Blade",
        EquipmentSlot.HELMET: "Celestial Halo",
        EquipmentSlot.ARMOR: "Chromaforge Mantle",
        EquipmentSlot.BOOTS: "Astral Ground Aura",
        EquipmentSlot.RING: "Dragonlight Familiar",
    }
    for sku, slot in SYSTEM_SHOP_RAINBOW_SLOTS.items():
        catalog.append(
            {
                "sku": sku,
                "name": f"{slot_names[slot]} Lv.{item_level}",
                "kind": "equipment",
                "slot": slot.value,
                "rarity": Rarity.RAINBOW.value,
                "level": item_level,
                "price": SYSTEM_SHOP_RAINBOW_COSTS[sku],
                "description": "System-only rainbow equipment with stronger stats and brighter effects than red gear.",
            }
        )
    return catalog


def generate_system_shop_equipment(
    sku: str,
    hero_level: int,
    rng: random.Random,
    owner_id: str | None = None,
) -> Equipment:
    if sku not in SYSTEM_SHOP_RAINBOW_SLOTS:
        raise KeyError(f"unknown system shop equipment sku: {sku}")

    slot = SYSTEM_SHOP_RAINBOW_SLOTS[sku]
    config = RARITY_CONFIG[Rarity.RAINBOW]
    item_level = max(20, hero_level + config.min_level_bonus + 8)
    multiplier = config.power_multiplier * 1.45
    base = max(1, item_level)

    attack = defense = max_hp = 0
    attack_speed = hp_regen = move_speed = attack_range = 0.0
    weapon_type = None
    if slot == EquipmentSlot.WEAPON:
        attack = int((9 + base * 2.7) * multiplier)
        weapon_type = rng.choice(("blade", "spear"))
        attack_range = {"blade": 8.0, "spear": 24.0}[weapon_type]
        attack_speed = {"blade": 0.28, "spear": 0.14}[weapon_type]
    elif slot == EquipmentSlot.HELMET:
        defense = int((4 + base * 1.35) * multiplier)
        max_hp = int((10 + base * 2.6) * multiplier)
    elif slot == EquipmentSlot.ARMOR:
        defense = int((7 + base * 2.35) * multiplier)
        max_hp = int((18 + base * 3.9) * multiplier)
    elif slot == EquipmentSlot.BOOTS:
        defense = int((3 + base * 1.2) * multiplier)
        max_hp = int((8 + base * 2.0) * multiplier)
        hp_regen = round(0.7 * multiplier, 2)
        move_speed = round(0.09 * multiplier, 3)
    elif slot == EquipmentSlot.RING:
        attack = int((3 + base * 1.55) * multiplier)
        max_hp = int((12 + base * 2.6) * multiplier)
        attack_speed = round(0.16 * multiplier, 2)

    slot_names = {
        EquipmentSlot.WEAPON: ("Prismatic Blade", "Radiant Edge"),
        EquipmentSlot.HELMET: ("Celestial Halo", "Aurora Crown"),
        EquipmentSlot.ARMOR: ("Chromaforge Mantle", "Dragonlight Mail"),
        EquipmentSlot.BOOTS: ("Astral Ground Aura", "Starwake Field"),
        EquipmentSlot.RING: ("Dragonlight Familiar", "Prismatic Companion"),
    }
    set_bonus = {
        "name": "Rainbow Ascension",
        "pieces_required": 2,
        "attack": int((8 + base) * config.power_multiplier),
        "defense": int((5 + base * 0.7) * config.power_multiplier),
        "max_hp": int((22 + base * 2.6) * config.power_multiplier),
    }
    return Equipment(
        id=f"item_{uuid4().hex[:12]}",
        name=f"{rng.choice(slot_names[slot])} Lv.{item_level}",
        slot=slot,
        rarity=Rarity.RAINBOW,
        level=item_level,
        attack=attack,
        defense=defense,
        max_hp=max_hp,
        attack_speed=attack_speed,
        hp_regen=hp_regen,
        move_speed=move_speed,
        attack_range=attack_range,
        weapon_type=weapon_type,
        owner_id=owner_id,
        tradable=True,
        special=True,
        set_id="rainbow_ascension",
        set_name="Rainbow Ascension",
        set_piece=SPECIAL_SLOT_PIECES[slot],
        set_bonus=set_bonus,
    )


def maybe_drop_equipment(
    level: int,
    rng: random.Random,
    chance_bonus: float = 0.0,
) -> Equipment | None:
    chance = min(0.95, BASE_DROP_CHANCE + chance_bonus)
    if rng.random() > chance:
        return None
    return generate_equipment(level, rng)


def create_decoration(
    index: int,
    x: float,
    rng: random.Random,
    forest_depth: int = 1,
) -> dict[str, object]:
    if forest_depth > 1:
        kind = rng.choice((
            "pine",
            "pine",
            "oak",
            "dark_pine",
            "bramble",
            "shadow_fern",
            "mushroom_cluster",
        ))
        layer = "back" if kind in {"pine", "oak", "dark_pine"} and rng.random() < 0.78 else "front"
        scale_min, scale_max = 0.95, 1.65
    else:
        kind = rng.choice(("pine", "oak", "fern", "stump", "mushroom_cluster"))
        layer = "back" if kind in {"pine", "oak"} and rng.random() < 0.65 else "front"
        scale_min, scale_max = 0.75, 1.35
    return {
        "id": f"decor_{index}",
        "kind": kind,
        "layer": layer,
        "x": round(x + rng.uniform(-18, 18), 2),
        "y": 224 if layer == "front" else 210,
        "scale": round(rng.uniform(scale_min, scale_max), 2),
        "forest_depth": forest_depth,
    }


def create_rift_decoration(
    theme: str,
    index: int,
    x: float,
    rng: random.Random,
) -> dict[str, object]:
    kind = rng.choice(RIFT_DECORATIONS[theme])
    layer = "back" if rng.random() < 0.58 else "front"
    return {
        "id": f"rift_decor_{theme}_{index}",
        "kind": kind,
        "layer": layer,
        "x": round(x + rng.uniform(-22, 22), 2),
        "y": 224 if layer == "front" else 204,
        "scale": round(rng.uniform(0.75, 1.45), 2),
        "theme": theme,
    }
