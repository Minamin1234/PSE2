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

alien = MovingActor("alien_pink", 250, 250)
alien2 = MovingActor("alien_green", 250, 350)

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
