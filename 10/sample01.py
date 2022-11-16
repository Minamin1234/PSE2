from pse2pgzrun import * # type: ignore

x = 0
y = 0

def draw():
    screen.clear()
    print(x,y)
    screen.draw.filled_circle((x,y),10,(255,0,0))

def on_mouse_move(pos):
    global x,y
    (x,y) = pos

pgzrun.go()