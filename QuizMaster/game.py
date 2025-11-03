"""
QuizMaster

Simple multiple-choice quiz game using pgzero library.
- This file contains the game logic, draw/update handlers and mouse input.
- Include the questions from 'questions.json' file.
- Run with: pgzrun game.py (or let the editor/IDE run the script with pgzero support).

"""

import pgzrun
import random
import time
from typing import TYPE_CHECKING

# Tell type checkers about the `screen` object injected by pgzero at runtime.(cause it shows error in the editor)
# This block is executed only by static analysis tools (TYPE_CHECKING=True).
# It has no runtime effect and does not change game behavior.
if TYPE_CHECKING:
    from pgzero.screen import Screen  # type: ignore
    screen: "Screen"  # type: ignore

# ---------------------------------------------------------------------------
# Game window / layout constants
# ---------------------------------------------------------------------------
WIDTH = 700
HEIGHT = 400  # reduced height
MID_X = WIDTH // 2
MID_Y = HEIGHT // 2
TITLE = "QUIZMASTER"

# ---------------------------------------------------------------------------
# Game state
# ---------------------------------------------------------------------------
# `game_state` controls which screen is shown: "start", "main", or "goodbye".
game_state = "start"

# ---------------------------------------------------------------------------
# Start screen: show title and simple Start / Quit buttons
# ---------------------------------------------------------------------------
def startgame():
    """Draw the welcome / start screen and compute button rectangles.

    This function draws the title and two labels (Start, Quit), and sets the
    global button rectangles used later for click detection.
    """
    screen.clear()
    screen.fill((50, 80, 120))

    title_y = MID_Y - int(HEIGHT * 0.12)
    buttons_y = MID_Y + int(HEIGHT * 0.08)

    screen.draw.text("Welcome to QuizMaster", center=(MID_X, title_y), fontsize=48, color="white")
    screen.draw.text("Start", center=(MID_X - 60, buttons_y), fontsize=36, color="yellow")
    screen.draw.text("Quit", center=(MID_X + 60, buttons_y), fontsize=36, color="red")

    # Button clickable areas: (x, y, width, height)
    global START_BUTTON, QUIT_BUTTON
    btn_w, btn_h = 140, 48
    START_BUTTON = (MID_X - 60 - btn_w // 2, buttons_y - btn_h // 2, btn_w, btn_h)
    QUIT_BUTTON = (MID_X + 60 - btn_w // 2, buttons_y - btn_h // 2, btn_w, btn_h)


# ---------------------------------------------------------------------------
# Main game screen: question, options, and timer
# ---------------------------------------------------------------------------
def maingame():
    """Draw the main quiz screen.

    - Draw the timer at the top
    - Lazy-load questions from disk the first time this runs
    - Choose a random question and format option text
    - Draw option texts and expose their click rectangles
    """
    screen.clear()
    screen.fill((30, 30, 40))

    # Layout anchors for question/options
    qx = int(WIDTH * 0.09)
    qy = int(HEIGHT * 0.18)

    # Read a module-level timer (seconds). If not present, default to 0.
    timer_seconds = globals().get("timer_seconds", 0)
    mins = timer_seconds // 60
    secs = timer_seconds % 60
    timer_text = f"{mins:02d}:{secs:02d}"

    # Draw timer centered above the question
    screen.draw.text(timer_text, center=(MID_X, MID_Y - int(HEIGHT * 0.25)), color="white", fontsize=84)

    # -----------------------------------------------------------------
    # Lazy-load questions from `questions.json` (only once)
    # Each question object is expected to have: question, options, answer
    # `answer` should be a 0-based index into the options list.
    # -----------------------------------------------------------------
    if "QUESTIONS" not in globals():
        try:
            import json
            from pathlib import Path
            p = Path("questions.json")

            if p.exists():
                raw = p.read_text(encoding="utf-8")
                data = json.loads(raw)
            else:
                data = []

            questions = []
            for it in data:
                # Read fields with safe defaults
                q = it.get("question", "")
                opts = list(it.get("options", []))
                ans = it.get("answer", 0)
                try:
                    ans = int(ans)
                except Exception:
                    ans = 0
                # Store as tuple: (question_text, [options], correct_index)
                questions.append((q, opts, ans))
        except Exception:
            questions = []
        # Expose QUESTIONS in module globals for reuse
        globals()["QUESTIONS"] = questions

        # Lazy-load questions from `questions.json` (only once)
        if "QUESTIONS" not in globals():
            try:
                import json
                from pathlib import Path
                # Use the script directory so the file is found reliably
                p = Path(__file__).parent / "questiosns.json"

                if p.exists():
                    raw = p.read_text(encoding="utf-8")
                    data = json.loads(raw)
                else:
                    data = []

                questions = []
                for it in data:
                    q = it.get("question", "")
                    opts = list(it.get("options", []))
                    ans = it.get("answer", 0)
                    try:
                        ans = int(ans)
                    except Exception:
                        ans = 0
                    questions.append((q, opts, ans))
            except Exception as e:
                questions = []
                print("Failed to load questions.json:", e)
            globals()["QUESTIONS"] = questions
            # Debug: confirm how many questions were loaded
            print(f"Loaded {len(questions)} questions from {p}")

    # -----------------------------------------------------------------
    # Choose a question to display and format the option strings
    # -----------------------------------------------------------------
    if globals().get("QUESTIONS"):
        total = len(globals()["QUESTIONS"])
        # choose a random question once and keep it until the user answers
        if "question_index" not in globals() or not (0 <= globals().get("question_index", -1) < total):
            globals()["question_index"] = random.randrange(total)
        q_index = globals()["question_index"]
        q_text, opts, correct_orig = globals()["QUESTIONS"][q_index]
        sample_question = q_text
        # Format options with letter prefixes (A), B), ...)
        options = [f"{chr(65 + i)}) {o}" for i, o in enumerate(opts)]
        # Store the correct option index for later click checking
        globals()["current_correct_index"] = correct_orig
    else:
        # Fallback question if no data file was found or parsing failed
        sample_question = "Which of the following options is correct?"
        options = [
            "A) First option",
            "B) Second option",
            "C) Third option",
            "D) Fourth option",
        ]

    # Draw the question text
    screen.draw.text(sample_question, center=(MID_X, MID_Y - int(HEIGHT * 0.06)), color="white", fontsize=20)

    # -----------------------------------------------------------------
    # Layout and draw option texts in two columns; also collect click rects
    # -----------------------------------------------------------------
    col_gap = int(WIDTH * 0.45)  # horizontal spacing between the two columns
    col_offsets = [qx + 20, qx + 20 + col_gap]
    line_spacing = int(HEIGHT * 0.18)  # vertical spacing between rows
    base_y = qy + 160
    btn_w = int(WIDTH * 0.4)
    btn_h = 48
    option_rects = []

    for i, opt in enumerate(options):
        col = i % 2
        row = i // 2
        x = col_offsets[col]
        y = base_y + row * line_spacing
        # store rect for click detection: (x, y, w, h)
        rect = (x, y, btn_w, btn_h)
        option_rects.append(rect)
        # Draw option text (slightly inset from the rect)
        screen.draw.text(opt, topleft=(x + 8, y + 8), color="yellow", fontsize=28)

    # Expose option rects globally for the mouse handler to use
    globals()["OPTION_RECTS"] = option_rects


# ---------------------------------------------------------------------------
# Goodbye screen: show final score
# ---------------------------------------------------------------------------
def goodbye():
    screen.clear()
    screen.fill((0, 0, 0))
    score = globals().get("score", 0)
    screen.draw.text("Goodbye!", center=(MID_X, MID_Y - 24), fontsize=48, color="white")
    screen.draw.text(f"Your score is: {score}", center=(MID_X, MID_Y + 24), fontsize=36, color="yellow")


# ---------------------------------------------------------------------------
# Input helpers
# ---------------------------------------------------------------------------
def _point_in_rect(pos, rect):
    """Return True if the point `pos` (x,y) is inside rect (x,y,w,h)."""
    x, y = pos
    rx, ry, rw, rh = rect
    return rx <= x <= rx + rw and ry <= y <= ry + rh


def on_mouse_down(pos):
    """Handle mouse clicks depending on the current `game_state`.

    - On the start screen checks Start / Quit buttons.
    - On the main screen checks which option rectangle was clicked and
      updates score and current question index.
    """
    global game_state
    if game_state == "start":
        if _point_in_rect(pos, START_BUTTON):
            game_state = "main"
        elif _point_in_rect(pos, QUIT_BUTTON):
            game_state = "goodbye"
    elif game_state == "main":
        option_rects = globals().get("OPTION_RECTS", [])
        for idx, rect in enumerate(option_rects):
            if _point_in_rect(pos, rect):
                # check correctness
                correct_idx = globals().get("current_correct_index", 0)
                score = globals().get("score", 0)
                if idx == correct_idx:
                    globals()["last_answer_correct"] = True
                    globals()["score"] = score + 1
                else:
                    globals()["last_answer_correct"] = False
                    globals()["score"] = score
                # pick the next random question (only after user chose an option)
                total = len(globals().get("QUESTIONS", []))
                if total:
                    current = globals().get("question_index", 0)
                    if total > 1:
                        nxt = current
                        while nxt == current:
                            nxt = random.randrange(total)
                    else:
                        nxt = 0
                    globals()["question_index"] = nxt
                break


# ---------------------------------------------------------------------------
# pgzero game loop handlers
# ---------------------------------------------------------------------------
def draw():
    # Call the appropriate screen-drawing function based on `game_state`.
    if game_state == "start":
        startgame()
    elif game_state == "main":
        maingame()
    elif game_state == "goodbye":
        goodbye()
    else:
        startgame()


def update():
    """Update game timers and handle end-of-time transition.

    This function initializes `timer_seconds` on first run and updates it
    once per second while the main game is active. When timer reaches zero,
    switch to the goodbye screen.
    """

    if "timer_seconds" not in globals():
        globals()["timer_seconds"] = 60
        globals()["_last_time"] = time.time()
    now = time.time()
    last = globals().get("_last_time", now)
    # only advance timer while in main game
    if globals().get("game_state") == "main":
        elapsed = now - last
        if elapsed >= 1.0:
            dec = int(elapsed)
            globals()["timer_seconds"] = max(0, globals()["timer_seconds"] - dec)
            globals()["_last_time"] = last + dec
            if globals()["timer_seconds"] == 0:
                globals()["game_state"] = "goodbye"


# Start the pgzero game loop (blocking)
pgzrun.go()