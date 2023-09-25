import pygame

import conf


class Brick(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = conf.brick_image
        self.rect = self.image.get_rect()


class Iron(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = conf.iron_image
        self.rect = self.image.get_rect()


class Home(pygame.sprite.Sprite):
    def __init__(self, home_destroyed):
        pygame.sprite.Sprite.__init__(self)
        if home_destroyed:
            self.image = conf.home_destroyed_image
            self.rect = self.image.get_rect()
            self.rect.left, self.rect.top = conf.home_rect
        else:
            self.image = conf.home_image
            self.rect = self.image.get_rect()
            self.rect.left, self.rect.top = conf.home_rect


class Map():
    def __init__(self, json_config):
        self.brickGroup = pygame.sprite.Group()
        self.ironGroup = pygame.sprite.Group()
        self.home = Home(False)

        if len(json_config) == 0 or json_config["brick_list"] is None:
            brick_place_list = []
        else:
            brick_place_list = json_config["brick_list"]

        if len(json_config) == 0 or json_config["iron_list"] is None:
            iron_place_list = []
        else:
            iron_place_list = json_config["iron_list"]

        for brick_place in brick_place_list:
            brick = Brick()
            brick.rect.left, brick.rect.top = brick_place[0], brick_place[1]
            self.brickGroup.add(brick)
        for iron_place in iron_place_list:
            iron = Iron()
            iron.rect.left, iron.rect.top = iron_place[0], iron_place[1]
            self.ironGroup.add(iron)

    def change_home_destroyed(self):
        self.home.image = conf.home_destroyed_image

    # 后面的渲染，会覆盖掉前面的渲染
    def this_blit(self, screen):
        # 画背景
        screen.blit(conf.background_image, (0, 0))
        # 画砖块
        for each in self.brickGroup:
            screen.blit(each.image, each.rect)
        # 画铁
        for each in self.ironGroup:
            screen.blit(each.image, each.rect)

        screen.blit(self.home.image, self.home.rect)
