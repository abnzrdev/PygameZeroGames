# QuizMaster

A simple multiple-choice quiz game built with the pgzero library.

## What it is
- A small quiz game with a start screen, timed questions, and a final score screen.
- Questions are read from `questions.json` in the same folder.

## How to run
1. Install pgzero if you don't have it:

```bash
pip install pgzero
```

2. Run the game from the `QuizMaster` folder:

```bash
pgzrun game.py
```

(If your environment doesn't expose `pgzrun` directly, run `python -m pgzero game.py`.)

## Controls
- Click the "Start" button to begin.
- Click an answer option to choose it.
- Click "Quit" or let the timer run out to see your final score.

## `questions.json` format
The file should contain a JSON array of question objects. Each object should look like:

```json
{
  "question": "What is the capital of France?",
  "options": ["Paris", "London", "Berlin", "Rome"],
  "answer": 0
}
```

- `options` is an array of strings.
- `answer` is a 0-based index pointing to the correct option.

## Notes
- The code uses pgzero's `screen` and mouse handlers; no extra assets are required for the basic quiz.
- Keep `questions.json` in the same folder as `game.py` so the game can find it.