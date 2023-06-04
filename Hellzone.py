# Imports necessary modules
import pygame
import sys 
import math

#Initializes all imported pygame modules
pygame.init()

#sets th size of the screen for display
display = pygame.display.set_mode((800, 600))

# creates an object to help trakc time
clock = pygame.time.Clock()

# creates a class for the player
class Player:
    def __init__(self, x, y, width, height): # Define initital properties of the player
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 5 #define player's speed

    def main(self, display, scroll): # Method for displaying the player
        pygame.draw.rect(display, (0,0,0), (self.x - scroll[0], self.y - scroll[1], self.width, self.height))

# Creates a class for the bullet
class PlayerBullet:
    def __init__(self, x, y, direction): #Define initial properties of the bullet
        self.x = x
        self.y = y
        self.speed = 10
        self.direction = direction

        # Condition to check the direction of the bullet and adjust velocity accordingly
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

    def main(self, display, scroll): # Method for moving and displaying the bullet
        self.x += self.x_vel
        self.y += self.y_vel

        pygame.draw.circle(display, (0,0,0), (self.x - scroll[0], self.y - scroll[1]), 5)

# Creates an instance of the player
player = Player(400, 300, 32, 32) 

# Defines the initial display scroll
display_scroll = [0,0]

# Creates a list to store player bullets
player_bullets = []

# starts the main game loop
while True:
    # Fills the display surface with color
    display.fill((255,0,0))

    # get the event from the queue
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # If the event is a quit, exit the game
            sys.exit()

    # Get a list of all keys currently being pressed down
    keys = pygame.key.get_pressed()

    #Check if bullet has been fired
    bullet_fired = False

    # Check for key presses to determine buller direction, create bullet if conditions are met
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

    # Move the player according to key presses -- Fixed Bug
    if keys[pygame.K_w]:
        player.y -= player.speed
    if keys[pygame.K_a]:
        player.x -= player.speed
    if keys[pygame.K_s]:
        player.y += player.speed
    if keys[pygame.K_d]:
        player.x += player.speed

    # Update the display scroll based on player's position
    display_scroll[0] = player.x - 400
    display_scroll[1] = player.y - 300

    # Draw a static rectangle to the screen, offset by the display scroll
    pygame.draw.rect(display, (255, 255, 255), (100-display_scroll[0], 100-display_scroll[1], 16, 16))

    # Update the player display
    player.main(display, display_scroll)

    # Update the bullet displays
    for bullet in player_bullets:
        bullet.main(display, display_scroll)

    # Limit the game to 60 frames per second
    clock.tick(60)

    #Update the full display surface to the screen
    pygame.display.update()
