# HT21A099 南　李玖
# スプライトの画像や音を変更する
from pse2pgzrun import *
import random

CATPIC_NORM = "cat01_dash"
CATPIC_ANGRY = "cat01_angry"
CATPIC_HAPPY = "cat01_happy"

cat = Actor(CATPIC_NORM)
cat.topright = 0,10

WIDTH = 750
HEIGHT = cat.height + 20

def draw():
    screen.clear()
    screen.fill((255,255,255))
    cat.draw()

def update():
    cat.left += 4
    if cat.left > WIDTH:
        cat.left = 0

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