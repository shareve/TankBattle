import json
import pygame

import conf

def gain_our_tank_img(player_id, level):
    tank_together_image = conf.p1_tank_L0_image
    if player_id == 0:
        if level == 0:
            tank_together_image = conf.p1_tank_L0_image
        elif level == 1:
            tank_together_image = conf.p1_tank_L0_image
        elif level == 2:
            tank_together_image = conf.p1_tank_L1_image
        elif level == 3:
            tank_together_image = conf.p1_tank_L2_image
    if player_id == 1:
        if level == 0:
            tank_together_image = conf.p2_tank_L0_image
        elif level == 1:
            tank_together_image = conf.p2_tank_L0_image
        elif level == 2:
            tank_together_image = conf.p2_tank_L1_image
        elif level == 3:
            tank_together_image = conf.p2_tank_L2_image
    return tank_together_image


def gain_enemy_tank_img(kind, has_prop):
    if kind == 1:
        if not has_prop:
            return conf.enemy_1_0_image
        else:
            return conf.enemy_1_3_image
    if kind == 2:
        if not has_prop:
            return conf.enemy_2_0_image
        else:
            return conf.enemy_2_3_image
    if kind == 3:
        if not has_prop:
            return conf.enemy_3_0_image
        else:
            return conf.enemy_3_3_image
    if kind == 4:
        if not has_prop:
            return conf.enemy_4_0_image
        else:
            return conf.enemy_4_3_image


def gain_num(num):
    if num:
        return num
    else:
        return 0


# 游戏位置值转化为像素位置值
def gain_pixel(pos):
    if pos:
        return pos * 24
    else:
        return 0


# 游戏位置值转化为像素位置值
def gain_pixel_xy(pos_xy):
    return [pos_xy[0] * 24, pos_xy[1] * 24]


# 像素位置值转化为游戏位置值
def gain_pos(pixel):
    if pixel:
        return pixel / 24
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
    for enemy in conf.enemyTankGroup:
        total_enemy_life = total_enemy_life + enemy.life_times

    total_our_life = 0
    for our in conf.ourTankGroup:
        total_our_life = total_our_life + our.life_times

    if total_enemy_life <= 0:
        event = pygame.event.Event(conf.EVENT_NONE_ENEMY_LIFE)
        pygame.event.post(event)

    if total_our_life <= 0:
        event = pygame.event.Event(conf.EVENT_NONE_OUR_LIFE)
        pygame.event.post(event)
