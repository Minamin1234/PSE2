# HT21A099 南　李玖
# renshu01からrenshu04までの内容を含んでいる
from pse2pgzrun import * # type ignore

WIDTH = 550
HEIGHT = 600

tone_crash = tone.create('F5',0.01)
tone_bounce = tone.create('G3',0.01)

score = 0

paddle = Actor("paddle",center=(275,550))

ballvx  = 200
ballvy = 200
ball = Actor("ball",center=(145,400))

paddle_move_speed = [1, 1]
block_size = [40, 15]

blockmap =[
    [1,0,0,0,0,1],
    [0,1,0,0,1,0],
    [0,0,1,1,0,0],
    [0,0,1,1,0,0],
    [0,1,0,0,1,0],
    [1,0,0,0,0,1],
    [1,1,1,1,1,1],
    [1,1,1,1,1,1],
]

"""
blockmap =[
    [1,1,1,1,1,1],
    [0,0,0,0,0,0],
    [1,1,1,1,1,1],
    [0,0,0,0,0,0],
    [1,1,1,1,1,1],
    [0,0,0,0,0,0],
    [1,1,1,1,1,1],
    [0,0,0,0,0,0],
]
"""

offset = [0, 100]
blocks = []
for y in range(8):
    for x in range(6):
        if blockmap[y][x] == 1:
            bx = (WIDTH - 460) / 2 + block_size[0] + (block_size[0] * 2 * x)
            bx += offset[0]
            by = block_size[1] + (block_size[1] * 2 * y)
            by += offset[1]
            blocks.append(Actor("block",center=(bx, by)))

clear1 = False
clear2 = False
clear3 = False

def draw():
    screen.clear()
    screen.draw.text(
        "SCORE: " + str(score),
        left=350,top=25,fontsize=50, color="white"
    )
    paddle.draw()
    ball.draw()
    for b in blocks:
        b.draw()
    
    if blocks == []:
        screen.draw.text(
            "GAME CLEAR",
            center=(275,300), fontsize=100, color="green"
        )



def update(dt):
    global ballvx, ballvy ,score
    if blocks == []:
        return
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
        ballvx = -ballvx
    if ball.top < 0:
        ball.top = 0
        ballvy = -ballvy

    if paddle.colliderect(ball):
        overlapT = ball.bottom - paddle.top
        overlapB = paddle.bottom - ball.top
        overlapL = ball.right - paddle.left
        overlapR = paddle.right - ball.left
        smallest = min([overlapT, overlapB, overlapL, overlapR])
        if smallest == overlapT:
            ball.bottom = paddle.top
            ballvy = -ballvy
        elif smallest == overlapB:
            ball.top = paddle.bottom
            ballvy = -ballvy
        elif smallest == overlapL:
            ball.right = paddle.left
            ballvx = -ballvx
        elif smallest == overlapR:
            ball.left = paddle.right
            ballvx = -ballvx
        tone_bounce.play()

    for b in blocks:
        if b.colliderect(ball):
            overlapT = ball.bottom - b.top
            overlapB = b.bottom - ball.top
            overlapL = ball.right - b.left
            overlapR = b.right - ball.left
            smallest = min([overlapT,overlapB,overlapL,overlapR])
            if smallest == overlapT:
                ball.bottom = b.top
                ballvy = -ballvy
            elif smallest == overlapB:
                ball.top = b.bottom
                ballvy = -ballvy
            elif smallest == overlapL:
                ball.right = b.left
                ballvx = -ballvx
            elif smallest == overlapR:
                ball.left = b.right
                ballvx = -ballvx
            blocks.remove(b)
            tone_crash.play()
            score += 1
            break

def on_mouse_move(pos):
    paddle.center = (pos[0], paddle.center[1])

pgzrun.go()