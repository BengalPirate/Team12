import pygame
from pygame.math import Vector2 as vector
from pygame.mouse import get_pos as mouse_pos
from pygame.mouse import get_pressed as mouse_buttons
from support import *

# from pytmx.util_pygame import load_pygame


# Tile Config
class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)

# dimensions - settings
TILE_SIZE = 64

# data
# tmx_data = load_pygame('data/tmx/hellzone.tmx')
# sprite_group = pygame.sprite.Group()

# # cycle through all layers
# for layer in tmx_data.layers:
#     # if layer in ('lava', 'ground', 'detail and terrain', 'props'):
#     if hasattr(layer, 'data'):
#         for x, y, surf in layer.tiles():
#             print(layer)
#             pos = (x * 32, y * 32)
#             Tile(pos = pos, surf = surf, groups = sprite_group)


class Editor():
    def __init__(self, display_scroll, land_tiles, object_tiles):
        self.display_scroll = display_scroll
        self.land_tiles = land_tiles
        self.object_tiles = object_tiles


    def drawing_moving_background(self, object_tiles, display):
        display.blit(self.object_tiles['tile024'], (140 - self.display_scroll[0], 256 - self.display_scroll[1]))
        display.blit(self.object_tiles['tile024'], (5*TILE_SIZE - self.display_scroll[0], 6*TILE_SIZE - self.display_scroll[1]))

        display.blit(self.object_tiles['tile004'], (125, 125))
        display.blit(self.object_tiles['tile004'], (586, 129))
        display.blit(self.object_tiles['tile004'], (157, 337))
        display.blit(self.object_tiles['tile004'], (573, 381))
        display.blit(self.object_tiles['tile004'], (125, 125))
