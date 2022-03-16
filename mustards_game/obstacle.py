import random

import pygame

from mustards_game.config import SCREEN_HEIGHT
from mustards_game.config import SCREEN_WIDTH

obstacle_imgs = ["sprites/mountain.png", "sprites/win_mountain.png", "sprites/blacksmith.png", "sprites/windmill.png"]


class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.pos = (0, 0)
        self.height = 100
        self.size = 25
        self.surf = pygame.image.load(obstacle_imgs[random.randint(0, len(obstacle_imgs) - 1)]).convert_alpha()
        self.rect = self.surf.get_rect()
        self.randomize_pos([(0, 0)])
        self.randomize_height()
        self.randomize_size()
        self.rect = self.surf.get_rect()
        self.mask = pygame.mask.from_surface(self.surf)

    def randomize_pos(self, pos):
        pos_not_found = True
        while pos_not_found:
            pos_found = False
            x_size = self.rect.size[0]
            y_size = self.rect.size[0]
            x = random.randint(x_size, SCREEN_WIDTH - 2 * x_size)
            y = random.randint(y_size, SCREEN_HEIGHT - 2 * y_size)
            for (pos_x, pos_y) in pos:
                if x in range((pos_x - x_size), (pos_x + x_size)) and y in range((pos_y - y_size), (pos_y + y_size)):
                    pos_found = True
            if not pos_found:
                self.pos = (x, y)
                pos_not_found = False
                self.rect.move_ip(self.pos[0], self.pos[1])
        return self.pos

    def randomize_height(self):
        self.height = random.randint(100, 1000)

    def randomize_size(self):
        self.size = random.randint(10, 100)

    def reset(self):
        self.randomize_pos()
        self.randomize_height()
        self.surf = pygame.Surface((25, 25))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect()
        self.rect.move_ip(self.pos[0], self.pos[1])
