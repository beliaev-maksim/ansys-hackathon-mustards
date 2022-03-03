import numpy as np
import pygame

# Define constants for the screen width and height
GAS_SIZE = 5
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900


class Gas:
    """
    this class structure describes the information of each gas pixel
    """

    def __init__(self, position_x, position_y):
        # position information
        self.gas_position_x = position_x
        self.gas_position_y = position_y
        # gas density information 128 as default starting value
        self.gas_color = 0
        self.gas_level = 0
        self.altitude = 0
        # pygame objects
        self.gas_surf = pygame.Surface((GAS_SIZE, GAS_SIZE))

        self.gas_rect = self.gas_surf.get_rect()
        self.gas_rect.move_ip(self.gas_position_x, self.gas_position_y)

    def set_color(self, level, max_level):
        self.gas_color = 255 * level / max_level
        self.gas_surf.fill((self.gas_color, 255, self.gas_color))

    @property
    def position_x(self):
        """
        return gas pixel position x
        :return: int
        """
        return self.gas_position_x

    @property
    def position_y(self):
        """
        return gas pixel position y
        :return: int
        """
        return self.gas_position_y

    @property
    def surf(self):
        """
        return gas pixel surf
        :return: pygame.Surface
        """
        return self.gas_surf

    @property
    def rect(self):
        """
        return gas pixel rect
        :return: pygame.Surface.get_rect()
        """
        return self.gas_rect

    @property
    def level(self):
        """
        return gas level/density
        :return: int
        """
        return self.gas_color


class GasCloud:
    """
    this class describe the gas cloud separated by airplane
    """

    def __init__(self):
        self.positions = np.zeros((int(SCREEN_WIDTH / GAS_SIZE), int(SCREEN_HEIGHT / GAS_SIZE)), dtype=Gas)
        for x in range(0, int(SCREEN_WIDTH / GAS_SIZE)):
            for y in range(0, int(SCREEN_HEIGHT / GAS_SIZE)):
                self.positions[x, y] = Gas(x * GAS_SIZE, y * GAS_SIZE)
        self.max_level = 0

    def update(self, position_x, position_y, altitude):
        """
        This function add the density of gas pixel and altitude of a gas pixel
        :param altitude:
        :param position_x: int
        :param position_y: int
        :return: None
        """
        self.positions[int(position_x / GAS_SIZE), int(position_y / GAS_SIZE)].gas_level += 255 / GAS_SIZE
        if self.positions[int(position_x / GAS_SIZE), int(position_y / GAS_SIZE)].gas_level > self.max_level:
            self.max_level = self.positions[int(position_x / GAS_SIZE), int(position_y / GAS_SIZE)].gas_level
        self.positions[int(position_x / GAS_SIZE), int(position_y / GAS_SIZE)].altitude = altitude

    def degrade_gas(self):
        max_level_adjust = 0
        for x in range(0, int(SCREEN_WIDTH / GAS_SIZE)):
            for y in range(0, int(SCREEN_HEIGHT / GAS_SIZE)):
                if self.positions[x, y].altitude > 499:
                    self.positions[x, y].gas_level /= 2
                    self.positions[x, y].altitude /= 2
                    if self.positions[x, y].gas_level > max_level_adjust:
                        max_level_adjust = self.positions[x, y].gas_level
                    if (
                        x != int(SCREEN_WIDTH / GAS_SIZE) - 1
                        and y != int(SCREEN_HEIGHT / GAS_SIZE) - 1
                        and x != 0
                        and y != 0
                    ):
                        self.positions[x - 1, y].gas_level = self.positions[x, y].gas_level / 4
                        self.positions[x + 1, y].gas_level = self.positions[x, y].gas_level / 4
                        self.positions[x, y - 1].gas_level = self.positions[x, y].gas_level / 4
                        self.positions[x, y + 1].gas_level = self.positions[x, y].gas_level / 4
                        self.positions[x - 1, y].altitude = self.positions[x, y].altitude
                        self.positions[x + 1, y].altitude = self.positions[x, y].altitude
                        self.positions[x, y - 1].altitude = self.positions[x, y].altitude
                        self.positions[x, y + 1].altitude = self.positions[x, y].altitude
        self.max_level = max_level_adjust

    def get_area_covered(self):
        """
        This function return area covered by GasCloud
        :return: int
        """
        coverage = 0
        for x in range(0, int(SCREEN_WIDTH / GAS_SIZE)):
            for y in range(0, int(SCREEN_HEIGHT / GAS_SIZE)):
                if self.positions[x, y].gas_color > 100:
                    coverage += 1
        return coverage

    def get_cloud_volume(self):
        """
        This function returns the total volume of gas separated
        :return:
        """
        total_volume = 0
        for position in self.positions:
            total_volume += self.positions[position].level
        return total_volume

    def draw(self, myscreen):
        for x in range(0, int(SCREEN_WIDTH / GAS_SIZE)):
            for y in range(0, int(SCREEN_HEIGHT / GAS_SIZE)):
                if self.positions[x, y].gas_level != 0:
                    self.positions[x, y].set_color(self.positions[x, y].gas_level, self.max_level)
                    myscreen.blit(self.positions[x, y].surf, self.positions[x, y].rect)
