# melee.py

import pygame
import math
import time
from player import Player

# Creates a class for the melee attack
class MeleeAttack(Player):
    def __init__(self, x, y, direction, size, duration, projectile):
        self.rect = pygame.Rect(x, y, size, size)
        self.direction = direction
        self.duration = duration
        self.projectile = projectile
        self.speed = 5 # Adjust the speed as desired
        self.start_time = time.time()

        direction_angles = {
            "up": -math.pi / 2,
            "down": math.pi / 2,
            "left": math.pi,
            "right": 0,
            "northeast": -math.pi / 4,
            "northwest": -3 * math.pi / 4,
            "southeast": math.pi / 4,
            "southwest": 3 * math.pi / 4
        }

        if direction in direction_angles:
            self.direction = direction_angles[direction]


        if direction == "up":
            self.rect = pygame.Rect(x - size // 2, y - size, size, size)
        elif direction == "down":
            self.rect = pygame.Rect(x - size // 2, y, size, size)
        elif direction == "left":
            self.rect = pygame.Rect(x - size, y - size // 2, size, size)
        elif direction == "right":
            self.rect = pygame.Rect(x, y - size // 2, size, size)
        elif direction == "northeast":
            self.rect = pygame.Rect(x, y - size, size, size)
        elif direction == "northwest":
            self.rect = pygame.Rect(x - size, y - size, size, size)
        elif direction == "southeast":
            self.rect = pygame.Rect(x, y, size, size)
        elif direction == "southwest":
            self.rect = pygame.Rect(x - size, y, size, size)

    def main(self, display, scroll):
        if self.duration > 0:
            pygame.draw.rect(display, (128, 128, 128), self.rect.move(-scroll[0], -scroll[1]))
            self.duration -= 1
        else:
            active_melee_attacks.remove(self)
        
        if self.projectile:
            self.update_position()


    def update_position(self):
        dx = self.speed * math.cos(self.direction)
        dy = -self.speed * math.sin(self.direction)
        self.rect.x += dx
        self.rect.y += dy

    def time_elapsed(self):
        return time.time() - self.start_time
    
    def decrease_duration(self):
        self.duration -= 1

# Storing previous attacks to check if four attacks of the same type were done within 3 seconds
previous_attacks = []
active_melee_attacks = []

# This function will be triggered when a melee attack key is pressed
def melee_attack_pressed(direction):
    global previous_attacks
    
    # When the melee attack is initiated, store the direction and timestamp of attack in previous_attacks
    current_attack = {'direction': direction, 'time': time.time()}
    previous_attacks.append(current_attack)

    # Only keep the four most recent attacks
    previous_attacks = previous_attacks[-4:]

    # Check if the four most recent attacks were of the same type and within 3 seconds of each other
    if len(previous_attacks) == 4 and all(attack['direction'] == direction for attack in previous_attacks) and (previous_attacks[-1]['time'] - previous_attacks[0]['time'] <= 3):
        # Initiate a special attack that lasts for 10 seconds and ripples across the screen
        special_attack = MeleeAttack(player.rect.x, player.rect.y, direction, 800, 1000, True)
        active_melee_attacks.append(special_attack)
    # Changed duration of regular_attack to 0.1 (seconds)
    else:
        regular_attack = MeleeAttack(player.rect.x, player.rect.y, direction, 800, 0.1, False)
        active_melee_attacks.append(regular_attack)

