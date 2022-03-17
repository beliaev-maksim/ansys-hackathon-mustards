import pygame

from mustards_game.config import INFO_WIDTH
from mustards_game.config import SCREEN_HEIGHT
from mustards_game.config import SCREEN_WIDTH


class GameDisplay:
    """Class of methods to display the game and info section in a pygame screen."""

    def __init__(self, image):

        self.screen = pygame.display.set_mode((SCREEN_WIDTH + INFO_WIDTH, SCREEN_HEIGHT))
        self.screen.fill((0, 0, 0))

        self.game_background = image
        self.screen.blit(image, (0, 0))

        self.info_board = pygame.Surface((INFO_WIDTH, SCREEN_HEIGHT))
        self.info_board.fill((0, 0, 125))
        self.info_board_rect = self.info_board.get_rect()

    def game_display_update(self):
        """Update the content in the game section."""
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.game_background, (0, 0))

    def game_display(self, obj, pos):
        """Display at the game section with the object at the position provided.

        Parameters
        ----------
        obj : pygame.surf
        pos : (int, int)

        Returns
        -------

        """
        self.screen.blit(obj, pos)

    def info_display_update(self):
        """Update the content in the information section."""
        self.screen.blit(self.info_board, (SCREEN_WIDTH, 0))

    def info_display(self, obj, pos):
        """Display at the information section with the content at the position provided.

        Parameters
        ----------
        obj : pygame.font
        pos : (int, int)

        Returns
        -------

        """
        self.screen.blit(obj, pos)

    def update(self):
        """Function to update current display screen."""
        pygame.display.flip()
