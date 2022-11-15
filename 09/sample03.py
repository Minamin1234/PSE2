from pse2pgzrun import *

alien = Actor("alien")
alien.pos = 100,56

WIDTH = 500
HEIGHT = alien.height + 2

def draw():
    screen.clear()
    alien.draw()

pgzrun.go()