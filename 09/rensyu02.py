# HT21A099 南　李玖
# 画面を縦に広げて縦方向にも動くようにする
from pse2pgzrun import *
import random

CATPIC_NORM = "cat01_dash"
CATPIC_ANGRY = "cat01_angry"
CATPIC_HAPPY = "cat01_happy"

cat = Actor(CATPIC_NORM)
cat.topright = 0,10

WIDTH = 600
HEIGHT = cat.height + 600

def draw():
    screen.clear()
    screen.fill((255,255,255))
    cat.draw()

def update():
    cat.left += 4
    cat.x += 4
    cat.y += -8
    if cat.left > WIDTH:
        cat.left = 0
    if cat.top < -HEIGHT:
        cat.top = HEIGHT
    print(f"top:{cat.top}")

def set_cat_normal():
    cat.image = CATPIC_NORM
    

def set_cat_touched():
    num = random.random()
    if(num >= 0.5):
        cat.image = CATPIC_HAPPY
    else:
        cat.image = CATPIC_ANGRY
    sounds.eep.play()
    clock.schedule_unique(set_cat_normal,0.5)

def on_mouse_down(pos):
    if cat.collidepoint(pos):
        set_cat_touched()

pgzrun.go()