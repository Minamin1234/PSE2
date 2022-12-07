'''
プログラミング総合演習2 課題３
HT21A099 南　李玖

変更・追加内容
- randomモジュールのインポート
- ランダムなブロック配置の実装
- パドルのマウスによる操作の実装

評価してもらいたいこと
- 追加実装した内容が十分に満足しているかどうか
'''
from pse2pgzrun import * # type ignore
import random

WIDTH = 550
HEIGHT = 600

PREPLAY = 0
INPLAY = 1
POSTPLAY = 2

tone_crash = tone.create('A5',0.01)
tone_bounce = tone.create('A3',0.01)
tone_clear = tone.create("A5", 1.0)
tone_over = tone.create("A3", 1.0)

score = 0

paddle = Actor("paddle",center=(275,550))

ballvx  = 200
ballvy = 200
ball = Actor("ball",center=(145,400))

block_pattern = [[1, 1, 1, 1, 1],
                 [1, 0, 1, 0, 1],
                 [1, 0, 1, 0, 1],
                 [1, 1, 1, 1, 1]]
blocks = []
for j, y in enumerate([85,135,185,235]):
    for i, x in enumerate([75,175,275,375,475]):
        if block_pattern[j][i] == 1:
            blocks.append(Actor("block",center=(x,y)))

clear1 = False
clear2 = False
clear3 = False

# ランダムなブロック配置を生成します。
def randomPattern():
    global block_pattern
    for y in range(4):
        for x in range(5):
            block_pattern[y][x] = random.randint(0,1)
    return

def start():
    global mode, score, paddle, ball, blocks, ballvx, ballvy, block_pattern
    # モード
    mode = PREPLAY
    # スコア
    score = 0
    # パドル
    paddle = Actor('paddle', center=(275, 550))
    # ボール
    ballvx = 200
    ballvy = 200
    ball = Actor('ball', center=(145, 400))
    # ブロック
    blocks = []
    randomPattern()
    for j, y in enumerate([85,135,185,235]):
        for i, x in enumerate([75,175,275,375,475]):
            if block_pattern[j][i] == 1:
                blocks.append(Actor("block",center=(x,y)))

def collide_ball(a):
    global ballvx, ballvy
    rv = False
    if a.colliderect(ball):
        rv = True
        overlapT = ball.bottom - a.top
        overlapB = a.bottom - ball.top
        overlapL = ball.right - a.left
        overlapR = a.right - ball.left
        smallest = min([overlapT, overlapB, overlapL, overlapR])
        if smallest == overlapT:
            ball.bottom = a.top
            ballvy = -ballvy
        elif smallest == overlapB:
            ball.top = a.bottom
            ballvy = -ballvy
        elif smallest == overlapL:
            ball.right = a.left
            ballvx = -ballvx
        elif smallest == overlapR:
            ball.left = a.right
            ballvx = -ballvx
    return rv

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

    if mode == PREPLAY:
        screen.draw.text(
            "HIT SPACE KEY",
            center=(275, 300), fontsize=100, color="magenta"
        )
    elif mode == POSTPLAY:
        if blocks == []:
            screen.draw.text(
                "GAME CLEAR",
                center=(275, 300), fontsize=100, color="green"
            )
        else:
            screen.draw.text(
                "GAME OVER",
                center=(275, 300), fontsize=100, color="red"
            )
    
    if blocks == []:
        screen.draw.text(
            "GAME CLEAR",
            center=(275,300), fontsize=100, color="green"
        )



def update(dt):
    global ballvx, ballvy ,score, mode
    if mode == PREPLAY:
        if keyboard.space:
            mode = INPLAY
    elif mode == POSTPLAY:
        if keyboard.escape:
            exit()
        if keyboard.space:
            start()
    else:
        vx = 0
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

        if collide_ball(paddle):
            ballvx += 0.25 * vx
            tone_bounce.play()

        for b in blocks:
            if collide_ball(b):
                blocks.remove(b)
                tone_crash.play()
                score += 1
                break
        if ball.top > HEIGHT:
            tone_over.play()
            mode = POSTPLAY
        elif blocks == []:
            tone_clear.play()
            mode = POSTPLAY

def on_mouse_move(pos):
    paddle.center = (pos[0], paddle.center[1])

start()
pgzrun.go()