# Movement Speed And Regeneration Polish Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make move speed visibly affect map traversal and monster encounter cadence, and make HP regeneration work consistently while the hero is moving.

**Architecture:** Keep movement and healing rules in `idle_forest/engine.py`, with hero stat calculations staying in `idle_forest/models.py`. The frontend should display move speed clearly and use existing smooth visual interpolation so faster movement feels faster rather than merely changing backend ticks.

**Tech Stack:** Python game engine, `unittest`, vanilla HTML/CSS/Canvas frontend.

---

## File Structure

- Modify: `tests/test_engine.py`
  - Add regression tests for move-speed encounter timing and HP regen while approaching a monster.
- Modify: `idle_forest/engine.py`
  - Ensure regen is applied during every movement state, including approach movement in `_advance_combat`.
  - Keep `_roll_next_encounter_x()` distance-based so higher move speed naturally reaches monsters faster in real time.
- Modify: `web/index.html`
  - Add a visible move-speed stat beside attack speed and regen.
- Modify: `web/app.js`
  - Render `hero.speed` in the HUD.
  - Optionally add a subtle footstep/wind trail scale based on `hero.speed` so fast movement reads visually.
- Modify: `web/styles.css`
  - Adjust the stat grid so the extra move-speed stat fits cleanly on desktop and mobile.

---

### Task 1: Prove Move Speed Changes Encounter Timing

**Files:**
- Modify: `tests/test_engine.py`

- [ ] **Step 1: Add a failing regression test**

Add this test near the existing movement/combat tests:

```python
def test_move_speed_reaches_next_forest_encounter_faster(self) -> None:
    slow = GameEngine(seed=101)
    fast = GameEngine(seed=101)

    slow.hero.speed = 25.0
    fast.hero.speed = 75.0
    slow._next_encounter_x = 180.0
    fast._next_encounter_x = 180.0

    slow.advance(2.0)
    fast.advance(2.0)

    self.assertIsNone(slow.active_monster)
    self.assertIsNotNone(fast.active_monster)
```

- [ ] **Step 2: Run the targeted test**

Run:

```powershell
python -m unittest tests.test_engine.GameEngineTests.test_move_speed_reaches_next_forest_encounter_faster
```

Expected before any fix: this may already pass if backend movement is correct. If it passes, keep it as a guardrail.

- [ ] **Step 3: Confirm no hidden fixed-time encounter logic exists**

Inspect `idle_forest/engine.py` and keep encounter spawning tied to:

```python
self.hero.x += self.hero.move_speed * dt
if self.hero.x >= self._next_encounter_x:
    self._spawn_monster()
```

Do not replace distance-based encounters with timers. The player expectation is: higher move speed crosses map distance faster, so monsters are reached faster.

- [ ] **Step 4: Run the targeted test again**

Run:

```powershell
python -m unittest tests.test_engine.GameEngineTests.test_move_speed_reaches_next_forest_encounter_faster
```

Expected: PASS.

---

### Task 2: Fix HP Regen While Approaching A Monster

**Files:**
- Modify: `tests/test_engine.py`
- Modify: `idle_forest/engine.py`

- [ ] **Step 1: Add a failing regression test**

Add this test near `test_hp_regen_controls_travel_healing`:

```python
def test_hp_regen_ticks_while_approaching_monster(self) -> None:
    engine = GameEngine(seed=102)
    engine.hero.hp = 20
    engine.hero.base_hp_regen = 12.0
    engine.active_monster = Monster(
        id="far_monster",
        kind="forest_slime",
        level=1,
        max_hp=200,
        hp=200,
        attack=1,
        defense=0,
        exp_reward=0,
        gold_reward=0,
        x=engine.hero.x + 220,
        y=engine.hero.y,
    )

    engine.advance(1.0)

    self.assertGreater(engine.hero.hp, 20)
    self.assertIsNotNone(engine.active_monster)
```

- [ ] **Step 2: Run the targeted test and verify failure**

Run:

```powershell
python -m unittest tests.test_engine.GameEngineTests.test_hp_regen_ticks_while_approaching_monster
```

Expected before the fix: FAIL because `_advance_combat()` moves toward the monster but does not call `_heal_hero_over_time()`.

- [ ] **Step 3: Apply regen during approach movement**

In `idle_forest/engine.py`, update `_advance_combat()` so the approach branch heals while walking:

```python
if distance > attack_range:
    move_distance = min(distance - attack_range, self.hero.move_speed * dt)
    self.hero.x += move_distance
    self._heal_hero_over_time(self.hero.hp_regen, dt)
    distance = self.active_monster.x - self.hero.x
```

Keep combat-range behavior unchanged unless design later decides in-combat regen should also tick.

- [ ] **Step 4: Run the targeted test again**

Run:

```powershell
python -m unittest tests.test_engine.GameEngineTests.test_hp_regen_ticks_while_approaching_monster
```

Expected: PASS.

---

### Task 3: Make Move Speed Visible In The HUD

**Files:**
- Modify: `web/index.html`
- Modify: `web/app.js`
- Modify: `web/styles.css`
- Modify: `tests/test_web_static.py`

- [ ] **Step 1: Add static frontend expectations**

In `tests/test_web_static.py`, add a static test:

```python
def test_frontend_displays_move_speed_stat(self) -> None:
    html = (ROOT / "web" / "index.html").read_text(encoding="utf-8")
    script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")

    self.assertIn("moveSpeedText", html)
    self.assertIn("hero.speed", script)
    self.assertIn("moveSpeed", script)
```

- [ ] **Step 2: Run the static test and verify failure**

Run:

```powershell
python -m unittest tests.test_web_static.WebStaticTests.test_frontend_displays_move_speed_stat
```

Expected: FAIL because the HUD has attack speed and regen but not movement speed.

- [ ] **Step 3: Add the HUD element**

In `web/index.html`, add one stat between defense and attack speed:

```html
<div class="stat"><span>移速</span><strong id="moveSpeedText">0</strong></div>
```

- [ ] **Step 4: Wire the element in JavaScript**

In `web/app.js`, add the element to `els`:

```js
moveSpeedText: document.querySelector('#moveSpeedText'),
```

Then render it in `applySnapshot(snapshot)`:

```js
els.moveSpeedText.textContent = `${Number(hero.speed || 0).toFixed(1)} / ${t('seconds')}`
```

Also add translation keys:

```js
moveSpeed: '移速'
```

and:

```js
moveSpeed: 'Move Speed'
```

- [ ] **Step 5: Adjust the stat grid**

In `web/styles.css`, update `.hero-strip` to fit nine stats:

```css
.hero-strip {
  grid-template-columns: 0.7fr 1.2fr 1.2fr repeat(6, 0.85fr);
}
```

- [ ] **Step 6: Run the static test again**

Run:

```powershell
python -m unittest tests.test_web_static.WebStaticTests.test_frontend_displays_move_speed_stat
```

Expected: PASS.

---

### Task 4: Make Faster Movement Feel Faster On Canvas

**Files:**
- Modify: `web/app.js`
- Modify: `tests/test_web_static.py`

- [ ] **Step 1: Add a static visual-behavior guard**

In `tests/test_web_static.py`, add:

```python
def test_frontend_scales_movement_visuals_with_speed(self) -> None:
    script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")

    self.assertIn("movementIntensity", script)
    self.assertIn("drawMovementTrail", script)
```

- [ ] **Step 2: Run the static test and verify failure**

Run:

```powershell
python -m unittest tests.test_web_static.WebStaticTests.test_frontend_scales_movement_visuals_with_speed
```

Expected: FAIL until the movement visual helpers exist.

- [ ] **Step 3: Add movement intensity helper**

In `web/app.js`, add:

```js
function movementIntensity(entity) {
  const speed = Number(entity.speed || 0)
  return Math.max(0, Math.min(1, (speed - 38) / 70))
}
```

- [ ] **Step 4: Draw a subtle trail for fast movement**

In `drawHero(x, groundY, entity)`, before drawing the body, call:

```js
drawMovementTrail(x, groundY, entity)
```

Add:

```js
function drawMovementTrail(x, groundY, entity) {
  const intensity = movementIntensity(entity)
  if (intensity <= 0 || (entity.state !== 'walk' && entity.state !== 'approach')) {
    return
  }
  ctx.save()
  ctx.globalAlpha = 0.14 + intensity * 0.18
  ctx.strokeStyle = '#c7f0d0'
  ctx.lineWidth = 2
  for (let index = 0; index < 3; index += 1) {
    const offset = 20 + index * 12
    ctx.beginPath()
    ctx.moveTo(x - offset, groundY - 24 - index * 5)
    ctx.quadraticCurveTo(x - offset - 18, groundY - 32, x - offset - 34, groundY - 20)
    ctx.stroke()
  }
  ctx.restore()
}
```

- [ ] **Step 5: Run the static test again**

Run:

```powershell
python -m unittest tests.test_web_static.WebStaticTests.test_frontend_scales_movement_visuals_with_speed
```

Expected: PASS.

---

### Task 5: Final Verification

**Files:**
- No new files.

- [ ] **Step 1: Run all tests**

Run:

```powershell
python -m unittest
```

Expected: all tests pass.

- [ ] **Step 2: Browser check on local app**

Open or refresh:

```text
http://127.0.0.1:8000/
```

Check:

- Move-speed stat is visible.
- Higher move-speed heroes visibly cross ground faster.
- HP increases while walking toward a monster if the hero is below max HP.
- No console errors.

- [ ] **Step 3: Commit**

Run:

```powershell
git add tests/test_engine.py tests/test_web_static.py idle_forest/engine.py web/index.html web/app.js web/styles.css
git commit -m "fix: polish movement speed and regeneration"
```

Expected: commit succeeds.

---

## Self-Review

- Spec coverage: move speed clarity is covered by Tasks 1, 3, and 4. Moving-period HP regen is covered by Task 2. Final testing is covered by Task 5.
- Placeholder scan: no task contains TBD/TODO/fill-in instructions.
- Type consistency: all planned functions and ids are consistent with the current codebase names: `hero.speed`, `moveSpeedText`, `_advance_combat`, `_heal_hero_over_time`, and `tests.test_web_static.WebStaticTests`.
