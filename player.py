# player.py 

import pygame

# Creates a class for the player and attributes
class Player:
    def __init__(self, x, y, width, height):  # Define initial properties of the player
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.max_health = 100
        self.current_health = 100
        self.max_stamina = 100
        self.current_stamina = 100
        self.stamina_recovery_rate = 0.01
        self.max_power = 100
        self.current_power = 0
        self.speed = 5  # Define player's speed
        self.frame = 0
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.moving_northeast = False
        self.moving_northwest = False
        self.moving_southeast = False
        self.moving_southwest = False
        self.dash_speed = 10  # A faster speed for dashing
        self.dashing = False  # Indicates whether the player is currently dashing

        # Checks files for images to use when player moves in a particular direction
        try:
            self.images = {
                # The animation of each direction should cycle through different files
                # with each file in the set differing only by the last number
                # We would have to put all of the files in the brackets if we do not have a common last number
                # Below, I'm assuming we use 4 images for each direction. The more sprites we use, the more detail we have.
                "up": [pygame.image.load('path_to_up_image_{}.png'.format(i)) for i in range(4)],
                "down": [pygame.image.load('path_to_down_image_{}.png'.format(i)) for i in range(4)],
                "left": [pygame.image.load('path_to_left_image_{}.png'.format(i)) for i in range(4)],
                "right": [pygame.image.load('path_to_right_image_{}.png'.format(i)) for i in range(4)],
                "northeast": [pygame.image.load('path_to_northeast_image_{}.png'.format(i)) for i in range(4)],
                "northwest": [pygame.image.load('path_to_northwest_image_{}.png'.format(i)) for i in range(4)],
                "southeast": [pygame.image.load('path_to_southeast_image_{}.png'.format(i)) for i in range(4)],
                "southwest": [pygame.image.load('path_to_southwest_image_{}.png'.format(i)) for i in range(4)],
            }
            self.current_image = self.images["right"][0]
            self.image = pygame.Surface((width, height))
            self.image.blit(self.current_image, (0, 0))
            self.use_images = True

        # If no images can be found, we default to a black triangle
        except (pygame.error, FileNotFoundError):
            self.image = pygame.Surface((width, height))
            self.image.fill((0, 0, 0))
            self.use_images = False

    # Function to use in the main program that updates the player's image based on directional movement
    def update_image(self, direction):
        if self.use_images:
            self.frame = (self.frame + 1) % 4  # Cycle through frames 0-3
            self.direction = direction
            self.current_image = self.images[direction][self.frame]

    def draw_bars(self, display, screen_height):
        bar_width = 200
        bar_height = 10
        health_bar_color = (0, 255, 0)
        stamina_bar_color = (0, 0, 255)
        power_bar_color = (255, 255, 0)
        margin = 20
        health_bar_x = 20  # Distance from the left side of the screen
        health_bar_y = screen_height - (bar_height * 2) - (margin * 2)  # Distance from the top of the screen

        stamina_bar_x = 20  # Distance from the left side of the screen
        stamina_bar_y = screen_height - (bar_height * 1.5) - (margin * 1.5)  # Distance from the top of the screen

        power_bar_x = 20  # Distance from the left side of the screen
        power_bar_y = screen_height - bar_height - margin  # Distance from the top of the screen

        # Calculate the width of the health bar based on current health
        current_health_width = int((self.current_health / self.max_health) * bar_width)
        current_stamina_width = int((self.current_stamina / self.max_stamina) * bar_width)
        current_power_width = int((self.current_power / self.max_power) * bar_width)

        # Draw the full health bar
        pygame.draw.rect(display, (128, 128, 128), pygame.Rect(health_bar_x, health_bar_y, bar_width, bar_height))
        pygame.draw.rect(display, (128, 128, 128), pygame.Rect(stamina_bar_x, stamina_bar_y, bar_width, bar_height))
        pygame.draw.rect(display, (128, 128, 128), pygame.Rect(power_bar_x, power_bar_y, bar_width, bar_height))

        # Draw the current health on top of the full health bar
        pygame.draw.rect(display, health_bar_color,
                         pygame.Rect(health_bar_x, health_bar_y, current_health_width, bar_height))
        pygame.draw.rect(display, stamina_bar_color,
                         pygame.Rect(stamina_bar_x, stamina_bar_y, current_stamina_width, bar_height))
        pygame.draw.rect(display, power_bar_color,
                         pygame.Rect(power_bar_x, power_bar_y, current_power_width, bar_height))

        if not self.dashing:
            self.current_stamina += self.stamina_recovery_rate
            if self.current_stamina > self.max_stamina:
                self.current_stamina = self.max_stamina

    def bullet_hit(self):
        self.current_power += 5
        if self.current_power > self.max_power:
            self.current_power = self.max_power

    def main(self, display, scroll):  # Method for displaying the player
        if self.use_images:
            # The transform.scale changes the size of the player
            display.blit(pygame.transform.scale(self.current_image, (32, 42)),
                         (self.rect.x - scroll[0], self.rect.y - scroll[1]))
        else:
            pygame.draw.rect(display, (255, 255, 255),
                             (self.rect.x - scroll[0], self.rect.y - scroll[1], self.rect.width, self.rect.height))

        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.moving_northeast = False
        self.moving_northwest = False
        self.moving_southeast = False
        self.moving_southwest = False