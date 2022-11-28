from pse2pgzrun import * # type ignore

WIDTH = 550
HEIGHT = 600

tone_crash = tone.create('A5',0.01)
tone_bounce = tone.create('A3',0.01)

score = 0

paddle = Actor("paddle",center=(275,550))

ballvx  = 200
ballvy = 200
ball = Actor("ball",center=(145,400))

blocks = []
for y in [85,135,185,235]:
    for x in [75,175,275,375,475]:
        blocks.append(Actor("block",center=(x,y)))

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
        ballvx = -ballvx
    if ball.top < 0:
        ball.top = 0
        ballvy = -ballvy

    if paddle.colliderect(ball):
        ball.bottom = paddle.top
        ballvy = -ballvy
        ballvx += 0.25 * vx
        tone_bounce.play()

    for b in blocks:
        if b.colliderect(ball):
            ballvy = -ballvy
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

pgzrun.go()