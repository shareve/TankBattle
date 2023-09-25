import pygame
import random

import conf


class Prop(pygame.sprite.Sprite):
    def __init__(self,kind=None):
        pygame.sprite.Sprite.__init__(self)
        self.prop_boom = conf.prop_boom.convert_alpha()
        self.prop_clock = conf.prop_clock.convert_alpha()
        self.prop_gun = conf.prop_gun.convert_alpha()
        self.prop_iron = conf.prop_iron.convert_alpha()
        self.prop_protect = conf.prop_protect.convert_alpha()
        self.prop_star = conf.prop_star.convert_alpha()
        self.prop_life = conf.prop_life.convert_alpha()

        if kind == None:
            self.kind = random.choice(["boom", "lock", "star", "gun", "iron_home", "protect", "life"])
        else:
            self.kind = kind

        if self.kind == "boom":
            self.image = self.prop_boom
        elif self.kind == "lock":
            self.image = self.prop_clock
        elif self.kind == "iron_home":
            self.image = self.prop_iron
        elif self.kind == "protect":
            self.image = self.prop_protect
        elif self.kind == "star":
            self.image = self.prop_star
        elif self.kind == "gun":
            self.image = self.prop_gun
        elif self.kind == "life":
            self.image = self.prop_life

        self.rect = self.image.get_rect()
        self.rect.left = self.rect.top = random.randint(100, 500)

        self.life = True

    def change(self):
        self.kind = random.choice(["boom", "lock", "iron_home", "protect", "star", "gun", "life"])
        if self.kind == "boom":
            self.image = self.prop_boom
        elif self.kind == "lock":
            self.image = self.prop_clock
        elif self.kind == "iron_home":
            self.image = self.prop_iron
        elif self.kind == "protect":
            self.image = self.prop_protect
        elif self.kind == "star":
            self.image = self.prop_star
        elif self.kind == "gun":
            self.image = self.prop_gun
        elif self.kind == "life":
            self.image = self.prop_life

        self.rect.left = self.rect.top = random.randint(100, 500)
        self.life = True

    def this_blit(self, screen):
        if self.life == True:
            screen.blit(self.image, self.rect)
