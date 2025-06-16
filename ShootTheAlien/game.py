import pgzrun
from random import randint

# Defining the constants
WIDTH, HEIGHT = 800, 600
TITLE = "Shoot the aliens"

# Defining Game characters
alien = Actor("alien")
message = ""

# Adding the score functionality
score = 0
strscore = str(score)

# Drawing everything in the function
def draw():
    screen.clear()
    screen.blit("background2", (0,0))
    alien.draw()
    screen.draw.text(message, center=(400,50), fontsize = 60, color = "white")
    screen.draw.text(strscore, center=(700, 50), fontsize = 60, color = "black")

def alien_rndm_pos():
    alien.x = randint(0, WIDTH - 70)
    alien.y = randint(0, HEIGHT - 70)

def on_mouse_down(pos):
    global message, score , strscore
    if alien.collidepoint(pos):
        alien_rndm_pos()
        message = "Good Shot"
        score += 1
        strscore =  str(score)
    else:
        message = "Try Again"

alien_rndm_pos()
pgzrun.go()