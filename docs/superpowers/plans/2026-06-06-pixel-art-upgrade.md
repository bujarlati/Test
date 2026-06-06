# Pixel Art Upgrade Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace prototype visuals with a cohesive, smooth, dark-fantasy pixel-art presentation while keeping gameplay stable.

**Architecture:** Add a manifest-driven asset layer under `web/assets/pixel/v1/` and gradually move rendering logic out of the large `web/app.js` canvas renderer into focused renderer helpers. Existing sprite and procedural drawing code remains as fallback until each new visual path is verified.

**Tech Stack:** Python stdlib server, SQLite persistence, browser Canvas 2D, PNG sprite sheets, JSON manifests, Pixellab-generated pixel assets.

---

## File Structure

- `web/assets/pixel/v1/manifests/assets.json`: central manifest for heroes, monsters, maps, equipment, and effects.
- `web/assets/pixel/v1/heroes/`: male and female sprite sheets.
- `web/assets/pixel/v1/equipment/`: layered equipment visuals.
- `web/assets/pixel/v1/monsters/`: common, elite, and boss sprite sheets.
- `web/assets/pixel/v1/maps/`: tilesets and parallax backgrounds.
- `web/assets/pixel/v1/effects/`: attack effects, rarity particles, and talent auras.
- `web/renderer/assets.js`: load image paths and manifest records.
- `web/renderer/animation.js`: resolve frame indices and animation timing.
- `web/renderer/character.js`: draw hero base sprites and equipment layers.
- `web/renderer/monsters.js`: draw common monsters, elites, and bosses.
- `web/renderer/maps.js`: draw parallax maps and depth variants.
- `web/renderer/effects.js`: draw attack effects, rarity particles, and talent auras.
- `web/app.js`: keep orchestration, canvas setup, state updates, and fallback renderer calls.
- `tests/test_web_static.py`: static checks for manifest references and renderer modules.
- `tests/test_server_accounts.py`: market cancel and account market behavior tests.

---

### Task 1: Complete Market Cancel Polish

**Files:**
- Modify: `idle_forest/market.py`
- Modify: `idle_forest/engine.py`
- Modify: `server.py`
- Modify: `web/app.js`
- Test: `tests/test_server_accounts.py`
- Test: `tests/test_web_static.py`

- [ ] **Step 1: Keep the failing behavior tests**

Ensure these tests exist and fail before implementation if reverted:

```python
def test_market_listing_can_be_canceled_by_seller(self) -> None:
    seller = self._post("/account/register", {"username": "cancel", "password": "forest-pass"})
    seller_character = self._create_character(seller["session_token"], "Seller", "male")
    seller_id = seller_character["character"]["character_id"]
    runtime = self.server_module.CHARACTER_RUNTIMES[seller_id]
    item = generate_equipment(level=4, rng=runtime.engine.rng)
    item.owner_id = seller_id
    runtime.engine.hero.inventory.append(item)
    listed = self._post("/market/list", {"item_id": item.id, "price": 31}, token=seller["session_token"])
    canceled = self._post("/market/cancel", {"listing_id": listed["listing"]["id"]}, token=seller["session_token"])
    self.assertIn(item.id, [inventory_item["id"] for inventory_item in canceled["snapshot"]["hero"]["inventory"]])
```

- [ ] **Step 2: Run the focused tests**

Run:

```bash
python -m unittest tests.test_server_accounts.ServerAccountTests.test_market_listing_can_be_canceled_by_seller tests.test_server_accounts.ServerAccountTests.test_market_listing_cannot_be_canceled_by_other_account tests.test_web_static.WebStaticTests.test_frontend_renders_cancel_button_for_own_market_listing
```

Expected before implementation: fail with missing `/market/cancel` or missing cancel button.

- [ ] **Step 3: Implement cancel listing**

Add a `Market.cancel(listing_id, seller_id, current_tick)` method, a `GameEngine.cancel_listing(listing_id)` method, and a `POST /market/cancel` endpoint. The endpoint returns:

```json
{
  "item": {"id": "item_id"},
  "snapshot": {"market": {"active": []}}
}
```

- [ ] **Step 4: Verify focused tests pass**

Run the focused command from Step 2.

Expected after implementation: `Ran 3 tests ... OK`.

---

### Task 2: Add Pixel Asset Manifest Foundation

**Files:**
- Create: `web/assets/pixel/v1/manifests/assets.json`
- Create: `web/renderer/assets.js`
- Modify: `web/index.html`
- Test: `tests/test_web_static.py`

- [ ] **Step 1: Add static manifest test**

Add a test that checks:

```python
manifest = ROOT / "web" / "assets" / "pixel" / "v1" / "manifests" / "assets.json"
script = (ROOT / "web" / "renderer" / "assets.js").read_text(encoding="utf-8")
self.assertTrue(manifest.exists())
self.assertIn("loadPixelManifest", script)
```

- [ ] **Step 2: Create the manifest**

Create `assets.json` with this structure:

```json
{
  "version": "pixel-v1",
  "tileSize": 32,
  "heroes": {},
  "equipment": {},
  "monsters": {},
  "maps": {},
  "effects": {}
}
```

- [ ] **Step 3: Create asset loader**

Create `web/renderer/assets.js`:

```javascript
export async function loadPixelManifest(path = '/web/assets/pixel/v1/manifests/assets.json') {
  const response = await fetch(path)
  if (!response.ok) {
    throw new Error(`Pixel manifest failed: ${response.status}`)
  }
  return response.json()
}
```

- [ ] **Step 4: Wire module script**

Add the module script in `web/index.html` after the main app script only after the renderer is ready to use it. If the first pass keeps loading inside `web/app.js`, defer this step.

- [ ] **Step 5: Verify**

Run:

```bash
python -m unittest tests.test_web_static.WebStaticTests
node --check web/app.js
```

---

### Task 3: Import First Pixellab Style Bible

**Files:**
- Create: `web/assets/pixel/v1/heroes/male/`
- Create: `web/assets/pixel/v1/heroes/female/`
- Create: `web/assets/pixel/v1/monsters/common/`
- Create: `web/assets/pixel/v1/maps/forest/`
- Modify: `web/assets/pixel/v1/manifests/assets.json`
- Create: `web/assets/pixel/v1/PROMPTS.md`

- [ ] **Step 1: Generate approved assets in Pixellab**

Use these prompt bases:

```text
dark fantasy pixel art side-view game sprite, clean readable silhouette, upper-left warm rim light, transparent background, 96x96 sprite sheet, no text, no UI frame, no watermark
```

```text
dark fantasy pixel art forest tileset, 32x32 tiles, side-view platform ground, moss, roots, stones, warm upper-left light, seamless game tiles, no text, no watermark
```

- [ ] **Step 2: Save prompt records**

Create `PROMPTS.md` with the exact prompt, Pixellab settings, exported size, and approval note for every imported asset.

- [ ] **Step 3: Add manifest entries**

Use this manifest shape for the male hero:

```json
{
  "heroes": {
    "male_base": {
      "image": "/web/assets/pixel/v1/heroes/male/base.png",
      "frameWidth": 96,
      "frameHeight": 96,
      "anchors": {
        "feet": [48, 84],
        "mainHand": [62, 50],
        "offHand": [36, 51],
        "head": [48, 28],
        "torso": [48, 50]
      },
      "animations": {
        "idle": {"row": 0, "frames": 6, "frameMs": 120},
        "walk": {"row": 1, "frames": 8, "frameMs": 90},
        "attack": {"row": 2, "frames": 8, "frameMs": 70},
        "hurt": {"row": 3, "frames": 4, "frameMs": 90},
        "death": {"row": 4, "frames": 8, "frameMs": 110},
        "revive": {"row": 5, "frames": 8, "frameMs": 100}
      }
    }
  }
}
```

- [ ] **Step 4: Verify file paths**

Run:

```bash
python -m unittest tests.test_web_static.WebStaticTests
```

Expected: manifest path checks pass.

---

### Task 4: Add Animation Resolver

**Files:**
- Create: `web/renderer/animation.js`
- Test: `tests/test_web_static.py`

- [ ] **Step 1: Add static test**

Check that `animation.js` exports:

```python
self.assertIn("export function animationFrame", script)
self.assertIn("export function animationNameForEntity", script)
```

- [ ] **Step 2: Implement resolver**

Create:

```javascript
export function animationNameForEntity(entity) {
  if (!entity) return 'idle'
  if (entity.state === 'reviving') return 'revive'
  if (entity.state === 'combat') return 'attack'
  if (entity.state === 'approach' || entity.state === 'walk') return 'walk'
  if (entity.hp <= 0) return 'death'
  return 'idle'
}

export function animationFrame(animation, nowMs) {
  const frames = Math.max(1, Number(animation.frames || 1))
  const frameMs = Math.max(1, Number(animation.frameMs || 100))
  return Math.floor(nowMs / frameMs) % frames
}
```

- [ ] **Step 3: Verify**

Run:

```bash
python -m unittest tests.test_web_static.WebStaticTests
```

---

### Task 5: Replace Hero Rendering Behind a Fallback

**Files:**
- Create: `web/renderer/character.js`
- Modify: `web/app.js`
- Test: `tests/test_web_static.py`

- [ ] **Step 1: Add fallback test**

Check that `web/app.js` still contains `drawHeroRig` and also calls a pixel renderer hook:

```python
self.assertIn("drawHeroRig", script)
self.assertIn("drawPixelHero", script)
```

- [ ] **Step 2: Implement hero drawing helper**

Create a helper with this public shape:

```javascript
export function drawPixelHero(ctx, assets, entity, x, y, nowMs) {
  const gender = entity.gender === 'female' ? 'female_base' : 'male_base'
  const record = assets.heroes && assets.heroes[gender]
  if (!record || !record.imageElement) {
    return false
  }
  return true
}
```

- [ ] **Step 3: Wire fallback**

In `drawHero`, call `drawPixelHero(...)`; if it returns false, keep the existing `drawHeroRig(...)`.

- [ ] **Step 4: Visual smoke test**

Start the local server:

```bash
python server.py --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000/` and verify the hero is visible during idle, walk, attack, death, and revive.

---

### Task 6: Replace Monster and Boss Rendering

**Files:**
- Create: `web/renderer/monsters.js`
- Modify: `web/app.js`
- Modify: `web/assets/pixel/v1/manifests/assets.json`
- Test: `tests/test_web_static.py`

- [ ] **Step 1: Add manifest entries**

Add records for:

```json
{
  "monsters": {
    "slime": {"image": "/web/assets/pixel/v1/monsters/common/slime.png", "frameWidth": 64, "frameHeight": 64},
    "treant": {"image": "/web/assets/pixel/v1/monsters/common/treant.png", "frameWidth": 64, "frameHeight": 64},
    "forest_boss": {"image": "/web/assets/pixel/v1/monsters/bosses/forest_boss.png", "frameWidth": 128, "frameHeight": 128}
  }
}
```

- [ ] **Step 2: Implement fallback helper**

Create `drawPixelMonster(ctx, assets, entity, x, y, nowMs)` and return `false` when the manifest has no matching sprite.

- [ ] **Step 3: Wire fallback**

Call `drawPixelMonster(...)` in `drawMonster`; keep existing sprite/procedural monster drawing as fallback.

- [ ] **Step 4: Verify**

Run:

```bash
python -m unittest
node --check web/app.js
```

Then visually confirm monsters face the hero.

---

### Task 7: Upgrade Map Rendering

**Files:**
- Create: `web/renderer/maps.js`
- Modify: `web/app.js`
- Modify: `web/assets/pixel/v1/manifests/assets.json`

- [ ] **Step 1: Add forest and deep forest map records**

Use:

```json
{
  "maps": {
    "forest": {
      "tileset": "/web/assets/pixel/v1/maps/forest/tileset.png",
      "backgrounds": [
        "/web/assets/pixel/v1/maps/forest/far.png",
        "/web/assets/pixel/v1/maps/forest/mid.png",
        "/web/assets/pixel/v1/maps/forest/front.png"
      ]
    },
    "deep_forest": {
      "tileset": "/web/assets/pixel/v1/maps/deep_forest/tileset.png",
      "darkness": 0.32
    }
  }
}
```

- [ ] **Step 2: Draw parallax layers**

Create `drawPixelMap(ctx, assets, biome, cameraX, width, height)` and let it return false if images are unavailable.

- [ ] **Step 3: Verify visual depth**

Open local desktop and mobile widths. Confirm deep forest is darker, denser, and not just a recolored flat background.

---

### Task 8: Add Equipment and Talent Effects

**Files:**
- Create: `web/renderer/effects.js`
- Modify: `web/app.js`
- Modify: `web/assets/pixel/v1/manifests/assets.json`

- [ ] **Step 1: Add effect manifest entries**

Use:

```json
{
  "effects": {
    "slash_white": {"image": "/web/assets/pixel/v1/effects/attacks/slash_white.png", "frameWidth": 128, "frameHeight": 96},
    "slash_red": {"image": "/web/assets/pixel/v1/effects/attacks/slash_red.png", "frameWidth": 160, "frameHeight": 96},
    "aura_lightning": {"image": "/web/assets/pixel/v1/effects/auras/lightning.png", "frameWidth": 128, "frameHeight": 128}
  }
}
```

- [ ] **Step 2: Map rarity to effect**

Use this first-pass mapping:

```javascript
const RARITY_ATTACK_EFFECT = {
  white: 'slash_white',
  green: 'slash_white',
  blue: 'slash_blue',
  purple: 'slash_purple',
  gold: 'slash_gold',
  red: 'slash_red'
}
```

- [ ] **Step 3: Map talent to aura**

Use effect keys already in talents:

```javascript
const TALENT_AURA_EFFECT = {
  move_speed_pct: 'aura_lightning',
  defense_pct: 'aura_guard',
  max_hp_pct: 'aura_life',
  treasure_mimic_chance_pct: 'aura_treasure'
}
```

- [ ] **Step 4: Verify**

Check purple, gold, and red equipment in inventory/equipped state. Confirm particles are visible but do not hide the hero or monster health bars.

---

### Task 9: Final Visual Verification Package

**Files:**
- Modify: `docs/superpowers/specs/2026-06-06-pixel-art-upgrade-design.md`
- Modify: `docs/superpowers/plans/2026-06-06-pixel-art-upgrade.md`

- [ ] **Step 1: Run automated tests**

Run:

```bash
python -m unittest
node --check web/app.js
```

Expected: all tests pass and Node exits 0.

- [ ] **Step 2: Run local smoke test**

Start:

```bash
python server.py --host 127.0.0.1 --port 8000
```

Check:

- login and character select
- male and female hero display
- idle, walk, attack, hurt, death, revive
- equip starter sword
- list, cancel, and buy a market item
- enter and leave deeper forest

- [ ] **Step 3: Build deployment package**

Create a clean archive from tracked files and approved assets:

```powershell
git ls-files
```

Then package without `data/`, `.git/`, or `dist/`.

- [ ] **Step 4: Server verification**

After deployment, verify:

```bash
curl https://idel.fun/account
```

Then use two browser sessions to confirm two accounts can see and trade market listings.
