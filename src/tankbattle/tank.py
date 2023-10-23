import random

import pygame

import bullet
import conf
import utils


class Tank(pygame.sprite.Sprite):
    # speed是速度；x,y是位置；dir_x,dir_y是方向；
    def __init__(self, id, player_id, life_times, level, own_group, kind, has_prop, speed, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.id = id
        # level有4级；0级默认无变化，1级子弹加速，2级形状变化+子弹，3级形状再变化+子弹打铁+多挨打1次
        self.level = level
        self.own_group = own_group
        self.speed = speed
        self.player_id = player_id
        self.life_times = life_times
        self.x = x
        self.y = y
        self.protected = False
        self.locked = False

        if own_group == "our":
            self.tank_together_image = utils.gain_our_tank_img(player_id, level).convert_alpha()
            self.dir_x, self.dir_y = 0, 1
        if own_group == "enemy":
            self.kind = kind
            self.has_prop = has_prop
            self.tank_together_image = utils.gain_enemy_tank_img(kind, has_prop).convert_alpha()
            self.dir_x, self.dir_y = 0, -1

        self.tank_image = self.tank_together_image.subsurface((0, 0), (48, 48))
        self.rect = self.tank_image.get_rect()
        self.rect.left, self.rect.top = utils.gain_pixel(x), utils.gain_pixel(y)

    def shoot(self):
        bullet_speed = 10
        bullet_lv = 1

        if self.level == 1:
            bullet_speed = 10
            bullet_lv = 1
        if self.level == 2:
            bullet_speed = 16
            bullet_lv = 1
        if self.level == 3:
            bullet_speed = 16
            bullet_lv = 2
        the_bullet = bullet.Bullet(True, self.id, self.own_group, bullet_lv, bullet_speed, self.dir_x, self.dir_y)

        if the_bullet.dir_x == 0 and the_bullet.dir_y == -1:
            the_bullet.rect.left = self.rect.left + 15
            the_bullet.rect.bottom = self.rect.top + 1
        elif the_bullet.dir_x == 0 and the_bullet.dir_y == 1:
            the_bullet.rect.left = self.rect.left + 15
            the_bullet.rect.top = self.rect.bottom - 1
        elif the_bullet.dir_x == -1 and the_bullet.dir_y == 0:
            the_bullet.rect.right = self.rect.left - 1
            the_bullet.rect.top = self.rect.top + 15
        elif the_bullet.dir_x == 1 and the_bullet.dir_y == 0:
            the_bullet.rect.left = self.rect.right + 1
            the_bullet.rect.top = self.rect.top + 15

        conf.fire_sound.play()
        return the_bullet

    def level_up(self, num):
        if num == 0:
            return
        level = utils.gain_num(self.level) + num
        if 0 <= level <= 3:
            self.level = level
        elif level > 3:
            self.level = 3
        else:
            self.level = 0
        self.tank_together_image = utils.gain_our_tank_img(self.player_id, self.level).convert_alpha()

    def level_down(self, num):
        if num == 0:
            return
        level = self.level - num
        if 0 <= level <= 3:
            self.level = level
        elif level > 3:
            self.level = 3
        else:
            self.level = 0
        self.tank_together_image = utils.gain_our_tank_img(self.player_id, self.level).convert_alpha()

    # 先按照之前的方向走,如果碰撞，随机选择一个方向重新走
    def let_ai_action(self, bg_map, tank_group):
        if self.locked:
            return

        # 行动的概率为80/100
        action_choice = random.randint(1, 100)
        if action_choice <= 80:
            return

        # 先按照之前的方向走
        collision = not self.move_dir(bg_map, tank_group,[self.dir_x,self.dir_y])
        if collision:
            # 随机选择一个方向
            move_choice = random.choice((conf.up_dir, conf.down_dir, conf.left_dir, conf.right_dir))
            self.move_dir(bg_map, tank_group,move_choice)

        # shoot的概率为10/100
        shoot_choice = random.randint(1, 100)
        if shoot_choice <= 10:
            return self.shoot()

    # False说明发生碰撞
    def move_dir(self, bg_map, tank_group, dir_x_y):
        brick_group = bg_map.brickGroup
        iron_group = bg_map.ironGroup
        # 调整位置，四舍五入取整
        if self.dir_x == 0 and dir_x_y[0] != 0:
            self.rect.top = round(self.rect.top / 24) * 24
        elif self.dir_y == 0 and dir_x_y[1] != 0:
            self.rect.left = round(self.rect.left / 24) * 24

        self.dir_x, self.dir_y = dir_x_y
        self.rect = self.rect.move(self.speed * dir_x_y[0], self.speed * dir_x_y[1])
        if dir_x_y == conf.up_dir:
            self.tank_image = self.tank_together_image.subsurface((0, 0), (48, 48))
        elif dir_x_y == conf.down_dir:
            self.tank_image = self.tank_together_image.subsurface((0, 48), (48, 48))
        elif dir_x_y == conf.left_dir:
            self.tank_image = self.tank_together_image.subsurface((0, 96), (48, 48))
        elif dir_x_y == conf.right_dir:
            self.tank_image = self.tank_together_image.subsurface((0, 144), (48, 48))

        # if self.own_group == "our":
        #     print("move_dir", "pos_x", utils.gain_pos(self.rect.left), "pos_y", utils.gain_pos(self.rect.top))

        if utils.gain_pos(self.rect.top) < 0:
            self.rect = self.rect.move(self.speed * 0, self.speed * 1)
            return False
        if utils.gain_pos(self.rect.top) > 22:
            self.rect = self.rect.move(self.speed * 0, self.speed * -1)
            return False
        if utils.gain_pos(self.rect.left) < 0:
            self.rect = self.rect.move(self.speed * 1, self.speed * 0)
            return False
        if utils.gain_pos(self.rect.left) > 22:
            self.rect = self.rect.move(self.speed * -1, self.speed * 0)
            return False
        if pygame.sprite.spritecollide(self, brick_group, False, None) \
                or pygame.sprite.spritecollide(self, iron_group, False, None):
            # print("move_dir", "tank_group", "碰",dir_x,dir_y)
            # 反方向移动一格
            self.rect = self.rect.move(self.speed * - dir_x_y[0], self.speed * -dir_x_y[1])
            return False

        tank_group.remove(self)
        collide = pygame.sprite.spritecollide(self, tank_group, False, None)
        tank_group.add(self)
        if collide:
            # print("move_dir", "tank_group", "碰",dir_x,dir_y)
            # 反方向移动一格
            self.rect = self.rect.move(self.speed * -dir_x_y[0], self.speed * -dir_x_y[1])
            return False
        self.check_touch_prop()
        return True

    def check_touch_prop(self):
        if self.own_group == "our":
            # 坦克碰地图上道具
            collide_prop_list = pygame.sprite.spritecollide(self, conf.propGroup, True, None)
            if collide_prop_list:
                for prop in collide_prop_list:
                    if prop.kind == "boom":
                        custom_event = pygame.event.Event(conf.EVENT_ALL_ENEMY_BOOM)
                        pygame.event.post(custom_event)
                    if prop.kind == "lock":
                        custom_event = pygame.event.Event(conf.EVENT_LOCK)
                        pygame.event.post(custom_event)
                    if prop.kind == "iron_home":
                        custom_event = pygame.event.Event(conf.EVENT_IRON_HOME)
                        pygame.event.post(custom_event)
                    if prop.kind == "protect":
                        custom_event = pygame.event.Event(conf.EVENT_PROTECT, tank=self)
                        pygame.event.post(custom_event)
                    if prop.kind == "star":
                        custom_event = pygame.event.Event(conf.EVENT_LEVEL_STAR, tank=self)
                        pygame.event.post(custom_event)
                    if prop.kind == "gun":
                        custom_event = pygame.event.Event(conf.EVENT_LEVEL_GUN, tank=self)
                        pygame.event.post(custom_event)
                    if prop.kind == "life":
                        custom_event = pygame.event.Event(conf.EVENT_ADD_LIFE, tank=self)
                        pygame.event.post(custom_event)

    def this_blit(self, screen):
        screen.blit(self.tank_image, self.rect)
