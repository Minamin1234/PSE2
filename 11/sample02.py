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
clear1 = False
clear2 = False
clear3 = False

def draw():
    screen.clear()
    paddle.draw()
    ball.draw()
    if not clear1:
        block1.draw()
    if not clear2:
        block2.draw()
    if not clear3:
        block3.draw()
    if clear1 and clear2 and clear3:
        screen.draw.text(
            "GAME CLEAR",
            center=(275,300), fontsize=100, color="green"
        )



def update(dt):
    global ballvx, ballvy ,clear1 ,clear2 ,clear3 
    if clear1 and clear2 and clear3:
        return
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
        ballvx += 0.25 * vx

    if not clear1 and block1.colliderect(ball):
        ball.top = block1.bottom
        ballvy = -ballvy
        clear1 = True
    elif not clear2 and block2.colliderect(ball):
        ball.top = block2.bottom
        ballvy = -ballvy
        clear2 = True
    elif not clear3 and block3.colliderect(ball):
        ball.top = block3.bottom
        ballvy = -ballvy
        clear3 = True
    print(clear3)

pgzrun.go()