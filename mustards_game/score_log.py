import os

import pygame
from pygame.locals import K_ESCAPE
from pygame.locals import KEYDOWN
from pygame.locals import MOUSEBUTTONDOWN
from pygame.locals import QUIT

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900
INFO_WIDTH = 500


class ScoreLog:
    def __init__(self):
        cwd_path = os.getcwd()
        self.sore_log_file = os.path.join(cwd_path, "score_log.txt")

    def read_score(self):
        if not os.path.isfile(self.sore_log_file):
            return None
        else:
            with open(self.sore_log_file, "r") as input:
                data = input.readlines()
                return data

    def write_score(self, data):
        self.new_history = []
        history_data = self.read_score()
        if not history_data:
            output = open(self.sore_log_file, "w")
            output.write(str(data) + "\n")
            output.write("0\n")
            output.write("0\n")
            self.new_history = [data, 0, 0]
            output.close()
        else:
            first = int(history_data[0])
            second = int(history_data[1])
            third = int(history_data[2])
            output = open(self.sore_log_file, "w")
            if data > first:
                output.write(str(data) + "\n")
                output.write(str(first) + "\n")
                output.write(str(second) + "\n")
                self.new_history = [data, first, second]
            elif first > data > second:
                output.write(str(first) + "\n")
                output.write(str(data) + "\n")
                output.write(str(second) + "\n")
                self.new_history = [first, data, second]
            elif second > data > third:
                output.write(str(first) + "\n")
                output.write(str(second) + "\n")
                output.write(str(data) + "\n")
                self.new_history = [first, second, data]
            else:
                output.write(str(first) + "\n")
                output.write(str(second) + "\n")
                output.write(str(third) + "\n")
                self.new_history = [first, second, third]
            output.close()
        return self.new_history

    def display(self, screen):
        running = True
        output = 1  # 1 for continue the game, 0 for exit for the main menu, -1 for exit the game completely

        screen.fill((0, 0, 0))
        score_history_font = pygame.font.SysFont("monospace", 16)
        text1 = score_history_font.render(f"First: {self.new_history[0]} m²", True, (255, 0, 0))
        screen.blit(text1, (350, 300))
        text2 = score_history_font.render(f"Second: {self.new_history[1]} m²", True, (255, 0, 0))
        screen.blit(text2, (350, 360))
        text3 = score_history_font.render(f"Third: {self.new_history[2]} m²", True, (255, 0, 0))
        screen.blit(text3, (350, 420))

        re_start_button = pygame.Rect(270, 500, 400, 50)
        pygame.draw.rect(screen, (255, 0, 0), re_start_button)
        menu_font = pygame.font.SysFont("monospace", 16)
        start_info = menu_font.render("Do you want to restart the game?", True, (255, 255, 255))
        screen.blit(start_info, (300, 510))

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
                else:
                    output = 0
                    running = False
        return output
