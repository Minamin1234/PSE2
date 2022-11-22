# HT21A099 南　李玖
# sample05.pyを元にしてスプライト画像を変更

from pse2pgzrun import * # type ignore

WIDTH = 550
HEIGHT = 600

paddle = Actor("paddle",center=(275,550))

ballvx  = 200
ballvy = 200
ball = Actor("rocket",center=(145,400))


def draw():
    screen.clear()
    paddle.draw()
    ball.draw()

def update(dt):
    global ballvx,ballvy
    vx = 0
    if keyboard.right:
        vx = 100
    if keyboard.left:
        vx = -100
    paddle.x += vx + dt
    if paddle.right > WIDTH:
        paddle.right = WIDTH
    elif paddle.left < 0:
        paddle.left = 0
    
    ball.x += ballvx * dt
    ball.y += ballvy * dt

    if ball.right > WIDTH:
        ball.right = WIDTH
        ballvx = -ballvx
    elif ball.left < 0:
        ball.left = 0
        ball.vx = -ballvx
    if ball.top < 0:
        ball.top = 0
        ballvy = -ballvy

    if paddle.colliderect(ball):
        ball.bottom = paddle.top
        ballvy = -ballvy
        ballvx += 0.24 * vx

pgzrun.go()