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


while True:
    display.fill((255,0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(
            pygame.QUIT
            )

    player.main(display)

    clock.tick(60)
    pygame.display.update()