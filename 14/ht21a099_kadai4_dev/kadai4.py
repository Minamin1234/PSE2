# HT21A099 南　李玖
import math
import random

import pygame.mouse
from pse2pgzrun import *  # type: ignore

WIDTH = 750
HEIGHT = 750

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


# 二次元ベクトルを表すクラス
class Vector2:
    x: float = 0.0
    y: float = 0.0

    def get_vector(v):
        return Vector2(v.x, v.y)

    def __init__(self, x: float, y: float):
        self.x, self.y = x, y

    def __neg__(self):
        v = Vector2(-self.x, -self.y)
        return v

    def __mul__(self, other):
        v = Vector2(self.x * other, self.y * other)
        return v

    def __iadd__(self, other):
        v = Vector2(self.x + other.x, self.y + other.y)
        return v

    def __str__(self):
        return f"({self.x}, {self.y})"

    # 2点間の距離の二乗を返します
    def get_distance2(a, b):
        x = b.x - a.x
        y = b.y - a.y
        return x**2 + y**2

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
    Pawns = []

    def __init__(self):
        pass

    # ワールド内全てのオブジェクトを更新します
    def update(self, dt):
        for p in self.Pawns:
            p.update(dt)

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

    def __init__(self, pic_name):
        super().__init__(pic_name)
        self.location = Vector2(self.x, self.y)

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
        self.isBlock = True
        self.isKeyInput = False
        self.is_bounce = True
        self.bounces = 2
        self.velocity = 30.0
        self.owner = owner

    # 飛翔方向を設定します
    def set_direction(self, direction: Vector2):
        self.direction = direction
        pass

    def update(self, dt):
        super().update(dt)

        if self.is_collide_wall():
            if self.hit_once:
                self.destroy()
            if self.is_bounce:
                if self.bounces_ >= self.bounces:
                    self.destroy()
                self.bounces_ += 1

        if self.collide[self.LEFT] or self.collide[self.RIGHT]:
            self.direction.x = -self.direction.x
        if self.collide[self.UP] or self.collide[self.DOWN]:
            self.direction.y = -self.direction.y
        hits = self.is_hit()
        for p in hits:
            if p != self.owner and type(p) is not StaticObject:
                p.on_hit(self)
                if self.hit_once:
                    self.destroy()

        self.location.x += self.direction.x * self.velocity
        self.location.y += self.direction.y * self.velocity




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

    def __init__(self, owner: Pawn):
        self.fire_mode = self.FIRE_MODE_SINGLE
        self.owner = owner
        self.capacity_ = self.capacity
        pass

    # 弾を発射する
    def fire(self, at: Vector2):
        if not self.is_reloading_:  # 装填中でなければ
            if self.capacity_ > 0:  # 弾が残っていれば
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
                pass
            else:  # 弾が残っていない時
                sounds.handgun_empty.play()  # 空撃ち音を鳴らす
            pass
        pass

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


class HandGun(Weapon):

    def __init__(self, owner: Pawn):
        super().__init__(owner)
        self.capacity = 6
        self.capacity_ = self.capacity
        self.fire_rate = 0.5
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


# ゲーム内に配置可能な静的オブジェクト
class StaticObject(Pawn):
    Pic: str = ""

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
class Floor(StaticObject):
    def __init__(self):
        self.Pic = ""
        super().__init__(self.Pic)


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


class Map:
    world: World = None  # マップを生成するワールド
    ground_map: list = []  # 地面配置マップ
    ground_style_map: list = []  # 地面スタイルマップ
    ground_styles: list = []  # 地面スタイル一覧
    wallobj_map: list[list[Wall]] = []  # オブジェクト配置マップ
    wallobj_style_map: list[list[int]] = []  # オブジェクト種類マップ
    wallobj_styles: list[WallStyle] = []  # オブジェクト一覧
    size_: Vector2 = Vector2(10, 10)  # マップサイズ
    map_: list = []

    def __init__(self, world: World):
        self.world = world
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
                    print(ground.location)
                    ground.spawn(self.world)

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
                obj.spawn(self.world)

        """
        for y in range(0, self.size_.y):
            for x in range(0, self.size_.x):
                g = Ground()
                g.location.x = g.width * x
                g.location.y = g.height * y
                print(g.location)
                g.spawn(self.world)
                self.map_.append(g)
        """


# プレイヤー/敵共通のキャラクタークラス
class Character(Pawn):
    SkinPic: str = ""  # 外見の画像
    HP = 100  # 最大ヒットポイント
    Def_multiply: float = 0.0  # 防御乗数(ダメージの軽減率)
    CharacterMoveSpeed = 5  # キャラクターの移動速度
    weapon: Weapon = None  # キャラクターの所持している武器
    hp_ = 0  # 現在のHP

    def __init__(self, pic_name: str):
        super().__init__(self.SkinPic)
        pass

    def update(self, dt):
        super().update(dt)
        self.location.x += self.moveInput.x * self.CharacterMoveSpeed
        self.location.y += self.moveInput.y * -self.CharacterMoveSpeed

    def mouse_down_input(self, pos):
        pass

    def on_hit(self, actor):
        pass

    def apply_damage(self, bullet: Bullet):
        pass
    
    def key_input(self, keys):
        super().key_input(keys)


# プレイヤー
class Player(Character):

    def __init__(self):
        self.SkinPic = "manblue_gun"  # 画像とActorは90度ずれている
        super().__init__(self.SkinPic)
        self.HP = 100
        self.CharacterMoveSpeed = 5
        self.isBlock = True
        self.isKeyInput = True
        self.weapon = HandGun(self)
        self.Def_multiply = 0.5
        self.hp_ = self.HP

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
            self.moveInput.x = 1
        if keys.left or keys.a:
            self.moveInput.x = -1
        if keys.up or keys.w:
            self.moveInput.y = 1
        if keys.down or keys.s:
            self.moveInput.y = -1

        if keys.r:
            if not pressed_r:
                self.weapon.reload()
            pressed_r = True
        else:
            pressed_r = False

    def mouse_down_input(self, pos):
        super().mouse_down_input(pos)
        mousepos = Vector2(pos[0], pos[1])
        self.weapon.fire(mousepos)
        print(f"capacity: {self.weapon.capacity_}")

    def on_hit(self, actor):
        blt: Bullet = actor
        self.apply_damage(blt)

    def apply_damage(self, bullet: Bullet):
        self.hp_ -= Util.random_defenceddamage(bullet.damagem, self.Def_multiply)
        if self.hp_ <= 0:
            self.destroy()

        pass


# 敵クラス
class Enemy(Character):
    IsLookAtTarget: bool = True
    target_: Pawn = None

    def __init__(self):
        self.SkinPic = "manbrown_gun"
        super().__init__(self.SkinPic)
        self.HP = 50
        self.Def_multiply = 0.5
        self.CharacterMoveSpeed = 5
        self.weapon = None
        self.isBlock = True
        self.isKeyInput = False
        self.target_ = None
        self.hp_ = self.HP

    def update(self, dt):
        super().update(dt)
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

groundstyles = [
    "tile_01",
    "tile_05"
]

wallmap = [
    [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N],
    [N, N, N, N, L, R, N, U, CUL, CUR, N, N, N, N, N],
    [N, N, N, N, N, N, N, D, CDL, CDR, N, N, N, N, N],
    [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N],
    [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N],
    [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N],
    [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N],
    [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N],
    [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N],
    [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N],
    [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N],
    [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N],
    [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N],
    [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N],
    [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N]
]

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

wallstyles = [
    WallStyleOrange()
]

world = World()
mp = Map(world)
mp.size_ = Vector2(15, 15)
mp.ground_map = groundmap
mp.ground_style_map = groundstylemap
mp.ground_styles = groundstyles
mp.wallobj_map = wallmap
mp.wallobj_style_map = wallstylemap
mp.wallobj_styles = wallstyles
mp.generate()
player = Player()
enemy = Enemy()
enemy.location = Vector2(150, 150)
player.spawn(world)
enemy.spawn(world)
"""
for i in range(0, 600, 60):
    e = Enemy()
    e.location.x = i
    e.spawn(world)
"""

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
