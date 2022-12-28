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

    def __str__(self):
        return f"({self.x}, {self.y})"

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
        v.y = v1.y * math.cos(rad) - v1.y * math.cos(rad)
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
    pic: str = "ball_blue_small_2"  # 弾の画像
    damage = 15
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
            if p != self.owner:
                p.on_hit(self)
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
        if not self.is_reloading_:
            if self.capacity_ > 0:
                blt = Bullet(self.owner)
                blt.damage = Util.random_damage(self.damage, self.damage_multiply)
                blt.spawn(self.owner.world)
                blt.location = Vector2.get_vector(self.owner.location)
                direction = Vector2.get_angle2(self.owner.location, at)
                direction = Vector2.get_direction_fromdeg(direction - 90)
                blt.set_direction(direction)
                self.capacity_ -= 1
                sounds.handgun_shot.play()
                pass
            else:
                sounds.handgun_empty.play()
            pass
        pass

    # 弾の装填を行う
    def reload(self):
        if not self.is_reloading_:
            self.is_reloading_ = True
            sounds.handgun_reload.play()
            clock.schedule_unique(self.on_ended_reload, self.reload_time)
        pass

    # 装填が完了した際に呼ばれる
    def on_ended_reload(self):
        print("Reloaded")
        sounds.handgun_slide.play()
        self.capacity_ = self.capacity
        self.is_reloading_ = False


class HandGun(Weapon):

    def __init__(self, owner: Pawn):
        super().__init__(owner)
        self.capacity = 6
        self.capacity_ = self.capacity
        self.fire_rate = 0.5
        self.reload_time = 2.0
        self.diffusion = 0.1
        self.fire_mode = self.FIRE_MODE_SINGLE
        pass

    def fire(self, at: Vector2):
        super().fire(at)
        
    def reload(self):
        super().reload()
        return self


class Character(Pawn):
    SkinPic: str = ""
    HP = 100
    Def_multiply: float = 0.0
    CharacterMoveSpeed = 5
    weapon: Weapon = None
    hp_ = 0

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
    HP = 50
    IsLookAtTarget: bool = True
    target_: Pawn = None

    def __init__(self):
        self.SkinPic = "manbrown_gun"
        super().__init__(self.SkinPic)
        self.HP = 50
        self.CharacterMoveSpeed = 5
        self.weapon = None
        self.isBlock = True
        self.isKeyInput = False
        self.target_ = None

    def update(self, dt):
        super().update(dt)
        pass

    def on_hit(self, actor):
        super().on_hit(actor)
        print(f"hit: {actor}")


world = World()
player = Player()
enemy = Enemy()
player.spawn(world)
enemy.spawn(world)

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
