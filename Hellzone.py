# Imports necessary modules
import pygame
import sys 
import math


#Initializes all imported pygame modules
pygame.init()

pygame.mixer.init()

#load mp3 file
pygame.mixer.music.load('final_boss.mp3')

#Play the music indefinitely
pygame.mixer.music.play(-1)

print(pygame.get_error())

#sets th size of the screen for display
display = pygame.display.set_mode((800, 600))
SCREEN_WIDTH, SCREEN_HEIGHT = display.get_size()

# creates an object to help trakc time
clock = pygame.time.Clock()

# creates a class for the player and attributes
class Player:
    def __init__(self, x, y, width, height): # Define initital properties of the player
        self.x = x
        self.y = y
        self.max_health =100
        self.current_health = 100
        self.max_stamina = 100
        self.current_stamina = 100
        self.stamina_recovery_rate = 0.01
        self.max_power = 100
        self.current_power = self.max_power
        self.speed = 5 #define player's speed
        self.frame = 0
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.moving_northeast = False
        self.moving_northwest = False
        self.moving_southeast = False
        self.moving_southwest = False
        self.dash_speed = 10 # A faster speed for dashing
        self.dashing = False #Indicates whether the player is currently dashing
        

        # checks files for images to use when player moves in a particular direction
        try:
            self.images = {
                # the animation of each direction should cycle through different files
                # with each file in the set differing only by the last number
                # we would have to put all of the files in the prackets if we do not have a common last number
                # below im assuming we use 4 images for each direction, the more sprites we use the more detail we have
                "up": [pygame.image.load('path_to_up_image_{}.png'.format(i)) for i in range(4)],
                "down": [pygame.image.load('path_to_down_image_{}.png'.format(i)) for i in range(4)],
                "left": [pygame.image.load('path_to_left_image_{}.png'.format(i)) for i in range(4)],
                "right": [pygame.image.load('path_to_right_image_{}.png'.format(i)) for i in range(4)],
                "northeast": [pygame.image.load('path_to_northeast_image_{}.png'.format(i)) for i in range(4)],
                "northwest": [pygame.image.load('path_to_northwest_image_{}.png'.format(i)) for i in range(4)],
                "southeast": [pygame.image.load('path_to_southeast_image_{}.png'.format(i)) for i in range(4)],
                "southwest": [pygame.image.load('path_to_southwest_image_{}.png'.format(i)) for i in range(4)],
            }
            self.current_image = self.images["right"]
            self.width = self.current_image.get_width()
            self.height = self.current_image.get_height()
            self.use_images = True

        # if no images can be found we default to a black triangle
        except (pygame.error, FileNotFoundError):
            self.use_images = False
            self.width = 32
            self.height = 32

    #function to use in main program that updates the players image based on directional movement
    def update_image(self, direction):
        if self.use_images:
            self.frame = (self.frame +1) % 4 # cycle through frames 0-3
            self.direction = direction
            self.current_image = self.images[direction][self.frame]

    def draw_bars(self, display):
        bar_width = 200
        bar_height = 10
        health_bar_color = (0,255,0) 
        stamina_bar_color = (0,0,255)
        power_bar_color = (255,255,0)
        margin = 20
        health_bar_x = 20 # Distance from left side of the screen
        health_bar_y = SCREEN_HEIGHT - (bar_height *2) - (margin *2) # Distance from top of the screen

        stamina_bar_x = 20 # Distance from left side of the screen
        stamina_bar_y = SCREEN_HEIGHT - (bar_height *1.5) - (margin *1.5) # Distance from top of the screen

        power_bar_x = 20 # Distance from left side of the screen
        power_bar_y = SCREEN_HEIGHT - bar_height - margin # Distance from top of the screen


        # Calculate the width of the health bar based on current health
        current_health_width = int((self.current_health / self.max_health) * bar_width)
        current_stamina_width = int((self.current_stamina / self.max_stamina) * bar_width)
        current_power_width = int((self.current_power / self.max_power) * bar_width)

        # Draw the full health bar
        pygame.draw.rect(display, (128,128,128), pygame.Rect(health_bar_x, health_bar_y, bar_width, bar_height))
        pygame.draw.rect(display, (128,128,128), pygame.Rect(stamina_bar_x, stamina_bar_y, bar_width, bar_height))
        pygame.draw.rect(display, (128,128,128), pygame.Rect(power_bar_x, power_bar_y, bar_width, bar_height))

        # Draw the current health on top of the full health bar
        pygame.draw. rect(display, health_bar_color, pygame.Rect(health_bar_x, health_bar_y, current_health_width, bar_height))
        pygame.draw. rect(display, stamina_bar_color, pygame.Rect(stamina_bar_x, stamina_bar_y, current_stamina_width, bar_height))
        pygame.draw. rect(display, power_bar_color, pygame.Rect(power_bar_x, power_bar_y, current_power_width, bar_height))

        if not self.dashing:
            self.current_stamina += self.stamina_recovery_rate
            if self.current_stamina > self.max_stamina:
                self.current_stamina = self.max_stamina


    def main(self, display, scroll): # Method for displaying the player
        
        if self.use_images:
            #the transform.scale changes the size of the player
            display.blit(pygame.transform.scale(self.current_image, (32,42)), (self.x - scroll[0], self.y - scroll[1]))
        else:
            pygame.draw.rect(display, (0,0,0), (self.x - scroll[0], self.y - scroll[1], self.width, self.height))
  
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.moving_northeast = False
        self.moving_northwest = False
        self.moving_southeast = False
        self.moving_southwest = False
        
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

        # Let's assume that pygame.K_SPACE is the key for starting a dash


    # Get a list of all keys currently being pressed down
    keys = pygame.key.get_pressed()  


    player.main(display, display_scroll)
    player.draw_bars(display)


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

    # Move the player according to key presses and updates images
    if keys[pygame.K_w]:
        if keys[pygame.K_SPACE] and (player.current_stamina > 0):
            player.y -= player.dash_speed
            player.current_stamina -= 0.5
            pygame.time.set_timer(pygame.USEREVENT, 1000) #Dash lasts for 1 second
        else:
            player.y -= player.speed 
        #player.y -= player.speed
        player.update_image("up")
        player.moving_up = True
    if keys[pygame.K_a]:
        if keys[pygame.K_SPACE] and (player.current_stamina > 0):
            player.x -= player.dash_speed
            player.current_stamina -= 0.5
            pygame.time.set_timer(pygame.USEREVENT, 1000) #Dash lasts for 1 second
        else:
            player.x -= player.speed 
        #player.x -= player.speed
        player.update_image("left")
        player.moving_left = True
    if keys[pygame.K_s]:
        if keys[pygame.K_SPACE] and (player.current_stamina > 0):
            player.y += player.dash_speed
            player.current_stamina -= 0.5
            pygame.time.set_timer(pygame.USEREVENT, 1000) #Dash lasts for 1 second
        else:
            player.y += player.speed 
        #player.y += player.speed
        player.update_image("down")
        player.moving_down = True
    if keys[pygame.K_d]:
        if keys[pygame.K_SPACE] and (player.current_stamina > 0):
            player.x += player.dash_speed
            player.current_stamina -= 0.5
            pygame.time.set_timer(pygame.USEREVENT, 1000) #Dash lasts for 1 second
        else:
            player.x += player.speed 
        #player.x += player.speed
        player.update_image("right")
        player.moving_right = True
    if keys[pygame.K_w] and keys[pygame.K_d]:
        if keys[pygame.K_SPACE] and (player.current_stamina > 0):
            player.x += player.dash_speed / math.sqrt(2)
            player.y -= player.dash_speed / math.sqrt(2)
            player.current_stamina -= 0.5
            pygame.time.set_timer(pygame.USEREVENT, 1000) #Dash lasts for 1 second
        else:
            player.x += player.speed / math.sqrt(2)
            player.y -= player.speed / math.sqrt(2)
        #player.x += player.speed
        #player.y -= player.speed
        player.update_image("northeast")
        player.moving_northeast = True
    if keys[pygame.K_w] and keys[pygame.K_a]:
        if keys[pygame.K_SPACE] and (player.current_stamina > 0):
            player.x -= player.dash_speed / math.sqrt(2)
            player.y -= player.dash_speed / math.sqrt(2)
            player.current_stamina -= 0.5
            pygame.time.set_timer(pygame.USEREVENT, 1000) #Dash lasts for 1 second
        else:
            player.x -= player.speed / math.sqrt(2)
            player.y -= player.speed / math.sqrt(2)
        #player.x -= player.speed
        #player.y -= player.speed
        player.update_image("northwest")
        player.moving_northwest = True
    if keys[pygame.K_s] and keys[pygame.K_d]:
        if keys[pygame.K_SPACE] and (player.current_stamina > 0):
            player.x += player.dash_speed / math.sqrt(2)
            player.y += player.dash_speed / math.sqrt(2)
            player.current_stamina -= 0.5
            pygame.time.set_timer(pygame.USEREVENT, 1000) #Dash lasts for 1 second
        else:
            player.x += player.speed / math.sqrt(2)
            player.y += player.speed / math.sqrt(2)
        #player.x += player.speed
        #player.y += player.speed
        player.update_image("southeast")
        player.moving_southeast = True
    if keys[pygame.K_s] and keys[pygame.K_a]:
        if keys[pygame.K_SPACE] and (player.current_stamina > 0):
            player.x -= player.dash_speed / math.sqrt(2)
            player.y += player.dash_speed / math.sqrt(2)
            player.current_stamina -= 0.5
            pygame.time.set_timer(pygame.USEREVENT, 1000) #Dash lasts for 1 second
        else:
            player.x -= player.speed / math.sqrt(2)
            player.y += player.speed / math.sqrt(2)
        #player.x -= player.speed
        #player.y += player.speed
        player.update_image("southwest")
        player.moving_southwest = True

    if player.dashing and pygame.time.get_ticks() / 1000 > player.dash_time + player.dash_duration:
        player.dashing = False    

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
