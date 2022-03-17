import copy
from math import floor

import pygame
from pygame.locals import K_ESCAPE
from pygame.locals import KEYDOWN
from pygame.locals import MOUSEBUTTONDOWN
from pygame.locals import QUIT

import mustards_game.config
import mustards_game.obstacle
from mustards_game.background import Background
from mustards_game.background import Tileset
from mustards_game.config import INFO_WIDTH
from mustards_game.config import MAX_ALTITUDE
from mustards_game.config import SCREEN_HEIGHT
from mustards_game.config import SCREEN_WIDTH
from mustards_game.obstacle import Obstacle
from mustards_game.score_log import ScoreLog
from mustards_game.ufo import UFO


class GameDisplay:
    def __init__(self, image):

        self.screen = pygame.display.set_mode((SCREEN_WIDTH + INFO_WIDTH, SCREEN_HEIGHT))
        self.screen.fill((0, 0, 0))

        self.game_background = image
        self.screen.blit(image, (0, 0))

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
    tileset = Tileset("sprites/Grass_01_LQ.png", size=(128, 128))

    m = int(floor(SCREEN_WIDTH / tileset.size[0]) + 1)
    n = int(floor(SCREEN_HEIGHT / tileset.size[1]) + 1)
    background = Background(tileset, size=(m, n))
    background.render()

    # game & info initiate
    display = GameDisplay(image=background.image)

    # font texts
    altitude_font = pygame.font.SysFont("monospace", 16)
    fuel_font = pygame.font.SysFont("monospace", 16)
    score_font = pygame.font.SysFont("monospace", 16)

    # game objects
    ufo = UFO(MAX_ALTITUDE, SCREEN_WIDTH, SCREEN_HEIGHT)
    gas = ufo.gas_cloud
    mustards_game.obstacle.OBSTACLES = copy.deepcopy(mustards_game.config._OBST_REF)
    mustards_game.obstacle.NOT_OBSTACLES = copy.deepcopy(mustards_game.config._NOT_OBST_REF)
    obstacles = pygame.sprite.Group()
    humans = pygame.sprite.Group()
    pos_obstacles = [(0, 0)]

    for i in range(mustards_game.config.n_obstacles):
        new_obstacle = Obstacle()
        obstacles.add(new_obstacle)
        pos_obstacles.append(new_obstacle.randomize_pos(pos_obstacles))

    for i in range(mustards_game.config.n_humans):
        new_human = Obstacle(False)
        humans.add(new_human)
        pos_obstacles.append(new_human.randomize_pos(pos_obstacles))

    # Draw static map / obstacles background on screen
    for obstacle in obstacles:
        display.game_display(obstacle.surf, obstacle.rect)
        height = altitude_font.render(f"{obstacle.height}m", True, (255, 255, 255))
        display.game_display(height, (obstacle.pos[0], obstacle.pos[1]))

    for human in humans:
        display.game_display(human.surf, human.rect)

    run_time = 0
    # game run
    running = True
    while running:
        clock = pygame.time.Clock()  # Ensure program maintains a rate of 30 frames per second
        clock.tick(180)

        # Draw moving objects on screen
        ufo.fly()
        pressed_keys = pygame.key.get_pressed()
        ufo.change_altitude(pressed_keys)
        ufo.change_direction(pressed_keys)

        if ufo.fuel <= 0:
            # when we are out of fuel, start to decrease altitude
            ufo.altitude -= 1

        if ufo.check_hit_wall() or ufo.altitude <= 25:
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

        # Draw the gas cloud
        gas.degrade_gas(display.screen, ufo.current_pos_x, ufo.current_pos_y)

        # Draw UFO on the screen at the last step. It must overlay other objects
        display.game_display(ufo.surf, ufo.rect)

        # Check collision with obstacles
        obstacle_collided = pygame.sprite.spritecollide(ufo, obstacles, False, pygame.sprite.collide_mask)
        if obstacle_collided and obstacle_collided[0].height >= ufo.altitude:
            running = False
            print("Collision with an obstacle! GAME OVER!")

        if run_time % 20 == 0:
            # Display information
            display.info_display_update()  # update the info board section

            text = altitude_font.render(f"Altitude: {ufo.altitude} m", True, (255, 0, 0))
            display.info_display(text, (SCREEN_WIDTH, 20))

            fuel = fuel_font.render(f"Fuel left: {ufo.fuel}L", True, (255, 255, 255))
            display.info_display(fuel, (SCREEN_WIDTH, 80))

            score = score_font.render(f"Lethalcoverage: {gas.get_area_covered} m²", True, (255, 255, 255))
            display.info_display(score, (SCREEN_WIDTH, 140))

            # redraw obstacle heights to be always on top of the gas
            for obstacle in obstacles:
                height = altitude_font.render(f"{obstacle.height}m", True, (255, 255, 255))
                display.game_display(height, (obstacle.pos[0], obstacle.pos[1]))

        # Game & info display update
        display.update()
        run_time += 1

    return gas.get_area_covered, display.screen


def main_menu(running=True):
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
        end_info = menu_font.render("Exit the game", True, (255, 255, 255))
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

        response = None
        while (click_action and re_start_button.collidepoint((mouse_x, mouse_y))) or response == 1:
            # mouse clicks the start session button
            score, screen = main_game()
            SL = ScoreLog()
            history_score = SL.read_score()
            if not history_score:
                print("You have done great!")
            elif score < int(history_score["Third"]):
                print("Your result is not in the top 3 score. Try again!")
            elif int(history_score["First"]) > score > int(history_score["Third"]):
                print("Nice, you are in the top score list!")
            else:
                print("You have a new record!")
            SL.write_score(score)
            response = SL.display(screen)
            if response == -1:
                click_action = False
                running = False
            elif response == 0:
                click_action = False

        if click_action and end_button.collidepoint((mouse_x, mouse_y)):
            # mouse clicks the end session button
            running = False

        pygame.display.flip()
    pygame.quit()


def start_screen():
    start_game = True
    clock = pygame.time.Clock()  # Ensure program maintains a rate of 30 frames per second
    clock.tick(180)

    screen = pygame.display.set_mode((SCREEN_WIDTH + INFO_WIDTH, SCREEN_HEIGHT))
    screen.fill((0, 0, 0))

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                running = False

                # Check for QUIT event. If QUIT, then set running to false.
            elif event.type == QUIT:
                start_game = False
                running = False

                # Check for click the buttons
            elif event.type == MOUSEBUTTONDOWN:
                running = False

        pos_x = int(SCREEN_WIDTH / 2.5)
        pos_y = 100
        fontsize = int(SCREEN_WIDTH / 50)
        font = pygame.font.SysFont("monospace", fontsize)
        text = [
            "Welcome comrade! ",
            "",
            "Congratulations on joining the Mustards,",
            "an anarcho-syndicalist commune! We know that your path was ",
            "not easy, but you are finally here, and your first job is ",
            "waiting for you. Are you ready to prove your worthiness? ",
            "As you know, our goal is to establish a new, fair world ",
            "order. Unfortunately, not everyone shares our vision and ",
            "agrees with our genius, this is why we need to put all our ",
            "efforts in persuading them. In doing so, we have to resort ",
            "to... certain methods. So strap in and get ready to lift ",
            "your flying saucer.",
            "",
            "Your mission is to carry out commercial flights. On the ",
            "route your flying saucer will leave chemtrails - clouds of our ",
            "special gas that helps us control the minds of everyone who ",
            "had contact with it. Fly over most populated areas and make ",
            "sure to cover as much ground as possible. Keep an eye on the ",
            "dashboard on the right, there you can see how much ground has ",
            "been covered with a lethal dose of the gas, as well as your ",
            "current altitude and the amount of fuel left. Beware of the ",
            "obstacles, you can fly over them if your altitude is high ",
            "enough, but keep in mind, that flying high also consumes more ",
            "fuel! The higher you fly, less dense will be the gas on the ",
            "ground, you may need to fly over the same area twice to ",
            "increase the density. To control the direction of the ",
            "flying saucer use right and left arrows on your keyboard, use",
            "up and down arrows to increase and decrease your altitude. ",
            "",
            "Good luck and may the mustard be with you!",
            "",
            "",
            "",
            "",
            "press any key to continue...",
        ]
        i = 0
        for line in text:
            img = font.render(line, True, (255, 255, 255))
            screen.blit(img, (pos_x, pos_y + fontsize * i))
            i = i + 1

        pygame.display.flip()
    return start_game


if __name__ == "__main__":
    pygame.init()
    run_game = start_screen()
    main_menu(run_game)
