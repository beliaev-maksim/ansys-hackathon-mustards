import pygame
from numpy import zeros

from mustards_game.config import SCREEN_HEIGHT
from mustards_game.config import SCREEN_WIDTH

# Define constants for the screen width and height
GAS_SIZE = 5


class Gas:
    """
    this class structure describes the information of each gas pixel
    """

    def __init__(self, position_x, position_y):
        # position information
        self.gas_position_x = position_x
        self.gas_position_y = position_y
        # gas density information 128 as default starting value
        self.gas_level = 0.0
        self.altitude = 0
        # pygame objects
        self.gas_surf = pygame.Surface((GAS_SIZE, GAS_SIZE))
        self.gas_surf.set_colorkey((0, 0, 0))

        self.gas_rect = self.gas_surf.get_rect()
        self.gas_rect.move_ip(self.gas_position_x, self.gas_position_y)

    def set_color(self, level):
        """Function to define the color of a gas pixel based on its level.
        
        Parameters
        ----------
        level : float
           Current gas level.

        """
        if 30 < level < 100:
            self.gas_surf.fill((50 * level / 100, 50 * level / 100, 0))
        elif 100 < level < 100 * GAS_SIZE:
            self.gas_surf.fill((((50 * level / (100 * GAS_SIZE)) + 50), ((50 * level / (100 * GAS_SIZE)) + 50), 0))
        elif level > 100 * GAS_SIZE:
            self.gas_surf.fill((200, 200, 0))


class GasCloud:
    """
    this class describe the gas cloud created by Ufo
    """

    def __init__(self):
        self.positions = zeros((int(SCREEN_WIDTH / GAS_SIZE), int(SCREEN_HEIGHT / GAS_SIZE)), dtype=Gas)
        for x in range(int(SCREEN_WIDTH / GAS_SIZE)):
            for y in range(int(SCREEN_HEIGHT / GAS_SIZE)):
                self.positions[x, y] = Gas(x * GAS_SIZE, y * GAS_SIZE)
        self.critical = 100 * GAS_SIZE
        self.coverage = 0
        self.coverage_map = zeros((int(SCREEN_WIDTH / GAS_SIZE), int(SCREEN_HEIGHT / GAS_SIZE)), bool)

    def update(self, position_x, position_y, altitude):
        """
        This function add the density of gas pixel and altitude of a gas pixel
        Parameters
        ----------
        position_x: int
        position_y: int
        altitude: int

        Returns
        -------

        """
        self.positions[int(position_x / GAS_SIZE), int(position_y / GAS_SIZE)].gas_level += 2500 / GAS_SIZE
        self.positions[int(position_x / GAS_SIZE), int(position_y / GAS_SIZE)].altitude += altitude

    def degrade_gas(self, screen, position_x, position_y):
        """
        function draw and distribute the Gas by pushing parts of its density to the direct neighbouring pixel
        the gas degradation and drawing is limited to a 200x200 square around the given position
        Parameters
        ----------
        screen: pygame.display
            current displayed screen
        position_x: int
        position_y: int

        Returns
        -------

        """
        if position_x + 100 > SCREEN_WIDTH:
            my_x_max = int(SCREEN_WIDTH / GAS_SIZE) - 1
        else:
            my_x_max = int((position_x + 100) / GAS_SIZE)
        if position_x - 100 < 0:
            my_x_min = 0
        else:
            my_x_min = int((position_x - 100) / GAS_SIZE)
        if position_y + 100 > SCREEN_HEIGHT:
            my_y_max = int(SCREEN_HEIGHT / GAS_SIZE) - 1
        else:
            my_y_max = int((position_y + 100) / GAS_SIZE)
        if position_y - 100 < 0:
            my_y_min = 0
        else:
            my_y_min = int((position_y - 100) / GAS_SIZE)
        degradation = 1.25
        for x in range(my_x_min, my_x_max):
            for y in range(my_y_min, my_y_max):
                if self.positions[x, y].altitude > 25:
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
        Returns: int
            Area covered
        -------
        """
        return self.coverage

    def draw(self, screen, position_x, position_y):
        """
        function to draw the gas cloud and Compute the coverage
        draw the pixel and its direct neighbours
        Parameters
        ----------
        screen: pygame.display
            current displayed screen
        position_x: int
        position_y: int

        Returns
        -------

        """
        x = [0, 1, -1, 0, 0]
        y = [0, 0, 0, 1, -1]
        for idx in range(5):
            X = position_x + x[idx]
            Y = position_y + y[idx]
            if self.positions[X, Y].gas_level != 0:
                self.positions[X, Y].set_color(self.positions[X, Y].gas_level)
                screen.blit(self.positions[X, Y].gas_surf, self.positions[X, Y].gas_rect)
                if self.positions[X, Y].gas_level > self.critical and not self.coverage_map[X, Y]:
                    self.coverage += GAS_SIZE * GAS_SIZE
                    self.coverage_map[X, Y] = True
                elif self.positions[X, Y].gas_level < self.critical and self.coverage_map[X, Y]:
                    self.coverage -= GAS_SIZE * GAS_SIZE
                    self.coverage_map[X, Y] = False
