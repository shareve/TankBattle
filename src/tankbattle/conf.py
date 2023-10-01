import json

import pygame

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 630
SCREEN_HEIGHT = 630

enemy_tank_seq = 1000

# 创建字体对象
font_size = 36
font = pygame.font.SysFont("arialunicode", font_size)

# 创建屏幕对象
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# 定义游戏模式和开始游戏页面的选项
game_chapters = ["关卡1", "关卡2", "关卡3"]

# 创建新的任意1个敌对坦克
EVENT_NEW_ENEMY_TANK = pygame.constants.USEREVENT + 1
# 创建player坦克
EVENT_NEW_OUR_TANK = pygame.constants.USEREVENT + 2
# 页面出随机道具事件
EVENT_CREATE_PROP = pygame.constants.USEREVENT + 10

# 敌人全部爆
EVENT_ALL_ENEMY_BOOM = pygame.constants.USEREVENT + 100
# 敌方坦克静止8000
EVENT_LOCK = pygame.constants.USEREVENT + 101
EVENT_NOT_LOCK = pygame.constants.USEREVENT + 102
# 自己到star级
EVENT_LEVEL_STAR = pygame.constants.USEREVENT + 103
# 自己到gun级
EVENT_LEVEL_GUN = pygame.constants.USEREVENT + 104
# 家材料变铁
EVENT_IRON_HOME = pygame.constants.USEREVENT + 105
EVENT_NOT_IRON_HOME = pygame.constants.USEREVENT + 106
# 自己不受伤害
EVENT_PROTECT = pygame.constants.USEREVENT + 107
EVENT_NOT_PROTECT = pygame.constants.USEREVENT + 108
# 自己加一条命
EVENT_ADD_LIFE = pygame.constants.USEREVENT + 109
# 两个玩家都没有命了
EVENT_NONE_OUR_LIFE = pygame.constants.USEREVENT + 110
# 老家被打爆了
EVENT_HOME_DESTROYED = pygame.constants.USEREVENT + 111
# 对方都没有命了
EVENT_NONE_ENEMY_LIFE = pygame.constants.USEREVENT + 112

# game over
game_over = pygame.image.load(r"../../img/game_over.png")

# 声音
bang_sound = pygame.mixer.Sound(r"../../sound/bang.wav")
fire_sound = pygame.mixer.Sound(r"../../sound/Gunfire.wav")
start_sound = pygame.mixer.Sound(r"../../sound/start.wav")
hit_sound = pygame.mixer.Sound(r"../../sound/hit.wav")

# 子弹
bullet_up = pygame.image.load(r"../../img/bullet_up.png")
bullet_down = pygame.image.load(r"../../img/bullet_down.png")
bullet_left = pygame.image.load(r"../../img/bullet_left.png")
bullet_right = pygame.image.load(r"../../img/bullet_right.png")

# 背景等
background_image = pygame.image.load(r"../../img/background.png")
home_image = pygame.image.load(r"../../img/home.png")
home_destroyed_image = pygame.image.load(r"../../img/home_destroyed.png")
brick_image = pygame.image.load(r"../../img/brick.png")
iron_image = pygame.image.load(r"../../img/iron.png")

# our坦克
p1_tank_L0_image = pygame.image.load(r"../../img/tank_T1_0.png")
p1_tank_L1_image = pygame.image.load(r"../../img/tank_T1_1.png")
p1_tank_L2_image = pygame.image.load(r"../../img/tank_T1_2.png")
p2_tank_L0_image = pygame.image.load(r"../../img/tank_T2_0.png")
p2_tank_L1_image = pygame.image.load(r"../../img/tank_T2_1.png")
p2_tank_L2_image = pygame.image.load(r"../../img/tank_T2_2.png")

# 敌人坦克
enemy_1_0_image = pygame.image.load(r"../../img/enemy_1_0.png")
enemy_1_3_image = pygame.image.load(r"../../img/enemy_1_3.png")
enemy_2_0_image = pygame.image.load(r"../../img/enemy_2_0.png")
enemy_2_3_image = pygame.image.load(r"../../img/enemy_2_3.png")
enemy_3_0_image = pygame.image.load(r"../../img/enemy_3_0.png")
enemy_3_3_image = pygame.image.load(r"../../img/enemy_3_3.png")
enemy_4_0_image = pygame.image.load(r"../../img/enemy_4_0.png")
enemy_4_3_image = pygame.image.load(r"../../img/enemy_4_3.png")

# 道具
prop_boom = pygame.image.load(r"../../img/prop_boom.png")
prop_clock = pygame.image.load(r"../../img/prop_clock.png")
prop_gun = pygame.image.load(r"../../img/prop_gun.png")
prop_iron = pygame.image.load(r"../../img/prop_iron.png")
prop_protect = pygame.image.load(r"../../img/prop_protect.png")
prop_star = pygame.image.load(r"../../img/prop_star.png")
prop_life = pygame.image.load(r"../../img/prop_life.png")

# 定义精灵组:坦克，我方坦克，敌方坦克
propGroup = pygame.sprite.Group()
tankGroup = pygame.sprite.Group()
ourTankGroup = pygame.sprite.Group()
enemyTankGroup = pygame.sprite.Group()
bulletGroup = pygame.sprite.Group()
ourBulletGroup = pygame.sprite.Group()
enemyBulletGroup = pygame.sprite.Group()

home_rect = 291, 579


def gain_our_tank_img(player_id, level):
    tank_together_image = p1_tank_L0_image
    if player_id == 0:
        if level == 0:
            tank_together_image = p1_tank_L0_image
        elif level == 1:
            tank_together_image = p1_tank_L0_image
        elif level == 2:
            tank_together_image = p1_tank_L1_image
        elif level == 3:
            tank_together_image = p1_tank_L2_image
    if player_id == 1:
        if level == 0:
            tank_together_image = p2_tank_L0_image
        elif level == 1:
            tank_together_image = p2_tank_L0_image
        elif level == 2:
            tank_together_image = p2_tank_L1_image
        elif level == 3:
            tank_together_image = p2_tank_L2_image
    return tank_together_image


def gain_enemy_tank_img(kind, has_prop):
    if kind == 1:
        if not has_prop:
            return enemy_1_0_image
        else:
            return enemy_1_3_image
    if kind == 2:
        if not has_prop:
            return enemy_2_0_image
        else:
            return enemy_2_3_image
    if kind == 3:
        if not has_prop:
            return enemy_3_0_image
        else:
            return enemy_3_3_image
    if kind == 4:
        if not has_prop:
            return enemy_4_0_image
        else:
            return enemy_4_3_image


def gain_num(num):
    if num:
        return num
    else:
        return 0


# 读取配置文件
def load_json_conf(josn_name):
    with open(josn_name, "r") as file:
        config_json = json.load(file)
    return config_json


# 校验输赢
def check_lose_win():
    total_enemy_life = 0
    for enemy in enemyTankGroup:
        total_enemy_life = total_enemy_life + enemy.life_times

    total_our_life = 0
    for our in ourTankGroup:
        total_our_life = total_our_life + our.life_times

    if total_enemy_life <= 0:
        event = pygame.event.Event(EVENT_NONE_ENEMY_LIFE)
        pygame.event.post(event)

    if total_our_life <= 0:
        event = pygame.event.Event(EVENT_NONE_OUR_LIFE)
        pygame.event.post(event)
