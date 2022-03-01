import pygame
import random

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900


class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.pos = (0, 0)
        self.height = 100
        self.randomize_pos()
        self.randomize_height()
        self.surf = pygame.Surface((25, 25))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect()
        self.rect.move_ip(self.pos[0], self.pos[1])

    def randomize_pos(self):
        x = random.randint(0, SCREEN_WIDTH-25)
        y = random.randint(0, SCREEN_HEIGHT-25)
        self.pos = (x, y)

    def randomize_height(self):
        self.height = random.randint(100, 1000)

    def reset(self):
        self.randomize_pos()
        self.randomize_height()
        self.surf = pygame.Surface((25, 25))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect()
        self.rect.move_ip(self.pos[0], self.pos[1])
