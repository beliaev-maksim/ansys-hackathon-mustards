import pygame
from pygame.locals import K_DOWN
from pygame.locals import K_ESCAPE
from pygame.locals import K_LEFT
from pygame.locals import K_RIGHT
from pygame.locals import K_UP
from pygame.locals import KEYDOWN
from pygame.locals import QUIT
from gas_cloud import GasCloud

# Define constants for the screen width and height
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900


class Airplain(pygame.sprite.Sprite):
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
        x = self.direction[0] * 1
        y = self.direction[1] * 1
        self.rect.move_ip(x, y)

        self.current_pos_x += self.direction[0]
        self.current_pos_y += self.direction[1]
        self.gas_cloud.update(self.current_pos_x, self.current_pos_y)


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
        if pressed_keys[K_LEFT]:
            if self.direction == (1, 0):
                self.direction = (0, -1)
            elif self.direction == (0, -1):
                self.direction = (-1, 0)
            elif self.direction == (-1, 0):
                self.direction = (0, 1)
            elif self.direction == (0, 1):
                self.direction = (1, 0)

        elif pressed_keys[K_RIGHT]:
            if self.direction == (1, 0):
                self.direction = (0, 1)
            elif self.direction == (0, 1):
                self.direction = (-1, 0)
            elif self.direction == (-1, 0):
                self.direction = (0, -1)
            elif self.direction == (0, -1):
                self.direction = (1, 0)

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
    airplain = Airplain()

    running = True
    while running:
        # Ensure program maintains a rate of 30 frames per second
        clock = pygame.time.Clock()
        clock.tick(180)

        airplain.fly()
        if airplain.check_hit_wall() or airplain.altitude <= 0:
            # game over
            running = False

        # for loop through the event queue
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                # Get all the keys currently pressed, do it inside keydown event
                # to ensure a single click if user holds the button
                pressed_keys = pygame.key.get_pressed()
                # Update the airplain sprite based on user keypresses
                airplain.rotate(pressed_keys)

                # If the Esc key is pressed, then exit the main loop
                if event.key == K_ESCAPE:
                    running = False

            # Check for QUIT event. If QUIT, then set running to false.
            elif event.type == QUIT:
                running = False

        pressed_keys = pygame.key.get_pressed()
        airplain.change_altitude(pressed_keys)

        # Fill the screen with black
        screen.fill((0, 0, 0))

        text = altitude_font.render(f"Altitude: {airplain.altitude}m", True, (255, 0, 0))
        screen.blit(text, (20, 20))

        # Draw the airplain on the screen
        screen.blit(airplain.surf, airplain.rect)

        # Draw the gas cloud
        gas_positions = airplain.gas_cloud.positions
        for gas_position in gas_positions:
            gas = gas_positions[gas_position]
            # print(gas.position_x, gas.position_y, gas.level)
            screen.blit(gas.surf, gas.rect)

        # Update the display
        pygame.display.flip()


if __name__ == "__main__":

    main()
