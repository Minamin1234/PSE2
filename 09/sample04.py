from pse2pgzrun import *

alien = Actor("alien")
alien.topright = 0,10

WIDTH = 500
HEIGHT = alien.height + 2

def draw():
    screen.clear()
    alien.draw()

def update():
    alien.left += 2
    if alien.left > WIDTH:
        alien.right = 0

pgzrun.go()