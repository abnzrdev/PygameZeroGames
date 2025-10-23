import random
import pgzrun

# Screen Size
WIDTH = 800
HEIGHT = 600

# Star image names (red - the target)
STAR_IMAGES = [
    "blue-star",
    "green-star",
    "orange-star",
    "purple-star",
    "yellow-star"
]
TARGET_IMAGE = "red-star"

# Creating Class for multiple star instances
class Star:
    def __init__(self, image, x, y, speed):
        self.image = image
        self.x = x
        self.y = y
        self.speed = speed
        self.size = 64  # Assuming star images are 64x64

    def move(self):
        self.x += self.speed[0]
        self.y += self.speed[1]

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def collides_with_point(self, pos):
        px, py = pos
        # Simple bounding box collision
        return self.x <= px <= self.x + self.size and self.y <= py <= self.y + self.size

def spawn_stars(level):
    stars = []
    stars.append(Star(TARGET_IMAGE, 0, 0, (random.uniform(2, 4), random.uniform(2, 4))))
    # Add (level) more stars with random colors (not red)
    for _ in range(level):
        img = random.choice(STAR_IMAGES)
        stars.append(Star(img, 0, 0, (random.uniform(2, 4), random.uniform(2, 4))))
    random.shuffle(stars)  # Shuffle so red isn't always first
    return stars

level = 1
stars = spawn_stars(level)
game_over = False

def draw():
    screen.clear()
    screen.blit('space', (0, 0))
    if game_over:
        screen.draw.text("GAME OVER", center=(WIDTH//2, HEIGHT//2-30), fontsize=80, color="white")
        screen.draw.text(f"Level reached: {level}", center=(WIDTH//2, HEIGHT//2+40), fontsize=48, color="yellow")
        screen.draw.text("Click anywhere to restart", center=(WIDTH//2, HEIGHT//2+100), fontsize=36, color="orange")
    else:
        for star in stars:
            star.draw()
        screen.draw.text(f"Level: {level}", topleft=(10, 10), fontsize=40, color="white")

def update():
    global stars
    if not game_over:
        for star in stars:
            star.move()
        # Remove stars that go off screen
        stars = [s for s in stars if s.x < WIDTH and s.y < HEIGHT]
        # If all stars are gone (player did not click), game over
        if not stars:
            set_game_over()

def on_mouse_down(pos):
    global stars, level, game_over
    if game_over:
        restart_game()
        return
    for star in stars:
        if star.collides_with_point(pos):
            if star.image == TARGET_IMAGE:
                level += 1
                stars = spawn_stars(level)
            else:
                set_game_over()
            return

def set_game_over():
    global game_over
    game_over = True

def restart_game():
    global level, stars, game_over
    level = 1
    stars = spawn_stars(level)
    game_over = False

pgzrun.go()