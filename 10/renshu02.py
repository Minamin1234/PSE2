# HT21A099 南　李玖
# renshu01とrenshu02両方の内容を含んでいる。
# sample05.pyを元にしてスプライトの画像を変更する
# sample05.pyを元にしてボールを回転させる(ボールの部分は回転が分かるものに変更する)

from math import sin,cos,radians
import random
from pse2pgzrun import * # type ignore

WIDTH = 550
HEIGHT = 600

paddle = Actor("paddle",center=(275,550))

ballvx  = 200
ballvy = 200
ballw = 0
ball = Actor("rocket",center=(145,400)) #ボールの代わりにロケットの画像を用いる


def draw():
    screen.clear()
    paddle.draw()
    ball.draw()

# 回転速度をランダムに決定する関数
def setRandomRoll():
    global ballw
    ballw = random.random() * 100
    if random.random() >= 0.1:
        ballw = -ballw


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
    
    a = -radians(ball.angle + 90)
    ball.angle += ballw * dt

    ball.x += ballvx * cos(a) * dt
    ball.y += ballvy * sin(a) * dt

    if ball.right > WIDTH:
        ball.right = WIDTH
        ballvx = -ballvx
        setRandomRoll()
    elif ball.left < 0:
        ball.left = 0
        ball.vx = -ballvx
        setRandomRoll()
    if ball.top < 0:
        ball.top = 0
        ballvy = -ballvy
        setRandomRoll()

    if paddle.colliderect(ball):
        ball.bottom = paddle.top
        ballvy = -ballvy
        ballvx += 0.24 * vx
        setRandomRoll()
        

pgzrun.go()