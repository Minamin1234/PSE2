# HT21A099 南　李玖
import math
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


# ゲーム内全てのオブジェクトを管理するためのクラス
class World:
    Pawns = []  # ワールド内のオブジェクト
    Map = None  # ワールドのマップ

    def __init__(self):
        pass

    # ワールド内全てのオブジェクトとマップを更新します
    def update(self, dt):
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
            p.mouse_down_input(pos)

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


# UIの定義したクラス
class UI:
    owner = None
    center_: Vector2 = Vector2(0, 0)

    def __init__(self, owner):
        self.owner = owner
        self.center_ = Vector2(0, 0)
        self.center_.x = WIDTH / 2
        self.center_.y = HEIGHT / 2
        pass

    def draw(self):
        pass


# UI内の要素クラス
class UIElement:
    owner: UI = None  # 所有者(UIクラス)
    pos: Vector2 = Vector2(0, 0)  # 位置
    use_percentpos: bool = False  # 位置を画面サイズの比で指定するかどうか
    size: Vector2 = Vector2(0, 0)  # 要素のサイズ
    pos_: Vector2 = Vector2(0, 0)  # 配置時のサイズ

    def __init__(self, owner: UI):
        self.owner = owner
        if self.use_percentpos:  # 画面サイズの比で指定する場合
            self.pos_ = self.get_percentpos()  # 配置位置を求める
        else:  # 画面座標で指定する場合
            self.pos_ = Vector2.get_vector(self.pos)
        pass

    def draw(self):
        if self.use_percentpos:
            self.pos_ = self.get_percentpos()
        else:
            self.pos_ = Vector2.get_vector(self.pos)
        pass

    # 画面サイズの比から位置を求める
    def get_percentpos(self):
        pos = Vector2(0, 0)
        pos.x = WIDTH * self.pos.x
        pos.y = HEIGHT * self.pos.y
        return pos


# UI要素クラスを継承したUI内テキストクラス
class UIText(UIElement):
    content: str = ""
    fontsize: int = 32

    def __init__(self, owner: UI):
        super().__init__(owner)
        self.content = ""
        self.fontsize = 32

    def draw(self):
        super().draw()
        screen.draw.text(self.content, Vector2.get_tuple(self.pos_), fontsize=self.fontsize)


# UI要素クラスを継承した進捗バークラス
class UIProgressBar(UIElement):
    percent: float = 1.0  # 進捗率(1.0で満たされ、0.0は何もなし)
    filledcolor: ColorRGB = ColorRGB(0, 0, 0)  # 進捗が満たされた状態のカラー
    backgroundcolor: ColorRGB = ColorRGB(0, 0, 0)  # 進捗が満たレテいない状態(背景)のカラー

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

    def __init__(self, owner: UI):
        super().__init__(owner)
        self.bullets_UIText_ = UIText(owner)
        self.bullets_UIText_.content = f"{self.bullets}"
        self.percent = 1.0
        self.bullets_UIText_.use_percentpos = False

        pass

    def draw(self):
        super().draw()
        pos = Vector2(0, 0)
        pos.x = self.pos_.x + self.size.x + self.bullets_textpos_relative.x
        pos.y = self.pos_.y + self.bullets_textpos_relative.y
        self.bullets_UIText_.content = f"{self.bullets}"
        self.bullets_UIText_.pos = pos
        self.bullets_UIText_.draw()
        me: Player = self.owner.owner
        interval = self.size.x / me.weapon.capacity
        for i in range(0, me.weapon.capacity - 1):
            pos = Vector2(0, 0)
            pos.x = self.pos_.x + (interval * i)
            pos.y = self.pos_.y
            size = Vector2(0, 0)
            size.x = interval
            size.y = self.size.y
            rect = Rect(Vector2.get_tuple(pos),
                        Vector2.get_tuple(size))
            pygame.draw.rect(screen.surface, (0, 0, 0), rect, width=1)
            print(size)
        # pygame.draw.rect(screen.surface,(0, 0, 0), Rect((0, 0), (10, 10)), width=2)


# プレイヤーのUI
class PlayerUI(UI):
    hpbar: UIHPBar = None  # HPバー要素
    bulletguage: UIBulletGauge = None  # 残弾数ゲージ要素

    def __init__(self, owner):
        super().__init__(owner)
        me: Player = self.owner

        # HPバー要素
        self.hpbar = UIHPBar(self)
        self.hpbar.hp = 100
        self.hpbar.percent = 1.0
        self.hpbar.backgroundcolor = ColorRGB(150, 150, 150)  # HPが満たされていない状態のカラー(背景のカラー)
        self.hpbar.filledcolor = ColorRGB(0, 240, 140)  # HPが満たされた状態のカラー
        self.hpbar.pos = Vector2(0.05, 0.9)
        self.hpbar.use_percentpos = True
        self.hpbar.size = Vector2(450, 30)
        self.hpbar.hp_text_pos_relative = Vector2(10, 0)
        self.hpbar.hp_UItext_.fontsize = 52

        # 残弾数ゲージ要素
        self.bulletgauge = UIBulletGauge(self)
        self.bulletgauge.bullets = me.weapon.capacity
        self.bulletgauge.percent = 1.0
        self.bulletgauge.backgroundcolor = ColorRGB(150, 150, 150)
        self.bulletgauge.filledcolor = ColorRGB(230, 210, 30)
        self.bulletgauge.pos = Vector2(0.8, 0.9)
        self.bulletgauge.use_percentpos = True
        self.bulletgauge.size = Vector2(100, 20)
        self.bulletgauge.bullets_textpos_relative = Vector2(10, 0)
        self.bulletgauge.bullets_UIText_.fontsize = 32

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
        pass


# ゲーム内で配置/移動可能なオブジェクトクラス
class Pawn(Actor):
    LEFT = 0  # 左
    RIGHT = 1  # 右
    UP = 2  # 上
    DOWN = 3  # 下
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
        self.location = Vector2(self.x, self.y)
        self.moveInput = Vector2(0, 0)

    # 指定したワールドに出現させます
    def spawn(self, world: World):
        self.world = world
        world.addto_world(self)

    # ワールドから取り除きます(オブジェクトの破棄は行われません)
    def destroy(self):
        self.world.delete_pawn(self)

    # 更新処理
    def update(self, dt):
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

    # マウスのボタンクリックされた際の処理
    def mouse_down_input(self, pos):
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
        self.velocity = 30.0
        self.owner = owner

    # 飛翔方向を設定します
    def set_direction(self, direction: Vector2):
        self.direction = direction
        pass

    def bounce(self):
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

        self.location.x += self.direction.x * self.velocity
        self.location.y += self.direction.y * self.velocity


# ショットガン用の弾
class ShotShell(Bullet):

    def __init__(self, owner: Pawn):
        super().__init__(owner)
        self.velocity = 20
        self.owner = owner
        pass


# 武器クラス
class Weapon:
    owner: Pawn = None  # 所有者
    bullet: Bullet = None  # 発射する弾
    sound_fire: str = ""  # 発砲音
    sound_reload: str = ""  # 装填音
    sound_empty: str = ""  # 空撃ち音
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

    def __init__(self, owner: Pawn):
        self.fire_mode = self.FIRE_MODE_SINGLE
        self.owner = owner
        self.capacity_ = self.capacity
        self.is_ready = True
        pass

    # 弾を発射する
    def fire(self, at: Vector2):
        if not self.is_reloading_:  # 装填中でなければ
            if self.capacity_ > 0:  # 弾が残っていれば
                if self.is_ready:  # 武器が発射可能であれば
                    blt = Bullet(self.owner)  # 弾オブジェクトの生成
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
                    sounds.handgun_shot.play()  # 発砲音を鳴らす
                    self.is_ready = False
                    clock.schedule_unique(self.on_after_fire, self.fire_rate)
                pass
            else:  # 弾が残っていない時
                sounds.handgun_empty.play()  # 空撃ち音を鳴らす
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
            sounds.handgun_reload.play()  # 装填音を鳴らす
            clock.schedule_unique(self.on_ended_reload, self.reload_time)  # 装填時間分遅らせて装填完了処理を呼ぶ
        pass

    # 装填が完了した際に呼ばれる
    def on_ended_reload(self):
        print("Reloaded")
        sounds.handgun_slide.play()  # 銃スライド音を鳴らす
        self.capacity_ = self.capacity  # 現在の装填数を補充する
        self.is_reloading_ = False  # 装填中であるかどうかを設定する

    # 発射後一定の発射速度に達したあとに呼ばれる
    def on_after_fire(self):
        self.is_ready = True


# ハンドガン
class HandGun(Weapon):

    def __init__(self, owner: Pawn):
        super().__init__(owner)
        self.capacity = 6
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
        self.fire_rate = 0.15
        self.reload_time = 3.0
        self.diffusion = 0.5
        self.max_diffangle = 20
        self.fire_mode = self.FIRE_MODE_SINGLE
        pass

    def fire(self, at: Vector2):
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
        pass

    def fire(self, at: Vector2):
        if not self.is_reloading_:
            if self.capacity_ > 0:
                shotangle = self.shotdiffangle / (self.shells - 1)  # 拡散させる角度(弾毎に角度をつける)
                shotangle_ = -shotangle  # 負の角度から扇状に拡散させる
                if self.is_ready:
                    for i in range(self.shells):  # 弾の数だけ繰り返す
                        blt = ShotShell(self.owner)
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

    def reload(self):
        if not self.is_reloading_:
            self.is_reloading_ = True
            sounds.shotgun_reload.play()
            clock.schedule_unique(self.on_ended_reload, self.reload_time)
            pass

    def on_ended_reload(self):
        sounds.shotgun_pump.play()
        self.capacity_ = self.capacity
        self.is_reloading_ = False


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
    wall_up = ""
    wall_down = ""
    wall_left = ""
    wall_right = ""
    wall_corner_upleft = ""
    wall_corner_upright = ""
    wall_corner_downleft = ""
    wall_corner_downright = ""
    wall_joint_upleft = ""
    wall_joint_upright = ""
    wall_joint_downleft = ""
    wall_joint_donwright = ""

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


# プレイヤー/敵共通のキャラクタークラス
class Character(Pawn):
    SkinPic: str = ""  # 外見の画像
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



    def mouse_down_input(self, pos):
        pass

    # オブジェクト同士で衝突があった時に呼ばれる
    def on_hit(self, actor):
        pass

    # 弾によるダメージが適用される際に呼ばれる
    def apply_damage(self, bullet: Bullet):
        pass
    
    def key_input(self, keys):
        super().key_input(keys)


# プレイヤー
class Player(Character):

    def __init__(self):
        self.SkinPic = "manblue_gun"  # 画像とActorは90度ずれている
        super().__init__(self.SkinPic)
        self.HP = 500
        self.CharacterMoveSpeed = 5
        self.isBlock = True
        self.isKeyInput = True
        self.weapon = Shotgun(self)
        self.Def_multiply = 0.5
        self.hp_ = self.HP

        self.ui = PlayerUI(self)

    def update(self, dt):
        super().update(dt)

        mousepos = Vector2(0, 0)
        mousepos.x, mousepos.y = pygame.mouse.get_pos()

        lookat = Vector2.get_angle2(self.location, mousepos)
        self.angle = -lookat

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
            print("f")
            self.world.Map.set_tocenter(Vector2(100, 100))
            pressed_f = True
        else:
            pressed_r = False


    def mouse_down_input(self, pos):
        super().mouse_down_input(pos)
        mousepos = Vector2(pos[0], pos[1])
        """print("Pawns(Before):")
        for i in self.world.Pawns:
            print(i)"""
        self.weapon.fire(mousepos)
        """print("Pawns(After):")
        for i in self.world.Pawns:
            print(i)"""
        print(f"capacity: {self.weapon.capacity_}")

    def on_hit(self, actor):
        blt: Bullet = actor
        self.apply_damage(blt)

    def apply_damage(self, bullet: Bullet):
        self.hp_ -= Util.random_defenceddamage(bullet.damage, self.Def_multiply)
        if self.hp_ <= 0:
            self.destroy()

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
        self.SkinPic = "manbrown_gun"
        super().__init__(self.SkinPic)
        self.HP = 50
        self.Def_multiply = 0.5
        self.CharacterMoveSpeed = 5
        self.weapon = HandGun(self)
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
        # ワールド内のオブジェクトを探索し、自分の半径内に含まれるプレイヤーを抜き出す
        for p in self.world.Pawns:
            if type(p) is Player:
                distance = Vector2.get_distance(self.location, p.location)
                if distance <= self.FindDistance:
                    self.targets_.append(p)
                else:
                    if p in self.targets_:
                        self.targets_.remove(p)
        if self.targets_ == []:
            self.target_ = None
            return
        # 作成したターゲットリストについて、それぞれの距離を求めてリストにする
        dists: list[float] = []
        for p in self.targets_:
            dist = Vector2.get_distance(self.location, p.location)
            dists.append(dist)
        # 距離のリストから最短のものを求めて最も近くにあるオブジェクトを抜き出す
        mn = dists[0]
        mnidx = 0
        for i, dist in enumerate(dists):
            if mn >= dist:
                mn = dist
                mnidx = i
        self.target_ = self.targets_[mnidx]
        pass

    # 攻撃対象が存在する場合はその方向を向く。
    def look_at_target(self):
        if not self.IsLookAtTarget:
            return
        if self.target_ != None:
            rot = Vector2.get_angle2(self.location, self.target_.location)
            self.angle = -rot

    def moveto(self):
        if not self.ismoving_:
            self.ismoving_ = True
            self.moveto_ = self.world.Map.get_randomlocation_in_map()
            direction = Vector2.get_direction(self.world.Map.get_worldlocation(self.location), self.moveto_)
            self.direction_ = Vector2.get_vector(direction)
            clock.schedule_unique(self.on_ended_move, self.RefreshRate)
            print(f"RandomPos: {self.moveto_}")
            pass
        else:
            dir = Vector2.get_direction(self.world.Map.get_worldlocation(self.location), self.moveto_)
            self.moveInput = Vector2.get_vector(dir)
        pass

    def on_ended_move(self):
        self.ismoving_ = False
        self.direction_ = Vector2(0, 0)
        pass

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
        self.apply_damage(blt)

    def apply_damage(self, bullet: Bullet):
        super().apply_damage(bullet)
        dmg = Util.random_defenceddamage(bullet.damage, self.Def_multiply)
        self.hp_ -= dmg
        if self.hp_ <= 0:
            self.destroy()
        print(f"Bullet: {bullet.damage}, Damage: {dmg}, Enemy_HP: {self.hp_}")


# ワールド内を構成するマップクラス
class Map:
    player: Player = None  # プレイヤー
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

        # 物体の生成と配置
        for y in range(0, self.size_.y):
            for x in range(0, self.size_.x):
                obj_type = self.wallobj_map[y][x]
                obj: Wall = None
                objstyle = self.wallobj_styles[self.wallobj_style_map[y][x]]
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
                pass
                obj.location.x = obj.width * x
                obj.location.y = obj.height * y
                obj.initiallocation = Vector2.get_vector(obj.location)
                obj.spawn(self.world)
                self.objs_.append(obj)

    def update(self, dt):
        moveinput = self.player.moveInput
        diff = Vector2(0, 0)
        diff.x = -moveinput.x * self.player.CharacterMoveSpeed
        diff.y = moveinput.y * self.player.CharacterMoveSpeed
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
        #print(pos)
        return pos

# マップサイズ
mapsize = Vector2(15, 15)

# 地面オブジェクトの配置
groundmap = [
    [G, G, G, G, G, G, G, G, G, G, G, G, G, G, G],
    [G, G, G, G, G, G, G, G, G, G, G, G, G, G, G],
    [G, G, G, G, G, G, G, G, G, G, G, G, G, G, G],
    [G, G, G, G, G, G, G, G, G, G, G, G, G, G, G],
    [G, G, G, G, G, G, G, G, G, G, G, G, G, G, G],
    [G, G, G, G, G, G, G, G, G, G, G, G, G, G, G],
    [G, G, G, G, G, G, G, G, G, G, G, G, G, G, G],
    [G, G, G, G, G, G, G, G, G, G, G, G, G, G, G],
    [G, G, G, G, G, G, G, G, G, G, G, G, G, G, G],
    [G, G, G, G, G, G, G, G, G, G, G, G, G, G, G],
    [G, G, G, G, G, G, G, G, G, G, G, G, G, G, G],
    [G, G, G, G, G, G, G, G, G, G, G, G, G, G, G],
    [G, G, G, G, G, G, G, G, G, G, G, G, G, G, G],
    [G, G, G, G, G, G, G, G, G, G, G, G, G, G, G],
    [G, G, G, G, G, G, G, G, G, G, G, G, G, G, G],
]

# 地面のスタイル割り当て
groundstylemap = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

# 割り当てと使用する地面画像一覧
groundstyles = [
    "tile_01",
    "tile_05"
]

# 壁障害物の配置
wallmap = [
    [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N],
    [N, N, N, N, L, R, N, U, CUL, CUR, N, N, N, N, N],
    [N, N, N, N, N, N, N, D, CDL, CDR, N, N, N, N, N],
    [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N],
    [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N],
    [N, L, R, L, R, N, N, N, N, N, N, N, N, N, N],
    [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N],
    [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N],
    [N, N, N, N, N, N, N, N, N, N, N, N, U, N, N],
    [N, N, N, N, N, N, N, N, N, N, N, N, D, N, N],
    [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N],
    [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N],
    [N, N, N, N, N, N, N, N, N, N, N, N, U, N, N],
    [N, N, N, N, N, N, N, N, N, N, N, N, D, N, N],
    [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
]

# 壁障害物の種類の割り当て
wallstylemap = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

# 割り当てとその使用する種類
wallstyles = [
    WallStyleOrange()
]

world = World()
player = Player()

mp = Map(world, player)
mp.size_ = mapsize
mp.ground_map = groundmap
mp.ground_style_map = groundstylemap
mp.ground_styles = groundstyles
mp.wallobj_map = wallmap
mp.wallobj_style_map = wallstylemap
mp.wallobj_styles = wallstyles
mp.generate()
print(f"width: {mp.width_}, height: {mp.height_}")
world.set_map(mp)

player.location = Vector2.get_vector(mp.center_)
enemy = Enemy()
enemy.location = Vector2(150, 150)
enemy.spawn(world)
player.spawn(world)
mp.set_tocenter(Vector2(10, 800))


def draw():
    screen.clear()
    world.draw()
    pass


def update(dt):
    world.update(dt)
    pass


def on_mouse_down(pos):
    world.on_mousedown_input(pos)
    pass


pgzrun.go()
