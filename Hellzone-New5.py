# Imports necessary modules
import pygame
import sys 
import math
import random
import time
import spritesheet
from player import Player
from bullet import PlayerBullet
from enemy import Enemy
from dragon import DragonHead
from dragon import DragonBody
from melee import MeleeAttack
from pygame.math import Vector2

# Initializes all imported pygame modules
pygame.init()

all_sprites = pygame.sprite.Group()

# Sets the size of the screen for display
display = pygame.display.set_mode((1920, 1080))
SCREEN_WIDTH, SCREEN_HEIGHT = display.get_size()

# Creates an object to help track time
clock = pygame.time.Clock()
game_active = False
game_pause = False
selection_menu_font_size = 70
selection_menu_font = pygame.font.Font('/home/bengal_pirate/Team12/Team12/fonts/Pixeltype.ttf', selection_menu_font_size)
logo = pygame.image.load('/home/bengal_pirate/Team12/Team12/Title2.png')  # replace with the path to your logo

scroll_offset = [0, 0]

# Creates an instance of the player
player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 32, 32)

enemies = []
enemy1 = Enemy(200, 300, 32, 32, behavior_type=1)
enemy2 = Enemy(400, 200, 32, 32, behavior_type=2)
dragon1 = DragonHead(600, 400, 32, 32, behavior_type=1)
enemies.append(enemy1)
enemies.append(enemy2)
enemies.append(dragon1)

expansion_size = 3

# Defines the initial display scroll
display_scroll = [0, 0]
# Creates a list to store player bullets
player_bullets = []
# Creates a list to store active melee attacks
active_melee_attacks = []
# Creates a list to store active button presses
button_presses = []
button_press_timeout = 3000 # 3 seconds
cooldown_start_time = 0
melee_attack_count = 0
first_melee_attack_time = 0
melee_attack_direction = None
create_projectile_attack = False

game_state = 'start_menu'

game_over_menu_options = ['Yes', 'No']
game_over_menu_option = 0 #default option

BLACK = (0, 0, 0)
OFFSCREEN_ENEMY_COLOR = (0, 0, 255, 255)

plains_1 = pygame.image.load('/home/bengal_pirate/Team12/Team12/tilesets/plains/sprite_0.png').convert_alpha()

# number of start_menu images you have in the directory
num_images = 12
start_menu_background_images = []

for i in range(1, num_images + 1):
    image_path = f'/home/bengal_pirate/Team12/Team12/menu/start_menu/start_menu{i}.png'
    start_menu_background_images.append(pygame.image.load(image_path))

menu_background = random.choice(start_menu_background_images)

credits_background = pygame.image.load('/home/bengal_pirate/Team12/Team12/menu/credits/credits1.png')
controls_background = pygame.image.load('/home/bengal_pirate/Team12/Team12/menu/controls/controls1.png')
game_over_background = pygame.image.load('/home/bengal_pirate/Team12/Team12/menu/game_over/game_over1.png')

selection_menu_option = 0  # To cycle through the 4 options
selection_menu_options = ['Story Mode (Not Available)', 'Arcade Mode', 'Controls', 'Credits']  # The 4 options to select from

plains0_sprite_sheet = spritesheet.SpriteSheet(plains_1)

# # sprite_0 section
plain0_frame_0 = plains0_sprite_sheet.get_image(0, 16, 24, 3, BLACK)

def fade_to_black(surface, background, logo=None, alpha_step=12):
    fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))  # Create a new surface that's the size of the screen
    fade_surface.fill((0, 0, 0))  # Fill it with black

    for alpha in range(0, 255, alpha_step):  # Step from 0 to 255, changing by alpha_step each time
        fade_surface.set_alpha(alpha)  # Set the alpha level of the surface
        surface.blit(background, (0, 0))
        if logo is not None:  # If a logo is provided, draw it on the screen
            logo_rect = logo.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//4 - 100))
            surface.blit(logo, logo_rect)
        surface.blit(fade_surface, (0, 0))  # Draw the surface on the screen
        pygame.display.flip()  # Update the screen
        pygame.time.delay(5)  # Wait for 30 milliseconds

def fade_from_black(surface, background, logo=None, alpha_step=12):
    fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade_surface.fill((0, 0, 0))

    for alpha in range(255, -1, -alpha_step):
        fade_surface.set_alpha(alpha)
        surface.blit(background, (0, 0))  # Use the passed background
        if logo is not None:  # If a logo is provided, draw it on the screen
            logo_rect = logo.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//4 - 100))
            surface.blit(logo, logo_rect)
        surface.blit(fade_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(5)

game_background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
game_background.fill((255, 0, 0))

transitioned = False
# starts the main game loop
while True:

    # Get the screen height
    screen_height = display.get_height()

    # Get a list of all keys currently being pressed down
    keys = pygame.key.get_pressed()

    if player.current_health <= 0:
        game_state = 'game_over_screen'

    # get the event from the queue
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If the event is a quit, exit the game
            sys.exit()
        # Let's assume that pygame.K_SPACE is the key for starting a dash

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                fade_to_black(display, menu_background, logo)
                transitioned = False
                if game_state == 'start_menu':
                    game_state = 'selection_menu'
                elif game_state == 'selection_menu':
                    if selection_menu_option == 1:  # Arcade mode
                        game_state = 'game_active'
                    elif selection_menu_option == 2: # Controls
                        game_state = 'controls'
                    elif selection_menu_option == 3: # Credits
                        game_state = 'credits'
                elif game_state == 'game_over_screen':
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            game_over_menu_option = (game_over_menu_option - 1) % len(game_over_menu_options)
                        elif event.key == pygame.K_DOWN:
                            game_over_menu_option = (game_over_menu_option + 1) % len(game_over_menu_options)
                        elif event.key == pygame.K_RETURN:
                            if game_over_menu_option == 0:  # 'Yes' selected
                                # Here you need to reset all necessary variables for the game loop
                                # like player health, position, score, enemies, etc.                                    player.current_health = player.max_health
                                player.current_health = player.max_health
                                # Reset other variables as needed...
                                game_state = 'game_active'
                            elif game_over_menu_option == 1:  # 'No' selected
                                game_state = 'start_menu'


            # add this to cycle through the menu
            if (game_state == 'selection_menu') or (game_state == 'game_over'):
                if event.key == pygame.K_UP:
                    selection_menu_option = (selection_menu_option - 1) % len(selection_menu_options)
                elif event.key == pygame.K_DOWN:
                    selection_menu_option = (selection_menu_option + 1) % len(selection_menu_options)

            # Check for melee attack button press
            if event.key in [pygame.K_i, pygame.K_j, pygame.K_k, pygame.K_l]:
                if len(button_presses) == 0:
                    button_press_start_time = pygame.time.get_ticks()  # Set the start time of button presses
                button_presses.append(event.key)
        if event.type == pygame.KEYUP:  # Check for keys being released
            if event.key in [pygame.K_i, pygame.K_j, pygame.K_k, pygame.K_l]:
                # handle the logic to stop the attacks
                melee = None# remove 'pass' and replace with your code

    if game_state == 'selection_menu' and not transitioned:
        fade_from_black(display, menu_background, logo)
        transitioned = True

    elif game_state == 'game_active' and not transitioned:
        fade_from_black(display, game_background)
        transitioned = True

    elif game_state == 'controls' and not transitioned:
        fade_from_black(display, game_background)
        transitioned = True

    elif game_state == 'credits' and not transitioned:
        fade_from_black(display, game_background)
        transitioned = True

    if game_state == 'start_menu':
        display.blit(menu_background, (0,0))
        # Render the game title and blinking start prompt
        # Define your font and size
        font = pygame.font.Font(None, 50)

         # Blit the logo image
        logo_rect = logo.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//4 - 100))  # Place the logo at the top quarter of the screen
        display.blit(logo, logo_rect)

        # Create blinking text for the start prompt
        if pygame.time.get_ticks() % 1000 < 500:  # Change 1000 to control the speed of blinking
            start_text = font.render('Press Enter to Start Game', True, (255, 255, 255))  # White color
            start_rect = start_text.get_rect(center=(SCREEN_WIDTH//2, (SCREEN_HEIGHT//4)*3))  # 75% down the screen
            display.blit(start_text, start_rect)

    elif game_state == 'selection_menu':
        # Display the stored background
        display.blit(menu_background, (0, 0))

        # Blit the logo image
        logo_rect = logo.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//4 - 100))  # Place the logo at the top quarter of the screen
        display.blit(logo, logo_rect)

        for i, option in enumerate(selection_menu_options):
            color = (255, 255, 255) if selection_menu_option == i else (100, 100, 100)  # highlight the selected option
            # Use the larger selection_menu_font here
            option_text = selection_menu_font.render(option, True, color)
            # Shift the text down by increasing the y-coordinate
            option_rect = option_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100 + i * 80))  # Arrange options vertically
            display.blit(option_text, option_rect)

    elif game_state == 'game_over_screen':
        display.blit(game_over_background, (0, 0))
        for i, option in enumerate(game_over_menu_options):
            color = (255, 255, 255) if game_over_menu_option == i else (100, 100, 100)  # highlight the selected option
            option_text = selection_menu_font.render(option, True, color)
            option_rect = option_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100 + i * 80))  # Arrange options vertically
            display.blit(option_text, option_rect)

    elif game_state == 'controls':
        display.blit(controls_background, (0, 0))

        controls_text = [
            "W, A, S, D: Movement",

            "Space: Dash",

            "I, J, K, L: Melee attack",

            "Arrows: Fire bullets"
        ]
    
        for i, text in enumerate(controls_text):
            control_text_rendered = selection_menu_font.render(text, True, (255, 255, 255))
            control_text_rect = control_text_rendered.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100 + i * 80))
            display.blit(control_text_rendered, control_text_rect)

    elif game_state == 'credits':
        display.blit(credits_background, (0, 0))

        credits_text = [
            "Game Developer: Brandon Newton",

            "Graphics: Shaad",

            "Sound: Brandon Newton",

            "Special Thanks: Techwise"
        ]

        alpha_value = 255  # start fully visible
        alpha_change = -5  # change by this amount each frame

        running = True
        go_to_main_menu = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # 'Return' key is 'Enter'
                        go_to_main_menu = True
                        break

            if go_to_main_menu:
                break

            for i, text in enumerate(credits_text):
                credit_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                credit_text_rendered = selection_menu_font.render(text, True, (255, 255, 255))
                credit_text_rect = credit_text_rendered.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

                while alpha_value > 0:
                    # Clear screen
                    display.blit(credits_background, (0, 0))

                    # Blit text
                    credit_surface.blit(credit_text_rendered, credit_text_rect)

                    # Change alpha value
                    alpha_value += alpha_change
                    alpha_value = max(min(alpha_value, 255), 0)

                    # Apply new alpha value
                    credit_surface.fill((255, 255, 255, alpha_value), special_flags=pygame.BLEND_RGBA_MULT)

                    # Blit surface onto main display
                    display.blit(credit_surface, (0, 0))

                    pygame.display.flip()
                    pygame.time.delay(5)

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RETURN:  # 'Return' key is 'Enter'
                                go_to_main_menu = True
                                break

                if not running or go_to_main_menu:
                    break

                alpha_value = 255
                alpha_change = -5

            if not running or go_to_main_menu:
                break

            pygame.display.flip()

    elif game_state == 'game_active':
        # Fills the display surface with color
        display.fill((255, 0, 0))

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

        melee_combinations = {
            (pygame.K_i, pygame.K_l): "northeast",
            (pygame.K_i, pygame.K_j): "northwest",
            (pygame.K_k, pygame.K_l): "southeast",
            (pygame.K_k, pygame.K_j): "southwest",
            (pygame.K_i,): "up",
            (pygame.K_k,): "down",
            (pygame.K_j,): "left",
            (pygame.K_l,): "right"
        }

        melee_duration = 10 # Duration in frames

        for combination, direction in melee_combinations.items():
            if all(keys[key] for key in combination):
                if len(active_melee_attacks) == 0:
                    melee = MeleeAttack(
                        player.rect.x,
                        player.rect.y,
                        direction,
                        player.rect.width,
                        duration = 1,  # Duration is always 1 frame
                        projectile = 5
                    )
                    active_melee_attacks.append(melee)
            else:
                melee = None
        
        # ...
        # Update the display scroll based on player's position
        display_scroll[0] = player.rect.x - SCREEN_WIDTH // 2
        display_scroll[1] = player.rect.y - SCREEN_HEIGHT // 2


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

        # Draw a static rectangle to the screen, offset by the display scroll
        display.blit(plain0_frame_0, (100 - display_scroll[0], 100 - display_scroll[1]))
        ### here is where we will determine the plain for the spritesheet

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

        for melee in active_melee_attacks:
            melee.main(display, display_scroll)
            melee.decrease_duration()  # decrease duration for each melee

        # Update active_melee_attacks list after calling the main function on all of them
        active_melee_attacks = [melee for melee in active_melee_attacks if melee.duration > 0]

        # Handle dragon's interaction with enemies and player
        for i in range(len(enemies) - 1, -1, -1):  # Iterate over the indices in reverse
            for j in range(len(enemies) - 1, i, -1):  # Compare with every enemy after i
        
                # For player collision:
                if isinstance(enemies[i], DragonHead): #and expand_rect(enemies[i].rect, expansion_size).colliderect(player.rect):
                    player.health = 0  # Set player's health to 0
                else:
                    enemies[i].main(display, display_scroll, player)
                    enemies[i].update_position(player)
        
                # Check if the enemy is a DragonHead
                if isinstance(enemies[i], DragonHead):
                    # Update dragon's position and sprite based on its current direction
                    enemies[i].update_position(player)
                    enemies[i].update_sprite()  # Assuming the DragonHead class has an 'update_sprite' method

        # Draw the enemies
        for i in range(len(enemies) - 1, -1, -1):  # Iterate over the indices in reverse
            for j in range(len(enemies) - 1, i, -1):  # Compare with every enemy after i
        
                # For player collision:
                if isinstance(enemies[i], DragonHead) and expand_rect(enemies[i].rect, expansion_size).colliderect(player.rect):
                    player.health = 0  # Set player's health to 0
                else:
                    enemies[i].main(display, display_scroll, player)
                    enemies[i].update_position(player)  # Update enemy sprite based on direction
                  

                
        # Limit the game to 60 frames per second
        clock.tick(60)
        pass
    
    # Update the full display surface to the screen
    pygame.display.update()


