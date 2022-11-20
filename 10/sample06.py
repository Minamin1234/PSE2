from pse2pgzrun import * # type ignore
from math import sin,cos,radians

WIDTH = 600
HEIGHT = 800

rocket = Actor("rocket",center=(300,400))


def draw():
    screen.clear()
    rocket.draw()

def update(dt):
    v = 0
    w = 0
    if keyboard.up:
        v = 100
    if keyboard.down:
        v = -100
    if keyboard.left:
        w = 100
    if keyboard.right:
        w = -100
    rocket.angle += w * dt
    a = -radians(rocket.angle + 90)
    rocket.x += v * cos(a) * dt
    rocket.y += v * sin(a) * dt

    if rocket.right > WIDTH:
        rocket.right = WIDTH
    elif rocket.left < 0:
        rocket.left = 0
    if rocket.bottom > HEIGHT:
        rocket.bottom = HEIGHT
    elif rocket.top < 0:
        rocket.top = 0


pgzrun.go()