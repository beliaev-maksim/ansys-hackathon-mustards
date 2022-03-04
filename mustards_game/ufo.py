import math

import pygame
from pygame.locals import K_DOWN
from pygame.locals import K_ESCAPE
from pygame.locals import K_LEFT
from pygame.locals import K_RIGHT
from pygame.locals import K_UP
from pygame.locals import KEYDOWN
from pygame.locals import QUIT

from mustards_game.gas_cloud import GasCloud
from mustards_game.obstacle import Obstacle

# Define constants for the screen width and height
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900


class UFO(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((25, 25))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.direction = (0, 1)
        self.altitude = 500

        self.gas_cloud = GasCloud()
        self.current_pos_x = 0
        self.current_pos_y = 0

    def fly(self):
        # Store new float position
        self.current_pos_x += self.direction[0]
        self.current_pos_y += self.direction[1]

        # Compare new float position with the actual position of the rect
        # If new position differs by more than 1 pixel, move the rect
        move_x = int(self.current_pos_x - self.rect.left)
        move_y = int(self.current_pos_y - self.rect.top)
        self.rect.move_ip(move_x, move_y)

        self.gas_cloud.update(self.current_pos_x, self.current_pos_y, self.altitude)

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

    def rotate(self, pressed_keys):
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
            if self.altitude <= 1999:
                self.altitude += 1


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    altitude_font = pygame.font.SysFont("monospace", 16)
    n_obstacle = 5
    ufo = UFO()
    # Create sprite group of obstacles
    obstacles = pygame.sprite.Group()
    score_font = pygame.font.SysFont("monospace", 16)
    gas_density_font = pygame.font.SysFont("monospace", 16)
    for i in range(0, n_obstacle):
        new_obstacle = Obstacle()
        obstacles.add(new_obstacle)

    running = True
    while running:
        # Ensure program maintains a rate of 30 frames per second
        clock = pygame.time.Clock()
        clock.tick(180)

        ufo.fly()
        if ufo.check_hit_wall() or ufo.altitude <= 0:
            # game over
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

        pressed_keys = pygame.key.get_pressed()
        ufo.change_altitude(pressed_keys)
        ufo.rotate(pressed_keys)

        # Fill the screen with black
        screen.fill((0, 0, 0))

        text = altitude_font.render(f"Altitude: {ufo.altitude}m", True, (255, 0, 0))
        screen.blit(text, (20, 20))

        # Draw the gas cloud
        gas = ufo.gas_cloud
        gas.draw(screen)
        gas.degrade_gas()
        score = score_font.render(f"Lethalcoverage: {gas.get_area_covered()}", True, (255, 255, 255))
        screen.blit(score, (500, 20))
        for item in gas.gas_density:
            gas_density = gas_density_font.render(
                f"area with density over{item}: {gas.gas_density[item]}",
                True,
                (255, 255 / math.log10(item), 255 / math.log10(item)),
            )
            screen.blit(gas_density, (500, 15 * math.log10(item) + 30))

        # Draw obstacle on screen
        for obstacle in obstacles:
            screen.blit(obstacle.surf, obstacle.rect)
            height = altitude_font.render(f"{obstacle.height}m", True, (255, 255, 255))
            screen.blit(height, (obstacle.pos[0], obstacle.pos[1]))

        # Draw the ufo on the screen
        screen.blit(ufo.surf, ufo.rect)

        # Check collision with obstacles
        obstacle_collided = pygame.sprite.spritecollide(ufo, obstacles, False)
        if obstacle_collided and obstacle_collided[0].height >= ufo.altitude:
            running = False
            print("Collision with an obstacle! GAME OVER!")

        # Update the display
        pygame.display.flip()


if __name__ == "__main__":

    main()
