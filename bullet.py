# bullet.py

import pygame
import math

# Creates a class for the bullet
class PlayerBullet:
    def __init__(self, x, y, direction):  # Define initial properties of the bullet
        super().__init__()
        width = 10
        height = 10
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = 10
        self.direction = direction

        # Condition to check the direction of the bullet and adjust velocity accordingly
        if direction == "up":
            self.x_vel = 0
            self.y_vel = -self.speed
        elif direction == "down":
            self.x_vel = 0
            self.y_vel = self.speed
        elif direction == "left":
            self.x_vel = -self.speed
            self.y_vel = 0
        elif direction == "right":
            self.x_vel = self.speed
            self.y_vel = 0
        elif direction == "northeast":
            self.x_vel = self.speed / math.sqrt(2)
            self.y_vel = -self.speed / math.sqrt(2)
        elif direction == "northwest":
            self.x_vel = -self.speed / math.sqrt(2)
            self.y_vel = -self.speed / math.sqrt(2)
        elif direction == "southeast":
            self.x_vel = self.speed / math.sqrt(2)
            self.y_vel = self.speed / math.sqrt(2)
        elif direction == "southwest":
            self.x_vel = -self.speed / math.sqrt(2)
            self.y_vel = self.speed / math.sqrt(2)

    def main(self, display, scroll):  # Method for moving and displaying the bullet
        self.rect.x += self.x_vel
        self.rect.y += self.y_vel

        pygame.draw.circle(display, (0, 0, 0), (self.rect.x - scroll[0], self.rect.y - scroll[1]), 5)