# Idle Forest Polish Design

## Goal

Improve Idle Forest from a running prototype into a smoother playable slice: movement should feel continuous, combat should keep readable weapon distance, monsters should enter from ahead instead of popping onto the hero, and the first screen should support local login, character creation, gender selection, and up to three talent rolls.

## Scope

This pass keeps the game single-player and local-first. Browser localStorage stores the current profile and character choice. The Python server still owns the game loop and market prototype. The design leaves clear room for future server accounts and multiplayer market persistence, but does not add a database or real account service yet.

## Combat And Movement

The engine will expose enough combat metadata for the client to draw believable spacing:

- Hero has attack speed, health regeneration speed, and attack range.
- Equipped weapons can influence attack range and attack speed later. This pass starts with a melee range large enough to avoid overlap.
- Monsters spawn ahead of the hero at a visible approach distance. The hero keeps walking toward the encounter until the monster is inside attack range.
- Combat damage only starts when the distance is within the hero attack range.
- Snapshot scene entities include attack range, attack speed, hp regen, equipped weapon data, and whether the hero is walking or fighting.

This makes future bow support simple: add a ranged weapon type with a larger attack range.

## Animation

The backend continues to advance in small deterministic steps. The web client becomes responsible for presentation smoothing:

- Keep the previous and current snapshots.
- Interpolate entity positions between snapshots in requestAnimationFrame.
- Use elapsed time instead of frame count for sprite animation.
- Add approach, combat, and attack swing visual states so attacks feel animated instead of merely changing numbers.
- Keep canvas rendering stable under resize and high-DPI displays.

## Character Creation

The app starts with a local profile gate when no character exists:

1. Player enters a login/name.
2. Player chooses male or female.
3. Player rolls one set of three starting talents.
4. Player may reroll the full set up to three total rolls.
5. Player confirms the set and enters the game.

The confirmed profile is saved in localStorage. Resetting the game should reset the current run but not erase the local character unless a separate "new character" action is used.

## API

Add small HTTP endpoints while keeping the stdlib server:

- `GET /profile`: returns whether a character exists and the current character metadata.
- `POST /profile/roll`: creates or updates a draft roll for a name and gender, returning talents and remaining rolls.
- `POST /profile/confirm`: confirms the current draft and creates a GameEngine with the selected character.
- `POST /profile/clear`: clears the server-side profile for local testing.

The web client stores the same character in localStorage, and the server stores it in memory for the current process. This is intentionally lightweight until real accounts are added.

## UI

The main screen remains a playable tool surface, not a landing page. Add:

- Login/create-character overlay before the game.
- Gender segmented control.
- Talent roll cards with rarity colors.
- Attack speed and regeneration stats in the top strip.
- Weapon-aware hero drawing in combat.
- Monster approach from the right side of the scene.

## Testing

Backend tests cover:

- Monster spawn distance is larger than attack range.
- Hero does not attack before the monster is inside attack range.
- Attack speed changes attack interval.
- HP regeneration changes healing.
- Profile roll and confirm create a character with three talents and roll limits.

Frontend verification covers:

- Page opens.
- Login/create-character flow can confirm a character.
- Main game renders.
- Snapshot and tick endpoints respond.
