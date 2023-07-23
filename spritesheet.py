import pygame
from pygame.math import Vector2 as vector
from pygame.mouse import get_pos as mouse_pos
from pygame.mouse import get_pressed as mouse_buttons
from support import *

# dimensions - settings
display = pygame.display.set_mode((800, 600))
TILE_SIZE = 64
WINDOW_WIDTH, WINDOW_HEIGHT = display.get_size()


class SpriteSheet():
    def __init__(self, image):
        self.sheet = image

        # navigation
        self.origin = vector()
        self.display_surface = pygame.display.get_surface()

        # support lines
        self.support_line_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.support_line_surf.set_colorkey('green')
        self.support_line_surf.set_alpha(230)
    
    
    # support lines for drawing the background
    def draw_tile_lines(self):
        cols = WINDOW_WIDTH // TILE_SIZE
        rows = WINDOW_HEIGHT // TILE_SIZE

        origin_offset = vector(
            x = self.origin.x - int(self.origin.x / TILE_SIZE) * TILE_SIZE, 
            y = self.origin.y - int(self.origin.y / TILE_SIZE) * TILE_SIZE )
        
        self.support_line_surf.fill('green')

        for col in range(cols + 1):
            x = origin_offset.x + col * TILE_SIZE
            pygame.draw.line(self.support_line_surf, 'black', (x, 0), (x, WINDOW_HEIGHT))

        for row in range(rows + 1):
            y = origin_offset.y + row * TILE_SIZE
            pygame.draw.line(self.support_line_surf, 'black', (0, y), (WINDOW_WIDTH, y))

        self.display_surface.blit(self.support_line_surf, (0, 0))

    def get_current_cell(self):
        distance_to_origin = vector(mouse_pos()) - self.origin

        col = int(distance_to_origin.x / TILE_SIZE)
        row = int(distance_to_origin.y / TILE_SIZE)

        org_col = int(distance_to_origin.x)
        org_row = int(distance_to_origin.y)

        # print((org_col, org_row))
        # print((col, row))


    def canvas_add(self):
        if mouse_buttons()[0]:
            self.get_current_cell()

# importing the image file

class Editor():
    def __init__(self, display_scroll, land_tiles, object_tiles):
        self.display_scroll = display_scroll
        self.land_tiles = land_tiles
        self.object_tiles = object_tiles


    def drawing_background(self, land_tiles):
        # column - 0
        display.blit(self.land_tiles['tile008'], (0, 0))
        display.blit(self.land_tiles['tile028'], (0*TILE_SIZE, 1*TILE_SIZE)) 
        display.blit(self.land_tiles['tile028'], (0*TILE_SIZE, 2*TILE_SIZE)) 
        display.blit(self.land_tiles['tile028'], (0*TILE_SIZE, 3*TILE_SIZE))
        display.blit(self.land_tiles['tile028'], (0*TILE_SIZE, 4*TILE_SIZE)) 
        display.blit(self.land_tiles['tile028'], (0*TILE_SIZE, 5*TILE_SIZE)) 
        display.blit(self.land_tiles['tile028'], (0*TILE_SIZE, 6*TILE_SIZE)) 
        display.blit(self.land_tiles['tile028'], (0*TILE_SIZE, 7*TILE_SIZE)) 
        display.blit(self.land_tiles['tile084'], (0*TILE_SIZE, 8*TILE_SIZE)) 
        display.blit(self.land_tiles['tile000'], (0*TILE_SIZE, 9*TILE_SIZE)) 

        # column - 1
        display.blit(self.land_tiles['tile001'], (1*TILE_SIZE, 0*TILE_SIZE))
        display.blit(self.land_tiles['tile010'], (1*TILE_SIZE, 1*TILE_SIZE)) 
        display.blit(self.land_tiles['tile010'], (1*TILE_SIZE, 2*TILE_SIZE)) 
        display.blit(self.land_tiles['tile011'], (1*TILE_SIZE, 3*TILE_SIZE))
        display.blit(self.land_tiles['tile011'], (1*TILE_SIZE, 4*TILE_SIZE)) 
        display.blit(self.land_tiles['tile010'], (1*TILE_SIZE, 5*TILE_SIZE)) 
        display.blit(self.land_tiles['tile011'], (1*TILE_SIZE, 6*TILE_SIZE)) 
        display.blit(self.land_tiles['tile011'], (1*TILE_SIZE, 7*TILE_SIZE)) 
        display.blit(self.land_tiles['tile011'], (1*TILE_SIZE, 8*TILE_SIZE)) 
        display.blit(self.land_tiles['tile006'], (1*TILE_SIZE, 9*TILE_SIZE)) 

        # column - 2
        display.blit(self.land_tiles['tile001'], (2*TILE_SIZE, 0*TILE_SIZE))
        display.blit(self.land_tiles['tile010'], (2*TILE_SIZE, 1*TILE_SIZE)) 
        display.blit(self.land_tiles['tile010'], (2*TILE_SIZE, 2*TILE_SIZE)) 
        display.blit(self.land_tiles['tile011'], (2*TILE_SIZE, 3*TILE_SIZE))
        display.blit(self.land_tiles['tile011'], (2*TILE_SIZE, 4*TILE_SIZE)) 
        display.blit(self.land_tiles['tile010'], (2*TILE_SIZE, 5*TILE_SIZE)) 
        display.blit(self.land_tiles['tile011'], (2*TILE_SIZE, 6*TILE_SIZE)) 
        display.blit(self.land_tiles['tile011'], (2*TILE_SIZE, 7*TILE_SIZE)) 
        display.blit(self.land_tiles['tile011'], (2*TILE_SIZE, 8*TILE_SIZE)) 
        display.blit(self.land_tiles['tile006'], (2*TILE_SIZE, 9*TILE_SIZE)) 

        # column - 3
        display.blit(self.land_tiles['tile001'], (3*TILE_SIZE, 0*TILE_SIZE))
        display.blit(self.land_tiles['tile010'], (3*TILE_SIZE, 1*TILE_SIZE)) 
        display.blit(self.land_tiles['tile010'], (3*TILE_SIZE, 2*TILE_SIZE)) 
        display.blit(self.land_tiles['tile011'], (3*TILE_SIZE, 3*TILE_SIZE))
        display.blit(self.land_tiles['tile011'], (3*TILE_SIZE, 4*TILE_SIZE)) 
        display.blit(self.land_tiles['tile010'], (3*TILE_SIZE, 5*TILE_SIZE)) 
        display.blit(self.land_tiles['tile011'], (3*TILE_SIZE, 6*TILE_SIZE)) 
        display.blit(self.land_tiles['tile011'], (3*TILE_SIZE, 7*TILE_SIZE)) 
        display.blit(self.land_tiles['tile011'], (3*TILE_SIZE, 8*TILE_SIZE)) 
        display.blit(self.land_tiles['tile006'], (3*TILE_SIZE, 9*TILE_SIZE)) 

        # column - 4
        display.blit(self.land_tiles['tile001'], (4*TILE_SIZE, 0*TILE_SIZE))
        display.blit(self.land_tiles['tile010'], (4*TILE_SIZE, 1*TILE_SIZE)) 
        display.blit(self.land_tiles['tile010'], (4*TILE_SIZE, 2*TILE_SIZE)) 
        display.blit(self.land_tiles['tile011'], (4*TILE_SIZE, 3*TILE_SIZE))
        display.blit(self.land_tiles['tile011'], (4*TILE_SIZE, 4*TILE_SIZE)) 
        display.blit(self.land_tiles['tile010'], (4*TILE_SIZE, 5*TILE_SIZE)) 
        display.blit(self.land_tiles['tile011'], (4*TILE_SIZE, 6*TILE_SIZE)) 
        display.blit(self.land_tiles['tile011'], (4*TILE_SIZE, 7*TILE_SIZE)) 
        display.blit(self.land_tiles['tile011'], (4*TILE_SIZE, 8*TILE_SIZE)) 
        display.blit(self.land_tiles['tile006'], (4*TILE_SIZE, 9*TILE_SIZE)) 

        # column - 5
        display.blit(self.land_tiles['tile001'], (5*TILE_SIZE, 0*TILE_SIZE))
        display.blit(self.land_tiles['tile010'], (5*TILE_SIZE, 1*TILE_SIZE)) 
        display.blit(self.land_tiles['tile010'], (5*TILE_SIZE, 2*TILE_SIZE)) 
        display.blit(self.land_tiles['tile011'], (5*TILE_SIZE, 3*TILE_SIZE))
        display.blit(self.land_tiles['tile011'], (5*TILE_SIZE, 4*TILE_SIZE)) 
        display.blit(self.land_tiles['tile010'], (5*TILE_SIZE, 5*TILE_SIZE)) 
        display.blit(self.land_tiles['tile011'], (5*TILE_SIZE, 6*TILE_SIZE)) 
        display.blit(self.land_tiles['tile011'], (5*TILE_SIZE, 7*TILE_SIZE)) 
        display.blit(self.land_tiles['tile011'], (5*TILE_SIZE, 8*TILE_SIZE)) 
        display.blit(self.land_tiles['tile006'], (5*TILE_SIZE, 9*TILE_SIZE)) 

        # column - 6
        display.blit(self.land_tiles['tile001'], (6*TILE_SIZE, 0*TILE_SIZE))
        display.blit(self.land_tiles['tile010'], (6*TILE_SIZE, 1*TILE_SIZE)) 
        display.blit(self.land_tiles['tile010'], (6*TILE_SIZE, 2*TILE_SIZE)) 
        display.blit(self.land_tiles['tile011'], (6*TILE_SIZE, 3*TILE_SIZE))
        display.blit(self.land_tiles['tile011'], (6*TILE_SIZE, 4*TILE_SIZE)) 
        display.blit(self.land_tiles['tile010'], (6*TILE_SIZE, 5*TILE_SIZE)) 
        display.blit(self.land_tiles['tile011'], (6*TILE_SIZE, 6*TILE_SIZE)) 
        display.blit(self.land_tiles['tile011'], (6*TILE_SIZE, 7*TILE_SIZE)) 
        display.blit(self.land_tiles['tile011'], (6*TILE_SIZE, 8*TILE_SIZE)) 
        display.blit(self.land_tiles['tile006'], (6*TILE_SIZE, 9*TILE_SIZE)) 

        # column - 7
        display.blit(self.land_tiles['tile001'], (7*TILE_SIZE, 0*TILE_SIZE))
        display.blit(self.land_tiles['tile010'], (7*TILE_SIZE, 1*TILE_SIZE)) 
        display.blit(self.land_tiles['tile010'], (7*TILE_SIZE, 2*TILE_SIZE)) 
        display.blit(self.land_tiles['tile011'], (7*TILE_SIZE, 3*TILE_SIZE))
        display.blit(self.land_tiles['tile011'], (7*TILE_SIZE, 4*TILE_SIZE)) 
        display.blit(self.land_tiles['tile010'], (7*TILE_SIZE, 5*TILE_SIZE)) 
        display.blit(self.land_tiles['tile011'], (7*TILE_SIZE, 6*TILE_SIZE)) 
        display.blit(self.land_tiles['tile011'], (7*TILE_SIZE, 7*TILE_SIZE)) 
        display.blit(self.land_tiles['tile011'], (7*TILE_SIZE, 8*TILE_SIZE)) 
        display.blit(self.land_tiles['tile006'], (7*TILE_SIZE, 9*TILE_SIZE)) 

        # column - 8
        display.blit(self.land_tiles['tile001'], (8*TILE_SIZE, 0*TILE_SIZE))
        display.blit(self.land_tiles['tile010'], (8*TILE_SIZE, 1*TILE_SIZE)) 
        display.blit(self.land_tiles['tile010'], (8*TILE_SIZE, 2*TILE_SIZE)) 
        display.blit(self.land_tiles['tile011'], (8*TILE_SIZE, 3*TILE_SIZE))
        display.blit(self.land_tiles['tile011'], (8*TILE_SIZE, 4*TILE_SIZE)) 
        display.blit(self.land_tiles['tile010'], (8*TILE_SIZE, 5*TILE_SIZE)) 
        display.blit(self.land_tiles['tile011'], (8*TILE_SIZE, 6*TILE_SIZE)) 
        display.blit(self.land_tiles['tile011'], (8*TILE_SIZE, 7*TILE_SIZE)) 
        display.blit(self.land_tiles['tile011'], (8*TILE_SIZE, 8*TILE_SIZE)) 
        display.blit(self.land_tiles['tile006'], (8*TILE_SIZE, 9*TILE_SIZE)) 

        # column - 9
        display.blit(self.land_tiles['tile001'], (9*TILE_SIZE, 0*TILE_SIZE))
        display.blit(self.land_tiles['tile010'], (9*TILE_SIZE, 1*TILE_SIZE)) 
        display.blit(self.land_tiles['tile010'], (9*TILE_SIZE, 2*TILE_SIZE)) 
        display.blit(self.land_tiles['tile011'], (9*TILE_SIZE, 3*TILE_SIZE))
        display.blit(self.land_tiles['tile011'], (9*TILE_SIZE, 4*TILE_SIZE)) 
        display.blit(self.land_tiles['tile010'], (9*TILE_SIZE, 5*TILE_SIZE)) 
        display.blit(self.land_tiles['tile011'], (9*TILE_SIZE, 6*TILE_SIZE)) 
        display.blit(self.land_tiles['tile011'], (9*TILE_SIZE, 7*TILE_SIZE)) 
        display.blit(self.land_tiles['tile011'], (9*TILE_SIZE, 8*TILE_SIZE)) 
        display.blit(self.land_tiles['tile006'], (9*TILE_SIZE, 9*TILE_SIZE)) 

        # column - 10
        display.blit(self.land_tiles['tile001'], (10*TILE_SIZE, 0*TILE_SIZE))
        display.blit(self.land_tiles['tile010'], (10*TILE_SIZE, 1*TILE_SIZE)) 
        display.blit(self.land_tiles['tile010'], (10*TILE_SIZE, 2*TILE_SIZE)) 
        display.blit(self.land_tiles['tile011'], (10*TILE_SIZE, 3*TILE_SIZE))
        display.blit(self.land_tiles['tile011'], (10*TILE_SIZE, 4*TILE_SIZE)) 
        display.blit(self.land_tiles['tile010'], (10*TILE_SIZE, 5*TILE_SIZE)) 
        display.blit(self.land_tiles['tile011'], (10*TILE_SIZE, 6*TILE_SIZE)) 
        display.blit(self.land_tiles['tile011'], (10*TILE_SIZE, 7*TILE_SIZE)) 
        display.blit(self.land_tiles['tile011'], (10*TILE_SIZE, 8*TILE_SIZE)) 
        display.blit(self.land_tiles['tile006'], (10*TILE_SIZE, 9*TILE_SIZE)) 

        # column - 11
        display.blit(self.land_tiles['tile001'], (11*TILE_SIZE, 0*TILE_SIZE))
        display.blit(self.land_tiles['tile011'], (11*TILE_SIZE, 1*TILE_SIZE)) 
        display.blit(self.land_tiles['tile011'], (11*TILE_SIZE, 2*TILE_SIZE)) 
        display.blit(self.land_tiles['tile010'], (11*TILE_SIZE, 3*TILE_SIZE))
        display.blit(self.land_tiles['tile010'], (11*TILE_SIZE, 4*TILE_SIZE)) 
        display.blit(self.land_tiles['tile010'], (11*TILE_SIZE, 5*TILE_SIZE)) 
        display.blit(self.land_tiles['tile011'], (11*TILE_SIZE, 6*TILE_SIZE)) 
        display.blit(self.land_tiles['tile011'], (11*TILE_SIZE, 7*TILE_SIZE)) 
        display.blit(self.land_tiles['tile011'], (11*TILE_SIZE, 8*TILE_SIZE)) 
        display.blit(self.land_tiles['tile006'], (11*TILE_SIZE, 9*TILE_SIZE)) 

        # column - 12
        display.blit(self.land_tiles['tile009'], (12*TILE_SIZE, 0*TILE_SIZE))
        display.blit(self.land_tiles['tile031'], (12*TILE_SIZE, 1*TILE_SIZE)) 
        display.blit(self.land_tiles['tile031'], (12*TILE_SIZE, 2*TILE_SIZE)) 
        display.blit(self.land_tiles['tile031'], (12*TILE_SIZE, 3*TILE_SIZE))
        display.blit(self.land_tiles['tile031'], (12*TILE_SIZE, 4*TILE_SIZE)) 
        display.blit(self.land_tiles['tile031'], (12*TILE_SIZE, 5*TILE_SIZE)) 
        display.blit(self.land_tiles['tile031'], (12*TILE_SIZE, 6*TILE_SIZE)) 
        display.blit(self.land_tiles['tile031'], (12*TILE_SIZE, 7*TILE_SIZE)) 
        display.blit(self.land_tiles['tile087'], (12*TILE_SIZE, 8*TILE_SIZE)) 
        display.blit(self.land_tiles['tile000'], (12*TILE_SIZE, 9*TILE_SIZE)) 

    def drawing_moving_background(self, object_tiles):
        display.blit(self.object_tiles['tile024'], (140 - self.display_scroll[0], 256 - self.display_scroll[1]))
        display.blit(self.object_tiles['tile024'], (5*TILE_SIZE - self.display_scroll[0], 6*TILE_SIZE - self.display_scroll[1]))

        display.blit(self.object_tiles['tile004'], (125, 125))
        display.blit(self.object_tiles['tile004'], (586, 129))
        display.blit(self.object_tiles['tile004'], (157, 337))
        display.blit(self.object_tiles['tile004'], (573, 381))
        display.blit(self.object_tiles['tile004'], (125, 125))
