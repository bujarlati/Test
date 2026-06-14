# Pixellab Monster Upgrade Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a broader Pixellab monster roster with theme-specific rift minions, distinct rift bosses, and real monster attack animation playback.

**Architecture:** Keep backend combat balance unchanged and use existing `Monster.kind`, `role`, `theme`, and combat events to drive rendering. Add new PNG sheets and manifest records, then map exact monster kinds to `PIXEL_SPRITES.monsters` before falling back to the old family mapping. Track recent `monster_attack` events in the frontend so common monsters and bosses play the `attack` row only when they actually attack.

**Tech Stack:** Python unittest, Pixellab API helper `tools/pixellab_api_generate.py`, existing PNG reader `tools.import_assassin_sample.read_png`, frontend canvas renderer in `web/app.js`, static assets under `web/assets/pixel/v1/`.

---

## File Structure

- Modify `tests/test_web_static.py`: add failing tests for new monster assets, exact kind mapping, and attack event playback.
- Modify `tests/test_engine.py`: add a small roster exposure test so the frontend-facing monster kinds stay stable.
- Modify `idle_forest/content.py`: expose monster kind constants through a single frontend-friendly roster if needed by the engine test.
- Add generated PNGs under `web/assets/pixel/v1/monsters/common/` and `web/assets/pixel/v1/monsters/bosses/`.
- Modify `web/assets/pixel/v1/manifests/assets.json`: add one manifest record per new monster sprite sheet.
- Modify `web/app.js`: add asset paths, sprite records, exact `kind` mapping, monster attack event tracking, and cache-bust version bump.

---

### Task 1: Add Roster And Frontend Contract Tests

**Files:**
- Modify: `tests/test_engine.py`
- Modify: `tests/test_web_static.py`

- [ ] **Step 1: Write failing engine roster test**

Append this test to `GameEngineTests` in `tests/test_engine.py`:

```python
    def test_monster_roster_exposes_forest_rift_and_boss_kinds(self) -> None:
        from idle_forest.content import (
            DEEP_FOREST_MONSTER_KINDS,
            MONSTER_KINDS,
            RIFT_BOSSES,
            RIFT_MONSTERS,
        )

        self.assertEqual(len(MONSTER_KINDS), 5)
        self.assertEqual(len(DEEP_FOREST_MONSTER_KINDS), 5)
        self.assertEqual(set(RIFT_MONSTERS), {"cave", "sky", "castle"})
        self.assertEqual(set(RIFT_BOSSES), {"cave", "sky", "castle"})
        self.assertEqual(sum(len(kinds) for kinds in RIFT_MONSTERS.values()), 9)
        self.assertEqual(len(set(RIFT_BOSSES.values())), 3)
```

- [ ] **Step 2: Write failing static asset and mapping test**

Append this test to `WebStaticTests` in `tests/test_web_static.py`:

```python
    def test_pixellab_monster_roster_assets_exist_and_are_wired(self) -> None:
        manifest_path = ROOT / "web" / "assets" / "pixel" / "v1" / "manifests" / "assets.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")

        common = [
            "forest_slime",
            "thorn_boar",
            "moss_imp",
            "wild_mushroom",
            "bark_guard",
            "cave_bat",
            "crystal_lurker",
            "stone_crawler",
            "cloud_wisp",
            "storm_harpy",
            "sun_mote",
            "rust_guard",
            "hollow_knight",
            "cursed_squire",
        ]
        bosses = ["cave_warden", "tempest_seraph", "throne_keeper"]
        monsters = manifest["monsters"]

        for key in common:
            self.assertIn(key, monsters)
            record = monsters[key]
            self.assertEqual(record["frameWidth"], 64)
            self.assertEqual(record["frameHeight"], 64)
            self.assertEqual(record["source"], "pixellab")
            self.assertEqual(set(record["animations"]), {"idle", "walk", "attack", "hurt", "death"})
            image_path = ROOT / record["image"].lstrip("/")
            self.assertTrue(image_path.exists(), image_path)
            self.assertEqual(image_path.read_bytes()[:8], b"\x89PNG\r\n\x1a\n")
            self.assertIn(key, script)

        for key in bosses:
            self.assertIn(key, monsters)
            record = monsters[key]
            self.assertEqual(record["frameWidth"], 128)
            self.assertEqual(record["frameHeight"], 128)
            self.assertEqual(record["source"], "pixellab")
            self.assertEqual(set(record["animations"]), {"idle", "walk", "attack", "hurt", "death"})
            image_path = ROOT / record["image"].lstrip("/")
            self.assertTrue(image_path.exists(), image_path)
            self.assertEqual(image_path.read_bytes()[:8], b"\x89PNG\r\n\x1a\n")
            self.assertIn(key, script)

        self.assertIn("const MONSTER_KIND_SPRITES = {", script)
        self.assertIn("MONSTER_KIND_SPRITES[entity.kind]", script)
```

- [ ] **Step 3: Write failing monster attack animation test**

Append this test to `WebStaticTests` in `tests/test_web_static.py`:

```python
    def test_monster_attack_events_drive_pixel_attack_animation(self) -> None:
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")

        self.assertIn("monsterAttackEffects: []", script)
        self.assertIn("seenMonsterAttackEventKeys: new Set()", script)
        self.assertIn("function trackMonsterAttackEffects(events = [], scene = null)", script)
        self.assertIn("event.kind !== 'monster_attack'", script)
        self.assertIn("function recentMonsterAttackEffect(entity)", script)
        self.assertIn("if (recentMonsterAttackEffect(entity)) return 'attack'", script)
        self.assertIn("trackMonsterAttackEffects(snapshot.events || [], snapshot.scene)", script)
        self.assertNotIn("if (entity.role === 'boss') return 'attack'", script)
```

- [ ] **Step 4: Run tests to verify RED**

Run:

```powershell
python -m unittest tests.test_engine.GameEngineTests.test_monster_roster_exposes_forest_rift_and_boss_kinds tests.test_web_static.WebStaticTests.test_pixellab_monster_roster_assets_exist_and_are_wired tests.test_web_static.WebStaticTests.test_monster_attack_events_drive_pixel_attack_animation -v
```

Expected: the engine test may pass immediately because constants already exist; the static tests must fail because the new PNGs, mapping, and monster attack tracking do not exist yet.

---

### Task 2: Generate And Normalize Pixellab Monster Sheets

**Files:**
- Create: `web/assets/pixel/v1/monsters/common/forest_slime.png`
- Create: `web/assets/pixel/v1/monsters/common/thorn_boar.png`
- Create: `web/assets/pixel/v1/monsters/common/moss_imp.png`
- Create: `web/assets/pixel/v1/monsters/common/wild_mushroom.png`
- Create: `web/assets/pixel/v1/monsters/common/bark_guard.png`
- Create: `web/assets/pixel/v1/monsters/common/cave_bat.png`
- Create: `web/assets/pixel/v1/monsters/common/crystal_lurker.png`
- Create: `web/assets/pixel/v1/monsters/common/stone_crawler.png`
- Create: `web/assets/pixel/v1/monsters/common/cloud_wisp.png`
- Create: `web/assets/pixel/v1/monsters/common/storm_harpy.png`
- Create: `web/assets/pixel/v1/monsters/common/sun_mote.png`
- Create: `web/assets/pixel/v1/monsters/common/rust_guard.png`
- Create: `web/assets/pixel/v1/monsters/common/hollow_knight.png`
- Create: `web/assets/pixel/v1/monsters/common/cursed_squire.png`
- Create: `web/assets/pixel/v1/monsters/bosses/cave_warden.png`
- Create: `web/assets/pixel/v1/monsters/bosses/tempest_seraph.png`
- Create: `web/assets/pixel/v1/monsters/bosses/throne_keeper.png`

- [ ] **Step 1: Check Pixellab credentials**

Run:

```powershell
python tools\pixellab_api_generate.py balance
```

Expected: JSON balance output. If `PIXELLAB_API_KEY is not set`, stop and ask the user to provide the local key in `.env` or environment variables.

- [ ] **Step 2: Generate common monster sheets**

Run one Pixellab generation per common monster, using the same sheet format in every prompt. Example command for `thorn_boar`:

```powershell
python tools\pixellab_api_generate.py pro-image `
  --prompt "dark fantasy pixel art side-view monster spritesheet, thorn_boar, large horned forest boar with bramble armor and mossy tusks, facing right, transparent background, no text, no scenery, exact 8 columns and 5 rows, rows are idle walk attack hurt death, readable Monster Hunter inspired ecological beast silhouette, weighty charge attack row" `
  --width 512 --height 320 `
  --no-background `
  --out-dir artifacts\pixellab\api\monsters\thorn_boar
```

Repeat with these descriptions:

```text
forest_slime: heavy amber forest slime with leaf core, low beast-like body, lunging splash attack
moss_imp: small moss goblin predator with branch horns and claw swipe attack
wild_mushroom: squat fungal crawler with plated cap and spore burst attack
bark_guard: wooden bark guardian beast with root limbs and heavy slam attack
cave_bat: cavern wing creature with hooked claws and diving bite attack
crystal_lurker: low crystal panther-lizard with glowing jaw and shard pounce attack
stone_crawler: armored stone insect crawler with mandible snap attack
cloud_wisp: floating cloud spirit beast with curling tail and wind pulse attack
storm_harpy: storm-feather raptor-harpy with talon slash attack
sun_mote: bright solar floating creature with flare burst attack
rust_guard: rusted castle armor beast with broken halberd arm and chop attack
hollow_knight: hollow cursed knight creature with oversized helm and sword lunge attack
cursed_squire: small cursed shield squire construct with shield bash attack
```

- [ ] **Step 3: Generate boss sheets**

Run one Pixellab generation per boss. Example command for `cave_warden`:

```powershell
python tools\pixellab_api_generate.py pro-image `
  --prompt "dark fantasy pixel art side-view boss spritesheet, cave_warden, massive crystal-jawed cave apex monster, facing right, transparent background, no text, no scenery, exact 8 columns and 5 rows, rows are idle walk attack hurt death, 128 pixel boss frame style, readable giant silhouette, heavy lunge and crystal spike burst attack row" `
  --width 1024 --height 640 `
  --no-background `
  --out-dir artifacts\pixellab\api\monsters\cave_warden
```

Repeat with these descriptions:

```text
tempest_seraph: huge storm wing apex beast, feathered lightning wings, dive and wing sweep attack
throne_keeper: cursed throne guardian titan, plated royal armor, giant blade smash and shield crush attack
```

- [ ] **Step 4: Copy approved normalized PNGs into game asset paths**

For each generated output, inspect the PNG and copy the approved 5x8 sheet to the matching path. If Pixellab returns more than one candidate, choose the clearest side-view sheet. Use PowerShell `Copy-Item` only after visual inspection:

```powershell
Copy-Item artifacts\pixellab\api\monsters\thorn_boar\image_01.png web\assets\pixel\v1\monsters\common\thorn_boar.png
```

Expected: each final common PNG is `512x320`; each boss PNG is `1024x640`.

- [ ] **Step 5: Verify PNG dimensions**

Run:

```powershell
@'
from pathlib import Path
from tools.import_assassin_sample import read_png

common = Path("web/assets/pixel/v1/monsters/common")
bosses = Path("web/assets/pixel/v1/monsters/bosses")
for path in sorted(common.glob("*.png")):
    if path.stem in {"forest_slime","thorn_boar","moss_imp","wild_mushroom","bark_guard","cave_bat","crystal_lurker","stone_crawler","cloud_wisp","storm_harpy","sun_mote","rust_guard","hollow_knight","cursed_squire"}:
        width, height, _ = read_png(path)
        print(path.name, width, height)
        assert (width, height) == (512, 320)
for path in sorted(bosses.glob("*.png")):
    if path.stem in {"cave_warden","tempest_seraph","throne_keeper"}:
        width, height, _ = read_png(path)
        print(path.name, width, height)
        assert (width, height) == (1024, 640)
'@ | python -
```

Expected: all listed files print the expected dimensions with no assertion failures.

---

### Task 3: Wire Manifest, Asset Paths, And Exact Kind Mapping

**Files:**
- Modify: `web/assets/pixel/v1/manifests/assets.json`
- Modify: `web/app.js`
- Modify: `tests/test_web_static.py`

- [ ] **Step 1: Add manifest records**

For each common monster, add this shape under `manifest["monsters"]`, changing `image`, `drawWidth`, and `drawHeight` as needed:

```json
"thorn_boar": {
  "image": "/web/assets/pixel/v1/monsters/common/thorn_boar.png",
  "frameWidth": 64,
  "frameHeight": 64,
  "drawWidth": 78,
  "drawHeight": 76,
  "source": "pixellab",
  "animations": {
    "idle": {"row": 0, "frames": 8, "frameMs": 120},
    "walk": {"row": 1, "frames": 8, "frameMs": 92},
    "attack": {"row": 2, "frames": 8, "frameMs": 76},
    "hurt": {"row": 3, "frames": 4, "frameMs": 90},
    "death": {"row": 4, "frames": 8, "frameMs": 110}
  }
}
```

For each boss, use `frameWidth` and `frameHeight` of `128`, and `drawWidth`/`drawHeight` around `138` to `152` depending on silhouette.

- [ ] **Step 2: Add asset paths**

In `web/app.js`, add paths to `ASSET_PATHS` and bump `PIXEL_ASSET_VERSION` by one. Use this pattern:

```javascript
  pixelMonsterThornBoar: `/web/assets/pixel/v1/monsters/common/thorn_boar.png?v=${PIXEL_ASSET_VERSION}`,
  pixelMonsterCaveWarden: `/web/assets/pixel/v1/monsters/bosses/cave_warden.png?v=${PIXEL_ASSET_VERSION}`,
```

Use these key names:

```text
pixelMonsterForestSlime
pixelMonsterThornBoar
pixelMonsterMossImp
pixelMonsterWildMushroom
pixelMonsterBarkGuard
pixelMonsterCaveBat
pixelMonsterCrystalLurker
pixelMonsterStoneCrawler
pixelMonsterCloudWisp
pixelMonsterStormHarpy
pixelMonsterSunMote
pixelMonsterRustGuard
pixelMonsterHollowKnight
pixelMonsterCursedSquire
pixelMonsterCaveWarden
pixelMonsterTempestSeraph
pixelMonsterThroneKeeper
```

- [ ] **Step 3: Add sprite records**

Add `PIXEL_SPRITES.monsters` records like:

```javascript
    thorn_boar: {
      key: 'pixelMonsterThornBoar',
      frameWidth: 64,
      frameHeight: 64,
      drawWidth: 78,
      drawHeight: 76,
      actions: PIXEL_MONSTER_ACTIONS
    },
```

Boss records use `frameWidth: 128`, `frameHeight: 128`, and larger draw dimensions.

- [ ] **Step 4: Replace fuzzy-first mapping with exact mapping**

Add this constant near `PIXEL_SPRITES`:

```javascript
const MONSTER_KIND_SPRITES = {
  forest_slime: 'forest_slime',
  thorn_boar: 'thorn_boar',
  moss_imp: 'moss_imp',
  wild_mushroom: 'wild_mushroom',
  bark_guard: 'bark_guard',
  shadow_slime: 'forest_slime',
  bramble_wolf: 'thorn_boar',
  gloom_imp: 'moss_imp',
  venom_mushroom: 'wild_mushroom',
  ancient_bark_guard: 'bark_guard',
  cave_bat: 'cave_bat',
  crystal_lurker: 'crystal_lurker',
  stone_crawler: 'stone_crawler',
  cloud_wisp: 'cloud_wisp',
  storm_harpy: 'storm_harpy',
  sun_mote: 'sun_mote',
  rust_guard: 'rust_guard',
  hollow_knight: 'hollow_knight',
  cursed_squire: 'cursed_squire',
  cave_warden: 'cave_warden',
  tempest_seraph: 'tempest_seraph',
  throne_keeper: 'throne_keeper'
}
```

Update `pixelMonsterRecord(entity)` to:

```javascript
function pixelMonsterRecord(entity) {
  const exact = entity && MONSTER_KIND_SPRITES[entity.kind]
  if (exact && PIXEL_SPRITES.monsters[exact]) {
    return PIXEL_SPRITES.monsters[exact]
  }
  const name = entity.name || entity.kind || ''
  if (entity.role === 'boss') {
    return PIXEL_SPRITES.monsters.forest_boss
  }
  if (name.includes('thorn') || name.includes('bramble') || name.includes('ancient') || name.includes('bark')) {
    return PIXEL_SPRITES.monsters.thorn
  }
  if (name.includes('imp') || name.includes('guard') || name.includes('knight') || name.includes('squire')) {
    return PIXEL_SPRITES.monsters.imp
  }
  return PIXEL_SPRITES.monsters.slime
}
```

- [ ] **Step 5: Run mapping tests**

Run:

```powershell
python -m unittest tests.test_web_static.WebStaticTests.test_pixellab_monster_roster_assets_exist_and_are_wired tests.test_web_static.WebStaticTests.test_frontend_cache_busts_pixel_asset_paths -v
```

Expected: PASS.

---

### Task 4: Make Monster Attack Animations Event-Driven

**Files:**
- Modify: `web/app.js`
- Modify: `tests/test_web_static.py`

- [ ] **Step 1: Add attack tracking state**

In `state`, add:

```javascript
  monsterAttackEffects: [],
  seenMonsterAttackEventKeys: new Set(),
```

In `resetVisualSmoothing()`, add:

```javascript
  state.monsterAttackEffects = []
  state.seenMonsterAttackEventKeys = new Set()
```

- [ ] **Step 2: Track monster attack events**

Add this function near `trackAttackEffects`:

```javascript
function trackMonsterAttackEffects(events = [], scene = null) {
  const now = performance.now()
  const entities = scene && scene.entities ? scene.entities : []
  const monster = entities.find((entity) => entity.type === 'monster')
  for (const event of events) {
    if (event.kind !== 'monster_attack') {
      continue
    }
    const key = attackEventKey(event)
    if (state.seenMonsterAttackEventKeys.has(key)) {
      continue
    }
    state.seenMonsterAttackEventKeys.add(key)
    const data = event.data || {}
    state.monsterAttackEffects.push({
      id: `${key}:${now}`,
      monsterId: data.monster_id || (monster && monster.id) || '',
      createdAt: now
    })
  }
  if (state.seenMonsterAttackEventKeys.size > 100) {
    state.seenMonsterAttackEventKeys = new Set(Array.from(state.seenMonsterAttackEventKeys).slice(-60))
  }
  state.monsterAttackEffects = state.monsterAttackEffects.filter((effect) => now - effect.createdAt < ATTACK_EFFECT_DURATION_MS)
}
```

Call it from `applySnapshot(snapshot)` after `trackAttackEffects`:

```javascript
  trackMonsterAttackEffects(snapshot.events || [], snapshot.scene)
```

- [ ] **Step 3: Select monster action from events**

Add:

```javascript
function recentMonsterAttackEffect(entity) {
  if (!entity) {
    return null
  }
  const now = performance.now()
  return state.monsterAttackEffects.find((effect) => {
    if (now - effect.createdAt >= ATTACK_EFFECT_DURATION_MS) {
      return false
    }
    return !effect.monsterId || effect.monsterId === entity.id
  }) || null
}
```

Update `pixelMonsterAction(entity)` to:

```javascript
function pixelMonsterAction(entity) {
  if (!entity) return 'idle'
  if (Number(entity.hp || 0) <= 0) return 'death'
  if (recentMonsterAttackEffect(entity)) return 'attack'
  if (movingEntity(entity)) return 'walk'
  return 'idle'
}
```

- [ ] **Step 4: Expose debug count**

In `window.__idleForestDebug`, add:

```javascript
    monsterAttackEffects: state.monsterAttackEffects.length,
```

- [ ] **Step 5: Run attack animation tests**

Run:

```powershell
python -m unittest tests.test_web_static.WebStaticTests.test_monster_attack_events_drive_pixel_attack_animation tests.test_web_static.WebStaticTests.test_frontend_exposes_readonly_visual_debug_state -v
```

Expected: PASS.

---

### Task 5: Final Verification And Runtime Smoke Check

**Files:**
- Modify: `web/index.html`
- Possibly modify: `web/app.js`
- Test: full test suite

- [ ] **Step 1: Update HTML cache-bust references**

If `PIXEL_ASSET_VERSION` was bumped to `assassin-v73`, update:

```html
<link rel="stylesheet" href="/web/styles.css?v=assassin-v73" />
<script src="/web/app.js?v=assassin-v73"></script>
```

Also update `tests/test_web_static.py::test_frontend_cache_busts_pixel_asset_paths`.

- [ ] **Step 2: Run JS syntax check**

Run:

```powershell
C:\Users\赵春健\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe --check web\app.js
```

Expected: exit code 0 with no output.

- [ ] **Step 3: Run targeted tests**

Run:

```powershell
python -m unittest tests.test_engine.GameEngineTests.test_monster_roster_exposes_forest_rift_and_boss_kinds tests.test_web_static.WebStaticTests.test_pixellab_monster_roster_assets_exist_and_are_wired tests.test_web_static.WebStaticTests.test_monster_attack_events_drive_pixel_attack_animation tests.test_web_static.WebStaticTests.test_frontend_cache_busts_pixel_asset_paths -v
```

Expected: PASS.

- [ ] **Step 4: Run full test suite**

Run:

```powershell
python -m unittest discover -v
```

Expected: all tests pass.

- [ ] **Step 5: Verify local server references new version**

Run:

```powershell
try {
  $html=(Invoke-WebRequest -UseBasicParsing http://localhost:8000/ -TimeoutSec 5).Content
  if ($html -match 'app\.js\?v=assassin-v73' -and $html -match 'styles\.css\?v=assassin-v73') {
    'index references assassin-v73'
  } else {
    'index did not reference assassin-v73'
  }
} catch {
  $_.Exception.Message
}
```

Expected: `index references assassin-v73`. If the version differs, match this command to the actual bumped version.

---

## Self-Review

Spec coverage:

- Broader monster roster: covered by Task 2 and Task 3.
- Pixellab source workflow: covered by Task 2.
- Existing sheet format: covered by Task 2 and Task 3.
- Exact kind mapping: covered by Task 1 and Task 3.
- Attack animation playback: covered by Task 1 and Task 4.
- Compatibility fallback: covered by Task 3.
- No stat or economy changes: maintained by leaving backend combat formulas unchanged.
- Tests: covered by Tasks 1, 3, 4, and 5.

Empty-marker scan: no unfinished markers or copy-forward steps remain. Prompts and code snippets are concrete.

Type consistency: plan uses existing `Monster.kind`, `Monster.role`, `Monster.theme`, `event.kind`, `event.data.monster_id`, `PIXEL_SPRITES.monsters`, `ASSET_PATHS`, and `PIXEL_MONSTER_ACTIONS` names.
