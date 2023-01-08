original__file__ = __file__
from pse2pgzrun import * # type: ignore
import os

# スクリーンサイズ
WIDTH = 550  # 横幅
HEIGHT = 600  # 縦幅
TITLE = 'ブロック崩し' # タイトル

# モード
PREPLAY = 0
INPLAY = 1
POSTPLAY = 2


# ボールを表現するクラス（Actorクラスを継承）
class Ball(Actor):
    def __init__(self, image, x, y, vx, vy):
        super().__init__(image, center=(x,y))
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


# ゲーム全体を表現するクラス
class Game:
    def __init__(self):
        self.load_scores()
        print('開始前ランキング:')
        self.print_ranking()
        self.input_name()
        self.blocks = []
        self.score = 0
        self.start()
        # 音
        self.tone_crash = tone.create('A5', 0.01)
        self.tone_bounce = tone.create('A3', 0.01)
        self.tone_clear = tone.create('A5', 1.0)
        self.tone_over = tone.create('A3', 1.0)

    def load_scores(self):
        self.filepath = os.path.join(os.path.dirname(original__file__), 'blockscores.txt')
        print(self.filepath)
        self.bestscores = {}
        try:
            with open(self.filepath, 'r') as file:
                for line in file:
                    words = line.split()
                    if len(words) >= 2:
                        self.bestscores[words[0]] = int(words[1])
        except OSError as e:
            print('ベストスコアのファイルがない')

    def save_scores(self):
        with open(self.filepath, 'w') as file:
            for i in self.bestscores.items():
                file.write(f'{i[0]}\t{i[1]}\n')

    def print_ranking(self):
        for i in sorted(self.bestscores.items(), key=lambda x: x[1], reverse=True):
            print(f'{i[0]:10} {i[1]:3}')

    def input_name(self):
        self.name = input('あなたの名前: ')
        if self.name == '':
            exit()
        if self.name in self.bestscores:
            print(f'{self.name}は登録済み')
        else:
            print(f'{self.name}は新規')
            self.bestscores[self.name] = 0 # 仮のスコア

    def start(self):
        if self.blocks != []:
            self.score = 0
        self.mode = PREPLAY
        # パドル
        self.paddle = Paddle('paddle', 275, 550)
        # ボール
        self.ball = Ball('ball', 145, 400, 200, 200)
        # ブロック
        block_pattern = [[1, 1, 1, 1, 1],
                        [1, 0, 1, 0, 1],
                        [1, 0, 1, 0, 1],
                        [1, 1, 1, 1, 1]]
        self.blocks = []
        for j, y in enumerate([85, 135, 185, 235]):
            for i, x in enumerate([75, 175, 275, 375, 475]):
                if block_pattern[j][i] == 1:
                    self.blocks.append(Block('block', x, y))

    def draw(self):
        screen.clear()
        screen.draw.text(
            'SCORE: ' + str(self.score),
            left=350, top=25, fontsize=50, color='white')
        self.paddle.draw()
        self.ball.draw()
        for b in self.blocks:
            b.draw()
        if self.mode == PREPLAY:
            screen.draw.text(
                'HIT SPACE KEY',
                center=(275, 300), fontsize=100, color='magenta')
        elif self.mode == POSTPLAY:
            if self.blocks == []:
                screen.draw.text(
                    'GAME CLEAR',
                    center=(275, 300), fontsize=100, color='green')
            else:
                screen.draw.text(
                    'GAME OVER',
                    center=(275, 300), fontsize=100, color='red')

    def update(self, dt):
        if self.mode == PREPLAY:
            if keyboard.space:
                self.mode = INPLAY
        elif self.mode == POSTPLAY:
            if keyboard.escape:
                print('最終ランキング:')
                self.print_ranking()
                self.save_scores()
                exit()
            if keyboard.RETURN:
                self.start()
        else:
            self.paddle.vx = 0
            if keyboard.right:
                self.paddle.vx = 300
            if keyboard.left:
                self.paddle.vx = -300
            self.paddle.update(dt)

            # ボールの移動
            self.ball.update(dt)

            # ボールとパドルの衝突処理
            if self.paddle.collide_ball(self.ball):
                self.tone_bounce.play()

            # ボールとブロックの衝突処理
            for b in self.blocks:
                if b.collide_ball(self.ball):
                    self.blocks.remove(b)
                    self.tone_crash.play()
                    self.score += 1
                    break

            # 勝敗判定
            if self.ball.top > HEIGHT:
                self.tone_over.play()
                self.mode = POSTPLAY
                if self.score > self.bestscores[self.name]:
                    print('最高点更新')
                    self.bestscores[self.name] = self.score
                    self.print_ranking()
            elif self.blocks == []:
                self.tone_clear.play()
                self.mode = POSTPLAY


game = Game()


def draw():
    game.draw()


def update(dt):
    game.update(dt)


pgzrun.go()

