import pygame
import random
import math
from player import Player
from enemy import Enemy

class DragonHead(Enemy):
    def __init__(self, x, y, width, height, behavior_type):
        super().__init__(x, y, width, height, behavior_type)
        self.body = [self.rect]  # the body of the snake will be a list of Rects
        self.speed = 1

    def calculate_distance(self, rect1, rect2):
        dx = rect2.centerx - rect1.centerx
        dy = rect2.centery - rect1.centery
        return math.sqrt(dx**2 + dy**2)
    
    def distance(self, rect1, rect2):
        return ((rect1.x - rect2.x) ** 2 + (rect1.y - rect2.y) ** 2) ** 0.5

    def update_position(self, players, enemies):
        # Calculate the closest target
        closest_player = min(players, key=lambda player: self.distance(self.rect, player.rect))

        # Update the position based on the closest target
        if self.rect.x < closest_player.rect.x:
            self.rect.x += self.speed
        elif self.rect.x > closest_player.rect.x:
            self.rect.x -= self.speed

        if self.rect.y < closest_player.rect.y:
            self.rect.y += self.speed
        elif self.rect.y > closest_player.rect.y:
            self.rect.y -= self.speed

        # Check if collided with an enemy
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                self.body.append(DragonBody(self.body[-1].rect.x, self.body[-1].rect.y, self.width, self.height, self.behavior_type))
        
        # Move the body
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i] = self.body[i - 1].copy()
        if len(self.body) > 1:
            self.body[1] = self.rect.copy()

    def draw(self, display, display_scroll):
        for part in self.body:
            display.blit(self.animation_images[self.animation_count // 4], 
                         (part.x - display_scroll[0], part.y - display_scroll[1]))
        self.draw_bars(display, display_scroll)

class DragonBody(DragonHead):
    def __init__(self, x, y, width, height, behavior_type):
        super().__init__(x, y, width, height, behavior_type)