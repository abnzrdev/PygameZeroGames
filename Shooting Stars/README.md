# Shooting Stars

A simple target-clicking game built with Pygame Zero.

## Overview

In Shooting Stars you must click the red star (the target) before all stars leave the screen. Clicking a non-red star ends the game. Each successful hit increases the level and spawns more stars.

## Files

- `game.py` — main game logic (Pygame Zero).
- `images/` — game assets (star images and background).

## Controls

- Left mouse click on a star:
  - If the star is the red target, you advance to the next level.
  - If the star is not red, the game ends.
- On the Game Over screen, click anywhere to restart.

## Requirements

- Python 3.8 or newer
- `pygame`
- `pgzero` (Pygame Zero)

Install dependencies:

```
pip install pygame pgzero
```

## Run (Windows)

From the `Shooting Stars` project folder run:

```
pgzrun game.py
```

or

```
python -m pgzero game.py
```

## Notes

- Star images and background are under `images/`.
- Screen size is defined in `game.py` (WIDTH = 800, HEIGHT = 600).
- This repository had `app.py` removed; `game.py` is the entry point.

## License

Free to use and modify.

