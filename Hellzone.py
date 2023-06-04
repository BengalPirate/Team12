import pygame
import sys 
import math

pygame.init()

display = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

class Player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 5

    def main(self, display, scroll):
        pygame.draw.rect(display, (0,0,0), (self.x - scroll[0], self.y - scroll[1], self.width, self.height))

class PlayerBullet: 
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.speed = 10
        self.direction = direction

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

    def main(self, display, scroll):
        self.x += self.x_vel
        self.y += self.y_vel

        pygame.draw.circle(display, (0,0,0), (self.x - scroll[0], self.y - scroll[1]), 5)

player = Player(400, 300, 32, 32) 
display_scroll = [0,0]
player_bullets = []

while True:
    display.fill((255,0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    keys = pygame.key.get_pressed()
    bullet_fired = False

    if keys[pygame.K_UP] and keys[pygame.K_RIGHT] and not bullet_fired:
        player_bullets.append(PlayerBullet(player.x, player.y, "northeast"))
        bullet_fired = True
    elif keys[pygame.K_UP] and keys[pygame.K_LEFT] and not bullet_fired:
        player_bullets.append(PlayerBullet(player.x, player.y, "northwest"))
        bullet_fired = True
    elif keys[pygame.K_DOWN] and keys[pygame.K_RIGHT] and not bullet_fired:
        player_bullets.append(PlayerBullet(player.x, player.y, "southeast"))
        bullet_fired = True
    elif keys[pygame.K_DOWN] and keys[pygame.K_LEFT] and not bullet_fired:
        player_bullets.append(PlayerBullet(player.x, player.y, "southwest"))
        bullet_fired = True
    elif keys[pygame.K_UP] and not bullet_fired:
        player_bullets.append(PlayerBullet(player.x, player.y, "up"))
        bullet_fired = True
    elif keys[pygame.K_DOWN] and not bullet_fired:
        player_bullets.append(PlayerBullet(player.x, player.y, "down"))
        bullet_fired = True
    elif keys[pygame.K_LEFT] and not bullet_fired:
        player_bullets.append(PlayerBullet(player.x, player.y, "left"))
        bullet_fired = True
    elif keys[pygame.K_RIGHT] and not bullet_fired:
        player_bullets.append(PlayerBullet(player.x, player.y, "right"))
        bullet_fired = True

    if keys[pygame.K_w]:
        player.y -= player.speed
    if keys[pygame.K_a]:
        player.x -= player.speed
    if keys[pygame.K_s]:
        player.y += player.speed
    if keys[pygame.K_d]:
        player.x += player.speed

    display_scroll[0] = player.x - 400
    display_scroll[1] = player.y - 300

    pygame.draw.rect(display, (255, 255, 255), (100-display_scroll[0], 100-display_scroll[1], 16, 16))

    player.main(display, display_scroll)

    for bullet in player_bullets:
        bullet.main(display, display_scroll)

    clock.tick(60)
    pygame.display.update()
