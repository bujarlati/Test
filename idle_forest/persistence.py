"""Local JSON persistence for the idle forest prototype."""

from __future__ import annotations

from collections import deque
from contextlib import closing
import hashlib
import hmac
import json
from pathlib import Path
import secrets
import sqlite3
from typing import Any
import uuid

from .engine import GameEngine
from .market import Market, MarketListing
from .models import Equipment, EquipmentSlot, Event, Hero, Monster, Rarity, RiftRun, Talent, TalentTier


SAVE_VERSION = 1
MAX_CHARACTERS_PER_ACCOUNT = 3
PASSWORD_HASH_ITERATIONS = 160_000


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
        "auto_rift": engine.auto_rift,
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
    engine.auto_rift = bool(data.get("auto_rift", False))
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
        "donations": hero.donations,
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
        donations=int(data.get("donations", 0)),
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
        "move_speed": item.move_speed,
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
        move_speed=float(data.get("move_speed", 0.0)),
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


class SQLiteSaveStore:
    def __init__(
        self,
        path: Path,
        legacy_store: SaveStore | None = None,
        profile_id: str = "local",
    ) -> None:
        self.path = path
        self.legacy_store = legacy_store
        self.profile_id = profile_id

    def save(self, profile: dict[str, Any], engine: GameEngine) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with closing(self._connect()) as connection:
            self._ensure_schema(connection)
            previous_gold = self._previous_gold(connection, engine.hero.id)
            connection.execute("BEGIN")
            self._save_profile(connection, profile)
            self._save_engine_blob(connection, engine)
            self._sync_character(connection, engine)
            self._sync_items(connection, engine)
            self._sync_market(connection, engine)
            self._sync_gold_ledger(connection, engine, previous_gold)
            connection.commit()

    def load(self) -> dict[str, Any] | None:
        if self.path.exists():
            with closing(self._connect()) as connection:
                self._ensure_schema(connection)
                row = connection.execute(
                    "SELECT profile_json, engine_json FROM engine_saves WHERE profile_id = ?",
                    (self.profile_id,),
                ).fetchone()
                if row is not None:
                    return {
                        "profile": json.loads(row["profile_json"]),
                        "engine": engine_from_save(json.loads(row["engine_json"])),
                    }

        legacy = self.legacy_store.load() if self.legacy_store is not None else None
        if legacy is None:
            return None
        self.save(legacy["profile"], legacy["engine"])
        return legacy

    def delete(self) -> None:
        self.path.unlink(missing_ok=True)
        self.path.with_suffix(f"{self.path.suffix}-wal").unlink(missing_ok=True)
        self.path.with_suffix(f"{self.path.suffix}-shm").unlink(missing_ok=True)
        if self.legacy_store is not None:
            self.legacy_store.delete()

    def create_account(self, username: str, password: str) -> dict[str, Any]:
        clean_username = _clean_username(username)
        salt = secrets.token_hex(16)
        account_id = f"acct_{uuid.uuid4().hex}"
        with closing(self._connect()) as connection:
            self._ensure_schema(connection)
            try:
                connection.execute(
                    """
                    INSERT INTO accounts (
                        account_id, username, password_salt, password_hash, created_at, updated_at
                    )
                    VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                    """,
                    (
                        account_id,
                        clean_username,
                        salt,
                        _hash_password(password, salt),
                    ),
                )
                connection.commit()
            except sqlite3.IntegrityError as exc:
                raise ValueError("username already exists") from exc
        return {"account_id": account_id, "username": clean_username}

    def login_account(self, username: str, password: str) -> dict[str, Any]:
        clean_username = _clean_username(username)
        with closing(self._connect()) as connection:
            self._ensure_schema(connection)
            account = connection.execute(
                """
                SELECT account_id, username, password_salt, password_hash
                FROM accounts
                WHERE username = ?
                """,
                (clean_username,),
            ).fetchone()
            if account is None or not _verify_password(
                password,
                str(account["password_salt"]),
                str(account["password_hash"]),
            ):
                raise ValueError("invalid username or password")

            token = secrets.token_urlsafe(32)
            active_character_id = self._first_active_character_id(connection, str(account["account_id"]))
            connection.execute(
                """
                INSERT INTO sessions (
                    token, account_id, active_character_id, created_at, last_seen_at
                )
                VALUES (?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                """,
                (token, str(account["account_id"]), active_character_id),
            )
            connection.commit()

        return {
            "session_token": token,
            "account": {
                "account_id": str(account["account_id"]),
                "username": str(account["username"]),
            },
            "characters": self.list_characters(str(account["account_id"])),
            "active_character_id": active_character_id,
        }

    def resolve_session(self, token: str) -> dict[str, Any]:
        clean_token = str(token or "").strip()
        if not clean_token:
            raise ValueError("login required")
        with closing(self._connect()) as connection:
            self._ensure_schema(connection)
            row = connection.execute(
                """
                SELECT
                    sessions.token,
                    sessions.account_id,
                    sessions.active_character_id,
                    accounts.username
                FROM sessions
                JOIN accounts ON accounts.account_id = sessions.account_id
                WHERE sessions.token = ?
                """,
                (clean_token,),
            ).fetchone()
            if row is None:
                raise ValueError("login required")
            connection.execute(
                "UPDATE sessions SET last_seen_at = CURRENT_TIMESTAMP WHERE token = ?",
                (clean_token,),
            )
            connection.commit()
            return {
                "session_token": clean_token,
                "account_id": str(row["account_id"]),
                "username": str(row["username"]),
                "active_character_id": row["active_character_id"],
            }

    def set_active_character(self, token: str, character_id: str) -> dict[str, Any]:
        session = self.resolve_session(token)
        with closing(self._connect()) as connection:
            self._ensure_schema(connection)
            character = self._character_row(connection, session["account_id"], character_id)
            if character is None:
                raise ValueError("character not found")
            connection.execute(
                """
                UPDATE sessions
                SET active_character_id = ?, last_seen_at = CURRENT_TIMESTAMP
                WHERE token = ?
                """,
                (character_id, session["session_token"]),
            )
            connection.commit()
        return self.resolve_session(token)

    def create_character(
        self,
        account_id: str,
        profile: dict[str, Any],
        engine: GameEngine,
    ) -> dict[str, Any]:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        character_id = str(engine.hero.id)
        if not character_id:
            raise ValueError("character id is required")
        with closing(self._connect()) as connection:
            self._ensure_schema(connection)
            self._require_account(connection, account_id)
            slot_index = self._next_character_slot(connection, account_id)
            try:
                connection.execute(
                    """
                    INSERT INTO character_slots (
                        character_id, account_id, slot_index, name, gender,
                        profile_id, created_at, updated_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                    """,
                    (
                        character_id,
                        account_id,
                        slot_index,
                        engine.hero.name,
                        engine.hero.gender,
                        character_id,
                    ),
                )
                connection.commit()
            except sqlite3.IntegrityError as exc:
                raise ValueError("character slot is already occupied") from exc

        self.save_character(character_id, profile, engine)
        with closing(self._connect()) as connection:
            self._ensure_schema(connection)
            row = self._character_row(connection, account_id, character_id)
            if row is None:
                raise ValueError("character not found")
            return row

    def save_character(self, character_id: str, profile: dict[str, Any], engine: GameEngine) -> None:
        SQLiteSaveStore(self.path, profile_id=character_id).save(profile, engine)
        with closing(self._connect()) as connection:
            self._ensure_schema(connection)
            connection.execute(
                """
                UPDATE character_slots
                SET name = ?, gender = ?, updated_at = CURRENT_TIMESTAMP
                WHERE character_id = ? AND deleted_at IS NULL
                """,
                (engine.hero.name, engine.hero.gender, character_id),
            )
            connection.commit()

    def load_character(self, character_id: str) -> dict[str, Any]:
        loaded = SQLiteSaveStore(self.path, profile_id=character_id).load()
        if loaded is None:
            raise ValueError("character save not found")
        return loaded

    def market_snapshot(self, profile_id: str | None = None) -> dict[str, Any]:
        if not self.path.exists():
            return {"active": [], "history": []}
        with closing(self._connect()) as connection:
            self._ensure_schema(connection)
            rows = connection.execute(
                """
                SELECT
                    listing_id, profile_id, item_id, seller_id, buyer_id, price,
                    active, created_tick, sold_tick, item_json
                FROM market_listings
                ORDER BY active DESC, updated_at DESC, created_tick DESC
                """
            ).fetchall()

        listings = [
            _market_listing_from_row(row).to_dict()
            for row in rows
            if _listing_visible_to_profile(row, profile_id)
        ]
        return {
            "active": [listing for listing in listings if listing["active"]],
            "history": listings,
        }

    def load_market_listing(self, listing_id: str) -> dict[str, Any]:
        with closing(self._connect()) as connection:
            self._ensure_schema(connection)
            row = connection.execute(
                """
                SELECT
                    listing_id, profile_id, item_id, seller_id, buyer_id, price,
                    active, created_tick, sold_tick, item_json
                FROM market_listings
                WHERE listing_id = ?
                """,
                (listing_id,),
            ).fetchone()
        if row is None:
            raise KeyError(f"listing not found: {listing_id}")
        return {
            "profile_id": str(row["profile_id"]),
            "listing": _market_listing_from_row(row),
        }

    def list_characters(self, account_id: str) -> list[dict[str, Any]]:
        with closing(self._connect()) as connection:
            self._ensure_schema(connection)
            rows = connection.execute(
                """
                SELECT character_id, account_id, slot_index, name, gender, profile_id
                FROM character_slots
                WHERE account_id = ? AND deleted_at IS NULL
                ORDER BY slot_index ASC
                """,
                (account_id,),
            ).fetchall()
            return [_character_to_dict(row) for row in rows]

    def delete_character(self, account_id: str, character_id: str) -> None:
        with closing(self._connect()) as connection:
            self._ensure_schema(connection)
            row = self._character_row(connection, account_id, character_id)
            if row is None:
                raise ValueError("character not found")
            connection.execute(
                """
                UPDATE character_slots
                SET deleted_at = CURRENT_TIMESTAMP, updated_at = CURRENT_TIMESTAMP
                WHERE account_id = ? AND character_id = ? AND deleted_at IS NULL
                """,
                (account_id, character_id),
            )
            connection.execute(
                """
                UPDATE sessions
                SET active_character_id = NULL, last_seen_at = CURRENT_TIMESTAMP
                WHERE account_id = ? AND active_character_id = ?
                """,
                (account_id, character_id),
            )
            connection.commit()

    def migrate_local_character_to_account(self, account_id: str) -> dict[str, Any] | None:
        if self.profile_id != "local":
            return None
        with closing(self._connect()) as connection:
            self._ensure_schema(connection)
            if self._first_active_character_id(connection, account_id) is not None:
                return None
        loaded = self.load()
        if loaded is None or not loaded["profile"].get("confirmed"):
            return None
        return self.create_character(account_id, loaded["profile"], loaded["engine"])

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def _ensure_schema(self, connection: sqlite3.Connection) -> None:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS profiles (
                profile_id TEXT PRIMARY KEY,
                confirmed_json TEXT,
                draft_json TEXT,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS engine_saves (
                profile_id TEXT PRIMARY KEY,
                version INTEGER NOT NULL,
                profile_json TEXT NOT NULL,
                engine_json TEXT NOT NULL,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (profile_id) REFERENCES profiles(profile_id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS characters (
                hero_id TEXT PRIMARY KEY,
                profile_id TEXT NOT NULL,
                name TEXT NOT NULL,
                gender TEXT NOT NULL,
                level INTEGER NOT NULL,
                gold INTEGER NOT NULL,
                forest_depth INTEGER NOT NULL,
                mode TEXT NOT NULL,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (profile_id) REFERENCES profiles(profile_id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS item_instances (
                item_id TEXT PRIMARY KEY,
                owner_id TEXT,
                location TEXT NOT NULL,
                slot TEXT NOT NULL,
                rarity TEXT NOT NULL,
                level INTEGER NOT NULL,
                score INTEGER NOT NULL,
                item_json TEXT NOT NULL,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS market_listings (
                listing_id TEXT PRIMARY KEY,
                item_id TEXT NOT NULL,
                seller_id TEXT NOT NULL,
                buyer_id TEXT,
                price INTEGER NOT NULL,
                active INTEGER NOT NULL,
                created_tick INTEGER NOT NULL,
                sold_tick INTEGER,
                item_json TEXT NOT NULL,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS gold_ledger (
                entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
                hero_id TEXT NOT NULL,
                delta INTEGER NOT NULL,
                reason TEXT NOT NULL,
                related_id TEXT,
                balance_after INTEGER NOT NULL,
                tick INTEGER NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS accounts (
                account_id TEXT PRIMARY KEY,
                username TEXT NOT NULL UNIQUE,
                password_salt TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS character_slots (
                character_id TEXT PRIMARY KEY,
                account_id TEXT NOT NULL,
                slot_index INTEGER NOT NULL,
                name TEXT NOT NULL,
                gender TEXT NOT NULL,
                profile_id TEXT NOT NULL,
                deleted_at TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (account_id) REFERENCES accounts(account_id) ON DELETE CASCADE
            );

            CREATE UNIQUE INDEX IF NOT EXISTS active_character_slots
            ON character_slots(account_id, slot_index)
            WHERE deleted_at IS NULL;

            CREATE TABLE IF NOT EXISTS sessions (
                token TEXT PRIMARY KEY,
                account_id TEXT NOT NULL,
                active_character_id TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                last_seen_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (account_id) REFERENCES accounts(account_id) ON DELETE CASCADE
            );
            """
        )
        self._ensure_column(connection, "item_instances", "profile_id", "TEXT NOT NULL DEFAULT 'local'")
        self._ensure_column(connection, "market_listings", "profile_id", "TEXT NOT NULL DEFAULT 'local'")

    def _save_profile(self, connection: sqlite3.Connection, profile: dict[str, Any]) -> None:
        connection.execute(
            """
            INSERT INTO profiles (profile_id, confirmed_json, draft_json, updated_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(profile_id) DO UPDATE SET
                confirmed_json = excluded.confirmed_json,
                draft_json = excluded.draft_json,
                updated_at = CURRENT_TIMESTAMP
            """,
            (
                self.profile_id,
                _json(profile.get("confirmed")),
                _json(profile.get("draft")),
            ),
        )

    def _save_engine_blob(self, connection: sqlite3.Connection, engine: GameEngine) -> None:
        connection.execute(
            """
            INSERT INTO engine_saves (profile_id, version, profile_json, engine_json, updated_at)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(profile_id) DO UPDATE SET
                version = excluded.version,
                profile_json = excluded.profile_json,
                engine_json = excluded.engine_json,
                updated_at = CURRENT_TIMESTAMP
            """,
            (
                self.profile_id,
                SAVE_VERSION,
                _json(self._profile_snapshot(connection)),
                _json(engine_to_save(engine)),
            ),
        )

    def _profile_snapshot(self, connection: sqlite3.Connection) -> dict[str, Any]:
        row = connection.execute(
            "SELECT confirmed_json, draft_json FROM profiles WHERE profile_id = ?",
            (self.profile_id,),
        ).fetchone()
        if row is None:
            return {"confirmed": None, "draft": None}
        return {
            "confirmed": json.loads(row["confirmed_json"]) if row["confirmed_json"] else None,
            "draft": json.loads(row["draft_json"]) if row["draft_json"] else None,
        }

    def _sync_character(self, connection: sqlite3.Connection, engine: GameEngine) -> None:
        connection.execute(
            """
            INSERT INTO characters (
                hero_id, profile_id, name, gender, level, gold, forest_depth, mode, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(hero_id) DO UPDATE SET
                profile_id = excluded.profile_id,
                name = excluded.name,
                gender = excluded.gender,
                level = excluded.level,
                gold = excluded.gold,
                forest_depth = excluded.forest_depth,
                mode = excluded.mode,
                updated_at = CURRENT_TIMESTAMP
            """,
            (
                engine.hero.id,
                self.profile_id,
                engine.hero.name,
                engine.hero.gender,
                engine.hero.level,
                engine.hero.gold,
                engine.forest_depth,
                engine.mode,
            ),
        )

    def _sync_items(self, connection: sqlite3.Connection, engine: GameEngine) -> None:
        connection.execute("DELETE FROM item_instances WHERE profile_id = ?", (self.profile_id,))
        seen: set[str] = set()
        for item in engine.hero.inventory:
            self._insert_item(connection, item, item.owner_id or engine.hero.id, "inventory", seen)
        for item in engine.hero.equipped.values():
            self._insert_item(connection, item, item.owner_id or engine.hero.id, "equipped", seen)
        for listing in engine.market.all_listings():
            self._insert_item(
                connection,
                listing.item,
                listing.item.owner_id or listing.buyer_id or listing.seller_id,
                "market",
                seen,
            )

    def _insert_item(
        self,
        connection: sqlite3.Connection,
        item: Equipment,
        owner_id: str | None,
        location: str,
        seen: set[str],
    ) -> None:
        if item.id in seen:
            return
        seen.add(item.id)
        connection.execute(
            """
            INSERT OR REPLACE INTO item_instances (
                item_id, profile_id, owner_id, location, slot, rarity, level, score, item_json, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """,
            (
                item.id,
                self.profile_id,
                owner_id,
                location,
                item.slot.value,
                item.rarity.value,
                item.level,
                item.score,
                _json(equipment_to_save(item)),
            ),
        )

    def _sync_market(self, connection: sqlite3.Connection, engine: GameEngine) -> None:
        connection.execute("DELETE FROM market_listings WHERE profile_id = ?", (self.profile_id,))
        for listing in engine.market.all_listings():
            connection.execute(
                """
                INSERT OR REPLACE INTO market_listings (
                    listing_id, profile_id, item_id, seller_id, buyer_id, price, active,
                    created_tick, sold_tick, item_json, updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                """,
                (
                    listing.id,
                    self.profile_id,
                    listing.item.id,
                    listing.seller_id,
                    listing.buyer_id,
                    listing.price,
                    1 if listing.active else 0,
                    listing.created_tick,
                    listing.sold_tick,
                    _json(equipment_to_save(listing.item)),
                ),
            )

    def _sync_gold_ledger(
        self,
        connection: sqlite3.Connection,
        engine: GameEngine,
        previous_gold: int | None,
    ) -> None:
        current_gold = engine.hero.gold
        if previous_gold == current_gold:
            return
        connection.execute(
            """
            INSERT INTO gold_ledger (
                hero_id, delta, reason, related_id, balance_after, tick
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                engine.hero.id,
                current_gold if previous_gold is None else current_gold - previous_gold,
                "initial_sync" if previous_gold is None else "sync",
                None,
                current_gold,
                engine.tick,
            ),
        )

    def _previous_gold(self, connection: sqlite3.Connection, hero_id: str) -> int | None:
        self._ensure_schema(connection)
        row = connection.execute(
            "SELECT gold FROM characters WHERE hero_id = ?",
            (hero_id,),
        ).fetchone()
        return None if row is None else int(row["gold"])

    def _require_account(self, connection: sqlite3.Connection, account_id: str) -> None:
        row = connection.execute(
            "SELECT account_id FROM accounts WHERE account_id = ?",
            (account_id,),
        ).fetchone()
        if row is None:
            raise ValueError("account not found")

    def _next_character_slot(self, connection: sqlite3.Connection, account_id: str) -> int:
        rows = connection.execute(
            """
            SELECT slot_index
            FROM character_slots
            WHERE account_id = ? AND deleted_at IS NULL
            """,
            (account_id,),
        ).fetchall()
        used = {int(row["slot_index"]) for row in rows}
        for slot_index in range(MAX_CHARACTERS_PER_ACCOUNT):
            if slot_index not in used:
                return slot_index
        raise ValueError("account already has three characters")

    def _first_active_character_id(
        self,
        connection: sqlite3.Connection,
        account_id: str,
    ) -> str | None:
        row = connection.execute(
            """
            SELECT character_id
            FROM character_slots
            WHERE account_id = ? AND deleted_at IS NULL
            ORDER BY slot_index ASC
            LIMIT 1
            """,
            (account_id,),
        ).fetchone()
        return None if row is None else str(row["character_id"])

    def _character_row(
        self,
        connection: sqlite3.Connection,
        account_id: str,
        character_id: str,
    ) -> dict[str, Any] | None:
        row = connection.execute(
            """
            SELECT character_id, account_id, slot_index, name, gender, profile_id
            FROM character_slots
            WHERE account_id = ? AND character_id = ? AND deleted_at IS NULL
            """,
            (account_id, character_id),
        ).fetchone()
        return None if row is None else _character_to_dict(row)

    def _ensure_column(
        self,
        connection: sqlite3.Connection,
        table_name: str,
        column_name: str,
        definition: str,
    ) -> None:
        columns = {
            str(row["name"])
            for row in connection.execute(f"PRAGMA table_info({table_name})").fetchall()
        }
        if column_name not in columns:
            connection.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {definition}")


def _tuple_state(value: Any) -> Any:
    if isinstance(value, list):
        return tuple(_tuple_state(item) for item in value)
    return value


def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def _clean_username(username: str) -> str:
    clean = str(username).strip()
    if not clean:
        raise ValueError("username is required")
    if len(clean) > 32:
        raise ValueError("username is too long")
    return clean


def _hash_password(password: str, salt: str) -> str:
    clean = str(password)
    if len(clean) < 4:
        raise ValueError("password must be at least four characters")
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        clean.encode("utf-8"),
        salt.encode("utf-8"),
        PASSWORD_HASH_ITERATIONS,
    )
    return digest.hex()


def _verify_password(password: str, salt: str, expected_hash: str) -> bool:
    try:
        actual_hash = _hash_password(password, salt)
    except ValueError:
        return False
    return hmac.compare_digest(actual_hash, expected_hash)


def _character_to_dict(row: sqlite3.Row) -> dict[str, Any]:
    return {
        "character_id": str(row["character_id"]),
        "account_id": str(row["account_id"]),
        "slot_index": int(row["slot_index"]),
        "name": str(row["name"]),
        "gender": str(row["gender"]),
        "profile_id": str(row["profile_id"]),
    }


def _market_listing_from_row(row: sqlite3.Row) -> MarketListing:
    return MarketListing(
        id=str(row["listing_id"]),
        item=equipment_from_save(json.loads(row["item_json"])),
        seller_id=str(row["seller_id"]),
        price=int(row["price"]),
        created_tick=int(row["created_tick"]),
        active=bool(row["active"]),
        buyer_id=row["buyer_id"],
        sold_tick=row["sold_tick"],
    )


def _listing_visible_to_profile(row: sqlite3.Row, profile_id: str | None) -> bool:
    seller_id = str(row["seller_id"])
    if profile_id is None:
        return True
    if not seller_id.startswith("npc_"):
        return True
    return str(row["profile_id"]) == profile_id
