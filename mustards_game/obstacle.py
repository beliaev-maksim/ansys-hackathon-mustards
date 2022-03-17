import random

import pygame

from mustards_game.config import NOT_OBSTACLES
from mustards_game.config import OBSTACLES
from mustards_game.config import SCREEN_HEIGHT
from mustards_game.config import SCREEN_WIDTH


class Obstacle(pygame.sprite.Sprite):
    """
    This class describes the properties and static objects on the map.
    """

    def __init__(self, obs_bool=True):
        super().__init__()
        self.pos = (0, 0)
        self.height = 100
        self.size = 25
        object_list = OBSTACLES if obs_bool else NOT_OBSTACLES
        for obstacle in object_list:
            if obstacle["count"] > 0:
                obstacle["count"] -= 1
                break

        self.surf = pygame.image.load(obstacle["path"]).convert_alpha()
        self.rect = self.surf.get_rect()
        self.randomize_pos([(0, 0)])
        self.randomize_height(obstacle["min"], obstacle["max"])
        self.rect = self.surf.get_rect()
        self.mask = pygame.mask.from_surface(self.surf)

    def randomize_pos(self, pos):
        """
        Function to randomize a static objects position without intersecting other object.
        Parameter pos are  tuples of x,y positions.

        Parameters
        ----------
        pos : list of int tuples
        """
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

    def randomize_height(self, min_h=100, max_h=1000):
        """
        Function to randomize the height of the object within given range.

        Parameters
        ----------
        min_h : int
        max_h : int
        """
        self.height = random.randint(min_h, max_h)
