import math

import numpy as np
import pygame
from pygame.locals import K_DOWN
from pygame.locals import K_ESCAPE
from pygame.locals import K_LEFT
from pygame.locals import K_RIGHT
from pygame.locals import K_UP
from pygame.locals import KEYDOWN
from pygame.locals import MOUSEBUTTONDOWN
from pygame.locals import QUIT

from mustards_game.background import Background
from mustards_game.background import Tileset
from mustards_game.gas_cloud import GasCloud
from mustards_game.obstacle import Obstacle
from mustards_game.score_log import ScoreLog

# Define constants for the screen width and height
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900
INFO_WIDTH = 500

MAX_ALTITUDE = 1000


class UFO(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.size = 25
        self.surf = pygame.image.load("ufo_25.png").convert_alpha()
        self.rect = self.surf.get_rect()
        self.direction = (0, 1)
        self.altitude = 500

        self.gas_cloud = GasCloud()
        self.current_pos_x = 0
        self.current_pos_y = 0
        self.fuel = 10000

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
            or self.rect.right > SCREEN_WIDTH
            or self.rect.top <= 0
            or self.rect.bottom >= SCREEN_HEIGHT
        ):
            return True
        return False

    def change_direction(self, pressed_keys):
        """Rotate airplain based on LEFT or RIGHT key pressed.

        :param pressed_keys:
        :return:
        """
        # https://stackoverflow.com/questions/4183208/how-do-i-rotate-an-image-around-its-center-using-pygame

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
                if self.altitude <= MAX_ALTITUDE:
                    self.altitude += 1
                    self.consume_fuel()

    def check_collide(self, obj_rect):
        x, y = self.rect.center
        X, Y = obj_rect.center
        distance = math.hypot(X - x, Y - y)

        if distance < 1.5 * (25 + obj_rect.height):
            return True
        else:
            return False


class GameDisplay:
    def __init__(self, image):

        self.screen = pygame.display.set_mode((SCREEN_WIDTH + INFO_WIDTH, SCREEN_HEIGHT))
        self.screen.fill((0, 0, 0))

        self.game_background = image
        self.screen.blit(image, (0, 0))
        # self.game_background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        # self.game_background.fill((0, 0, 0))
        # self.game_background_rect = self.game_background.get_rect()

        self.info_board = pygame.Surface((INFO_WIDTH, SCREEN_HEIGHT))
        self.info_board.fill((0, 0, 125))
        self.info_board_rect = self.info_board.get_rect()

    def game_display_update(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.game_background, (0, 0))

    def game_display(self, obj, pos):
        self.screen.blit(obj, pos)

    def info_display_update(self):
        self.screen.blit(self.info_board, (SCREEN_WIDTH, 0))

    def info_display(self, obj, pos):
        self.screen.blit(obj, pos)

    def update(self):
        pygame.display.flip()


def main_game():
    # pygame.init()

    tileset = Tileset("Grass_01_LQ.png", size=(128, 128))

    m = int(np.floor(SCREEN_WIDTH / tileset.size[0]) + 1)
    n = int(np.floor(SCREEN_HEIGHT / tileset.size[1]) + 1)
    background = Background(tileset, size=(m, n))
    background.render()

    # game & info initiate
    display = GameDisplay(image=background.image)

    # font texts
    altitude_font = pygame.font.SysFont("monospace", 16)
    fuel_font = pygame.font.SysFont("monospace", 16)
    score_font = pygame.font.SysFont("monospace", 16)

    # game objects
    ufo = UFO()
    gas = ufo.gas_cloud
    obstacles = pygame.sprite.Group()
    n_obstacle = 5
    for i in range(0, n_obstacle):
        new_obstacle = Obstacle()
        obstacles.add(new_obstacle)

    ################################
    # Draw static map / obstacles background on screen
    for obstacle in obstacles:
        display.game_display(obstacle.surf, obstacle.rect)
        height = altitude_font.render(f"{obstacle.height}m", True, (255, 255, 255))
        display.game_display(height, (obstacle.pos[0], obstacle.pos[1]))

    run_time = 0
    # game run
    running = True
    while running:
        clock = pygame.time.Clock()  # Ensure program maintains a rate of 30 frames per second
        clock.tick(180)

        # if run_time % 20 == 0:
        #    display.game_display_update()  # update the game section

        ################################
        # Draw moving objects on screen
        ufo.fly()
        pressed_keys = pygame.key.get_pressed()
        ufo.change_altitude(pressed_keys)
        ufo.change_direction(pressed_keys)

        if ufo.fuel <= 0:
            # when we are out of fuel, start to decrease altitude
            ufo.altitude -= 5

        if ufo.check_hit_wall() or ufo.altitude <= 0:
            # game over
            print("UFO crashed! Game Over!")
            running = False

        # for loop through the event queue
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                # If the Esc key is pressed, then exit the main loop
                if event.key == K_ESCAPE:
                    running = False

            # Check for QUIT event. If QUIT, then set running to false.
            elif event.type == QUIT:
                running = False

        # Update obstacle if not collision
        for obstacle in obstacles:
            if ufo.check_collide(obstacle.rect):
                display.game_display(obstacle.surf, obstacle.rect)
                height = altitude_font.render(f"{obstacle.height}m", True, (255, 255, 255))
                display.game_display(height, (obstacle.pos[0], obstacle.pos[1]))

        # Draw the gas cloud
        gas.degrade_gas(display.screen, ufo.current_pos_x, ufo.current_pos_y)

        # Draw UFO on the screen at the last step. It must overlay other objects
        display.game_display(ufo.surf, ufo.rect)

        # Check collision with obstacles
        obstacle_collided = pygame.sprite.spritecollide(ufo, obstacles, False)
        if obstacle_collided and obstacle_collided[0].height >= ufo.altitude:
            running = False
            print("Collision with an obstacle! GAME OVER!")

        if run_time % 20 == 0:
            ################################
            # Display information
            display.info_display_update()  # update the info board section

            text = altitude_font.render(f"Altitude: {ufo.altitude} m", True, (255, 0, 0))
            display.info_display(text, (SCREEN_WIDTH, 20))

            fuel = fuel_font.render(f"Fuel left: {ufo.fuel}L", True, (255, 255, 255))
            display.info_display(fuel, (SCREEN_WIDTH, 80))

            score = score_font.render(f"Lethalcoverage: {gas.get_area_covered()} m²", True, (255, 255, 255))
            display.info_display(score, (SCREEN_WIDTH, 140))

        ################################
        # Game & info display update
        display.update()  # Update the display
        run_time += 1

    SL = ScoreLog()
    history_score = SL.read_score()
    if not history_score:
        print("you have done great")
    elif gas.get_area_covered() < int(history_score[2]):
        print("please continue")
    elif int(history_score[0]) > gas.get_area_covered() > int(history_score[2]):
        print("nice, you are in list")
    else:
        print("you have new record")
    SL.write_score(gas.get_area_covered())
    SL.display(display.screen)


def main_menu():
    pygame.init()
    running = True
    while running:
        clock = pygame.time.Clock()  # Ensure program maintains a rate of 30 frames per second
        clock.tick(180)

        screen = pygame.display.set_mode((SCREEN_WIDTH + INFO_WIDTH, SCREEN_HEIGHT))
        screen.fill((0, 0, 0))

        re_start_button = pygame.Rect((SCREEN_WIDTH + INFO_WIDTH) // 2 - 100, SCREEN_HEIGHT // 2 - 100, 200, 50)
        end_button = pygame.Rect((SCREEN_WIDTH + INFO_WIDTH) // 2 - 100, SCREEN_HEIGHT // 2, 200, 50)
        pygame.draw.rect(screen, (255, 0, 0), re_start_button)
        pygame.draw.rect(screen, (255, 0, 0), end_button)
        menu_font = pygame.font.SysFont("monospace", 16)
        start_info = menu_font.render("Start the game", True, (255, 255, 255))
        end_info = menu_font.render("End the game", True, (255, 255, 255))
        screen.blit(start_info, ((SCREEN_WIDTH + INFO_WIDTH) // 2 - 75, SCREEN_HEIGHT // 2 - 88))
        screen.blit(end_info, ((SCREEN_WIDTH + INFO_WIDTH) // 2 - 75, SCREEN_HEIGHT // 2 + 12))

        click_action = False
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # for loop through the event queue
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                # If the Esc key is pressed, then exit the main loop
                if event.key == K_ESCAPE:
                    running = False

            # Check for QUIT event. If QUIT, then set running to false.
            elif event.type == QUIT:
                running = False

            # Check for click the buttons
            elif event.type == MOUSEBUTTONDOWN:
                click_action = True

        if click_action and re_start_button.collidepoint((mouse_x, mouse_y)):
            # mouse clicks the start session button
            main_game()
        elif click_action and end_button.collidepoint((mouse_x, mouse_y)):
            # mouse clicks the end session button
            running = False

        pygame.display.flip()


if __name__ == "__main__":

    main_menu()
