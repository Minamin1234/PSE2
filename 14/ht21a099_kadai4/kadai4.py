# HT21A099 南　李玖
from pse2pgzrun import * # type: ignore

WIDTH = 500
HEIGHT = 500

def draw():
    color_ = 100, 100, 100
    rect_ = Rect((20, 20), (100, 100))
    screen.draw.filled_rect(rect_, color_)
    pass

def update(dt):
    pass

pgzrun.go()