from pse2pgzrun import *

alien = Actor("alien")
alien.topright = 0,10

WIDTH = 500
HEIGHT = alien.height + 20

def draw():
    screen.clear()
    alien.draw()

def update():
    alien.left += 2
    if alien.left > WIDTH:
        alien.right = 0

def on_mouse_down(pos):
    if alien.collidepoint(pos):
        alien.image = 'alien_hurt'
        sounds.eep.play()

pgzrun.go()