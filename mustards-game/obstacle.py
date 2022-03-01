import pygame
import random

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900


class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf =[]
        self.rect = []
        self.count = 5
        self.pos = []
        for obs in range(0, self.count):
            self.randomize_pos()
        for i, pos in enumerate(self.pos):
            self.surf.append(pygame.Surface((25, 25)))
            self.surf[i].fill((255, 0, 0))
            self.rect.append(self.surf[i].get_rect())
            self.rect[i].move_ip(pos[0],pos[1])

    def randomize_pos(self):
        x = random.randint(0, SCREEN_WIDTH-25)
        y = random.randint(0, SCREEN_HEIGHT-25)
        self.pos.append((x, y))

    def reset(self):
        self.count = 5
        self.pos = []
        for obs in range(0, self.count):
            self.randomize_pos()
        for i, pos in enumerate(self.pos):
            self.surf.append(pygame.Surface((25, 25)))
            self.surf[i].fill((255, 0, 0))
            self.rect.append(self.surf[i].get_rect())
            self.rect[i].move_ip(pos[0],pos[1])

    def add_obstacles(self, number):
        start_count = self.count
        self.count += number
        for obs in range(0, number):
            self.randomize_pos()
        for i, pos in enumerate(self.pos):
            if i > start_count-1:
                self.surf.append(pygame.Surface((25, 25)))
                self.surf[i].fill((255, 0, 0))
                self.rect.append(self.surf[i].get_rect())
                self.rect[i].move_ip(pos[0], pos[1])
