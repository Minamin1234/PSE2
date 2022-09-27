from cmath import rect
from operator import mod
from turtle import *
shape("turtle")
col = ["orange","limegreen","gold","plum","tomato"]
circles = 50
radius = 150
drad = radius / circles
dy = 10

up()
left(-90)
forward(200)
left(90)
left(180)
forward(200)
left(-180)
for i in range(circles):
    color(col[i%5])
    r = radius - (drad * (i+1))
    forward(dy)
    speed(10)
    down()
    circle(r)
    up()
    left(90)
    forward(drad*2)
    left(-90)
    ##left(72)
done()