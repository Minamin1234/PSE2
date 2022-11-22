from pse2pgzrun import * # type ignore

WIDTH = 550
HEIGHT = 600

paddle = Actor("paddle",center=(275,550))

ballvx  = 200
ballvy = 200
ball = Actor("ball",center=(145,400))

block1 = Actor("block",center=(175,85))
block2 = Actor("block",center=(275,85))
block3 = Actor("block",center=(375,85))

def draw():
    screen.clear()
    paddle.draw()
    ball.draw()
    block1.draw()
    block2.draw()
    block3.draw()


def update(dt):
    global ballvx,ballvy
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

    if block1.colliderect(ball):
        ball.top = block1.bottom
        ballvy = -ballvy
    elif block2.colliderect(ball):
        ball.top = block2.bottom
        ballvy = -ballvy
    elif block3.colliderect(ball):
        ball.top = block3.bottom
        ballvy = -ballvy

pgzrun.go()