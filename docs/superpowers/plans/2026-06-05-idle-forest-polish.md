# Idle Forest Polish Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add smooth frontend animation, readable combat spacing, attack speed and regeneration stats, and a local login/character creation flow.

**Architecture:** Keep Python as the game-state authority and make the browser responsible for interpolation and presentation. Add lightweight in-memory profile endpoints plus localStorage persistence so the future server account system can replace the storage layer without rewriting the UI flow.

**Tech Stack:** Python stdlib HTTP server, unittest, vanilla JavaScript, Canvas, CSS.

---

### Task 1: Backend Combat Stats And Spacing

**Files:**
- Modify: `idle_forest/config.py`
- Modify: `idle_forest/models.py`
- Modify: `idle_forest/engine.py`
- Test: `tests/test_engine.py`

- [ ] Write failing tests:
  - `test_monster_spawns_ahead_beyond_attack_range`
  - `test_hero_waits_to_attack_until_inside_weapon_range`
  - `test_attack_speed_controls_attack_interval`
  - `test_hp_regen_controls_travel_healing`
- [ ] Run `python -m unittest tests.test_engine.GameEngineTests.test_monster_spawns_ahead_beyond_attack_range -v` and confirm failure.
- [ ] Add constants for default attack range, spawn approach distance, base attack speed, and base hp regen.
- [ ] Add Hero properties `attack_speed`, `attack_interval`, `attack_range`, and `hp_regen`.
- [ ] Spawn monsters at `hero.x + MONSTER_APPROACH_DISTANCE`.
- [ ] In combat, move the hero until `distance <= hero.attack_range`, then process hero and monster attacks.
- [ ] Use `hero.attack_interval` instead of a fixed attack interval.
- [ ] Use `hero.hp_regen` for travel healing.
- [ ] Add combat metadata to `hero.to_dict()` and scene entities.
- [ ] Run full `python -m unittest discover -v`.

### Task 2: Profile And Character Creation API

**Files:**
- Modify: `idle_forest/engine.py`
- Modify: `server.py`
- Test: `tests/test_engine.py`

- [ ] Write failing tests:
  - `test_engine_accepts_character_name_gender_and_talents`
  - `test_profile_rolls_are_limited_to_three`
- [ ] Add optional GameEngine constructor args `hero_name`, `hero_gender`, `starting_talents`.
- [ ] Include `gender` in `Hero` and `hero.to_dict()`.
- [ ] Add server module profile state for draft name, gender, roll count, rolled talents, and confirmed character.
- [ ] Add `GET /profile`, `POST /profile/roll`, `POST /profile/confirm`, and `POST /profile/clear`.
- [ ] Confirming a profile creates `GameEngine(seed=11, hero_name=..., hero_gender=..., starting_talents=...)`.
- [ ] Run profile endpoint smoke checks with local HTTP requests.

### Task 3: Frontend Login, Character Creation, And Stats

**Files:**
- Modify: `web/index.html`
- Modify: `web/styles.css`
- Modify: `web/app.js`

- [ ] Add login/create-character overlay before the main app.
- [ ] Add name input, male/female segmented buttons, roll button, confirm button, and three talent cards.
- [ ] Store confirmed character in localStorage.
- [ ] On load, show creation UI if no local character exists; otherwise call `/profile/confirm` or `/snapshot`.
- [ ] Add attack speed and regeneration stat cells.
- [ ] Add a "new character" action that clears localStorage and `/profile/clear`.
- [ ] Keep text short and control-like; avoid instructional copy inside the running game surface.

### Task 4: Frontend Smoothing And Combat Presentation

**Files:**
- Modify: `web/app.js`
- Modify: `web/styles.css`

- [ ] Keep previous and current snapshots with timestamps.
- [ ] Interpolate hero and monster positions in `renderScene`.
- [ ] Replace frame-count animation timing with timestamp-based animation.
- [ ] Draw weapon range and a swing arc during combat.
- [ ] Draw equipped weapon variants from `hero.equipped.weapon`.
- [ ] Make monster approach visually from the right instead of appearing on top of the hero.
- [ ] Keep canvas dimensions stable on desktop and mobile.

### Task 5: Verification

**Files:**
- No planned source edits.

- [ ] Run `python -m unittest discover -v`.
- [ ] Restart the local server.
- [ ] Verify `GET /`, `GET /snapshot`, profile roll, profile confirm, and `POST /tick`.
- [ ] Open the app in the browser when available and confirm the creation flow reaches the main game.
- [ ] Check browser console errors if browser tooling is available.
- [ ] Confirm `git status --short --branch` only contains intended files.

## Self-Review

Spec coverage: combat spacing, smooth animation, stats, login/creation, local storage, and future server migration path are each covered by tasks.

Placeholder scan: no placeholder-only tasks remain.

Type consistency: planned fields use `attack_speed`, `attack_interval`, `attack_range`, `hp_regen`, `gender`, and `talents` consistently.
