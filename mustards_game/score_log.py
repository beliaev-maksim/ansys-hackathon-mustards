import json
import os

import pygame
from pygame.locals import K_ESCAPE
from pygame.locals import KEYDOWN
from pygame.locals import MOUSEBUTTONDOWN
from pygame.locals import QUIT


class ScoreLog:
    """
    this class defines the reading, writing, and displaying game score
    """

    def __init__(self):
        cwd_path = os.getcwd()
        self.sore_log_file = os.path.join(cwd_path, "score_log.json")

    def read_score(self):
        """
        this method reads the score in history, if not return none
        Returns:
            list

        """

        if not os.path.isfile(self.sore_log_file):
            return {"First": 0, "Second": 0, "Third": 0}
        else:
            json_file = open(self.sore_log_file)
            return json.load(json_file)

    def write_score(self, data):
        """
        this method write the current score into the score file,
        and return a list of current three scores history
        Args:
            data: int

        Returns:
            list

        """
        self.history_data = self.read_score()
        output = open(self.sore_log_file, "w")
        if data > self.history_data["First"]:
            self.history_data["Third"] = self.history_data["Second"]
            self.history_data["Second"] = self.history_data["First"]
            self.history_data["First"] = data
        elif self.history_data["First"] > data > self.history_data["Second"]:
            self.history_data["Third"] = self.history_data["Second"]
            self.history_data["Second"] = data
            self.history_data["First"] = self.history_data["First"]
        elif self.history_data["Second"] > data > self.history_data["Third"]:
            self.history_data["Third"] = data
        json.dump(self.history_data, output, indent=4)
        output.close()
        return self.history_data

    def display(self, screen):
        """
        this method display the scores to the user and give users the option to continue / end the game
        Args:
            screen: pygame.screen

        Returns:
            int: -1 as end the game, 1 as re-start the game

        """
        running = True
        output = 1  # 1 for continue the game, 0 for exit for the main menu, -1 for exit the game completely

        screen.fill((0, 0, 0))
        score_history_font = pygame.font.SysFont("monospace", 16)
        text1 = score_history_font.render(f"First: {self.history_data['First']} m²", True, (255, 0, 0))
        screen.blit(text1, (350, 300))
        text2 = score_history_font.render(f"Second: {self.history_data['Second']} m²", True, (255, 0, 0))
        screen.blit(text2, (350, 360))
        text3 = score_history_font.render(f"Third: {self.history_data['Third']} m²", True, (255, 0, 0))
        screen.blit(text3, (350, 420))

        re_start_button = pygame.Rect(270, 500, 300, 50)
        end_button = pygame.Rect(270, 600, 300, 50)
        pygame.draw.rect(screen, (255, 0, 0), re_start_button)
        pygame.draw.rect(screen, (255, 0, 0), end_button)
        menu_font = pygame.font.SysFont("monospace", 16)
        start_info = menu_font.render("Try again", True, (255, 255, 255))
        end_info = menu_font.render("End the game", True, (255, 255, 255))
        screen.blit(start_info, (360, 510))
        screen.blit(end_info, (350, 610))

        pygame.display.flip()

        while running:
            click_action = False
            mouse_x, mouse_y = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    # If the Esc key is pressed, then exit the main loop
                    if event.key == K_ESCAPE:
                        output = -1
                        running = False

                # Check for QUIT event. If QUIT, then set running to false.
                elif event.type == QUIT:
                    output = -1
                    running = False

                # Check for QUIT event. If QUIT, then set running to false.
                elif event.type == MOUSEBUTTONDOWN:
                    click_action = True

            if click_action:
                if re_start_button.collidepoint((mouse_x, mouse_y)):
                    output = 1
                    running = False
                elif end_button.collidepoint((mouse_x, mouse_y)):
                    output = -1
                    running = False
        return output
