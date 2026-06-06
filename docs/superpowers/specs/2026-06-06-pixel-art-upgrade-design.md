# Pixel Art Upgrade Design

## Goal

Upgrade Idle Forest from rough prototype visuals to a cohesive, attractive pixel-art action-idle game. The target is a smooth side-view pixel game with readable characters, stylish monsters, layered forest maps, clear equipment identity, and effects that make rare items and talents feel valuable.

## Scope

This design covers the visual upgrade pipeline and the first production pass for:

- player character sprites for male and female heroes
- layered equipment visuals for weapons, helmets, armor, boots, rings, and future dual wielding
- common monsters, elite monsters, and bosses
- forest, deep forest, cave, and ruin map tilesets
- attack, rarity, loot, death, revive, and talent aura effects
- cancel-listing market polish needed to keep testing clean

This does not replace combat rules, account logic, or server persistence. It also does not add multiplayer combat.

## Visual Direction

The game should read as a dark fantasy pixel side-scroller with clean silhouettes and warm forest lighting. The current hand-drawn canvas rig can stay as a fallback, but the main presentation should move to sprite-sheet animation.

Target qualities:

- beautiful enough that players want to keep the page open
- clear silhouettes at small sizes on mobile
- smooth action using authored animation frames instead of procedural limb drawing
- consistent lighting direction from upper left
- restrained but satisfying particles for rarity and talents
- deep forest should feel darker, denser, and more dangerous

## Asset Standards

Hero sprites:

- base frame size: 96x96
- side-view facing right; canvas can flip for facing left later
- actions: idle, walk, attack, hurt, death, revive
- minimum frames: idle 6, walk 8, attack 8, hurt 4, death 8, revive 8
- male and female share the same anchor layout for equipment

Monster sprites:

- common monster frame size: 64x64
- elite monster frame size: 96x96
- boss frame size: 128x128
- actions: idle, walk, attack, hurt, death
- monsters should face the hero directly, not show their back

Map assets:

- tile size: 32x32
- tilesets: forest, deep forest, cave, ruin
- layers: sky, far background, mid background, front props, ground, foreground accents
- deep forest uses more dense foreground silhouettes and lower brightness

Effects:

- attack effect size: 96x96 to 160x96 depending on weapon reach
- rarity aura sprites or particle presets for purple, gold, and red items
- talent aura sprites for movement, lightning, gold, defense, life, and treasure themes
- loot and gold-loss floaters stay in canvas text for now but get pixel-styled glow

## Pixellab Workflow

Pixellab should be used to generate consistent pixel assets, but each asset must be reviewed before import. The workflow is:

1. Generate a small style bible first:
   - male hero idle/walk/attack
   - female hero idle/walk/attack
   - slime, wolf, treant, imp, bat
   - one boss
   - forest and deep forest tileset
2. Keep prompts consistent:
   - "dark fantasy pixel art side-view game sprite"
   - "clean readable silhouette"
   - "upper-left warm rim light"
   - "transparent background"
   - "96x96 sprite sheet"
   - "no text, no UI frame, no watermark"
3. Export PNG sprite sheets and keep original prompts in metadata files.
4. Import only approved assets under `web/assets/pixel/v1/`.
5. Keep old assets under `web/assets/sprites/` until the new renderer has fallback coverage.

## File Layout

New visual assets should live under:

```text
web/assets/pixel/v1/
  heroes/
    male/
    female/
  equipment/
    weapons/
    helmets/
    armor/
    boots/
    rings/
  monsters/
    common/
    elite/
    bosses/
  maps/
    forest/
    deep_forest/
    cave/
    ruin/
  effects/
    attacks/
    auras/
    loot/
  manifests/
```

Each animated asset gets a manifest entry with:

- image path
- frame width and height
- frames per action
- frame duration
- anchor points for feet, weapon hand, off hand, head, torso, and hitbox
- optional rarity and talent effect metadata

## Renderer Direction

`web/app.js` is already large, so the pixel-art upgrade should avoid adding more visual complexity there. The first art pass may add small helpers in `web/app.js`, but the planned end state is:

- `web/renderer/assets.js`: loads manifests and images
- `web/renderer/animation.js`: resolves current animation frame
- `web/renderer/character.js`: draws hero base sprite and equipment layers
- `web/renderer/monsters.js`: draws monster and boss sprites
- `web/renderer/maps.js`: draws parallax maps and tiles
- `web/renderer/effects.js`: draws attack effects and talent auras

The existing renderer remains as fallback until each replacement is visually verified.

## Gameplay Integration

The server snapshot already exposes enough state for the first pass:

- hero gender
- hero state
- equipped items
- weapon type and rarity
- monster role, kind, threat, and theme
- forest depth and mode
- attack events
- loot events

The renderer maps this data to visual keys. No server schema migration is required for the first art pass. Later, content tables can add explicit `visual_id` fields for monsters and equipment.

## Cancel Listing

Market polish must include cancel listing before broad visual testing continues. The behavior is:

- sellers can cancel their own active listing
- canceled items return to the seller inventory
- canceled listings disappear from active market views
- other players cannot cancel someone else's listing
- front-end shows "Cancel Listing" only on the current hero's own active listings

## Rollout Phases

Phase 1: market cleanup and asset foundation.

- add cancel-listing endpoint and UI
- add asset directories and manifest format
- add documentation for Pixellab prompts and export settings

Phase 2: hero replacement.

- import male and female base sprite sheets
- render idle, walk, attack, hurt, death, and revive
- align weapon hand and equipment anchors
- preserve current skeleton renderer as fallback

Phase 3: equipment visuals.

- import starter sword, sword, axe, spear, and rare weapon variants
- add helmet, armor, boots, and ring visual layers
- add rarity particles for purple, gold, and red equipment

Phase 4: monster and boss replacement.

- import five common monsters, two elite variants, and one boss
- make monster facing consistent
- add hit and death animations

Phase 5: map upgrade.

- import forest and deep forest tilesets
- add richer parallax layers
- make forest depth affect darkness, density, and prop selection

Phase 6: effects pass.

- import weapon slash effects
- import lightning, life, treasure, and defense talent auras
- connect rare item particles to equipped gear

## Verification

Every visual phase must pass:

- `python -m unittest`
- `node --check web/app.js`
- desktop browser smoke test at 127.0.0.1:8000
- mobile-width smoke test
- visual check for no blank sprites, no flicker, no severe overlap, and correct equipment anchors

## Success Criteria

The upgrade is successful when:

- hero movement and attacks use smooth sprite animation
- male and female characters are visually distinct and attractive
- equipment visibly changes the character
- monsters and bosses look intentional and face the player
- deep forest looks darker and more dangerous than normal forest
- rare gear and talents have memorable but readable effects
- the old prototype visual layer can remain only as fallback, not as the main look
