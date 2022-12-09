from pse2pgzrun import * # type: ignore

# スクリーンサイズ
WIDTH = 550  # 横幅
HEIGHT = 600  # 縦幅

# モード
PREPLAY = 0
INPLAY = 1
POSTPLAY = 2

# 音
tone_crash = tone.create('A5', 0.01)
tone_bounce = tone.create('A3', 0.01)
tone_clear = tone.create('A5', 1.0)
tone_over = tone.create('A3', 1.0)


# ボールを表現するクラス（Actorクラスを継承）
class Ball(Actor):
    def __init__(self, image, x, y, vx, vy):
        super().__init__(image, center=(x, y))
        self.vx = vx
        self.vy = vy

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        if self.right > WIDTH:
            self.right = WIDTH
            self.vx = -self.vx
        elif self.left < 0:
            self.left = 0
            self.vx = -self.vx
        if self.top < 0:
            self.top = 0
            self.vy = -self.vy


# ブロックを表現するクラス（Actorクラスを継承）
class Block(Actor):
    def __init__(self, image, x, y):
        super().__init__(image, center=(x,y))

    def collide_ball(self, b:Ball):
        rv = False
        if self.colliderect(b):
            rv = True
            overlapT = b.bottom - self.top
            overlapB = self.bottom - b.top
            overlapL = b.right - self.left
            overlapR = self.right - b.left
            smallest = min([overlapT, overlapB, overlapL, overlapR])
            if smallest == overlapT:
                b.bottom = self.top
                b.vy = -b.vy
            elif smallest == overlapB:
                b.top = self.bottom
                b.vy = -b.vy
            elif smallest == overlapL:
                b.right = self.left
                b.vx = -b.vx
            elif smallest == overlapR:
                b.left = self.right
                b.vx = -b.vx
        return rv


# パドルを表現するクラス（Blockクラスを継承）
class Paddle(Block):
    def __init__(self, image, x, y):
        super().__init__(image, x, y)
        self.vx = 0
        self.vy = 0

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        if self.right > WIDTH:
            self.right = WIDTH
        elif self.left < 0:
            self.left = 0
        if self.bottom > HEIGHT:
            self.bottom = HEIGHT
        elif self.top < 0:
            self.top = 0

    def collide_ball(self, b):
        if super().collide_ball(b):
            b.vx += 0.25 * self.vx
            b.vy += 0.25 * self.vy
            return True
        return False


def start():
    global mode, score, paddle, ball, blocks
    # モード
    mode = PREPLAY
    # スコア
    score = 0
    # パドル
    paddle = Paddle('paddle', 275, 550)
    # ボール
    ball = Ball('ball', 145, 400, 200, 200)
    # ブロック
    block_pattern = [[1, 1, 1, 1, 1],
                     [1, 0, 1, 0, 1],
                     [1, 0, 1, 0, 1],
                     [1, 1, 1, 1, 1]]
    blocks = []
    for j, y in enumerate([85, 135, 185, 235]):
        for i, x in enumerate([75, 175, 275, 375, 475]):
            if block_pattern[j][i] == 1:
                blocks.append(Block('block', x, y))


def draw():
    screen.clear()
    screen.draw.text(
        'SCORE: ' + str(score),
        left=350, top=25, fontsize=50, color='white')
    paddle.draw()
    ball.draw()
    for b in blocks:
        b.draw()
    if mode == PREPLAY:
        screen.draw.text(
            'HIT SPACE KEY',
            center=(275, 300), fontsize=100, color='magenta')
    elif mode == POSTPLAY:
        if blocks == []:
            screen.draw.text(
                'GAME CLEAR',
                center=(275, 300), fontsize=100, color='green')
        else:
            screen.draw.text(
                'GAME OVER',
                center=(275, 300), fontsize=100, color='red')


def update(dt):
    global mode, score
    if mode == PREPLAY:
        if keyboard.space:
            mode = INPLAY
    elif mode == POSTPLAY:
        if keyboard.escape:
            exit()
        if keyboard.RETURN:
            start()
    else:
        paddle.vx = 0
        if keyboard.right:
            paddle.vx = 300
        if keyboard.left:
            paddle.vx = -300
        paddle.update(dt)

        # ボールの移動
        ball.update(dt)

        # ボールとパドルの衝突処理
        if paddle.collide_ball(ball):
            tone_bounce.play()

        # ボールとブロックの衝突処理
        for b in blocks:
            if b.collide_ball(ball):
                blocks.remove(b)
                tone_crash.play()
                score += 1
                break

        # 勝敗判定
        if ball.top > HEIGHT:
            tone_over.play()
            mode = POSTPLAY
        elif blocks == []:
            tone_clear.play()
            mode = POSTPLAY


start()
pgzrun.go()

