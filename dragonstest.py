import pygame
import random
import math
import time

# Global constants
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
BLOCK_SIZE = 20
SNAKE_SPEED = 5
DIRECTION_UPDATE_DELAY = 0  # delay in seconds

RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

class SnakePart:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE))

class SnakeHead(SnakePart):
    def __init__(self, x, y):
        super().__init__(x, y, RED)

class SnakeBody(SnakePart):
    def __init__(self, x, y):
        super().__init__(x, y, WHITE)

class Snake:
    def __init__(self):
        self.direction = random.choice([(BLOCK_SIZE, 0), (-BLOCK_SIZE, 0), (0, BLOCK_SIZE), (0, -BLOCK_SIZE)])
        self.body = [SnakeHead(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)]
        self.body.extend([SnakeBody(WINDOW_WIDTH // 2 - i*BLOCK_SIZE, WINDOW_HEIGHT // 2) for i in range(1, 3)])
        self.last_direction_change = time.time()

    def update(self, food):
        # Make the snake's body follow the head
        self.body = [SnakeHead(self.body[0].x + self.direction[0], self.body[0].y + self.direction[1])] + \
                    [SnakeBody(part.x, part.y) for part in self.body[:-1]]

        # Check if the snake hit the wall
        if self.body[0].x < 0 or self.body[0].x >= WINDOW_WIDTH or self.body[0].y < 0 or self.body[0].y >= WINDOW_HEIGHT:
            return False  # Game over

        # Check if the snake has eaten the food
        if food.position == (self.body[0].x, self.body[0].y):
            food.position = food.get_random_position()  # food respawns at a new location
            self.body.append(SnakeBody(self.body[-1].x, self.body[-1].y))  # The snake grows

        # Update the snake's direction
        now = time.time()
        if now - self.last_direction_change >= DIRECTION_UPDATE_DELAY:
            self.change_direction_toward_food(food)
            self.last_direction_change = now

        return True

    def change_direction_toward_food(self, food):
        head = self.body[0]
        dx = food.position[0] - head.x
        dy = food.position[1] - head.y

        if dx < 0:  # food is to the left
            dirx = -BLOCK_SIZE
        elif dx > 0:  # food is to the right
            dirx = BLOCK_SIZE
        else:
            dirx = 0

        if dy < 0:  # food is above
            diry = -BLOCK_SIZE
        elif dy > 0:  # food is below
            diry = BLOCK_SIZE
        else:
            diry = 0

        self.direction = (dirx, diry)

    def draw(self, screen):
        for part in self.body:
            part.draw(screen)


class Food:
    def __init__(self):
        self.position = self.get_random_position()

    def get_random_position(self):
        x = random.randrange(0, WINDOW_WIDTH, BLOCK_SIZE)
        y = random.randrange(0, WINDOW_HEIGHT, BLOCK_SIZE)
        return (x, y)

    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, pygame.Rect(self.position[0], self.position[1], BLOCK_SIZE, BLOCK_SIZE))

    def move(self, direction):
        dx, dy = direction
        new_x, new_y = self.position[0] + dx, self.position[1] + dy

        if 0 <= new_x < WINDOW_WIDTH and 0 <= new_y < WINDOW_HEIGHT:
            self.position = (new_x, new_y)

def main():
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    snake = Snake()
    food = Food()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    food.move((0, -BLOCK_SIZE))
                elif event.key == pygame.K_DOWN:
                    food.move((0, BLOCK_SIZE))
                elif event.key == pygame.K_LEFT:
                    food.move((-BLOCK_SIZE, 0))
                elif event.key == pygame.K_RIGHT:
                    food.move((BLOCK_SIZE, 0))
                elif event.key == pygame.K_w:
                    food.move((-BLOCK_SIZE, -BLOCK_SIZE))
                elif event.key == pygame.K_s:
                    food.move((BLOCK_SIZE, -BLOCK_SIZE))
                elif event.key == pygame.K_a:
                    food.move((-BLOCK_SIZE, BLOCK_SIZE))
                elif event.key == pygame.K_d:
                    food.move((BLOCK_SIZE, BLOCK_SIZE))

        screen.fill((0, 0, 0))  # Fill the screen with black to differentiate the snake body (white), head (red), and food (blue)

        if not snake.update(food):
            pygame.quit()
            return

        for part in snake.body:  # changed from snake.parts to snake.body
            part.draw(screen)

        food.draw(screen)

        pygame.display.update()
        clock.tick(SNAKE_SPEED)

if __name__ == "__main__":
    main()

