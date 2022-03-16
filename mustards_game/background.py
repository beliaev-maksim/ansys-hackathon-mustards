import numpy as np
import pygame


class Tileset:
    """Class contains images with tiles."""

    def __init__(self, file, size=(512, 512), margin=0, spacing=0):
        """

        Parameters
        ----------
        file: str: path to the image with tiles
        size: tuple of ints: size of each tile in pixels
        margin: int: number of margin pixels in the image
        spacing: int: number of pixels between the tiles
        """
        self.file = file
        self.size = size
        self.margin = margin
        self.spacing = spacing
        self.image = pygame.image.load(file)
        self.rect = self.image.get_rect()
        self.tiles = []
        self.load()

    def load(self):
        self.tiles = []
        x0 = y0 = self.margin
        w, h = self.rect.size
        dx = self.size[0] + self.spacing
        dy = self.size[1] + self.spacing

        for x in range(x0, w, dx):
            for y in range(y0, h, dy):
                tile = pygame.Surface(self.size)
                tile.blit(self.image, (0, 0), (x, y, *self.size))
                self.tiles.append(tile)


class Background:
    """Class creates an image by combining different tiles."""

    def __init__(self, tileset, size=(4, 4)):
        """

        Parameters
        ----------
        tileset: object of class Tileset with loaded tiles
        size: tuple of int: number of tiles to combine in each direction
        """
        self.size = size
        self.tilesize = tileset.size
        self.map = np.zeros(size, dtype=int)
        self.tileset = tileset

        h, w = self.size
        self.image = pygame.Surface((self.tilesize[0] * w, self.tilesize[1] * h))
        self.rect = self.image.get_rect()

    def render(self):
        m, n = self.map.shape
        for i in range(m):
            for j in range(n):
                tile = self.tileset.tiles[self.map[i, j]]
                self.image.blit(tile, (j * self.tilesize[0], i * self.tilesize[1]))

    def set_all_zero(self):
        """
        Creates a map filled with zeros, thus putting tile number 0 from the tileset in all positions.
        """
        self.map = np.zeros(self.size, dtype=int)
        self.render()
