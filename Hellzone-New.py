# Imports necessary modules
import pygame
import sys 
import math
import random
import spritesheet
from player import Player
from bullet import PlayerBullet
from enemy import Enemy

# Initializes all imported pygame modules
pygame.init()

all_sprites = pygame.sprite.Group()

# Sets the size of the screen for display
display = pygame.display.set_mode((800, 600))
SCREEN_WIDTH, SCREEN_HEIGHT = display.get_size()

# Creates an object to help track time
clock = pygame.time.Clock()
game_active = False
game_pause = False
text_font = pygame.font.Font('fonts/Pixeltype.ttf', 50)

scroll_offset = [0, 0]

# Creates an instance of the player
player = Player(400, 300, 32, 32)

enemies = []
enemy1 = Enemy(200, 300, 32, 32, behavior_type=1)
enemy2 = Enemy(400, 200, 32, 32, behavior_type=2)

enemies.append(enemy1)
enemies.append(enemy2)

# Defines the initial display scroll
display_scroll = [0, 0]

# Creates a list to store player bullets
player_bullets = []

BLACK = (0, 0, 0)
OFFSCREEN_ENEMY_COLOR = (0, 0, 255, 255)

plains_1 = pygame.image.load('tilesets/plains/sprite_0.png').convert_alpha()

plains0_sprite_sheet = spritesheet.SpriteSheet(plains_1)

# # sprite_0 section
plain0_frame_0 = plains0_sprite_sheet.get_image(0, 16, 24, 3, BLACK)
# starts the main game loop
while True:
    # Fills the display surface with color
    # display.fill((80,155,102))
    display.fill((255, 0, 0))

    # Get the screen height
    screen_height = display.get_height()

    # Get a list of all keys currently being pressed down
    keys = pygame.key.get_pressed()

    # get the event from the queue
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If the event is a quit, exit the game
            sys.exit()
        # Let's assume that pygame.K_SPACE is the key for starting a dash

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                game_active = True

    if game_active:

        player.main(display, display_scroll)
        player.draw_bars(display, screen_height)

        all_sprites.update()
        all_sprites.draw(display, screen_height)

        # Check if bullet has been fired
        bullet_fired = False

        key_combinations = {
            (pygame.K_UP, pygame.K_RIGHT): "northeast",
            (pygame.K_UP, pygame.K_LEFT): "northwest",
            (pygame.K_DOWN, pygame.K_RIGHT): "southeast",
            (pygame.K_DOWN, pygame.K_LEFT): "southwest",
            (pygame.K_UP,): "up",
            (pygame.K_DOWN,): "down",
            (pygame.K_LEFT,): "left",
            (pygame.K_RIGHT,): "right"
        }

        for combination, direction in key_combinations.items():
            if all(keys[key] for key in combination) and not bullet_fired:
                player_bullets.append(PlayerBullet(player.rect.x, player.rect.y, direction))
                bullet_fired = True

        key_movements = {
            (pygame.K_w,): ("up", 0, -1),
            (pygame.K_a,): ("left", -1, 0),
            (pygame.K_s,): ("down", 0, 1),
            (pygame.K_d,): ("right", 1, 0),
            (pygame.K_w, pygame.K_d): ("northeast", 1, -1),
            (pygame.K_w, pygame.K_a): ("northwest", -1, -1),
            (pygame.K_s, pygame.K_d): ("southeast", 1, 1),
            (pygame.K_s, pygame.K_a): ("southwest", -1, 1)
        }

        for keys_combination, (direction, dx, dy) in key_movements.items():
            if all(keys[key] for key in keys_combination):
                if keys[pygame.K_SPACE] and (player.current_stamina > 0):
                    player.rect.x += player.dash_speed * dx / math.sqrt(2)
                    player.rect.y += player.dash_speed * dy / math.sqrt(2)
                    player.current_stamina -= 0.5
                    pygame.time.set_timer(pygame.USEREVENT, 1000)  # Dash lasts for 1 second
                else:
                    player.rect.x += player.speed * dx / math.sqrt(2)
                    player.rect.y += player.speed * dy / math.sqrt(2)
                player.update_image(direction)
                setattr(player, "moving_" + direction, True)

        if player.dashing and pygame.time.get_ticks() / 1000 > player.dash_time + player.dash_duration:
            player.dashing = False

        # Update the display scroll based on player's position
        display_scroll[0] = player.rect.x - 400
        display_scroll[1] = player.rect.y - 300

        # Draw a static rectangle to the screen, offset by the display scroll
        display.blit(plain0_frame_0, (100 - display_scroll[0], 100 - display_scroll[1]))

        # Update the player display
        player.main(display, display_scroll)

        # Update the bullet displays
        for bullet in player_bullets:
            bullet.main(display, display_scroll)

            for enemy in enemies:
                if bullet.rect.colliderect(enemy.rect):
                    if enemy.take_damage(0.5):
                        enemies.remove(enemy)
                    player_bullets.remove(bullet)
                    player.current_power = min(player.max_power, player.current_power + 0.2)
                    break

        # Draw the enemies
        for enemy in enemies:
            enemy.main(display, display_scroll, player)
            enemy.update_position(player)
            '''
            enemy_pos = pygame.Vector2(enemy.rect.x, enemy.rect.y)
            player_pos = pygame.Vector2(player.rect.x, player.rect.y)
            direction = enemy_pos - player_pos
            distance = direction.length()
            
            if distance != 0:
                direction.normalize_ip()

            if distance > SCREEN_WIDTH:
                angle = math.degrees(math.atan2(direction.y, direction.x))

                if -45 <= angle < 45:
                    offscreen_indicator = pygame.Rect(SCREEN_WIDTH - 50, 0, 50, SCREEN_HEIGHT)
                elif 45 <= angle < 135:
                    offscreen_indicator = pygame.Rect(0, 0, SCREEN_WIDTH, 50)
                elif -135 <= angle < -45:
                    offscreen_indicator = pygame.Rect(0,SCREEN_HEIGHT -5, SCREEN_WIDTH, 50)
                else:
                    offscreen_indicator = pygame.Rect(0, 0, 50, SCREEN_HEIGHT)
                
                s = pygame.Surface((offscreen_indicator.width, offscreen_indicator.height))
                s.set_alpha(128)
                s.fill(OFFSCREEN_ENEMY_COLOR)
                display.blit(s, offscreen_indicator)
                '''
                
        # Limit the game to 60 frames per second
        clock.tick(60)
        pass
    else:
        color_black = (0, 0, 0)
        display.fill((84, 12, 123))
        header_text = text_font.render('Start Game', False, color_black)
        header_rect = header_text.get_rect(center=(800 // 2, 50))
        start_game_text = text_font.render('Press Enter to Start Game', False, color_black)
        start_game_text_rect = start_game_text.get_rect(center=(800 // 2, 600 // 2))
        display.blit(header_text, header_rect)
        display.blit(start_game_text, start_game_text_rect)
    # Update the full display surface to the screen
    pygame.display.update()
