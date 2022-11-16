from pse2pgzrun import * # type ignore

WIDTH = 550
HEIGHT = 600

paddle = Actor("paddle",center=(275,550))


def draw():
    screen.clear()
    paddle.draw()

def update(dt):
    vx = 0
    if keyboard.right:
        vx = 300
    if keyboard.left:
        vx = -300
    paddle.x += vx + dt
    if paddle.right > WIDTH:
        paddle.right = WIDTH
    elif paddle.left < 0:
        paddle.left = 0

pgzrun.go()