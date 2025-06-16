import pgzrun
from random import randint

# Defining the constants
WIDTH, HEIGHT = 800, 600
TITLE = "Shoot the aliens"

# Defining Game characters
alien = Actor("alien")

# Drawing everything in the function
def draw():
    screen.clear()
    screen.blit("background2", (0, 0))
    alien.draw()

def alien_rndm_pos():
    alien.x = randint(0, WIDTH - 50)
    alien.y = randint(0, HEIGHT - 50)

def on_mouse_down(pos):
    if alien.collidepoint(pos):
        alien_rndm_pos()  # Move the alien to a new random position

pgzrun.go()