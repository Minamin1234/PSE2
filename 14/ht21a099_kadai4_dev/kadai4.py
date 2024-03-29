# HT21A099 南　李玖
import math
import os.path
import random

import pygame.mouse
from pse2pgzrun import *  # type: ignore

WIDTH = 1250 * 0.75
HEIGHT = 850 * 0.75


class Util:

    # 指定した最小値/最大値の範囲内で値を返す
    def clamp_value(val, val_max, val_min):
        if val < val_min:
            return val_min
        if val > val_max:
            return val_max
        return val

    # ランダムな真偽値を返します(percentで真になる確率を指定します)
    def random_bool(percent: float):
        val = random.random()
        return val <= percent

    # 基本ダメージからランダムな乗数を掛けたダメージを返します
    def random_damage(dmg: float, dmg_multiply: float):
        multi = random.uniform(-dmg_multiply, dmg_multiply)
        result = dmg + (dmg * multi)
        if result < 0:
            result = 0.0
        return result

    # ダメージからランダムな防御乗数を掛けたダメージを返します
    def random_defenceddamage(dmg: float, def_multiply: float):
        multi = random.uniform(0, def_multiply)
        result = dmg - (dmg * multi)
        if result < 0:
            result = 0.0
        return result

    # 指定した方向ベクトルをランダムな角度に回転させます
    def random_rotatevector(v, max_angle):
        rot = random.uniform(-max_angle, max_angle)
        vec = Vector2.rotate(v, rot)
        return vec


# RGB情報を表すクラス
class ColorRGB:
    r: int = 0
    g: int = 0
    b: int = 0

    def __init__(self, r: int, g: int, b: int):
        self.r = r % 256
        self.g = g % 256
        self.b = b % 256

    def get_tuple(self):
        return (self.r, self.g, self.b)


# 二次元ベクトルを表すクラス
class Vector2:
    x: float = 0.0
    y: float = 0.0

    # ベクトルから新たにインスタンスを作成します
    def get_vector(v):
        return Vector2(v.x, v.y)

    def get_tuple(v):
        return (v.x, v.y)

    # xとyからベクトルを作成します
    def __init__(self, x: float, y: float):
        self.x, self.y = x, y

    # 加算演算子の定義(ベクトル同士の足し算)
    def __add__(self, other):
        v = Vector2(self.x + other.x, self.y + other.y)
        return v

    # 減算演算子の定義(ベクトル同士の引き算)
    def __sub__(self, other):
        v = Vector2(self.x - other.x, self.y - other.y)
        return v

    # -演算子の定義(各要素の反転)
    def __neg__(self):
        v = Vector2(-self.x, -self.y)
        return v

    # 乗算演算子の定義(スカラー倍)
    def __mul__(self, other):
        v = Vector2(self.x * other, self.y * other)
        return v

    # +=演算子の定義(ベクトル同士の加算)
    def __iadd__(self, other):
        v = Vector2(self.x + other.x, self.y + other.y)
        return v

    # ベクトルの文字列化
    def __str__(self):
        return f"({self.x}, {self.y})"

    # ベクトルの長さを返します。
    def get_vectorlength(v):
        return math.sqrt(v.x**2 + v.y**2)

    # 正規化したベクトルを返します。
    def normalize(v):
        vec = Vector2(0, 0)
        length = Vector2.get_vectorlength(v)
        if length == 0:
            return Vector2(v.x, v.y)
        vec.x = v.x / length
        vec.y = v.y / length
        return vec

    # 2点間の距離の二乗を返します
    def get_distance2(a, b):
        x = b.x - a.x
        y = b.y - a.y
        return x**2 + y**2

    # 2点間の距離を返します
    def get_distance(a, b):
        x = b.x - a.x
        y = b.y - a.y
        xy = x**2 + y**2
        return math.sqrt(xy)

    # 二つのベクトルをなす角度を返します(度数)
    def get_angle2(a, b):
        rad = math.atan2(b.y - a.y, b.x - a.x)
        return math.degrees(rad)

    # 角度から方向ベクトルを取得します
    def get_direction_fromdeg(angle: float):
        rad = math.radians(angle)
        x, y = 0, 1
        v = Vector2(0, 0)
        v.x = x * math.cos(rad) - y * math.sin(rad)
        v.y = x * math.sin(rad) + y * math.cos(rad)
        return v

    # 二つのベクトルのなす角度を方向ベクトルで返します
    def get_direction(v1, v2):
        angle = Vector2.get_angle2(v1, v2)
        direction = Vector2.get_direction_fromdeg(-angle)
        return direction

    # ベクトルを指定した角度回転させる
    def rotate(v1, angle: float):
        rad = math.radians(angle)
        v = Vector2(0, 0)
        v.x = v1.x * math.cos(rad) - v1.y * math.sin(rad)
        v.y = v1.x * math.sin(rad) + v1.y * math.cos(rad)
        return v

    # 移動方向と物体の方向から反射ベクトルを返します
    def get_reflection(v1, obj_angle: float):
        obj_angle = abs(obj_angle)
        v2 = Vector2.get_direction_fromdeg(obj_angle)
        angle = Vector2.get_angle2(-v1, v2)
        reflect = Vector2.rotate(-v1, 2 * angle)
        return reflect


# スコアデータクラス
class ScoreData:
    playername: str = ""  # プレイヤー名
    score: int = 0  # スコア
    kills: int = 0  # 敵の撃破数
    playerhp = 0  # ゲーム終了時のHP
    hits: int = 0  # 被弾数
    mxcounts_: int = 0  # (テキスト用)このデータでの最大桁/文字数

    def __init__(self):
        self.playername = ""
        self.score = 0
        self.kills = 0
        self.playerhp = 0
        self.hits = 0
        self.mxcounts_ = 0
        pass

    # データの整形を行い最大文字数を格納します。
    def fit(self):
        self.mxcounts_ = max(self.mxcounts_, len(self.playername))
        self.mxcounts_ = max(self.mxcounts_, len(str(self.score)))
        self.mxcounts_ = max(self.mxcounts_, len(str(self.kills)))
        if self.playerhp < 0:
            self.playerhp = 0
            pass
        self.mxcounts_ = max(self.mxcounts_, len(str(self.playerhp)))
        self.mxcounts_ = max(self.mxcounts_, len(str(self.hits)))
        pass


# スコア集計クラス
class Totalizer:
    scores_: dict = dict()
    loaded: bool = False

    def __init__(self):
        self.initialize()
        pass

    def initialize(self):
        self.scores_ = dict()
        self.loaded = False

    # スコアテキストファイルから読み込みを行う
    def input(self, filename: str):
        if self.loaded:
            return
        path_ = self.joint_currentdirectoryfile(filename)
        try:
            with open(path_, "r") as f:
                data_ = f.readlines()
                pass
            pass
        except OSError as e:
            print("ScoreTextFile is not found.")
            return
            pass

        for i, d in enumerate(data_):
            if i == 0 or len(d) < 6:
                continue
                pass
            datas_ = d.split()
            newdata_ = ScoreData()
            newdata_.playername = datas_[1]
            newdata_.score = int(datas_[2])
            newdata_.kills = int(datas_[3])
            newdata_.hits = int(datas_[4])
            newdata_.playerhp = int(datas_[5])
            self.scores_[datas_[1]] = newdata_
            pass
        self.loaded = True
        pass

    # スコアデータを追加する
    def add_scoredata(self, newdata: ScoreData):
        if newdata.playername in self.scores_:
            data: ScoreData = self.scores_[newdata.playername]
            if newdata.score > data.score:
                self.scores_[newdata.playername] = newdata
                pass
            pass
        else:
            self.scores_[newdata.playername] = newdata
            pass
        pass

    # 読み込んだスコアデータ群をテキストファイルに書き出す
    def output_scores(self, filename: str):
        path = self.joint_currentdirectoryfile(filename)
        mxcnt = 10
        for data in self.scores_.values():
            d: ScoreData = data
            d.fit()
            mxcnt = max(mxcnt, d.mxcounts_)
            pass
        with open(path, "w") as f:
            rk = "Rank"
            pn = "PlayerName"
            sc = "Score"
            ks = "Kills"
            hs = "Hits"
            ph = "PlayerHP"
            ranklen = max(len(str(len(self.scores_))), len(rk))
            f.write(f"{rk:{ranklen}} ")
            f.write(f"{pn:{mxcnt}} ")
            f.write(f"{sc:{mxcnt}} ")
            f.write(f"{ks:{mxcnt}} ")
            f.write(f"{hs:{mxcnt}} ")
            f.write(f"{ph:{mxcnt}}\n")
            for i, data in enumerate(sorted(self.scores_.values(), reverse=True, key=lambda sd: sd.score)):
                d: ScoreData = data
                f.write(f"{str(i + 1):{ranklen}} ")
                f.write(f"{d.playername:{mxcnt}} ")
                f.write(f"{str(d.score):{mxcnt}} ")
                f.write(f"{str(d.kills):{mxcnt}} ")
                f.write(f"{str(d.hits):{mxcnt}} ")
                f.write(f"{str(d.playerhp):{mxcnt}}\n")
                pass
            pass
        pass
        print(path)
        print("--Done--")

    # 指定したプレイヤー名の順位を返す。存在しない場合等は0を返す
    def get_rank(self, playername: str):
        if not self.loaded:
            return 0
        rank = 1
        for data in sorted(self.scores_.values(), reverse=True, key=lambda ds: ds.score):
            d: ScoreData = data
            if d.playername == playername:
                return rank
            rank += 1
            pass
        return 0
        pass

    # 本プログラムと同一ディレクトリにあるファイル名と結合してフルパスを返す
    def joint_currentdirectoryfile(self, filename: str):
        result_ = os.path.join(os.getcwd(), filename)
        return result_


# ゲーム内全てのオブジェクトを管理するためのクラス
class World:
    owner = None  # このワールドを所有するゲームクラス
    Pawns = []  # ワールド内のオブジェクト
    Map = None  # ワールドのマップ
    ispause_: bool = False  # 更新を一時停止するかどうか

    def __init__(self, owner):
        self.owner = owner
        pass

    # ワールド内全てのオブジェクトとマップを更新します
    def update(self, dt):
        if not self.ispause_:
            for p in self.Pawns:
                p.update(dt)
            self.Map.update(dt)

    # ワールド内全てのオブジェクトの描画処理を呼び出します
    def draw(self):
        for p in self.Pawns:
            if p.visible:
                p.draw()

    def on_mousedown_input(self, pos):
        for p in self.Pawns:
            p.on_mouse_down(pos)

    def on_mouseup_input(self, pos):
        for p in self.Pawns:
            pw: Pawn = p
            pw.on_mouse_up(pos)

    def on_key_down(self, key):
        for p in self.Pawns:
            pw: Pawn = p
            pw.on_key_down(key)
            pass
        pass

    def on_key_up(self, key):
        for p in self.Pawns:
            pw: Pawn = p
            pw.on_key_up(key)
            pass
        pass

    # 指定したオブジェクトをワールドに追加します
    def addto_world(self, pawn):
        self.Pawns.append(pawn)

    # 指定したオブジェクトをワールドから削除し更新/描画処理から除外させます
    def delete_pawn(self, pawn):
        if not pawn in self.Pawns:
            return
        self.Pawns.remove(pawn)

    # マップを設定します
    def set_map(self, newmap):
        self.Map = newmap

    # オブジェクトの更新処理の停止を設定する
    def set_pause(self, pause: bool):
        self.ispause_ = pause

    # 現在、オブジェクトの更新処理が一時停止しているかどうかを返す
    def get_pause(self):
        return self.ispause_


# UIの定義したクラス
class UI:
    owner = None
    center_: Vector2 = Vector2(0, 0)
    elements_: list = []

    # 初期化の処理について記述する  注)UI要素はelementsに追加すること！
    def __init__(self, owner):
        self.owner = owner
        self.center_ = Vector2(0, 0)
        self.center_.x = WIDTH / 2
        self.center_.y = HEIGHT / 2
        pass

    # UI要素をUIに追加する
    def addto_viewport(self, element):
        self.elements_.append(element)
        pass

    # 描画処理について記述する
    def draw(self):
        pass

    def on_key_down(self, key):
        for e in self.elements_:
            elt: UIElement = e
            elt.on_key_down(key)
        pass

    def on_key_up(self, key):
        for e in self.elements_:
            elt: UIElement = e
            elt.on_key_up(key)
        pass

    def on_mouse_down(self, pos):
        for e in self.elements_:
            elt: UIElement = e
            elt.on_mouse_down(pos)
        pass

    def on_mosue_up(self, pos):
        for e in self.elements_:
            elt: UIElement = e
            elt.on_mouse_up(pos)
        pass


# UI内の要素クラス
class UIElement:
    owner: UI = None  # 所有者(UIクラス)
    pos: Vector2 = Vector2(0, 0)  # 位置
    use_percentpos: bool = False  # 位置を画面サイズの比で指定するかどうか
    is_center: bool = False
    size: Vector2 = Vector2(0, 0)  # 要素のサイズ
    pos_: Vector2 = Vector2(0, 0)  # 配置時のサイズ

    def __init__(self, owner: UI):
        self.owner = owner
        if self.use_percentpos:  # 画面サイズの比で指定する場合
            self.pos_ = self.get_percentpos()  # 配置位置を求める
        else:  # 画面座標で指定する場合
            self.pos_ = Vector2.get_vector(self.pos)
        if self.is_center:
            self.pos_.x = self.pos_.x - (self.size.x / 2)
            self.pos_.y = self.pos_.y + (self.size.y / 2)
        pass

    def draw(self):
        if self.use_percentpos:
            self.pos_ = self.get_percentpos()
        else:
            self.pos_ = Vector2.get_vector(self.pos)

        if self.is_center:
            self.pos_.x = self.pos_.x - (self.size.x / 2)
            self.pos_.y = self.pos_.y + (self.size.y / 2)
        pass

    # 画面サイズの比から位置を求める
    def get_percentpos(self):
        pos = Vector2(0, 0)
        pos.x = WIDTH * self.pos.x
        pos.y = HEIGHT * self.pos.y
        return pos

    def on_mouse_down(self, pos):
        pass

    def on_mouse_up(self, pos):
        pass

    def on_key_down(self, key):
        pass

    def on_key_up(self, key):
        pass


# UI要素クラスを継承したUI内テキストクラス
class UIText(UIElement):
    content: str = ""
    fontsize: int = 32
    fontcolor: ColorRGB = ColorRGB(255, 255, 255)

    def __init__(self, owner: UI):
        super().__init__(owner)
        self.content = ""
        self.fontsize = 32

    def draw(self):
        super().draw()
        screen.draw.text(self.content,
                         Vector2.get_tuple(self.pos_),
                         fontsize=self.fontsize,
                         color=self.fontcolor.get_tuple())
        pass


# テキスト入力/表示が可能なテキストボックス
class UITextBox(UIText):
    is_focus: bool = False  # テキストボックスがフォーカスされているかどうか
    on_enter = None

    def __init__(self, owner: UI):
        super().__init__(owner)
        self.is_focus = False
        pass

    def draw(self):
        super().draw()
        pass

    def on_key_down(self, key):
        if self.is_focus:
            if key == pygame.K_RETURN:
                self.is_focus = False
                if self.on_enter is not None and callable(self.on_enter):
                    self.on_enter(self)
            elif key == pygame.K_BACKSPACE:
                self.content = self.content[:-1]
            else:
                if 0 <= key <= 0x10ffff:
                    self.content += chr(key)
        pass


# ボタン要素クラス
class UIButton(UIElement):
    backgroundcolor: ColorRGB = ColorRGB(0, 0, 0)  # ボタンのカラー
    rect_: Rect = None  # ボタンの四角形オブジェクト
    on_click = None  # ボタンが押された際の処理関数

    def __init__(self, owner: UI):
        super().__init__(owner)
        self.rect_ = Rect(Vector2.get_tuple(self.pos_),
                          Vector2.get_tuple(self.size))

    def draw(self):
        super().draw()
        self.rect_ = Rect(Vector2.get_tuple(self.pos_),
                    Vector2.get_tuple(self.size))
        screen.draw.filled_rect(self.rect_, self.backgroundcolor.get_tuple())

    # ボタンが押された時の処理
    def on_clicked(self):
        if not self.on_click is None and callable(self.on_click):
            self.on_click(self)
        pass

    def on_mouse_down(self, pos):
        if self.rect_.collidepoint(pos):
            self.on_clicked()
        pass


# テキスト付ボタン要素クラス
class UITextedButton(UIButton):
    textcolor: ColorRGB = ColorRGB(0, 0, 0)
    textpos: Vector2 = Vector2(0, 0)
    uitext: UIText = None

    def __init__(self, owner: UI):
        super().__init__(owner)
        self.uitext = UIText(owner)
        self.uitext.size = self.size
        self.uitext.use_percentpos = False
        self.uitext.is_center = True

    def draw(self):
        super().draw()
        pos = Vector2(0, 0)
        pos.x = self.pos_.x + self.textpos.x
        pos.y = self.pos_.y + self.textpos.y
        self.uitext.pos = pos
        self.uitext.draw()
        pass


# UI要素クラスを継承した進捗バークラス
class UIProgressBar(UIElement):
    percent: float = 1.0  # 進捗率(1.0で満たされ、0.0は何もなし)
    filledcolor: ColorRGB = ColorRGB(0, 0, 0)  # 進捗が満たされた状態のカラー
    backgroundcolor: ColorRGB = ColorRGB(0, 0, 0)  # 進捗が満たされていない状態(背景)のカラー

    def __init__(self, owner: UI):
        super().__init__(owner)
        self.percent = 1.0
        self.filledcolor = ColorRGB(0, 0, 0)
        self.backgroundcolor = ColorRGB(0, 0, 0)

    def draw(self):
        super().draw()
        # 四角の生成
        rect_size = Vector2.get_vector(self.size)
        rect_size.x = rect_size.x * self.percent
        bar: Rect = Rect(Vector2.get_tuple(self.pos_),
                         Vector2.get_tuple(rect_size))
        bar_background: Rect = Rect(Vector2.get_tuple(self.pos_),
                                    Vector2.get_tuple(self.size))

        # 四角の描画処理
        screen.draw.filled_rect(bar_background, self.backgroundcolor.get_tuple())
        screen.draw.filled_rect(bar, self.filledcolor.get_tuple())
        pass


# HPバークラス(HPバーとHP値テキスト)
class UIHPBar(UIProgressBar):
    hp: float = 100  # HP値
    hp_text_pos_relative: Vector2 = Vector2(0, 0)  # HPテキストの相対位置
    hp_UItext_: UIText = None  # UITextオブジェクト

    def __init__(self, owner: UI):
        super().__init__(owner)
        self.hp_UItext_ = UIText(owner)
        self.hp_UItext_.content = f"{self.hp:.0f}"
        self.percent = 1.0
        self.hp_UItext_.use_percentpos = False
        pass

    def draw(self):
        super().draw()
        pos = Vector2(0, 0)
        pos.x = self.pos_.x + self.size.x + self.hp_text_pos_relative.x
        pos.y = self.pos_.y + self.hp_text_pos_relative.y
        self.hp_UItext_.content = f"{self.hp:.0f}"
        self.hp_UItext_.pos = pos
        self.hp_UItext_.draw()


# 残弾数ゲージクラス(残弾数ゲージ+残弾数テキスト)
class UIBulletGauge(UIProgressBar):
    bullets: int = 10  # 残弾数
    bullets_textpos_relative: Vector2 = Vector2(0, 0)  # 残弾数テキストの相対位置
    bullets_UIText_: UIText = None  # 残弾数テキストオブジェクト
    bulletsgauge_linecolor: ColorRGB = ColorRGB(0, 0, 0)  # ゲージのラインカラー

    def __init__(self, owner: UI):
        super().__init__(owner)
        self.bullets_UIText_ = UIText(owner)
        self.bullets_UIText_.content = f"{self.bullets}"
        self.percent = 1.0
        self.bullets_UIText_.use_percentpos = False

        pass

    def draw(self):
        super().draw()  # Progressバーの描画処理
        # 残弾数テキストの描画処理
        pos = Vector2(0, 0)
        pos.x = self.pos_.x + self.size.x + self.bullets_textpos_relative.x
        pos.y = self.pos_.y + self.bullets_textpos_relative.y
        self.bullets_UIText_.content = f"{self.bullets}"
        self.bullets_UIText_.pos = pos
        self.bullets_UIText_.draw()
        me: Player = self.owner.owner

        # ゲージのライン描画処理
        interval = self.size.x / me.weapon.capacity  # ラインの描画間隔
        for i in range(1, me.weapon.capacity):
            offset = 1
            pos_lower = Vector2(0, 0)
            pos_upper = Vector2(0, 0)
            pos_lower.x = self.pos_.x + (interval * i)
            pos_lower.y = self.pos_.y - offset
            pos_upper.x = pos_lower.x
            pos_upper.y = pos_lower.y + self.size.y
            pygame.draw.line(screen.surface,
                             self.bulletsgauge_linecolor.get_tuple(),
                             Vector2.get_tuple(pos_lower),
                             Vector2.get_tuple(pos_upper), 1)


# プレイヤー名入力用UI
class PlayerNameUI(UI):
    t_caption: UIText = None
    tb_textbox: UITextBox = None

    def __init__(self, owner):
        super().__init__(owner)
        self.pos = Vector2(0.5, 0.5)
        self.t_caption = UIText(self)
        self.t_caption.content = "PlayerName: "
        self.t_caption.fontsize = 64
        self.t_caption.pos = Vector2(0.2, 0.5)
        self.t_caption.use_percentpos = True
        self.addto_viewport(self.t_caption)

        self.tb_textbox = UITextBox(self)
        self.tb_textbox.content = ""
        self.tb_textbox.fontsize = 64
        self.tb_textbox.pos = Vector2(0.5, 0.5)
        self.tb_textbox.use_percentpos = True
        self.tb_textbox.is_focus = True
        self.tb_textbox.on_enter = self.on_enter
        self.addto_viewport(self.tb_textbox)
        pass

    def draw(self):
        super().draw()
        self.t_caption.draw()
        self.tb_textbox.draw()
        pass

    # Enterが押された時の処理
    def on_enter(self, sender):
        tb: UITextBox = sender
        me: Player = self.owner
        me.playername = tb.content
        me.show_menu()
        pass


# メニューUIクラス
class MenuUI(UI):
    buttoncolor: ColorRGB = ColorRGB(120, 120, 120)

    def __init__(self, owner):
        super().__init__(owner)
        self.maintext = UIText(self)
        self.maintext.content = "Pause"
        self.maintext.pos = Vector2(0.45, 0.5)
        self.maintext.use_percentpos = True
        self.maintext.fontsize = 64
        pass

    def draw(self):
        super().draw()
        self.maintext.draw()
        pass


# プレイヤーのUI
class PlayerUI(UI):
    hpbar: UIHPBar = None  # HPバー要素
    bulletguage: UIBulletGauge = None  # 残弾数ゲージ要素
    scoretext: UIText = None  # スコアテキスト
    pausetext: UIText = None  # 一時停止時のテキスト

    def __init__(self, owner):
        super().__init__(owner)
        me: Player = self.owner

        # HPバー要素
        self.hpbar = UIHPBar(self)
        self.hpbar.hp = 100
        self.hpbar.percent = 1.0
        self.hpbar.backgroundcolor = ColorRGB(150, 150, 150)  # HPが満たされていない状態のカラー(背景のカラー)
        self.hpbar.filledcolor = ColorRGB(0, 240, 140)  # HPが満たされた状態のカラー
        self.hpbar.pos = Vector2(0.75, 0.86)
        self.hpbar.use_percentpos = True
        self.hpbar.size = Vector2(175, 10)
        self.hpbar.hp_text_pos_relative = Vector2(10, 0)
        self.hpbar.hp_UItext_.fontsize = 24
        self.addto_viewport(self.hpbar)

        # 残弾数ゲージ要素
        self.bulletgauge = UIBulletGauge(self)
        self.bulletgauge.bullets = me.weapon.capacity
        self.bulletgauge.percent = 1.0
        self.bulletgauge.backgroundcolor = ColorRGB(150, 150, 150)
        self.bulletgauge.filledcolor = ColorRGB(230, 210, 30)
        self.bulletgauge.bulletsgauge_linecolor = ColorRGB(120, 110, 10)
        self.bulletgauge.pos = Vector2(0.75, 0.9)
        self.bulletgauge.use_percentpos = True
        self.bulletgauge.size = Vector2(175, 10)
        self.bulletgauge.bullets_textpos_relative = Vector2(10, -4)
        self.bulletgauge.bullets_UIText_.fontsize = 24
        self.addto_viewport(self.bulletgauge)

        self.scoretext = UIText(self)
        self.scoretext.pos = Vector2(0.05, 0.05)
        self.scoretext.use_percentpos = True
        self.scoretext.content = "0"
        self.scoretext.fontsize = 32
        self.addto_viewport(self.scoretext)

        self.pausetext = UIText(self)
        self.pausetext.pos = Vector2(0.45, 0.45)
        self.pausetext.use_percentpos = True
        self.pausetext.content = "Pause"
        self.pausetext.fontsize = 64
        self.addto_viewport(self.pausetext)

        pass

    def draw(self):
        super().draw()
        # PlayerのHP情報の取得
        me: Player = self.owner

        # HPバーの更新と描画
        self.hpbar.hp = (me.hp_ / me.HP) * 100
        self.hpbar.percent = me.hp_ / me.HP
        self.hpbar.draw()

        # 残弾数ゲージの更新と描画
        self.bulletgauge.bullets = me.weapon.capacity_
        self.bulletgauge.percent = me.weapon.capacity_ / me.weapon.capacity
        self.bulletgauge.draw()

        self.scoretext.content = f"Score: {str(me.score_)}"
        self.scoretext.draw()

        if me.world.get_pause():
            self.pausetext.draw()

        pass


# 終了時のスコア/順位表示UI
class ResultUI(UI):
    t_ended: UIText = None  # 終了テキストオブジェクト
    t_score: UIText = None  # スコアテキストオブジェクト
    t_rank: UIText = None  # 順位テキストオブジェクト
    pos: Vector2 = Vector2(0, 0)  # 表示位置(画面比率)
    endedtext_finishedcolor: ColorRGB = ColorRGB(76, 227, 0)  # 成功時の終了テキストカラー
    endedtext_gameovercolor: ColorRGB = ColorRGB(200, 20, 0)  # ゲームオーバー時の終了テキストカラー
    endedtext_finishedtext: str = "Finish!"  # 成功時の終了テキスト内容
    endedtext_gameovertext: str = "GameOver!"  # ゲームオーバー字の終了テキスト内容

    def __init__(self, owner, asfinish=False):
        super().__init__(owner)
        self.pos = Vector2(0.375, 0.5)
        self.t_ended = UIText(self)
        self.t_ended.pos = self.pos
        self.t_ended.use_percentpos = True
        self.t_ended.fontsize = 64
        if asfinish:
            self.t_ended.fontcolor = self.endedtext_finishedcolor
            self.t_ended.content = self.endedtext_finishedtext
        else:
            self.t_ended.fontcolor = self.endedtext_gameovercolor
            self.t_ended.content = self.endedtext_gameovertext
        self.addto_viewport(self.t_ended)

        me: Player = self.owner

        self.t_score = UIText(self)
        self.t_score.pos = Vector2(0, 0)
        self.t_score.pos.x = self.pos.x
        self.t_score.pos.y = self.pos.y + 0.1
        self.t_score.use_percentpos = True
        self.t_score.fontsize = 32
        self.t_score.content = f"Score: {str(me.score_)}"
        self.addto_viewport(self.t_score)

        gm: Game = me.world.owner
        rank = gm.get_playerrank()

        self.t_rank = UIText(self)
        self.t_rank.pos = Vector2(0, 0)
        self.t_rank.pos.x = self.pos.x
        self.t_rank.pos.y = self.pos.y + 0.2
        self.t_rank.use_percentpos = True
        self.t_rank.fontsize = 32
        self.t_rank.content = f"Rank: {rank}"
        self.addto_viewport(self.t_rank)

        pass

    def draw(self):
        super().draw()
        self.t_ended.draw()
        self.t_score.draw()
        self.t_rank.draw()


# ゲーム内で配置/移動可能なオブジェクトクラス
class Pawn(Actor):
    LEFT = 0  # 左
    RIGHT = 1  # 右
    UP = 2  # 上
    DOWN = 3  # 下
    SkinPic: str = ""  # 外見の画像
    Skins = None  # スキンセット
    visible: bool = True  # 表示/非表示を設定します
    world: World = None  # 自身が配置されているワールド
    location: Vector2 = Vector2(0, 0)  # 位置
    isBlock: bool = False  # 壁にブロックされるかどうか
    isKeyInput: bool = False  # キー入力を有効にするかどうか
    moveInput: Vector2 = Vector2(0, 0)  # 入力
    collide = False, False, False, False  # 現在、壁に衝突しているかどうか
    collideobjects_ = []  # 現在衝突しているオブジェクト一覧

    def __init__(self, pic_name):
        super().__init__(pic_name)
        self.SkinPic = pic_name
        self.location = Vector2(self.x, self.y)
        self.moveInput = Vector2(0, 0)

    # 指定したワールドに出現させます
    def spawn(self, world: World):
        self.world = world
        world.addto_world(self)

    # ワールドから取り除きます
    def destroy(self):
        self.world.delete_pawn(self)
        del self

    # 更新処理
    def update(self, dt):
        self.image = self.SkinPic
        self.moveInput.x, self.moveInput.y = 0, 0
        # self.location.x, self.location.y = self.x, self.y
        self.x, self.y = self.location.x, self.location.y
        if self.isKeyInput:
            self.key_input(keyboard)
        collides = self.is_collide_walls()

        if self.isBlock:
            # left
            if collides[self.LEFT]:
                self.left = 0
            # right
            if collides[self.RIGHT]:
                self.right = WIDTH
                pass
            # up(=top)
            if collides[self.UP]:
                self.top = 0
                pass
            # down(=bottom)
            if collides[self.DOWN]:
                self.bottom = HEIGHT
                pass
        self.collide = collides

        pass

    # キー入力を受け取った際の処理
    def key_input(self, keys):
        pass

    # マウスのボタンが押された際の処理
    def on_mouse_down(self, pos):
        pass

    # マウスのボタンが離された際の処理
    def on_mouse_up(self, pos):
        pass

    # キーが押された際の処理
    def on_key_down(self, key):
        pass

    # キーが離された際の処理
    def on_key_up(self, key):
        pass

    # 枠に衝突しているかどうかを判定します
    def is_collide_wall(self):
        for c in self.collide:
            if c:
                return True
        return False

    # 枠に衝突しているかどうかを判定しそれぞれの衝突判定結果を返します。
    def is_collide_walls(self):
        left = (self.left < 0)
        right = (self.right > WIDTH)
        up = (self.top < 0)
        down = (self.bottom > HEIGHT)

        return left, right, up, down

    # ワールド内のオブジェクトと衝突しているかどうかを判定し、
    # 衝突しているオブジェクト一覧を返します
    def is_hit(self):
        hits = []
        for p in self.world.Pawns:
            if p == self:
                continue
            if p.colliderect(self):
                hits.append(p)
        self.collideobjects_ = hits
        return hits

    # Pawn同士で衝突した際に呼ばれます
    def on_hit(self, actor):
        pass


# 発射する弾クラス
class Bullet(Pawn):
    owner: Pawn = None  # 所有者(発砲者)
    pic: str = "ball_red_small_2"  # 弾の画像
    damage = 15  # 基本ダメージ
    direction = Vector2(0, 0)  # 弾の飛翔方向
    velocity: float = 0.0  # 飛翔速度
    is_bounce: bool = False  # 障害物や壁に反発するかどうか
    bounces: int = 0  # 反発回数(is_bounceが有効の場合)
    hit_once: bool = False  # オブジェクトの種類に関係なく一度当たったら消滅するか
    hurt_self: bool = False  # その弾は発砲者自身にダメージを与えるか
    bounces_: int = 0  # 現在の反発回数
    hit_ignore_owner = False  # 弾は発砲者の衝突判定を無視するかどうか

    def __init__(self, owner: Pawn):
        super().__init__(self.pic)
        self.isBlock = False
        self.isKeyInput = False
        self.is_bounce = True
        self.bounces = 2
        self.velocity = 900.0
        self.owner = owner

    # 飛翔方向を設定します
    def set_direction(self, direction: Vector2):
        self.direction = direction
        pass

    def bounce(self):
        if not self.is_bounce:
            self.destroy()
        if self.bounces_ >= self.bounces:
            self.destroy()
        self.bounces_ += 1

    def update(self, dt):
        super().update(dt)

        worldpos = self.world.Map.get_worldlocation(self.location)
        world_width = self.world.Map.width_
        world_height = self.world.Map.height_

        if worldpos.x >= world_width:
            self.direction.x = -self.direction.x
            self.bounce()
        if worldpos.x <= 0:
            self.direction.x = -self.direction.x
            self.bounce()
        if worldpos.y >= world_height:
            self.direction.y = -self.direction.y
            self.bounce()
        if worldpos.y <= 0:
            self.direction.y = -self.direction.y
            self.bounce()

        if self.isBlock:
            if self.collide[self.LEFT] or self.collide[self.RIGHT]:
                self.direction.x = -self.direction.x
            if self.collide[self.UP] or self.collide[self.DOWN]:
                self.direction.y = -self.direction.y

        hits = self.is_hit()
        for p in hits:
            if p != self.owner and type(p) is not Ground:
                p.on_hit(self)
                if self.hit_once:
                    self.destroy()
                if type(p) is Wall:
                    self.direction = -self.direction
                    self.bounce()

        self.location.x += self.direction.x * self.velocity * dt
        self.location.y += self.direction.y * self.velocity * dt


# ショットガン用の弾
class ShotShell(Bullet):

    def __init__(self, owner: Pawn):
        super().__init__(owner)
        self.velocity = 600
        self.owner = owner
        pass


class SMGShell(Bullet):
    def __init__(self, owner: Pawn):
        super().__init__(owner)
        self.velocity = 900
        self.is_bounce = False
        self.hit_once = True


# キャラクタースキン
class CharacterSkins:
    def __init__(self):
        self.handgun: str = ""  # 拳銃を所持しているスキン
        self.shotgun: str = ""  # ショットガンを所持しているスキン
        self.smg: str = ""  # サブマシンガンを所持しているスキン
        self.reloding: str = ""  # 装填しているスキン
        pass

    # characterが所有している武器の種類に応じてスキンを変更する
    def set_skin(self, owner):
        chara: Character = owner
        if type(chara.weapon) is HandGun:
            chara.SkinPic = self.handgun
        elif type(chara.weapon) is Shotgun:
            chara.SkinPic = self.shotgun
        elif type(chara.weapon) is SMG:
            chara.SkinPic = self.smg
        pass


# プレイヤーのスキン
class PlayerSkins(CharacterSkins):
    def __init__(self):
        super().__init__()
        self.handgun = "manblue_gun"
        self.shotgun = "manblue_silencer"
        self.smg = "manblue_machine"
        self.reloding = "manblue_reload"
        pass


# 敵のスキン
class EnemySkins(CharacterSkins):
    def __init__(self):
        super().__init__()
        self.handgun = "manbrown_gun"
        self.shotgun = "manbrown_silencer"
        self.smg = "manbrown_machine"
        self.reloding = "manbrown_reload"
        pass


# 武器クラス
class Weapon:
    owner: Pawn = None  # 所有者
    bullet = None  # 発射する弾クラス
    sound_fire: pygame.mixer.Sound = None  # 発砲音
    sound_reload: pygame.mixer.Sound = None  # 装填音
    sound_empty: pygame.mixer.Sound = None  # 空撃ち音
    sound_slide: pygame.mixer.Sound = None  # 装填完了時のスライド音
    damage = 15  # 基本ダメージ
    damage_multiply = 0.5  # ダメージ乗数
    capacity: int = 10  # 装弾数
    fire_rate = 0.25  # 発射速度
    reload_time: float = 3.0  # 装填時間
    diffusion: float = 0.2  # 拡散値
    max_diffangle: float = 30  # 最大拡散角度
    fire_mode: str = ""  # 発射モード
    FIRE_MODE_SINGLE = "single"  # トリガーを引いたら一発のみ発射する
    FIRE_MODE_AUTO = "auto"  # トリガーを引いている間ずっと連射する
    FIRE_MODE_SHOT = "shot"  # 一度に弾を複数発射する
    capacity_: int = 0  # 現在の弾数
    is_reloading_: bool = False  # 現在装填中かどうか
    is_ready: bool = True  # 発射可能かどうか
    volume_: float = 1.0

    def __init__(self, owner: Pawn):
        self.fire_mode = self.FIRE_MODE_SINGLE
        self.owner = owner
        self.capacity_ = self.capacity
        self.is_ready = True
        self.bullet = Bullet
        self.sound_fire = sounds.handgun_shot
        self.sound_empty = sounds.handgun_empty
        self.sound_reload = sounds.handgun_reload
        self.sound_slide = sounds.handgun_slide
        pass

    # 弾を発射する
    def fire(self, at: Vector2):
        if not self.is_reloading_:  # 装填中でなければ
            if self.capacity_ > 0:  # 弾が残っていれば
                if self.is_ready:  # 武器が発射可能であれば
                    blt = self.bullet(self.owner)  # 弾オブジェクトの生成
                    blt.damage = Util.random_damage(self.damage, self.damage_multiply)  # 弾の持つダメージをランダムに算定し設定する
                    blt.spawn(self.owner.world)  # 弾をワールドに生成する
                    blt.location = Vector2.get_vector(self.owner.location)  # 弾の位置を設定
                    direction = Vector2.get_angle2(self.owner.location, at)  # 弾の角度(発砲者とマウスカーソル位置のなす角度)
                    direction = Vector2.get_direction_fromdeg(direction - 90)  # 角度から方向ベクトルを取得
                    if Util.random_bool(self.diffusion):  # 拡散値の確率によって、拡散させるかどうかをランダムに決定する
                        direction = Util.random_rotatevector(direction, self.max_diffangle)  # 方向ベクトルにランダムな角度に回転させる
                        print("Diffusion")
                    blt.set_direction(direction)  # 飛翔方向を設定
                    blt.location += direction * 10
                    self.capacity_ -= 1  # 現在の装弾数を減らす
                    #sounds.handgun_shot.set_volume(self.volume_)
                    #sounds.handgun_shot.play()  # 発砲音を鳴らす
                    self.sound_fire.set_volume(self.volume_)
                    self.sound_fire.play()
                    self.is_ready = False
                    clock.schedule_unique(self.on_after_fire, self.fire_rate)
                pass
            else:  # 弾が残っていない時
                # sounds.handgun_empty.play()  # 空撃ち音を鳴らす
                self.sound_empty.set_volume(self.volume_)
                self.sound_empty.play()
            pass
        pass

    # 現在の残弾数がないかどうかを返します
    def isempty(self):
        return self.capacity_ <= 0

    # 現在、装填中かどうかを返します
    def isreloading(self):
        return self.is_reloading_

    # 弾の装填を行う
    def reload(self):
        if not self.is_reloading_:  # 装填中でなければ
            self.is_reloading_ = True  # 装填中であるかどうかを設定する(処理が重複しないように)
            # sounds.handgun_reload.play()  # 装填音を鳴らす
            self.sound_reload.set_volume(self.volume_)
            self.sound_reload.play()
            self.set_reloadingskin()
            clock.schedule_unique(self.on_ended_reload, self.reload_time)  # 装填時間分遅らせて装填完了処理を呼ぶ
        pass

    # 装填時のスキンを設定する
    def set_reloadingskin(self, ended=False):
        skins: CharacterSkins = self.owner.Skins
        if ended:
            skins.set_skin(self.owner)
        else:
            self.owner.SkinPic = skins.reloding
            pass
        pass

    # 装填が完了した際に呼ばれる
    def on_ended_reload(self):
        print("Reloaded")
        #sounds.handgun_slide.play()  # 銃スライド音を鳴らす
        self.sound_slide.play()  # 銃スライド音を鳴らす
        self.set_reloadingskin(True)
        self.capacity_ = self.capacity  # 現在の装填数を補充する
        self.is_reloading_ = False  # 装填中であるかどうかを設定する

    # 発射後一定の発射速度に達したあとに呼ばれる
    def on_after_fire(self):
        self.is_ready = True


# ハンドガン
class HandGun(Weapon):

    def __init__(self, owner: Pawn):
        super().__init__(owner)
        self.capacity = 10
        self.capacity_ = self.capacity
        self.fire_rate = 0.25
        self.reload_time = 2.0
        self.diffusion = 0.2
        self.max_diffangle = 10
        self.fire_mode = self.FIRE_MODE_SINGLE
        pass

    def fire(self, at: Vector2):
        super().fire(at)
        
    def reload(self):
        super().reload()
        return self


# サブマシンガン(連射が可能な銃)
class SMG(Weapon):
    def __init__(self, owner: Pawn):
        super().__init__(owner)
        self.capacity = 30
        self.capacity_ = self.capacity
        self.fire_rate = 0.05
        self.reload_time = 3.0
        self.diffusion = 0.5
        self.max_diffangle = 20
        self.fire_mode = self.FIRE_MODE_AUTO
        self.bullet = SMGShell
        self.sound_fire = sounds.smg_shot
        self.sound_empty = sounds.smg_empty
        self.sound_reload = sounds.smg_reload
        self.sound_slide = sounds.smg_attach
        pass


# ショットガン(一度の射撃で複数弾が扇状に拡散する銃)
class Shotgun(Weapon):
    shells: int = 5  # 一度に発射する弾数
    shotdiffangle: float = 15  # 拡散角度

    def __init__(self, owner: Pawn):
        super().__init__(owner)
        self.capacity = 6
        self.capacity_ = self.capacity
        self.fire_rate = 1.25
        self.reload_time = 7.5
        self.diffusion = 0.75
        self.max_diffangle = 5.0
        self.fire_mode = self.FIRE_MODE_SHOT
        self.shotdiffangle = 15
        self.sound_fire = sounds.shotgun_shot
        self.sound_empty = sounds.shotgun_empty
        self.sound_reload = sounds.shotgun_reload
        self.sound_slide = sounds.shotgun_pump
        pass

    def fire(self, at: Vector2):
        if not self.is_reloading_:
            if self.capacity_ > 0:
                shotangle = self.shotdiffangle / (self.shells - 1)  # 拡散させる角度(弾毎に角度をつける)
                shotangle_ = -shotangle  # 負の角度から扇状に拡散させる
                if self.is_ready:
                    for i in range(self.shells):  # 弾の数だけ繰り返す
                        blt = self.bullet(self.owner)
                        blt.damage = Util.random_damage(self.damage, self.damage_multiply)
                        blt.spawn(self.owner.world)
                        blt.location = Vector2.get_vector(self.owner.location)
                        direction = Vector2.get_angle2(self.owner.location, at)
                        direction = Vector2.get_direction_fromdeg(direction - 90)
                        direction = Vector2.rotate(direction, shotangle_)
                        if Util.random_bool(self.diffusion):
                            direction = Util.random_rotatevector(direction, self.max_diffangle)
                        blt.set_direction(direction)
                        blt.location += direction * 10
                        shotangle_ += shotangle
                        pass
                    sounds.shotgun_shot.play()
                    self.capacity_ -= 1
                    self.is_ready = False
                    clock.schedule_unique(self.on_after_fire, self.fire_rate)
                pass
            else:
                pass
                sounds.shotgun_empty.play()
            pass
        pass

    def on_after_fire(self):
        super().on_after_fire()
        sounds.shotgun_pump.play()
        pass


# ゲーム内に配置可能な静的オブジェクト
class StaticObject(Pawn):
    Pic: str = ""
    initiallocation: Vector2 = Vector2(0, 0)

    def __init__(self, pic: str):
        self.Pic = pic
        super().__init__(self.Pic)
        self.isKeyInput = False


# 地面/タイルのクラス
class Ground(StaticObject):
    def __init__(self, pic: str):
        self.Pic = pic
        super().__init__(self.Pic)


# 床のクラス
class Floor(Ground):
    def __init__(self):
        self.Pic = ""
        super().__init__(self.Pic)


# 壁障害物の種類とそれに対応する画像ファイル名の定義をまとめたクラス
class WallStyle:
    wall_up = ""  # U
    wall_down = ""  # D
    wall_left = ""  # L
    wall_right = ""  # R
    wall_corner_upleft = ""  # CUL
    wall_corner_upright = ""  # CUR
    wall_corner_downleft = ""  # CDL
    wall_corner_downright = ""  # CDR
    wall_joint_upleft = ""  # JUL
    wall_joint_upright = ""  # JUR
    wall_joint_downleft = ""  # JDL
    wall_joint_donwright = ""  # JDR
    wall_lefttoright = ""  # LR
    wall_uptodown = ""  # UD
    wall_joint_uptodown_left = ""  # JUDL
    wall_joint_updodown_right = ""  # JUDR
    wall_joint_lefttoright_up = ""  # JLRU
    wall_joint_lefttoright_down = ""  # JLRD
    wall_pillar = ""  # P

    def __init__(self):
        pass


# オレンジ色の壁障害物
class WallStyleOrange(WallStyle):
    def __init__(self):
        super().__init__()
        self.wall_up = "wall_orange_up"
        self.wall_down = "wall_orange_down"
        self.wall_left = "wall_orange_left"
        self.wall_right = "wall_orange_right"
        self.wall_corner_upleft = "wall_orange_corner_upleft"
        self.wall_corner_upright = "wall_orange_corner_upright"
        self.wall_corner_downleft = "wall_orange_corner_downleft"
        self.wall_corner_downright = "wall_orange_corner_downright"
        self.wall_joint_upleft = "wall_orange_joint_upleft"
        self.wall_joint_upright = "wall_orange_joint_upright"
        self.wall_joint_downleft = "wall_orange_joint_downleft"
        self.wall_joint_donwright = "wall_orange_joint_downright"
        self.wall_lefttoright = "wall_orange_leftright"
        self.wall_uptodown = "wall_orange_updown"
        self.wall_joint_uptodown_left = "wall_orange_joint_updown_left"
        self.wall_joint_updodown_right = "wall_orange_joint_updown_right"
        self.wall_joint_lefttoright_up = "wall_orange_joint_leftright_up"
        self.wall_joint_lefttoright_down = "wall_orange_joint_leftright_down"
        self.wall_pillar = "wall_orange_pillar"
        pass


class WallStyleWood(WallStyle):
    def __init__(self):
        super().__init__()
        self.wall_up = "wall_wood_up"
        self.wall_down = "wall_wood_down"
        self.wall_left = "wall_wood_left"
        self.wall_right = "wall_wood_right"
        self.wall_corner_upleft = "wall_wood_corner_upleft"
        self.wall_corner_upright = "wall_wood_corner_upright"
        self.wall_corner_downleft = "wall_wood_corner_downleft"
        self.wall_corner_downright = "wall_wood_corner_downright"
        self.wall_joint_upleft = "wall_wood_joint_upleft"
        self.wall_joint_upright = "wall_wood_joint_upright"
        self.wall_joint_downleft = "wall_wood_joint_downleft"
        self.wall_joint_donwright = "wall_wood_joint_downright"
        self.wall_lefttoright = "wall_wood_leftright"
        self.wall_uptodown = "wall_wood_updown"
        self.wall_joint_uptodown_left = "wall_wood_joint_updown_left"
        self.wall_joint_updodown_right = "wall_wood_joint_updown_right"
        self.wall_joint_lefttoright_up = "wall_wood_joint_leftright_up"
        self.wall_joint_lefttoright_down = "wall_wood_joint_leftright_down"
        self.wall_pillar = "wall_wood_pillar"
        pass


# 壁クラス
class Wall(StaticObject):
    def __init__(self, pic):
        self.Pic = pic
        super().__init__(self.Pic)


# マップに配置する種類を表す定数
N = 0  # None
G = 1  # Ground
U = 1  # Up
D = 2  # Down
L = 3  # Left
R = 4  # Right
JUL = 5  # Joint_upleft
JUR = 6  # Joint_upright
JDL = 7  # Joint_downleft
JDR = 8  # Joint_downright
CUL = 9  # Corner_upleft
CUR = 10  # Corner_upright
CDL = 11  # Corner_downleft
CDR = 12  # Corner_downright
LR = 13  # LeftToRight
UD = 14  # UpToDown
JUDL = 15  # Joint_UpToDown_Left
JUDR = 16  # Joint_UpTODown_Right
JLRU = 17  # Joint_LeftToRight_Up
JLRD = 18  # Joint_LeftToRight_Down
P = 19  # Pillar
E = 20  # Enemy


# プレイヤー/敵共通のキャラクタークラス
class Character(Pawn):
    HP = 100  # 最大ヒットポイント
    Def_multiply: float = 0.0  # 防御乗数(ダメージの軽減率)
    CharacterMoveSpeed = 5  # キャラクターの移動速度
    weapon: Weapon = None  # キャラクターの所持している武器
    ui: UI = None  # UI
    hp_ = 0  # 現在のHP

    def __init__(self, pic_name: str):
        super().__init__(self.SkinPic)
        pass

    def draw(self):
        super().draw()
        if self.ui is not None:
            self.ui.draw()

    def update(self, dt):
        super().update(dt)
        self.is_hit()
        for obj in self.collideobjects_:
            if type(obj) is Wall:
                direction = Vector2.get_direction(self.location, obj.location)
                direction = -direction
                direction = Vector2.rotate(direction, -90)
                self.moveInput = direction

    def on_mouse_down(self, pos):
        super().on_mouse_down(pos)
        if self.ui is not None:
            self.ui.on_mouse_down(pos)
            pass
        pass

    def on_mouse_up(self, pos):
        super().on_mouse_up(pos)
        if self.ui is not None:
            self.ui.on_mosue_up(pos)
            pass
        pass

    def on_key_down(self, key):
        super().on_key_down(key)
        if self.ui is not None:
            self.ui.on_key_down(key)
        pass

    def on_key_up(self, key):
        super().on_key_up(key)
        if self.ui is not None:
            self.ui.on_key_up(key)
        pass

    # オブジェクト同士で衝突があった時に呼ばれる
    def on_hit(self, actor):
        pass

    # 弾によるダメージが適用される際に呼ばれる
    def apply_damage(self, bullet: Bullet):
        pass

    # スコアを与える際に呼ばれる
    def apply_score(self, hp: int):
        pass
    
    def key_input(self, keys):
        super().key_input(keys)

    # UIを差し替えます
    def swap_ui(self, newui: UI):
        self.ui = newui


# プレイヤー
class Player(Character):
    playername: str = ""  # プレイヤー名
    mousepressed_: bool = False  # 現在、マウスのボタンが押された状態かどうか
    score_max_multiply: int = 5  # スコア加点時の最大乗数
    score_bonus_percent: float = 0.2  # ボーナス加点される確率
    score_: int = 0  # 現在のスコア
    kills_: int = 0  # 現在のキル数(撃破した敵の数)
    hits_: int = 0  # 現在のヒット数(打たれた回数)
    ui_main: UI = None  # ゲーム中のUI
    ui_pause: UI = None  # 一時停止中のUI
    weapons: list = []

    def __init__(self):
        self.Skins = PlayerSkins()
        self.weapon = HandGun(self)
        self.Skins.set_skin(self)
        # self.SkinPic = "manblue_gun"  # 画像とActorは90度ずれている
        super().__init__(self.SkinPic)
        self.HP = 500
        self.CharacterMoveSpeed = 150
        self.isBlock = True
        self.isKeyInput = True
        self.weapons = [
            self.weapon,
            Shotgun(self),
            SMG(self)
        ]
        self.Def_multiply = 0.5
        self.hp_ = self.HP

        self.ui_main = PlayerUI(self)
        self.ui_pause = MenuUI(self)
        self.ui = self.ui_main

    def update(self, dt):
        super().update(dt)

        mousepos = Vector2(0, 0)
        mousepos.x, mousepos.y = pygame.mouse.get_pos()

        lookat = Vector2.get_angle2(self.location, mousepos)
        self.angle = -lookat
        if self.mousepressed_ and \
                self.weapon.fire_mode == Weapon.FIRE_MODE_AUTO and \
            not self.weapon.isempty():
            self.weapon.fire(mousepos)

    def key_input(self, keys):
        pressed_r = False
        super().key_input(keys)
        if keys.right or keys.d:
            if keys.left or keys.a:
                self.moveInput.x = 0
            else:
                self.moveInput.x = 1

        if keys.left or keys.a:
            if keys.right or keys.d:
                self.moveInput.x = 0
            else:
                self.moveInput.x = -1

        if keys.up or keys.w:
            if keys.down or keys.s:
                self.moveInput.y = 0
            else:
                self.moveInput.y = 1

        if keys.down or keys.s:
            if keys.up or keys.w:
                self.moveInput.y = 0
            else:
                self.moveInput.y = -1

        if keys.r:
            if not pressed_r:
                self.weapon.reload()
            pressed_r = True
        else:
            pressed_r = False

        pressed_f = False
        if keys.f:
            if not pressed_f:
                pass
            pressed_f = True
        else:
            pressed_r = False

    def on_mouse_down(self, pos):
        super().on_mouse_down(pos)

        self.mousepressed_ = True
        mousepos = Vector2(pos[0], pos[1])
        if not self.world.get_pause():
            self.weapon.fire(mousepos)
            print(f"capacity: {self.weapon.capacity_}")
        pass

    def on_mouse_up(self, pos):
        super().on_mouse_up(pos)
        self.mousepressed_ = False
        pass

    def on_key_down(self, key):
        super().on_key_down(key)
        if key == pygame.K_ESCAPE:  # Escを押した時の挙動
            self.show_menu()
        if not self.world.get_pause():  # ワールドが一時停止状態でなければ
            c = chr(key)
            if c.isdecimal():
                i = int(c) - 1
                if 0 <= i <= 9:
                    self.swap_weapon(i)
                    self.Skins.set_skin(self)
                    pass

        pass

    def on_hit(self, actor):
        blt: Bullet = actor
        self.apply_damage(blt)

    def apply_damage(self, bullet: Bullet):
        self.hp_ -= Util.random_defenceddamage(bullet.damage, self.Def_multiply)
        self.hits_ += 1
        if self.hp_ <= 0:
            #self.visible = False
            gm: Game = self.world.owner
            gm.on_ended_game()

        pass

    # スコアを加点します(hp: 倒した敵のHP)
    def apply_score(self, hp):
        multply = random.uniform(1, self.score_max_multiply)  # ランダムな乗数を決める
        score = int(hp * multply)  # 決めた乗数でHPをかけた値がスコア
        if Util.random_bool(self.score_bonus_percent):  # ボーナスを一定の確率で適用する
            score = int(score * multply)
        self.score_ += score
        self.kills_ += 1
        print(self.score_)
        pass

    # プレイヤーのスコアデータを返します
    def get_scoredata(self):
        data_ = ScoreData()
        data_.playername = self.playername
        data_.score = int(self.score_)
        data_.kills = int(self.kills_)
        data_.hits = int(self.hits_)
        data_.playerhp = int((self.hp_ / self.HP) * 100)
        return data_

    # メニューの表示/非表示を切り替える
    def show_menu(self):
        if not self.world.get_pause():
            self.world.set_pause(True)
            self.swap_ui(self.ui_pause)
        else:
            self.world.set_pause(False)
            self.swap_ui(self.ui_main)
        pass

    # 武器を切り替える(インデックスが範囲外の場合は変化しない)
    def swap_weapon(self, index: int):
        if len(self.weapons) <= index:
            return
        self.weapon = self.weapons[index]
        pass


# 敵クラス
class Enemy(Character):
    IsLookAtTarget: bool = True
    FindDistance: float = 100  # 発見距離
    RefreshRate: float = 5  # 更新間隔
    target_: Pawn = None  # 現在の攻撃対象
    targets_ = []  # 発見したターゲット一覧
    ismoving_: bool = False  # 移動中かどうか
    moveto_: Vector2 = Vector2(0, 0)

    def __init__(self):
        self.Skins = EnemySkins()
        self.weapon = HandGun(self)
        self.weapon.fire_rate = 0.75
        self.Skins.set_skin(self)
        super().__init__(self.SkinPic)
        self.HP = 50
        self.Def_multiply = 0.5
        self.CharacterMoveSpeed = 0
        self.isBlock = False
        self.isKeyInput = False
        self.target_ = None
        self.hp_ = self.HP

        self.IsLookAtTarget = True
        self.FindDistance = 400
        self.target_ = None
        self.targets_ = []
        self.direction_ = Vector2(0, 0)


    # ワールド内のオブジェクトを探索し、自身から指定した半径内に含まれるプレイヤーを探します。
    def find(self):
        gm: Game = self.world.owner
        plyer: Player = gm.player
        dist = Vector2.get_distance(self.location, plyer.location)
        if dist <= self.FindDistance:
            self.target_ = plyer
        else:
            self.target_ = None
        pass

    # 攻撃対象が存在する場合はその方向を向く。
    def look_at_target(self):
        if not self.IsLookAtTarget:
            return
        if self.target_ != None:
            rot = Vector2.get_angle2(self.location, self.target_.location)
            self.angle = -rot

    # 所持している武器を発砲します
    def fire(self):
        if self.weapon.isempty():
            if not self.weapon.is_reloading_:
                self.weapon.reload()
        else:
            self.weapon.fire(self.target_.location)

    def update(self, dt):
        super().update(dt)
        self.find()
        self.look_at_target()
        if self.target_ != None:
            self.fire()
        self.location.x += self.moveInput.x * self.CharacterMoveSpeed
        self.location.y += self.moveInput.y * self.CharacterMoveSpeed
        pass

    def on_hit(self, actor):
        super().on_hit(actor)
        blt: Bullet = actor
        if type(blt.owner) is not Enemy:
            self.apply_damage(blt)

    def apply_damage(self, bullet: Bullet):
        super().apply_damage(bullet)
        dmg = Util.random_defenceddamage(bullet.damage, self.Def_multiply)
        self.hp_ -= dmg
        if self.hp_ <= 0:
            self.destroy()
            bullet.owner.apply_score(self.HP)
            gm: Game = self.world.owner
            gm.on_destroyed_enemy(self)

        print(f"Bullet: {bullet.damage}, Damage: {dmg}, Enemy_HP: {self.hp_}")


# ワールド内を構成するマップクラス
class Map:
    player: Player = None  # プレイヤー
    enemy_class = None  # 敵クラスオブジェクト
    world: World = None  # マップを生成するワールド
    ground_map: list = []  # 地面配置マップ
    ground_style_map: list = []  # 地面スタイルマップ
    ground_styles: list = []  # 地面スタイル一覧
    wallobj_map = []  # オブジェクト配置マップ
    wallobj_style_map = []  # オブジェクト種類マップ
    wallobj_styles = []  # オブジェクト一覧
    width_: float = 0  # マップの横幅
    height_: float = 0  # マップの縦
    size_: Vector2 = Vector2(10, 10)  # マップサイズ(タイル数)
    map_: list = []  # マップ内に配置されているオブジェクト一覧(地面)
    objs_: list = []  # マップ内に配置されているオブジェクト一覧(壁/障害物)
    center_: Vector2 = Vector2(0, 0)  # 画面の中心
    location_diff_: Vector2 = Vector2(0, 0) # 現在のマップの相対位置

    def __init__(self, world: World, player):
        self.world = world
        self.player = player
        self.enemy_class = Enemy
        self.center_.x = WIDTH / 2
        self.center_.y = HEIGHT / 2
        self.width_ = 0
        self.height_ = 0
        pass

    # マップ内の全オブジェクトを指定した方向だけ移動させます
    def move_map(self, locationdiff: Vector2):
        self.location_diff_ = Vector2.get_vector(locationdiff)
        for obj in self.world.Pawns:
            if type(obj) == Player:
                continue
            else:
                obj.location = obj.location + self.location_diff_
        pass

    # 指定したワールド位置に中心を持ってくる
    def set_tocenter(self, newlocation: Vector2):
        diff = Vector2(0, 0)
        diff = self.get_worldlocation(self.center_) - newlocation
        self.move_map(Vector2.get_vector(diff))
        pass

    # マップを生成します
    def generate(self):
        # 地面の生成と配置
        for y in range(0, self.size_.y):
            for x in range(0, self.size_.x):
                if self.ground_map[y][x] == G:
                    style = self.ground_styles[self.ground_style_map[y][x]]
                    ground = Ground(style)
                    ground.location.x = (ground.width * 0.5) + ground.width * x
                    ground.location.y = (ground.height * 0.5) + ground.height * y
                    ground.initiallocation = Vector2.get_vector(ground.location)
                    ground.spawn(self.world)
                    self.map_.append(ground)

        self.width_ = self.map_[0].width * self.size_.x
        self.height_ = self.map_[0].height * self.size_.y

        enemies = []

        # 物体の生成と配置
        for y in range(0, self.size_.y):
            for x in range(0, self.size_.x):
                obj_type = self.wallobj_map[y][x]
                obj: Wall = None
                objstyle: WallStyle = self.wallobj_styles[self.wallobj_style_map[y][x]]
                if obj_type == N:
                    continue
                if obj_type == U:
                    obj = Wall(objstyle.wall_up)
                    pass
                elif obj_type == D:
                    obj = Wall(objstyle.wall_down)
                    pass
                elif obj_type == L:
                    obj = Wall(objstyle.wall_left)
                    pass
                elif obj_type == R:
                    obj = Wall(objstyle.wall_right)
                    pass
                elif obj_type == JUL:
                    obj = Wall(objstyle.wall_joint_upleft)
                    pass
                elif obj_type == JUR:
                    obj = Wall(objstyle.wall_joint_upright)
                    pass
                elif obj_type == JDL:
                    obj = Wall(objstyle.wall_joint_downleft)
                    pass
                elif obj_type == JDR:
                    obj = Wall(objstyle.wall_joint_donwright)
                    pass
                elif obj_type == CUL:
                    obj = Wall(objstyle.wall_corner_upleft)
                    pass
                elif obj_type == CUR:
                    obj = Wall(objstyle.wall_corner_upright)
                    pass
                elif obj_type == CDL:
                    obj = Wall(objstyle.wall_corner_downleft)
                    pass
                elif obj_type == CDR:
                    obj = Wall(objstyle.wall_corner_downright)
                    pass
                elif obj_type == LR:
                    obj = Wall(objstyle.wall_lefttoright)
                    pass
                elif obj_type == UD:
                    obj = Wall(objstyle.wall_uptodown)
                    pass
                elif obj_type == JUDL:
                    obj = Wall(objstyle.wall_joint_uptodown_left)
                    pass
                elif obj_type == JUDR:
                    obj = Wall(objstyle.wall_joint_updodown_right)
                    pass
                elif obj_type == JLRU:
                    obj = Wall(objstyle.wall_joint_lefttoright_up)
                    pass
                elif obj_type == JLRD:
                    obj = Wall(objstyle.wall_joint_lefttoright_down)
                elif obj_type == P:
                    obj = Wall(objstyle.wall_pillar)
                    pass
                elif obj_type == E:
                    e = self.enemy_class()
                    e.location = Vector2(0, 0)
                    e.location.x = (self.map_[0].width * x) + self.map_[0].width * 0.5
                    e.location.y = (self.map_[0].height * y) + self.map_[0].height * 0.5
                    enemies.append(e)
                    continue
                    pass
                pass
                obj.location.x = (obj.width * x) + obj.width * 0.5
                obj.location.y = (obj.height * y) + obj.width * 0.5
                obj.initiallocation = Vector2.get_vector(obj.location)
                obj.spawn(self.world)
                self.objs_.append(obj)
                pass
            pass
        pass
        for e in enemies:
            e.spawn(self.world)
            gm: Game = self.world.owner
            gm.enemies.append(e)
    pass

    def update(self, dt):
        moveinput = self.player.moveInput
        diff = Vector2(0, 0)
        diff.x = -moveinput.x * self.player.CharacterMoveSpeed * dt
        diff.y = moveinput.y * self.player.CharacterMoveSpeed * dt
        playerpos = self.get_worldlocation(self.center_)
        if playerpos.x >= self.width_:
            self.move_map(-diff * 3)
            diff.x = 0
        if playerpos.x <= 0:
            self.move_map(-diff * 3)
            diff.x = 0
        if playerpos.y >= self.height_:
            self.move_map(-diff * 3)
            diff.y = 0
        if playerpos.y <= 0:
            self.move_map(-diff * 3)
            diff.y = 0
        self.move_map(diff)
        self.player.location = Vector2.get_vector(self.center_)
        pass

    # マップの原点を取得します
    def get_maporigin(self):
        map_origin = Vector2.get_vector(self.map_[0].location)
        map_origin.x = map_origin.x - (self.map_[0].width / 2)
        map_origin.y = map_origin.y - (self.map_[0].height / 2)
        return map_origin

    # 画面座標からワールド位置に変換します。
    def get_worldlocation(self, displaypos: Vector2):
        origin = self.get_maporigin()
        pos = Vector2(0, 0)
        pos.x = displaypos.x - origin.x
        pos.y = displaypos.y - origin.y
        return pos

    # マップ内でランダムな場所を返します
    def get_randomlocation_in_map(self):
        pos = Vector2(0, 0)
        pos.x = random.uniform(0, self.width_)
        pos.y = random.uniform(0, self.height_)
        return pos


# ゲームを実行/管理するクラス
class Game:
    sound_killed: pygame.mixer.Sound = None
    sound_finished: pygame.mixer.Sound = None
    sound_gameover: pygame.mixer.Sound = None
    volume: float = 1
    totalizer: Totalizer = None  # スコア集計オブジェクト
    enemies: list = []

    def __init__(self):
        self.sound_killed = sounds.sfx_killed
        self.sound_finished = sounds.sfx_finished
        self.sound_gameover = sounds.sfx_dead
        self.volume = 1.0
        self.enemies = []
        self.mapsize = Vector2(0, 0)
        self.groundmap= []
        self.groundstylemap = []
        self.groundstyles = []
        self.wallmap = []
        self.wallstylemap = []
        self.wallstyles = []
        self.world: World = None
        self.map: Map = None
        self.player: Player = None
        self.enemy: Enemy = None
        self.enemy2: Enemy = None
        self.isloading: bool = False
        self.totalizer = Totalizer()
        pass

    def initialize(self):
        self.isloading = True
        self.mapsize = Vector2(30, 15)  # マップサイズ
        self.groundmap = [  # 地面オブジェクトの配置
            [G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G],
            [G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G],
            [G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G],
            [G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G],
            [G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G],
            [G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G],
            [G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G],
            [G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G],
            [G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G],
            [G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G],
            [G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G],
            [G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G],
            [G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G],
            [G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G],
            [G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G]
        ]
        self.groundstylemap = [  # 地面のスタイル割り当て
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        self.groundstyles = [  # 割り当てと使用する地面画像一覧
            "tile_01",
            "tile_05",
            "tile_42"
        ]
        self.wallmap = [  # 壁障害物の配置
            [N   , N   , N   , N   , N   , N   , N   , N   , N   , N   , N   , N   , N   , N   , N   , N   , N   , E   , N   , N   , N   , N   , N   , N   , N   , N   , N   , N   , N   , N   ],
            [N   , N   , N   , E   , L   , R   , N   , U   , CUL , CUR , E   , N   , N   , N   , E   , N   , N   , JUL , LR  , LR  , LR  , LR  , JUR , N   , N   , N   , N   , N   , N   , N   ],
            [N   , N   , N   , N   , N   , N   , N   , D   , CDL , CDR , N   , N   , N   , N   , N   , N   , N   , UD  , N   , N   , N   , N   , UD  , N   , N   , N   , N   , N   , E   , N   ],
            [N   , N   , N   , N   , N   , N   , N   , N   , N   , N   , N   , N   , N   , N   , N   , N   , N   , UD  , N   , N   , E   , N   , UD  , N   , N   , N   , N   , E   , N   , E   ],
            [N   , N   , N   , N   , N   , N   , N   , N   , N   , N   , N   , N   , N   , N   , N   , N   , N   , UD  , N   , L   , R   , N   , D   , N   , N   , N   , N   , N   , E   , N   ],
            [N   , L   , R   , L   , R   , N   , N   , N   , N   , E   , L   , LR  , LR  , JUR , N   , N   , N   , UD  , N   , N   , N   , N   , N   , E   , N   , N   , N   , N   , N   , N   ],
            [N   , N   , N   , N   , N   , N   , N   , N   , N   , N   , N   , N   , N   , D   , N   , N   , N   , UD  , N   , N   , N   , N   , P   , N   , N   , N   , N   , N   , N   , N   ],
            [N   , N   , N   , N   , N   , N   , N   , N   , N   , N   , U   , N   , N   , N   , N   , N   , N   , D   , N   , N   , N   , N   , N   , N   , E   , N   , N   , N   , N   , N   ],
            [N   , N   , N   , N   , N   , N   , JUL , LR  , LR  , LR  , JUDL, N   , N   , U   , N   , N   , N   , N   , N   , N   , E   , N   , U   , N   , N   , N   , N   , N   , N   , N   ],
            [N   , N   , N   , N   , N   , N   , D   , N   , N   , N   , JDL , R   , N   , D   , N   , N   , N   , U   , N   , N   , N   , N   , UD  , N   , N   , N   , N   , N   , N   , N   ],
            [N   , N   , N   , N   , N   , N   , N   , N   , N   , N   , N   , N   , N   , N   , N   , N   , U   , JDL , LR  , LR  , LR  , LR  , JDR , N   , N   , N   , N   , N   , N   , N   ],
            [N   , N   , N   , N   , N   , N   , N   , N   , N   , N   , N   , N   , N   , P   , N   , N   , UD  , N   , N   , N   , N   , N   , N   , N   , U   , N   , N   , N   , N   , N   ],
            [N   , N   , N   , N   , N   , N   , U   , N   , N   , N   , N   , N   , N   , E   , N   , N   , UD  , N   , N   , N   , N   , N   , N   , N   , UD  , N   , N   , N   , N   , N   ],
            [N   , N   , N   , N   , N   , N   , JDL , LR  , LR  , LR  , LR  , LR  , LR  , R   , N   , N   , D   , N   , N   , N   , N   , N   , N   , N   , D   , N   , N   , N   , N   , N   ],
            [N   , N   , N   , N   , N   , N   , N   , N   , N   , N   , N   , N   , N   , N   , N   , N   , N   , N   , N   , N   , N   , N   , N   , N   , E   , N   , N   , N   , N   , N   ]
        ]
        self.wallstylemap = [  # 壁障害物の種類の割り当て
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]
        ]
        self.wallstyles = [  # 割り当てとその使用する種類
            WallStyleOrange(),
            WallStyleWood()
        ]

        self.world = World(self)
        self.player = Player()
        self.map = Map(self.world, self.player)
        self.map.size_ = self.mapsize
        self.map.ground_map = self.groundmap
        self.map.ground_style_map = self.groundstylemap
        self.map.ground_styles = self.groundstyles
        self.map.wallobj_map = self.wallmap
        self.map.wallobj_style_map = self.wallstylemap
        self.map.wallobj_styles = self.wallstyles
        self.map.generate()
        print(f"width: {self.map.width_}, height: {self.map.height_}")
        self.world.set_map(self.map)

        self.player.location = Vector2.get_vector(self.map.center_)
        self.enemy = Enemy()
        self.enemy2 = Enemy()
        self.enemy.location = Vector2(150, 150)
        self.enemy2.location = Vector2(400, 150)
        self.enemy.spawn(self.world)
        self.enemy2.spawn(self.world)
        self.player.spawn(self.world)
        self.enemies.append(self.enemy)
        self.enemies.append(self.enemy2)
        self.map.set_tocenter(Vector2(10, 800))
        self.isloading = False
        self.player.swap_ui(PlayerNameUI(self.player))
        self.world.set_pause(True)
        pass

    def draw(self):
        screen.clear()
        if not self.isloading:
            self.world.draw()
        pass

    def update(self, dt):
        if not self.isloading:
            self.world.update(dt)
        pass

    def on_mouse_down(self, pos):
        if not self.isloading:
            self.world.on_mousedown_input(pos)
        pass

    def on_mouse_up(self, pos):
        if not self.isloading:
            self.world.on_mouseup_input(pos)
        pass

    def on_key_down(self, key):
        if not self.isloading:
            self.world.on_key_down(key)
        pass

    def on_key_up(self, key):
        if not self.isloading:
            self.world.on_key_up(key)
        pass

    def get_playerrank(self):
        return self.totalizer.get_rank(self.player.playername)

    def on_ended_game(self, asfinish=False):
        data_ = self.player.get_scoredata()
        datas_ = self.totalizer
        datas_.input("scores.txt")
        datas_.add_scoredata(data_)
        datas_.output_scores("scores.txt")
        self.player.swap_ui(ResultUI(self.player, asfinish))
        self.world.set_pause(True)
        if asfinish:
            self.sound_finished.set_volume(self.volume)
            self.sound_finished.play()
            pass
        else:
            self.sound_gameover.set_volume(self.volume)
            self.sound_gameover.play()
            pass
        pass

    # 敵が撃破された際に呼ばれる
    def on_destroyed_enemy(self, enemy: Enemy):
        if enemy in self.enemies:
            self.enemies.remove(enemy)
            self.sound_killed.set_volume(self.volume)
            self.sound_killed.play()
        if len(self.enemies) <= 0:
            self.on_ended_game(asfinish=True)
        pass


game = Game()  # ゲームインスタンス
game.initialize()  # 初期化


def draw():
    game.draw()
    pass


def update(dt):
    game.update(dt)
    pass


def on_mouse_down(pos):
    game.on_mouse_down(pos)
    pass


def on_mouse_up(pos):
    game.on_mouse_up(pos)
    pass


def on_key_down(key):
    game.on_key_down(key)
    pass


def on_key_up(key):
    game.on_key_up(key)
    pass


pgzrun.go()
