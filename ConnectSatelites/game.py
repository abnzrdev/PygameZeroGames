import pgzrun
import random

# ===================== Game Constants =====================
WIDTH = 600
HEIGHT = 400
SAT_SIZE = 64  #Satelite image dimensions
NUM_SATS = 6
FPS = 60

# ===================== Game Dynamics =====================
sats = [
    Actor(
        'satellite.png',
        (
            random.randint(SAT_SIZE // 2, WIDTH - SAT_SIZE // 2),
            random.randint(SAT_SIZE // 2, HEIGHT - SAT_SIZE // 2)
        )
    )
    for i in range(NUM_SATS)
]
connections = []  # List to store connected satellite pairs
stopwatch = 0.0

# ===================== Draw Functions =====================
def draw_grid():
    for i, sat in enumerate(sats):
        sat.draw()
        screen.draw.text(str(i + 1), (sat.x + 20, sat.y - 10), color="white", fontsize=24)
    # Draw lines for connections
    for sat1, sat2 in connections:
        screen.draw.line((sat1.x, sat1.y), (sat2.x, sat2.y), (255, 255, 0))

# ===================== Game State Check =====================
def is_game_finished():
    """Game is finished when all satellites are connected in sequence."""
    return len(connections) == NUM_SATS - 1

# ===================== Game Logic =====================
last_clicked_index = None

def on_mouse_down(pos):
    global last_clicked_index, connections, stopwatch
    for i, sat in enumerate(sats):
        if sat.collidepoint(pos):
            if last_clicked_index is not None:
                if i == last_clicked_index + 1:
                    connections.append((sats[last_clicked_index], sat))
                    last_clicked_index = i
                else:
                    # Restart the game
                    connections.clear()
                    last_clicked_index = None
                    stopwatch = 0.0
            else:
                last_clicked_index = i
            break

# ===================== Main Draw Function =====================
def draw():
    screen.blit('background', (0, 0))
    draw_grid()
    if is_game_finished():
        screen.fill((30, 30, 80))
        screen.draw.text(f"Time: {stopwatch:.2f}s", (WIDTH // 2 - 80, HEIGHT // 2), color="yellow", fontsize=40)
    else:
        screen.draw.text(f"Time: {stopwatch:.2f}s", (10, 10), color="white", fontsize=32)

# ===================== Update Function =====================
def update():
    global stopwatch
    if not is_game_finished():
        stopwatch += 1 / FPS

pgzrun.go()