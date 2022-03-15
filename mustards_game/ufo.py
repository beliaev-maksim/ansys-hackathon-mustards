import math

import pygame
from pygame.locals import K_DOWN
from pygame.locals import K_LEFT
from pygame.locals import K_RIGHT
from pygame.locals import K_UP

from mustards_game.gas_cloud import GasCloud


class UFO(pygame.sprite.Sprite):
    def __init__(self, max_altitude=1000, screen_width=900, screen_height=900):
        super().__init__()
        self.size = 25
        self.surf = pygame.image.load("sprites/ufo_25.png").convert_alpha()
        self.rect = self.surf.get_rect()

        # apply mask to make a perfect collision based on pixels
        self.mask = pygame.mask.from_surface(self.surf)
        self.direction = (0, 1)
        self.altitude = 500

        self.gas_cloud = GasCloud()
        self.current_pos_x = 0
        self.current_pos_y = 0
        self.fuel = 10000
        self.max_altitude = max_altitude
        self.screen_width = screen_width
        self.screen_height = screen_height

    def fly(self):
        # Store new float position
        self.current_pos_x += self.direction[0]
        self.current_pos_y += self.direction[1]

        # Compare new float position with the actual position of the rect
        # If new position differs by more than 1 pixel, move the rect
        move_x = int(self.current_pos_x - self.rect.left)
        move_y = int(self.current_pos_y - self.rect.top)
        self.rect.move_ip(move_x, move_y)

        self.gas_cloud.update(
            self.current_pos_x + int(self.size / 2), self.current_pos_y + int(self.size / 2), self.altitude
        )
        self.consume_fuel()

    def consume_fuel(self):
        if self.fuel > 0:
            self.fuel -= 1

    def check_hit_wall(self):
        """Check if airplain hits the outer bounderaies of the screen.

        This should be end of the game.
        """
        if (
            self.rect.left < 0
            or self.rect.right > self.screen_width
            or self.rect.top <= 0
            or self.rect.bottom >= self.screen_height
        ):
            return True
        return False

    def change_direction(self, pressed_keys):
        """Rotate airplain based on LEFT or RIGHT key pressed.

        :param pressed_keys:
        :return:
        """

        rot_step = 1  # degrees
        r = 1

        rot_step = math.radians(rot_step)
        direction = list(self.direction)
        x = direction[1]
        y = direction[0]
        angle = math.atan2(y, x)

        if pressed_keys[K_LEFT]:
            angle = angle + rot_step
        elif pressed_keys[K_RIGHT]:
            angle = angle - rot_step

        x = math.cos(angle) * r
        y = math.sin(angle) * r
        direction_new = (y, x)

        self.direction = direction_new

    def change_altitude(self, pressed_keys):
        if pressed_keys[K_DOWN]:
            self.altitude -= 1

        elif pressed_keys[K_UP]:
            if self.fuel > 0:
                # go up only if you have fuel
                if self.altitude <= self.max_altitude:
                    self.altitude += 1
                    self.consume_fuel()
