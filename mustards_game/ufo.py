import math

import pygame
from pygame.locals import K_DOWN
from pygame.locals import K_LEFT
from pygame.locals import K_RIGHT
from pygame.locals import K_UP

from mustards_game.gas_cloud import GasCloud


class UFO(pygame.sprite.Sprite):
    """
    This class describes the UFO and its methods.
    """

    def __init__(self, max_altitude=1000, screen_width=900, screen_height=900):
        """

        Parameters
        ----------
        max_altitude: int: max altitude the ufo can achieve in meter.
        screen_width: int: screen width in pixels
        screen_height: int: screen height in pixels
        """
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
        """
        This method updates the position of the ufo on the screen for each iteration of the main game loop.
        """

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
        """
        Reduce amount of fuel in the tak for each iteration of the main loop.
        """
        if self.fuel > 0:
            self.fuel -= 1

    def check_hit_wall(self):
        """
        Check if ufo hits the outer boundaries of the screen.
        This should end the game.
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
        """
        Rotate ufo based on LEFT or RIGHT key pressed.

        Parameters
        ----------
        pressed_keys: pygame key reference
        """

        rot_step = 1  # step of rotation in degrees

        r = 1
        rot_step = math.radians(rot_step)
        direction = list(self.direction)
        x = direction[1]
        y = direction[0]
        angle = math.atan2(y, x)  # calculate new direction angle between 0 and 2pi

        if pressed_keys[K_LEFT]:
            angle = angle + rot_step
        elif pressed_keys[K_RIGHT]:
            angle = angle - rot_step

        x = math.cos(angle) * r
        y = math.sin(angle) * r

        direction_new = (y, x)  # new direction in screen pixel terms

        self.direction = direction_new

    def change_altitude(self, pressed_keys):
        """
        Change altitude of the ufo depending on the player input.

        Parameters
        ----------
        pressed_keys: pygame key reference.
        """
        if pressed_keys[K_DOWN]:
            self.altitude -= 1

        elif pressed_keys[K_UP]:
            if self.fuel > 0:
                # go up only if you have fuel
                if self.altitude <= self.max_altitude:
                    self.altitude += 1
                    self.consume_fuel()
