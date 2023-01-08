original__file__ = __file__
from pse2pgzrun import * # type: ignore
import os

# スクリーンサイズ
WIDTH = 550  # 横幅
HEIGHT = 600  # 縦幅

def start():
    global blocks
    # ブロック
    block_pattern = []
    try:
        filepath = os.path.join(os.path.dirname(original__file__), 'blockpattern.txt')
        with open(filepath, 'r') as file:
            for line in file:
                words = line.split()
                numbers = []
                for w in words:
                    numbers.append(int(w))
                block_pattern.append(numbers)
    except OSError as e:
        print('ブロックパターンのファイルがない')
        exit()
    print(block_pattern)
    blocks = []
    for j, y in enumerate([85, 135, 185, 235]):
        for i, x in enumerate([75, 175, 275, 375, 475]):
            if block_pattern[j][i] == 1:
                blocks.append(Actor('block', center=(x,y)))


def draw():
    screen.clear()
    for b in blocks:
        b.draw()

start()
pgzrun.go()

