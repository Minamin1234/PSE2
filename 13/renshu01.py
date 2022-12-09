# HT21A099 南　李玖
from pse2pgzrun import * # type: ignore

WIDTH = 500
HEIGHT = 500

class MovingActor(Actor):
    def __init__(self, name, x, y, angle=0):
        super().__init__(name, center=(x, y))
        self.vx = 0
        self.vy = 0
        self.va = angle

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        if self.left > WIDTH:
            self.right = 0
        if self.right < 0:
            self.left = WIDTH
        if self.top > HEIGHT:
            self.bottom = 0
        if self.bottom < 0:
            self.top = HEIGHT
        self.angle = self.va
        

alien = MovingActor("alien_pink", 250, 250)
alien2 = MovingActor("alien_green", 250, 350, 90)

def draw():
    screen.clear()
    alien.draw()
    alien2.draw()

def update(dt):
    if keyboard.right:
        alien.vx += 10
    if keyboard.left:
        alien.vx -= 10
    if keyboard.down:
        alien.vy += 10
    if keyboard.up:
        alien.vy -= 10

    if keyboard.right:
        alien2.vx += 10
    if keyboard.left:
        alien2.vx -= 10
    if keyboard.down:
        alien2.vy += 10
    if keyboard.up:
        alien2.vy -= 10
    alien.va += 10
    alien.update(dt)
    alien2.update(dt)

pgzrun.go()
