# System Shop Recycle Donation Effects Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a system shop, rainbow equipment, equipment recycling, score-based own-listing sales, repeatable donation talent expansion, and Pixellab-powered premium talent effects.

**Architecture:** Extend the existing engine-first action pattern: `GameEngine` owns rules, `server.py` exposes POST endpoints and persistence, `web/app.js` renders controls and calls actions. Rainbow rarity is a normal `Rarity` value but only system-shop generated in this pass. Premium effects are static Pixellab pixel assets loaded through the existing cache-busted asset table and animated by the canvas renderer.

**Tech Stack:** Python stdlib game engine/server, SQLite persistence through existing save blobs, browser DOM + Canvas frontend, Pixellab API helper for transparent pixel effect assets, unittest.

---

### Task 1: Engine Economy Rules

**Files:**
- Modify: `idle_forest/models.py`
- Modify: `idle_forest/config.py`
- Modify: `idle_forest/content.py`
- Modify: `idle_forest/engine.py`
- Test: `tests/test_engine.py`

- [ ] **Step 1: Write failing engine tests**

Add tests for:

```python
def test_system_shop_sells_rainbow_equipment_stronger_than_red(self) -> None:
    engine = GameEngine(seed=201, starter_gold=250000)
    red = generate_special_set_equipment(20, engine.rng, rarity=Rarity.RED)
    bought = engine.buy_system_shop_item("rainbow_weapon")
    self.assertEqual(bought["purchase"]["item"]["rarity"], "rainbow")
    self.assertGreater(bought["purchase"]["item"]["score"], red.score)
    self.assertLess(engine.hero.gold, 250000)

def test_recycle_inventory_item_grants_score_gold(self) -> None:
    engine = GameEngine(seed=202, starter_gold=10)
    item = generate_equipment(8, engine.rng)
    item.owner_id = engine.hero.id
    engine.hero.inventory.append(item)
    result = engine.recycle_item(item.id)
    self.assertEqual(result["gold"], item.score)
    self.assertEqual(engine.hero.gold, 10 + item.score)
    self.assertNotIn(item.id, [owned.id for owned in engine.hero.inventory])

def test_sell_own_listing_uses_score_not_listing_price(self) -> None:
    engine = GameEngine(seed=203, starter_gold=0)
    item = generate_equipment(8, engine.rng)
    item.owner_id = engine.hero.id
    engine.hero.inventory.append(item)
    listing = engine.list_item(item.id, price=999999)
    result = engine.sell_own_listing_to_system(listing.id)
    self.assertEqual(result["gold"], item.score)
    self.assertEqual(engine.hero.gold, item.score)
```

- [ ] **Step 2: Verify RED**

Run: `python -m unittest tests.test_engine.GameEngineTests -v`

Expected: FAIL because `Rarity.RAINBOW`, `buy_system_shop_item`, `recycle_item`, and `sell_own_listing_to_system` do not exist.

- [ ] **Step 3: Implement minimal engine rules**

Add `RAINBOW` to `Rarity`, `RARITY_APPEARANCE`, `RARITY_CONFIG`, and `RARITY_ORDER`. Add shop constants and helpers in `content.py`:

```python
SYSTEM_SHOP_DONATION_SKU = "donation_5"
SYSTEM_SHOP_RAINBOW_SKUS = ("rainbow_weapon", "rainbow_helmet", "rainbow_armor", "rainbow_boots", "rainbow_ring")
```

Add `Hero.donations: int = 0` and expose it plus `can_expand_talent` in `Hero.to_dict()`.

Add `GameEngine` methods:

```python
def buy_system_shop_item(self, sku: str) -> dict[str, Any]: ...
def recycle_item(self, item_id: str) -> dict[str, Any]: ...
def recycle_all_inventory(self) -> dict[str, Any]: ...
def sell_own_listing_to_system(self, listing_id: str) -> dict[str, Any]: ...
def donate_for_talent(self) -> dict[str, Any]: ...
```

Use `score` for recycle and own-listing sale gold. Donation SKU grants 5 donations. Rainbow shop SKUs generate non-drop rainbow equipment with high price.

- [ ] **Step 4: Verify GREEN**

Run: `python -m unittest tests.test_engine.GameEngineTests -v`

Expected: PASS.

### Task 2: Server Routes And Account Persistence

**Files:**
- Modify: `server.py`
- Modify: `idle_forest/persistence.py`
- Test: `tests/test_server_accounts.py`

- [ ] **Step 1: Write failing server tests**

Add authenticated tests for `/shop/buy`, `/inventory/recycle`, `/inventory/recycle-all`, `/market/sell-own`, and `/talent/donate`. Include a cross-account sell-own rejection test.

- [ ] **Step 2: Verify RED**

Run: `python -m unittest tests.test_server_accounts -v`

Expected: FAIL with 404 or missing route errors.

- [ ] **Step 3: Implement routes**

Follow existing POST action pattern: pick active runtime if logged in, mutate engine, save via `_save_character_runtime`, and return result plus snapshot.

Persist new `Hero.donations` through engine save blob by updating `hero_to_save` / `hero_from_save` if needed.

- [ ] **Step 4: Verify GREEN**

Run: `python -m unittest tests.test_server_accounts -v`

Expected: PASS.

### Task 3: Frontend UI Wiring

**Files:**
- Modify: `web/index.html`
- Modify: `web/app.js`
- Modify: `web/styles.css`
- Modify: `web/assets/pixel/v1/manifests/assets.json`
- Test: `tests/test_web_static.py`

- [ ] **Step 1: Write failing static tests**

Assert:

```python
self.assertIn("systemShopList", html)
self.assertIn("recycleAllButton", html)
self.assertIn("data-action=\"recycle\"", script)
self.assertIn("/inventory/recycle", script)
self.assertIn("/inventory/recycle-all", script)
self.assertIn("/market/sell-own", script)
self.assertIn("/talent/donate", script)
self.assertIn("rainbow", script)
self.assertIn("talentLightningEffect", script)
```

- [ ] **Step 2: Verify RED**

Run: `python -m unittest tests.test_web_static.WebStaticTests -v`

Expected: FAIL on missing UI markers.

- [ ] **Step 3: Implement UI**

Add a compact system shop panel near market/equipment. Add backpack header button and item recycle buttons. Add own market listing sell button. Add talent donation line and expand button.

Add rainbow labels/palette and render stronger canvas aura/equipment effects for rainbow.

- [ ] **Step 4: Verify GREEN**

Run: `python -m unittest tests.test_web_static.WebStaticTests -v`

Expected: PASS.

### Task 4: Pixellab Premium Talent Effects

**Files:**
- Create: `web/assets/pixel/v1/effects/talent_lightning.png`
- Create: `web/assets/pixel/v1/effects/talent_flame.png`
- Create: `web/assets/pixel/v1/effects/talent_dragon.png`
- Modify: `web/app.js`
- Modify: `web/assets/pixel/v1/manifests/assets.json`
- Test: `tests/test_web_static.py`

- [ ] **Step 1: Generate effects with Pixellab**

Use:

```powershell
python tools\pixellab_api_generate.py map-object --prompt "side-view transparent pixel art lightning aura ring for dark fantasy assassin talent effect, electric arcs, no character, no background, game VFX sprite" --width 128 --height 128 --view side --outline "single color outline" --detail "medium detail" --shading "medium shading" --out-dir artifacts\pixellab\api\talent_lightning_effect
```

Repeat with flame and coiling dragon prompts. Copy approved output to `web/assets/pixel/v1/effects/`.

- [ ] **Step 2: Wire assets**

Add cache-busted asset keys and draw them around hero when talent effects qualify:

- lightning for high attack/attack speed talent emphasis
- flame for high all-stats/gold/exp emphasis
- dragon for all-current-talents-mythic or rainbow equipped heroes

- [ ] **Step 3: Verify browser**

Restart `server.py`, open `http://localhost:8000/?v=<new-version>`, and capture a screenshot.

### Task 5: Full Verification And Commit

**Files:**
- All touched files

- [ ] **Step 1: Run full tests**

Run:

```powershell
python -m unittest tests.test_engine -v
python -m unittest tests.test_server_accounts -v
python -m unittest tests.test_web_static -v
```

- [ ] **Step 2: Inspect git scope**

Run: `git status --short` and ensure `data/`, `dist/`, and raw `artifacts/` are not staged.

- [ ] **Step 3: Commit**

Commit message:

```text
Add system shop recycling and donation talents
```
