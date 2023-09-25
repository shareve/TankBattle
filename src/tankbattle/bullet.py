import pygame

import conf

class Bullet(pygame.sprite.Sprite):
    def __init__(self, life, owner, own_group, strong, speed, dir_x, dir_y):
        pygame.sprite.Sprite.__init__(self)

        self.bullet_up = conf.bullet_up
        self.bullet_down = conf.bullet_down
        self.bullet_left = conf.bullet_left
        self.bullet_right = conf.bullet_right


        # 速度
        self.speed = speed
        # 是否活着
        self.life = life
        # 是否能打铁
        self.strong = strong

        self.owner = owner
        # 属于哪个组
        self.ownGroup = own_group

        # 方向
        self.dir_x, self.dir_y = dir_x, dir_y
        # 根据方向判断用哪个图片
        if self.dir_x == 0 and self.dir_y == -1:
            self.bullet_img = self.bullet_up
        elif self.dir_x == 0 and self.dir_y == 1:
            self.bullet_img = self.bullet_down
        elif self.dir_x == -1 and self.dir_y == 0:
            self.bullet_img = self.bullet_left
        elif self.dir_x == 1 and self.dir_y == 0:
            self.bullet_img = self.bullet_right

        self.rect = self.bullet_img.get_rect()

    def move(self):
        self.rect = self.rect.move(self.speed * self.dir_x, self.speed * self.dir_y)

        # 碰撞地图边缘
        if self.rect.top < 3 or self.rect.bottom > 630 - 3 or self.rect.left < 3 or self.rect.right > 630 - 3:
            self.life = False
            if self.ownGroup == "our":
                conf.ourBulletGroup.remove(self)
                conf.bulletGroup.remove(self)
            if self.ownGroup == "enemy":
                conf.enemyBulletGroup.remove(self)
                conf.bulletGroup.remove(self)

    def this_blit(self, screen, bg_map):
        if self.life == True:
            self.move()
            screen.blit(self.bullet_img, self.rect)
            if self.ownGroup == "our":
                # 子弹碰子弹
                if pygame.sprite.spritecollide(self, conf.enemyBulletGroup, True, None):
                    self.life = False
                    conf.ourBulletGroup.remove(self)
                    conf.bulletGroup.remove(self)
                    conf.hit_sound.play()
                # 子弹碰对方坦克
                bullet_collide_enemy_tank_list = pygame.sprite.spritecollide(self, conf.enemyTankGroup, False, None)
                if bullet_collide_enemy_tank_list:
                    self.life = False
                    conf.ourBulletGroup.remove(self)
                    conf.bulletGroup.remove(self)
                    conf.bang_sound.play()
                    for enemy_tank in bullet_collide_enemy_tank_list:
                        conf.enemyTankGroup.remove(enemy_tank)
                        conf.tankGroup.remove(enemy_tank)
                        if enemy_tank.has_prop:
                            enemy_tank.has_prop = False
                            # 创建一个页面出随机道具事件对象，并携带参数
                            custom_event = pygame.event.Event(conf.EVENT_CREATE_PROP)
                            # 将自定义事件放入事件队列
                            pygame.event.post(custom_event)
                        if enemy_tank.life_times > 0:
                            enemy_tank.life_times -= 1
                            # 创建一个页面出随机道具事件对象，并携带参数
                            event_rand_enemy = pygame.event.Event(conf.EVENT_NEW_ENEMY_TANK, tank=enemy_tank)
                            # 将自定义事件放入事件队列
                            pygame.event.post(event_rand_enemy)

                # 子弹碰墙
                if pygame.sprite.spritecollide(self, bg_map.brickGroup, True, None):
                    self.life = False
                    conf.ourBulletGroup.remove(self)
                    conf.bulletGroup.remove(self)
                # 子弹碰铁
                if pygame.sprite.spritecollide(self, bg_map.ironGroup, False, None):
                    self.life = False
                    conf.ourBulletGroup.remove(self)
                    conf.bulletGroup.remove(self)
                    conf.hit_sound.play()
                # 子弹碰家
                if self.rect.colliderect(bg_map.home.rect):
                    print("我方子弹和家发生碰撞")
                    event = pygame.event.Event(conf.EVENT_HOME_DESTROYED)
                    pygame.event.post(event)
                    self.life = False
                    conf.ourBulletGroup.remove(self)
                    conf.bulletGroup.remove(self)
            if self.ownGroup == "enemy":
                # 子弹碰子弹
                if pygame.sprite.spritecollide(self, conf.ourBulletGroup, True, None):
                    self.life = False
                    conf.enemyBulletGroup.remove(self)
                    conf.bulletGroup.remove(self)
                    conf.hit_sound.play()
                # 子弹碰our坦克
                tankCollideList = pygame.sprite.spritecollide(self, conf.ourTankGroup, False, None)
                if tankCollideList:
                    self.life = False
                    conf.enemyBulletGroup.remove(self)
                    conf.bulletGroup.remove(self)
                    conf.bang_sound.play()
                    for tank in tankCollideList:
                        if tank.protected == False:
                            conf.ourTankGroup.remove(tank)
                            conf.tankGroup.remove(tank)
                            if tank.life_times > 0:
                                tank.life_times -= 1
                                # 创建一个页面出随机道具事件对象，并携带参数
                                event = pygame.event.Event(conf.EVENT_NEW_OUR_TANK, tank=tank)
                                # 将自定义事件放入事件队列
                                pygame.event.post(event)

                # 子弹碰墙
                if pygame.sprite.spritecollide(self, bg_map.brickGroup, True, None):
                    self.life = False
                    conf.enemyBulletGroup.remove(self)
                    conf.bulletGroup.remove(self)
                # 子弹碰铁
                if pygame.sprite.spritecollide(self, bg_map.ironGroup, False, None):
                    self.life = False
                    conf.enemyBulletGroup.remove(self)
                    conf.bulletGroup.remove(self)
                    conf.hit_sound.play()
                # 子弹碰家
                if self.rect.colliderect(bg_map.home.rect):
                    print("敌方子弹和家发生碰撞")
                    event = pygame.event.Event(conf.EVENT_HOME_DESTROYED)
                    pygame.event.post(event)
                    self.life = False
                    conf.enemyBulletGroup.remove(self)
                    conf.bulletGroup.remove(self)
