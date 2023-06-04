#Importing necessary modules
import pygame
import sys 

#initializing all imported pygame modules
pygame.init()

# creates a window for diaplaying the game
display = pygame.display.set_mode((800, 600))

# creates a clock object that can be used to track time
clock = pygame.time.Clock()

# Defines a class Player
class Player:
    # The init method is the intializer (similar to a constructor) that gets called
    # when a new object is created from the class
    def __init__(self, x, y, width, height):
        # x and y are the coordinates of the player
        self.x = x
        self.y = y
        # width and height are the dimensions of the player
        self.width = width
        self.height = height
    # Defining the main mething which is responsible for drawing the player object
    def main(self, display):
        pygame.draw.rect(display, (0,0,0), (self.x, self.y, self.width, self.height))

# creating a player bject at position (400,300) with width and height of (32, 32)
player = Player(400, 300, 32, 32) 

#initializing a scroll variable for the display
display_scroll = [0,0]

#starting the main game loop
while True:

    #filling the display with red color
    display.fill((255,0,0))

    #getting all the events from the queue
    for event in pygame.event.get():
        #if the event is quit (closing the window), terminate the program
        if event.type == pygame.QUIT:
            sys.exit(
            pygame.QUIT
            )
    # getting the state of all keyboard buttons
    keys = pygame.key.get_pressed()

    #drawing a white rectangle on the display at position (100,100) with width and height of 16 pixels
    pygame.draw.rect(display, (255, 255, 255), (100-display_scroll[0], 100-display_scroll[1], 16, 16))

    #if a key is pressed move screen to the right
    if keys[pygame.K_a]:
        display_scroll[0] -= 5
    #if d key is pressed move screen to the left
    if keys[pygame.K_d]:
        display_scroll[0] += 5
    #if w key is pressed move screen downward
    if keys[pygame.K_w]:
        display_scroll[1] -= 5
    #if s key is pressed move screen upward
    if keys[pygame.K_s]:
        display_scroll[1] += 5

    #drawing the player on the display
    player.main(display)

    #delay to get 60 fps
    clock.tick(60)

    #updating the contents of the entire display
    pygame.display.update()