from pse2pgzrun import * # type: ignore

# Paygame Zeroで文字列入力をするためのクラス
class StringInput:
    def __init__(self, left=0, top=0, fontsize=100, color='white', start=True):
        self.left = left
        self.top = top
        self.fontsize = fontsize
        self.color = color
        self.ready = start
        self.working = start
        self.string = ''

    def start(self):
        self.string = ''
        self.working = True
        self.ready = True

    def on_key_down(self, key):
        if self.working and self.ready:
            if key == keys.RETURN:
                self.working = False
            elif key == keys.BACKSPACE:
                if self.string != '':
                    self.string = self.string[:-1]
            else:
                if 0 <= key <= 0x10ffff:
                    self.string += chr(key)

    def get(self):
        if self.working or not self.ready:
            return None
        else:
            self.ready = False
            return self.string
        
    def draw(self):
        screen.draw.text(
            self.string + ('_' if self.working else ''),
            left=self.left, top=self.top, 
            fontsize=self.fontsize, color=self.color)

si = StringInput(left=250)

def draw():
    screen.clear()
    screen.draw.text(
        'name:',
        left=0, top=0, fontsize=100, color='white')
    si.draw()

def update():
    name = si.get()
    if name is not None:
        print('name:', name)
        si.start()

def on_key_down(key):
    si.on_key_down(key)

pgzrun.go()

