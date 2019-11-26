from typing import List, Tuple
import enum
import random

import pygame

from colors import Colors

Point = list
Dimensions = Tuple[int, int]


class Direction(enum.Enum):
    up = 0
    right = 1
    down = 2
    left = 3


class World:
    def __init__(self, grid_dims: Dimensions, screen_dims: Dimensions):
        self.grid_dims = grid_dims
        self.screen_dims = screen_dims
        self.sprites = {
            'Bullet': pygame.sprite.Group(),
            'Invader': pygame.sprite.Group()
        }

    def remove(self, obj):
        self.sprites[obj.__class__.__name__].remove(obj)

    def add(self, obj):
        self.sprites[obj.__class__.__name__].add(obj)

    def update(self):
        for cls_name, sprite_group in self.sprites.copy().items():
            for obj in sprite_group:
                obj.counter_incr()
            sprite_group.update()


class GameObject:
    def __init__(self, world: World, pos: Point, callback=lambda: None):
        cls_name = self.__class__.__name__
        if cls_name not in world.sprites:
            world.sprites[cls_name] = pygame.sprite.Group()
        world.add(self)

        self.callback = callback

        self.world = world
        self.pos = [pos[0] % world.grid_dims[0], pos[1] % world.grid_dims[1]]

        self.counter = 0

        img_width = img_height = world.screen_dims[0] / world.grid_dims[0]
        self.image = pygame.Surface([0.8 * img_width, 0.8 * img_height])
        self.image.fill(Colors.red)

        self.rect = self.image.get_rect()

        self.v = 0, 0
        self.freq = 1

    def counter_incr(self):
        self.counter += 1
        if self.counter % self.freq == 0:
            self.move()
            self.counter = 0

    def move(self):
        self.pos = self.pos[0] + self.v[0], self.pos[1] + self.v[1]

    def _update(self):
        rows_n, cols_n = self.world.grid_dims
        screen_w, screen_h = self.world.screen_dims
        x, y = self.pos
        if not (0 <= x <= cols_n and 0 <= y <= rows_n):
            self.world.remove(self)
            self.callback()
            return
        self.rect.x = x * screen_w / cols_n
        self.rect.y = y * screen_h / rows_n

    def update(self):
        self._update()


class Player(GameObject, pygame.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        GameObject.__init__(self, *args, **kwargs)

    def shoot(self):
        return Bullet([0, -1], self.world, (self.pos[0], self.pos[1] - 1))


class Bullet(GameObject, pygame.sprite.Sprite):
    def __init__(self, v, *args, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        GameObject.__init__(self, *args, **kwargs)
        self.v = v
        self.freq = 10


class Invader(GameObject, pygame.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        GameObject.__init__(self, *args, **kwargs)
        self.freq = 10
        self.reg = 0

    def move(self):
        self.reg += 1
        if self.reg % 2 == 0:
            self.v = 1, 0
        else:
            self.v = -1, 0

        if self.reg % 4 == 0:
            self.spawn()
        self.reg %= 16
        super().move()

    def spawn(self):
        return Bullet([0, 1], self.world, (self.pos[0], self.pos[1] + 1))
