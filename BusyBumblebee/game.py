import pgzrun
from random import randint

# Game Constants
TITLE = "Busy Bumblebee"
WIDTH = 600
HEIGHT = 400
SCORE_POS = (20, 20)
TIME_POS = (WIDTH - 180, 20)
SCORE_FONT_SIZE = 48
TIME_FONT_SIZE = 48

# Game Dynamics
score = 0
time_left = 60
bee = Actor('bee.png')
flower = Actor('flower.png')
bee.x = WIDTH / 2
bee.y = HEIGHT / 2
flower.x = randint(0, WIDTH - 70)
flower.y = randint(0, HEIGHT - 70)

# Direction flags
moving_left = False
moving_right = False
moving_up = False
moving_down = False

def on_key_down(key):
    global moving_left, moving_right, moving_up, moving_down
    if key == keys.LEFT:
        moving_left = True
    elif key == keys.RIGHT:
        moving_right = True
    elif key == keys.UP:
        moving_up = True
    elif key == keys.DOWN:
        moving_down = True

def on_key_up(key):
    global moving_left, moving_right, moving_up, moving_down
    if key == keys.LEFT:
        moving_left = False
    elif key == keys.RIGHT:
        moving_right = False
    elif key == keys.UP:
        moving_up = False
    elif key == keys.DOWN:
        moving_down = False

def update():
    # handling movement for better FPS
    global time_left
    if moving_left and bee.x > 35:
        bee.x -= 5
    if moving_right and bee.x < WIDTH - 35:
        bee.x += 5
    if moving_up and bee.y > 35:
        bee.y -= 5
    if moving_down and bee.y < HEIGHT - 35:
        bee.y += 5

    if bee.colliderect(flower):
        global score
        score += 1
        flower.x = randint(0, WIDTH - 70)
        flower.y = randint(0, HEIGHT - 70)

    time_left -= 1/60

def draw():
    if time_left > 0:
        screen.blit('background.png', (0, 0))
        screen.draw.text(str(score), SCORE_POS, color="white", fontsize=SCORE_FONT_SIZE)
        screen.draw.text(f"Time: {int(time_left)}", TIME_POS, color="purple", fontsize=TIME_FONT_SIZE)
        bee.draw()
        flower.draw()
    else:
        screen.fill((30, 30, 80))
        screen.draw.text("GAME OVER", center=(WIDTH // 2, HEIGHT // 2 - 40), color="white", fontsize=64)
        screen.draw.text(f"Your score: {score}", center=(WIDTH // 2, HEIGHT // 2 + 20), color="yellow", fontsize=48)

pgzrun.go()