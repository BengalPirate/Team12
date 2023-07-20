# enemy.py

import pygame
import random
from player import Player

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, behavior_type):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.animation_images = []
        for i in range(4):
            try:
                self.animation_images.append(pygame.Surface((20, 20)))
            except pygame.error:
                self.animation_images.append(pygame.Surface((20, 20)))
                self.animation_images[i].fill((0, 255, 0))  # Fills the enemy's surface with green color
        self.animation_count = 0
        self.reset_offset = 0
        self.offset_x = random.randrange(-150, 150)
        self.offset_y = random.randrange(-150, 150)
        self.max_health = 100
        self.current_health = 100
        self.max_stamina = 100
        self.current_stamina = 100
        self.max_power = 100
        self.current_power = 100
        self.behavior_type = behavior_type

    def draw_bars(self, display, display_scroll):
        bar_width = 40
        bar_height = 5
        health_bar_color = (0, 255, 0)
        stamina_bar_color = (0, 0, 255)
        margin = 5

        # Calculate the position of the health bar and stamina bar relative to the enemy's position and the display scroll
        health_bar_x = self.rect.x - display_scroll[0] + (self.rect.width // 2) - (bar_width // 2)
        health_bar_y = self.rect.y - display_scroll[1] - (2 * bar_height) - (2 * margin)

        stamina_bar_x = self.rect.x - display_scroll[0] + (self.rect.width // 2) - (bar_width // 2)
        stamina_bar_y = self.rect.y - display_scroll[1] - bar_height - margin

        current_health_width = int((self.current_health / self.max_health) * bar_width)
        current_stamina_width = int((self.current_stamina / self.max_stamina) * bar_width)

        pygame.draw.rect(display, (128, 128, 128), pygame.Rect(health_bar_x, health_bar_y, bar_width, bar_height))
        pygame.draw.rect(display, (128, 128, 128), pygame.Rect(stamina_bar_x, stamina_bar_y, bar_width, bar_height))

        pygame.draw.rect(display, health_bar_color,
                         pygame.Rect(health_bar_x, health_bar_y, current_health_width, bar_height))
        pygame.draw.rect(display, stamina_bar_color,
                         pygame.Rect(stamina_bar_x, stamina_bar_y, current_stamina_width, bar_height))

    def update_position(self, player):
        if self.behavior_type == 1:
            if self.animation_count + 1 == 16:
                self.animation_count = 0
            self.animation_count += 1

            if self.reset_offset == 0:
                self.offset_x = random.randrange(-150, 150)
                self.offset_y = random.randrange(-150, 150)
                self.reset_offset = random.randrange(120, 150)
            else:
                self.reset_offset -= 1

            if player.rect.x + self.offset_x > self.rect.x:  # -display_scroll[0]:
                self.rect.x += 1
            elif player.rect.x + self.offset_x < self.rect.x:  # -display_scroll[0]:
                self.rect.x -= 1

            if player.rect.y + self.offset_y > self.rect.y:  # -display_scroll[1]:
                self.rect.y += 1
            elif player.rect.y + self.offset_y < self.rect.y:  # -display_scroll[1]:
                self.rect.y -= 1

        elif self.behavior_type == 2:
            if self.animation_count + 1 == 16:
                self.animation_count = 0
            self.animation_count += 1

            if self.reset_offset == 0:
                self.offset_x = random.randrange(-150, 150)
                self.offset_y = random.randrange(-150, 150)
                self.reset_offset = random.randrange(120, 150)
            else:
                self.reset_offset -= 1

            if self.rect.x < player.rect.x:
                self.rect.x += 2  # Adjust the enemy's horizontal speed as desired
            elif self.rect.x > player.rect.x:
                self.rect.x -= 2

            if self.rect.y < player.rect.y:
                self.rect.y += 2  # Adjust the enemy's vertical speed as desired
            elif self.rect.y > player.rect.y:
                self.rect.y -= 2

    def main(self, display, display_scroll, player):
        self.update_position(player)
        display.blit(pygame.transform.scale(self.animation_images[self.animation_count // 4], (32, 30)),
                     (self.rect.x - display_scroll[0], self.rect.y - display_scroll[1]))
        self.draw_bars(display, display_scroll)

    def take_damage(self, damage):
        self.current_health -= damage
        if self.current_health <= 0:
            return True
        return False