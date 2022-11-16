from pse2pgzrun import * # type: ignore

x = 0
y = 0

def draw():
    print(x,y)
    if x < 300 and y < 200:
        color = (255,0,0)
    else:
        color = (0,255,0)
    screen.draw.filled_circle((x,y),5,color)

def on_mouse_move(pos):
    global x,y
    (x,y) = pos

pgzrun.go()