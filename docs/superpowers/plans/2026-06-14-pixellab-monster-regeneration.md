# Pixellab Monster Regeneration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the temporary safe-generated monster sheets with real Pixellab-generated monster animation assets that are complete, side-view, and game-ready.

**Architecture:** Generate one approved Pixellab seed frame per monster, animate each action from that seed, normalize frames into fixed sprite sheets, and only import sheets that pass automated frame completeness checks. Keep the safe generator as a fallback/testing utility, but the active manifest records should use `source: "pixellab"`.

**Tech Stack:** Pixellab API helper `tools/pixellab_api_generate.py`, Python PNG utilities, Canvas sprite renderer in `web/app.js`, manifest data in `web/assets/pixel/v1/manifests/assets.json`, Python unittest.

---

### Task 1: Confirm Pixellab Access

**Files:**
- Read: `docs/pixellab-api-workflow.md`
- Use: `tools/pixellab_api_generate.py`

- [ ] **Step 1: Check account balance**

Run:

```powershell
C:\Users\赵春健\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe tools\pixellab_api_generate.py balance
```

Expected: JSON balance output. If the key is missing or the API is unavailable, stop and report that Pixellab generation cannot proceed locally.

### Task 2: Generate Pixellab Seed Frames

**Files:**
- Create: `artifacts/pixellab/api/monsters/regenerated/<monster>/seed.png`

- [ ] **Step 1: Generate one transparent side-view seed per monster**

Use `tools\pixellab_api_generate.py image --model pixflux` for each monster at `128x128` for common monsters and `256x256` for bosses. Prompt requirements:

```text
dark fantasy pixel art side-view Monster Hunter inspired game monster, facing right, full body centered, transparent background, no text, no scenery, complete silhouette with head feet tail fully visible, readable at small game scale
```

- [ ] **Step 2: Reject incomplete seeds**

Use PNG alpha bounding-box checks. Reject seeds where visible pixels touch the canvas edge or where the visible area is too sparse.

### Task 3: Animate Pixellab Actions

**Files:**
- Create: `artifacts/pixellab/api/monsters/regenerated/<monster>/<action>/frame_*.png`

- [ ] **Step 1: Generate action strips from the approved seed**

For each monster and each action, run:

```powershell
C:\Users\赵春健\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe tools\pixellab_api_generate.py animate --first-frame artifacts\pixellab\api\monsters\regenerated\<monster>\seed.png --action "<action prompt>" --frame-count 8 --no-background --out-dir artifacts\pixellab\api\monsters\regenerated\<monster>\<action>
```

Actions:

```text
idle: subtle breathing idle loop, same monster, stable feet, no camera movement
walk: smooth in-place side-view walk loop, same monster, stable body scale, no travel across frame
attack: clear side-view attack animation, same monster, strike forward then recover, full body stays visible
hurt: brief recoil hurt animation, same monster, full body stays visible
death: collapse or dissolve death animation, same monster, full body stays visible
```

### Task 4: Normalize Into Game Sheets

**Files:**
- Create: `tools/import_pixellab_monster_sheets.py`
- Modify: `web/assets/pixel/v1/monsters/common/*.png`
- Modify: `web/assets/pixel/v1/monsters/bosses/*.png`
- Modify: `web/assets/pixel/v1/manifests/assets.json`

- [ ] **Step 1: Build one 8-column by 5-row sheet per monster**

Common monsters use `64x64` slots and boss monsters use `128x128` slots. Rows are `idle`, `walk`, `attack`, `hurt`, `death`.

- [ ] **Step 2: Normalize with shared scale and bottom-center anchor**

Scale all frames for one monster with one shared scale, keep transparent margins, and align visible bodies to a stable bottom-center anchor.

- [ ] **Step 3: Mark imported records as Pixellab**

Set each regenerated monster manifest record to:

```json
"source": "pixellab"
```

### Task 5: Verification

**Files:**
- Modify: `tests/test_web_static.py`

- [ ] **Step 1: Update tests to require Pixellab source**

The monster roster test should require `source == "pixellab"` for regenerated monsters.

- [ ] **Step 2: Run targeted checks**

Run:

```powershell
C:\Users\赵春健\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -m unittest tests.test_web_static.WebStaticTests.test_pixellab_monster_roster_assets_exist_and_are_wired tests.test_web_static.WebStaticTests.test_pixellab_monster_frames_are_normalized_inside_sprite_slots tests.test_web_static.WebStaticTests.test_pixellab_monster_body_frames_keep_stable_anchor -v
```

Expected: all pass.

- [ ] **Step 3: Run full checks**

Run:

```powershell
C:\Users\赵春健\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -m unittest discover -v
C:\Users\赵春健\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe --check web\app.js
```

Expected: tests pass and JS syntax check exits 0.
