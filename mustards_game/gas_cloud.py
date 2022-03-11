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
        self.gas_level = 0
        self.altitude = 0
        # pygame objects
        self.gas_surf = pygame.Surface((GAS_SIZE, GAS_SIZE))

        self.gas_rect = self.gas_surf.get_rect()
        self.gas_rect.move_ip(self.gas_position_x, self.gas_position_y)

    def set_color(self, level):
        if 10 < level < 100:
            self.gas_surf.fill((50 * level / 100, 50 * level / 100, 0))
        elif 100 < level < 500:
            self.gas_surf.fill((((50 * level / 500) + 50), ((50 * level / 500) + 50), 0))
        elif level > 500:
            self.gas_surf.fill((200, 200, 0))

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
        return self.gas_level


class GasCloud:
    """
    this class describe the gas cloud separated by airplane
    """

    def __init__(self):
        self.positions = np.zeros((int(SCREEN_WIDTH / GAS_SIZE), int(SCREEN_HEIGHT / GAS_SIZE)), dtype=Gas)
        for x in range(int(SCREEN_WIDTH / GAS_SIZE)):
            for y in range(int(SCREEN_HEIGHT / GAS_SIZE)):
                self.positions[x, y] = Gas(x * GAS_SIZE, y * GAS_SIZE)
        self.critical = 500
        self.coverage = 0
        self.coverage_map = np.zeros((int(SCREEN_WIDTH / GAS_SIZE), int(SCREEN_HEIGHT / GAS_SIZE)), bool)

    def update(self, position_x, position_y, altitude):
        """
        This function add the density of gas pixel and altitude of a gas pixel
        :param altitude:
        :param position_x: int
        :param position_y: int
        :return: None
        """
        self.positions[int(position_x / GAS_SIZE), int(position_y / GAS_SIZE)].gas_level += 1000 / GAS_SIZE
        self.positions[int(position_x / GAS_SIZE), int(position_y / GAS_SIZE)].altitude = altitude

    def degrade_gas(self, screen, position_x, position_y):
        if position_x + 100 > 900:
            my_x_max = int(900 / GAS_SIZE) - 1
        else:
            my_x_max = int((position_x + 100) / GAS_SIZE)
        if position_x - 100 < 0:
            my_x_min = 0
        else:
            my_x_min = int((position_x - 100) / GAS_SIZE)
        if position_y + 100 > 900:
            my_y_max = int(900 / GAS_SIZE) - 1
        else:
            my_y_max = int((position_y + 100) / GAS_SIZE)
        if position_y - 100 < 0:
            my_y_min = 0
        else:
            my_y_min = int((position_y - 100) / GAS_SIZE)
        degradation = 1.25
        for x in range(my_x_min, my_x_max):
            for y in range(my_y_min, my_y_max):
                if self.positions[x, y].altitude > 50:
                    self.positions[x, y].gas_level /= degradation
                    self.positions[x, y].altitude /= degradation
                    if (
                        x != int(SCREEN_WIDTH / GAS_SIZE) - 1
                        and y != int(SCREEN_HEIGHT / GAS_SIZE) - 1
                        and x != 0
                        and y != 0
                    ):
                        self.positions[x - 1, y].gas_level += (self.positions[x, y].gas_level * (degradation - 1)) / 4
                        self.positions[x + 1, y].gas_level += (self.positions[x, y].gas_level * (degradation - 1)) / 4
                        self.positions[x, y - 1].gas_level += (self.positions[x, y].gas_level * (degradation - 1)) / 4
                        self.positions[x, y + 1].gas_level += (self.positions[x, y].gas_level * (degradation - 1)) / 4
                        self.positions[x - 1, y].altitude = self.positions[x, y].altitude
                        self.positions[x + 1, y].altitude = self.positions[x, y].altitude
                        self.positions[x, y - 1].altitude = self.positions[x, y].altitude
                        self.positions[x, y + 1].altitude = self.positions[x, y].altitude

                    self.draw(screen, x, y)

    def get_area_covered(self):
        """
        This function return area covered by GasCloud
        :return: int
        """

        return self.coverage

    def get_cloud_volume(self):
        """
        This function returns the total volume of gas separated
        :return:
        """
        total_volume = 0
        for x in range(int(SCREEN_WIDTH / GAS_SIZE)):
            for y in range(int(SCREEN_HEIGHT / GAS_SIZE)):
                total_volume += self.positions[x, y].gas_level
        return total_volume

    def draw(self, myscreen, position_x, position_y):
        x = [0, 1, -1, 0, 0]
        y = [0, 0, 0, 1, -1]
        for idx in range(5):
            X = position_x + x[idx]
            Y = position_y + y[idx]
            if self.positions[X, Y].gas_level != 0:
                self.positions[X, Y].set_color(self.positions[X, Y].gas_level)
                myscreen.blit(self.positions[X, Y].surf, self.positions[X, Y].rect)
                if self.positions[X, Y].gas_level > self.critical and not self.coverage_map[X, Y]:
                    print(self.positions[X, Y].gas_level)
                    self.coverage += GAS_SIZE * GAS_SIZE
                    self.coverage_map[X, Y] = True
                elif self.positions[X, Y].gas_level < self.critical and self.coverage_map[X, Y]:
                    self.coverage -= GAS_SIZE * GAS_SIZE
                    self.coverage_map[X, Y] = False
