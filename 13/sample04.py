from pse2pgzrun import * # type: ignore

WIDTH = 500
HEIGHT = 500

alien = Actor("alien_pink")
alien.center = 250, 250
vx = 0
vy = 0

def draw():
    screen.clear()
    alien.draw()

def update(dt):
    global vx, vy
    if keyboard.right:
        vx += 10
    if keyboard.left:
        vx -= 10
    if keyboard.down:
        vy += 10
    if keyboard.up:
        vy -= 10

    alien.x += vx * dt
    alien.y += vy * dt
    if alien.left > WIDTH:
        alien.right = 0
    if alien.right < 0:
        alien.left = WIDTH
    if alien.top > HEIGHT:
        alien.bottom = 0
    if alien.bottom < 0:
        alien.top = HEIGHT

pgzrun.go()