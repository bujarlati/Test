# Pixellab Monster Upgrade Design

## Goal

Upgrade Idle Forest's monster presentation from a small set of reused models into a broader dark-fantasy pixel monster roster. The new direction combines ecological forest creatures, theme-specific rift mutations, and larger apex rift bosses. Every new monster model must include a readable attack animation so combat feels alive rather than like monsters are only walking or idling.

The intended inspiration is the hunting-game feeling of large, grounded creatures with clear silhouettes and weighty attacks, without copying any specific Monster Hunter creature designs.

## Current Context

The current monster sprite format is already suitable for this upgrade:

- common monsters use `64x64` frames
- boss monsters use `128x128` frames
- sheets use 8 columns and 5 animation rows: `idle`, `walk`, `attack`, `hurt`, `death`
- assets live under `web/assets/pixel/v1/monsters/`
- the manifest lives at `web/assets/pixel/v1/manifests/assets.json`

The backend already has more monster `kind` values than the frontend currently displays. Forest, deep forest, rift minions, and rift bosses are distinguished in `idle_forest/content.py`, but the frontend currently collapses many kinds into only a few sprites. The frontend also has an attack row available for monsters, but ordinary monsters are effectively rendered as walking and bosses as attacking, instead of reacting to monster attack events.

## Visual Direction

Forest monsters should feel like wild ecology:

- horned forest boars and tusked beasts
- moss-backed reptile or wyvern-like small predators
- armored insects and fungal crawlers
- bark guards and bramble beasts

Rift minions should be theme mutations:

- cave: crystal beasts, stone crawlers, cavern wing-creatures
- sky: storm birds, cloud wisps, sun motes, windborne predators
- castle: rust guards, hollow knights, cursed squires, haunted constructs

Rift bosses should be apex encounters:

- cave boss: a crystal-jawed cave warden with a lunge, bite, or crystal-spike burst
- sky boss: a tempest wing-seraph with a dive, lightning wing sweep, or wind slash
- castle boss: a throne keeper with a heavy blade smash, shield crush, or cursed charge

All monsters should remain side-view, facing right, with strong silhouettes and readable hit boxes at game scale.

## Asset Pipeline

Pixellab generation should follow the existing project workflow in `docs/pixellab-api-workflow.md` and `web/assets/pixel/v1/PROMPTS.md`.

For each monster:

- generate or select a clean approved first frame
- generate one full animation sheet or strip rather than isolated frames
- use transparent background
- preserve side-view facing direction
- preserve a stable bottom-center foot or body anchor
- keep outlines and contrast readable over forest and rift backgrounds
- keep source generations in `artifacts/pixellab/api/`
- copy only approved normalized assets into `web/assets/pixel/v1/monsters/`

Target format:

- common monsters: `64x64`, 8 columns, rows `idle`, `walk`, `attack`, `hurt`, `death`
- rift bosses: `128x128`, 8 columns, rows `idle`, `walk`, `attack`, `hurt`, `death`

If Pixellab returns separate strips, combine them into the project sheet format before wiring them into the manifest.

## Runtime Integration

The frontend should map monster sprites by exact `monster.kind` first. Name substring fallback may remain only as a safety net for older saves or missing assets.

Recommended sprite mapping groups:

- forest and deep forest kinds receive distinct common monster sprites where possible
- cave, sky, and castle rift minions receive theme-specific sprites
- each rift boss kind receives its own boss sprite

Monster animation selection should become state-aware:

- dead monster: `death`
- recently damaged monster: `hurt`
- monster attack event just occurred: `attack`
- moving toward hero: `walk`
- otherwise: `idle`

The renderer should track recent `monster_attack` events just as it already tracks hero attack effects. This makes the attack rows meaningful for ordinary monsters and bosses.

## Data And Compatibility

No backend stat changes are required for this visual upgrade. Existing `kind`, `role`, `theme`, `position`, and combat events are enough to drive the new rendering.

Existing saves should keep working:

- if a monster kind has no dedicated sprite yet, use a fallback by kind family or current slime/thorn/imp/forest boss assets
- old treasure mimic rendering remains unchanged in this pass
- missing assets should degrade to existing canvas fallback instead of breaking combat rendering

## Testing

Static frontend tests should verify:

- new asset keys are declared in `ASSET_PATHS`
- `PIXEL_SPRITES.monsters` includes the new common and boss records
- `pixelMonsterRecord` maps by exact `entity.kind`
- monster attack events are tracked
- `pixelMonsterAction` can return `attack` for normal monsters and bosses
- every declared new PNG exists and has a valid PNG signature
- the manifest includes the new monster records with the expected animation rows

Engine tests should verify the backend still exposes the existing forest, deep forest, rift minion, and rift boss kind values needed by the frontend.

## Scope

This pass focuses on monster and rift boss presentation. It does not change rewards, monster stats, rift progression, drop rates, equipment, talents, or player combat balance.

The first implementation batch should prioritize enough variety to make the change visible:

- at least 5 forest or deep-forest common monster sprites
- at least 9 rift minion sprites, one for each existing rift minion kind
- at least 3 rift boss sprites, one for each existing rift boss kind
- attack animation wired for all pixel monster sprites
