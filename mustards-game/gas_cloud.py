import pygame


# Define constants for the screen width and height
GAS_SIZE = 25


class Gas:
    """
    this class structure describes the information of each gas pixel
    """
    def __init__(self, position_x, position_y):
        # position information
        self.gas_position_x = position_x
        self.gas_position_y = position_y
        # gas density information 128 as default starting value
        self.gas_level = 255

        # pygame objects
        self.gas_surf = pygame.Surface((GAS_SIZE, GAS_SIZE))
        self.gas_surf.fill((self.gas_level, 255, self.gas_level))

        self.gas_rect = self.gas_surf.get_rect()
        self.gas_rect.move_ip(self.gas_position_x, self.gas_position_y)

    def increase_level(self):
        """
        increase the gas level/density. update the color of pygame surf
        :return: None
        """
        if self.gas_level < 100:
            return
        self.gas_level -= 100
        print(self.gas_level)
        self.gas_surf.fill((self.gas_level, 255, self.gas_level))
        self.gas_rect = self.gas_surf.get_rect()
        self.gas_rect.move_ip(self.gas_position_x, self.gas_position_y)

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


class GasCloud():
    """
    this class describe the gas cloud separated by airplane
    """
    def __init__(self):
        self.positions = {tuple([0, 0]): Gas(0, 0)}

    def update(self, position_x, position_y):
        """
        This function add new gas pixel to the GasCloud / update the density of gas pixel
        :param position_x: int
        :param position_y: int
        :return: None
        """
        if tuple([position_x, position_y]) not in self.positions:

            self.positions[tuple([position_x, position_y])] = Gas(position_x, position_y)
        else:
            print("here is over lap")
            self.positions[tuple([position_x, position_y])].increase_level()

    def get_area_covered(self):
        """
        This function return area covered by GasCloud
        :return: int
        """
        return len(self.positions)

    def get_cloud_volume(self):
        """
        This function returns the total volume of gas separated
        :return:
        """
        total_volume = 0
        for position in self.positions:
            total_volume += self.positions[position].level
        return total_volume

    def positions(self):
        """
        this function returns dictionary of gas pixels
        :return: dict
        """
        return self.positions
