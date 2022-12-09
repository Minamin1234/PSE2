# HT21A099 南　李玖
# renshu02とrenshu03の内容を含んでいる
from pse2pgzrun import * # type: ignore

WIDTH = 500
HEIGHT = 500

class MovingActor(Actor):
    def __init__(self, name, x, y):
        super().__init__(name, center=(x, y))
        self.vx = 0
        self.vy = 0

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

class Alien(MovingActor):
    def __init__(self, x, y):
        self.alien_normal = "alien_pink"
        self.alien_hurt = "alien_hurt"
        self.STATE_HURT = "hurt"
        self.STATE_NORMAL = "normal"
        self.state = self.STATE_NORMAL
        self.vx = 0
        self.vy = 0
        super().__init__(self.alien_normal, x, y)

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        frag = False
        if self.left <= 0:
            self.left = 0
            self.vx = -self.vx
            frag = True
        if self.right > WIDTH:
            self.right = WIDTH
            self.vx = -self.vx
            frag = True
        if self.bottom > HEIGHT:
            self.bottom = HEIGHT
            self.vy = -self.vy
            frag = True
        if self.top < 0:
            self.top = 0
            self.vy = -self.vy
            frag = True
        if frag:
            self.state = self.STATE_HURT
            clock.schedule_interval(self.on_endedbound, 0.75)


    def draw(self):
        super().draw()
        if self.state == self.STATE_NORMAL:
            self.image = self.alien_normal
        if self.state == self.STATE_HURT:
            self.image = self.alien_hurt

    def on_endedbound(self):
        self.state = self.STATE_NORMAL


alien = Alien(250, 250)
alien2 = Alien(250, 350)

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

    alien.update(dt)
    alien2.update(dt)

pgzrun.go()
