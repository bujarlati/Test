# Pixel Asset Prompt Notes

These first-pass assets are generated locally with `tools/generate_pixel_assets.py`.
They establish the file layout, frame sizes, animation rows, and anchors that future
Pixellab exports should follow.

Recommended Pixellab prompt base:

```text
dark fantasy pixel art side-view game sprite, clean readable silhouette, upper-left
warm rim light, transparent background, sprite sheet, no text, no UI frame, no watermark
```

Hero export target:

- 96x96 frame size
- 8 columns
- rows: idle, walk, attack_unarmed, attack_blade, attack_dual, attack_bow,
  attack_spear, attack_heavy, hurt, death, revive
- base hero frames must keep both hands empty; weapons are separate overlays attached
  by per-frame hand anchors in the frontend

Monster export target:

- common monsters: 64x64 frame size
- boss monsters: 128x128 frame size
- 8 columns
- rows: idle, walk, attack, hurt, death
