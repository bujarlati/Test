# Pixellab API Workflow

This project should use the Pixellab API for future pixel asset generation instead
of manual web clicks.

## Sources

- API overview: https://www.pixellab.ai/pixellab-api
- Interactive v2 docs: https://api.pixellab.ai/v2/docs
- LLM-readable v2 docs: https://api.pixellab.ai/v2/llms.txt
- OpenAPI schema: https://api.pixellab.ai/v2/openapi.json

## Authentication

Pixellab v2 uses Bearer token authentication.

Store the token locally and never commit it:

```powershell
$env:PIXELLAB_API_KEY = "YOUR_API_TOKEN"
```

Linux:

```bash
export PIXELLAB_API_KEY="YOUR_API_TOKEN"
```

Or create a local `.env` file in the project root:

```text
PIXELLAB_API_KEY=YOUR_API_TOKEN
```

`.env` is ignored by git.

The API base URL is:

```text
https://api.pixellab.ai/v2
```

## Recommended Endpoints

Use these first for the game asset pipeline:

- `POST /create-image-pixflux`
  - Synchronous single image.
  - Good for polished 128x128 to 400x400 concepts.
  - Supports `init_image`, forced palette, and transparent background.

- `POST /create-image-pixen`
  - Synchronous smaller sprite/image generation.
  - Supports `detail`, `outline`, `view`, `direction`, and transparent background.
  - Good for quick 64x64 or 128x128 sprite experiments.

- `POST /generate-image-v2`
  - Async pro image generation.
  - Returns `background_job_id`; poll `GET /background-jobs/{job_id}`.
  - Good for 2x2 or 4x4 candidate sheets and style/reference-image work.

- `POST /animate-with-text-v3`
  - Async animation from a first frame and text action.
  - Good for `idle`, `run`, `attack`, `hurt`, `death`, and `revive` strips.
  - Frame count guideline from the docs: 4 for simple loops, 8 for walk/run,
    16 for complex attacks.

- `POST /estimate-skeleton`
  - Synchronous skeleton keypoint estimation for a character image.
  - Good for extracting per-frame weapon and equipment attachment points.
  - The response contains normalized keypoints, not a browser-runtime Spine
    or DragonBones rig.

- `POST /animate-with-skeleton`
  - Skeleton-controlled animation generation.
  - Good when a weapon action must follow deliberately authored poses instead
    of text-only motion.

- `POST /create-character-v3`
  - Async character generation with 8 rotations.
  - Useful as a reference pass, but for this side-scroller game inspect output
    carefully because pure side views can become too narrow.

- `POST /map-objects`
  - Async transparent object generation.
  - Good for equipment previews, pets, wings, halos, foot circles, chests,
    forest props, and world items.

- `POST /create-1-direction-object`
  - Async object pipeline for one-direction objects.
  - Good for side-scroller equipment/props when we do not need rotations.

- `POST /create-8-direction-object`
  - Async object pipeline for 8-direction objects.
  - Useful only when the same object must rotate consistently.

## Useful Request Fields

Common fields:

```json
{
  "description": "dark long-haired female assassin...",
  "image_size": { "width": 128, "height": 128 },
  "no_background": true,
  "seed": 42
}
```

Style enums confirmed from OpenAPI:

- `outline`: `single color black outline`, `single color outline`,
  `selective outline`, `lineless`
- `detail`: `low detail`, `medium detail`, `highly detailed`
- `shading`: `flat shading`, `basic shading`, `medium shading`,
  `detailed shading`, `highly detailed shading`
- `view`: `side`, `low top-down`, `high top-down`
- `direction`: `north`, `north-east`, `east`, `south-east`, `south`,
  `south-west`, `west`, `north-west`

## Local Helper

Use `tools/pixellab_api_generate.py`.

Check balance:

```powershell
python tools\pixellab_api_generate.py balance
```

Generate a single transparent Pixflux image:

```powershell
python tools\pixellab_api_generate.py image `
  --model pixflux `
  --prompt "dark long-haired female assassin, side-view facing right, empty hands, no weapon, black shadow armor, long black-violet hair, game-ready pixel sprite" `
  --width 128 --height 128 `
  --no-background `
  --out artifacts\pixellab\api\female_assassin_pixflux.png
```

Generate a 2x2 candidate sheet through the async Pro endpoint:

```powershell
python tools\pixellab_api_generate.py pro-image `
  --prompt "Create a 2x2 pose sheet of the same dark long-haired female assassin: idle, run, attack, hurt. Empty hands, no weapon, transparent background, same proportions." `
  --width 128 --height 128 `
  --no-background `
  --out-dir artifacts\pixellab\api\female_assassin_pose_sheet
```

Animate from an approved first frame:

```powershell
python tools\pixellab_api_generate.py animate `
  --first-frame artifacts\pixellab\female_assassin_dark_reference.png `
  --action "smooth side-view running loop, same character, stable foot anchor" `
  --frame-count 8 `
  --no-background `
  --out-dir artifacts\pixellab\api\female_assassin_run
```

Estimate a skeleton for one approved frame:

```powershell
python tools\pixellab_api_generate.py estimate-skeleton `
  --image artifacts\pixellab\api\female_assassin_v2_seed_right.png `
  --out artifacts\pixellab\api\skeleton\female_assassin_v2_seed_right.json
```

Generate a transparent equipment or pet object:

```powershell
python tools\pixellab_api_generate.py map-object `
  --prompt "tiny cute shadow fox pet, dark fantasy pixel art, side-view, black purple glow, transparent background" `
  --width 128 --height 128 `
  --view side `
  --outline "single color outline" `
  --detail "medium detail" `
  --shading "medium shading" `
  --out-dir artifacts\pixellab\api\shadow_fox_pet
```

Generate through the Pixellab object pipeline:

```powershell
python tools\pixellab_api_generate.py object `
  --directions 1 `
  --prompt "floating dark violet halo aura for assassin helmet slot, pixel art, transparent background" `
  --size 64 `
  --view sidescroller `
  --out-dir artifacts\pixellab\api\helmet_halo_object
```

## Game Pipeline Notes

- Keep generated source files in `artifacts/pixellab/api/` until approved.
- Only copy approved, normalized sprites into `web/assets/pixel/v1/`.
- For heroes, prefer 96x96 or 128x128 working frames with transparent background.
- Keep base hero hands empty because weapons are attached by the game runtime.
- For side-scroller characters, inspect side-view output before accepting.
  The Pixellab 8-direction character generator can produce narrow side views.
- After choosing a base frame, generate animation strips from that frame rather
  than generating every animation frame independently.
- For weapon alignment, estimate skeletons for each approved animation frame
  and convert hand/arm keypoints into `frameAnchors` in the frontend.
- Treat Pixellab's estimated angle as a starting point. If a single frame points
  backward, clamp or hand-tune the weapon angle while keeping the estimated hand
  position.
