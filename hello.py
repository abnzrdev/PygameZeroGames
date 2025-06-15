import pgzrun

WIDTH = 600
HEIGHT = 600

def draw():
    screen.draw.text("Abenezer", center=(300,300), fontsize=40, color="blue")
    screen.draw.text("Abenezer", topleft=(300,300), fontsize=40, color="blue")
    screen.draw.text("Abenezer", topright=(300,300), fontsize=40, color="blue")
pgzrun.go()