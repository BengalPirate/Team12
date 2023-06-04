import pygame
import sys 
pygame.init()

display = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

class Player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    def main(self, display):
        pygame.draw.rect(display, (0,0,0), (self.x, self.y, self.width, self.height))

player = Player(400, 300, 32, 32) 

display_scroll = [0,0]

while True:
    display.fill((255,0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(
            pygame.QUIT
            )

    keys = pygame.key.get_pressed()

    pygame.draw.rect(display, (255, 255, 255), (100-display_scroll[0], 100-display_scroll[1], 16, 16))

    if keys[pygame.K_a]:
        display_scroll[0] -= 5
    if keys[pygame.K_d]:
        display_scroll[0] += 5
    if keys[pygame.K_w]:
        display_scroll[1] -= 5
    if keys[pygame.K_s]:
        display_scroll[1] += 5


    player.main(display)

    clock.tick(60)
    pygame.display.update()