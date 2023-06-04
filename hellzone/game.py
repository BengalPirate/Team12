
import pygame
import time
from socket import *



# DIMENSIONS x CONFIGURATIONS
WIDTH, HEIGHT = 500, 500
BACKGROUND = (169, 223, 191)


class Entity():
    pass

class Game:
    def __init__(self):
        pygame.init()
        self.running = True
        self.surface = pygame.display.set_mode((WIDTH, HEIGHT))

        pygame.display.set_caption('Team 12')

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            self.surface.fill(BACKGROUND) # add colour



            pygame.display.flip()
            # time.sleep(0.08)
            
if __name__ == '__main__':
    game = Game()
    game.run()