import pygame
import random
import sys


class Snake:
    def __init__(self, field):
        self.speed = field.FPS // 10
        self.positions = [[0, 2], [0, 1], [0, 0]]
        self.directions = {
            "up": (-1, 0),
            "down": (1, 0),
            "right": (0, 1),
            "left": (0, -1),
        }
        self.direction = "right"
        self.is_alive = True

    def move(self, field):
        prev_pos = self.positions[0].copy()

        self.positions[0][0] += self.directions[self.direction][0]
        self.positions[0][1] += self.directions[self.direction][1]

        status = self.check(field)

        if status == "dead":
            self.positions[0] = prev_pos
            return

        for i in range(1, len(self.positions)):
            self.positions[i], prev_pos = prev_pos.copy(), self.positions[i]

        if status == "apple":
            self.positions.append(prev_pos.copy())
            field.generate_apple(self)
            pygame.display.set_caption(f"Snake score: {len(self.positions) - 3}")

    def check(self, field):
        if self.positions[0][0] >= field.HEIGHT or self.positions[0][0] < 0:
            self.is_alive = False
            return "dead"

        if self.positions[0][1] >= field.WIDTH or self.positions[0][1] < 0:
            self.is_alive = False
            return "dead"

        if self.positions.count(self.positions[0]) > 1:
            self.is_alive = False
            return "dead"

        if self.positions[0] == field.apple_position:
            return "apple"

        return "nothing"

    def change_direction(self, event):
        if event.key == pygame.K_RIGHT and self.direction != "left":
            self.direction = "right"
        if event.key == pygame.K_LEFT and self.direction != "right":
            self.direction = "left"
        if event.key == pygame.K_UP and self.direction != "down":
            self.direction = "up"
        if event.key == pygame.K_DOWN and self.direction != "up":
            self.direction = "down"


class Field:
    def __init__(self):
        self.WINDOW_WIDTH = 640
        self.WINDOW_HEIGHT = 480

        self.CELL_SIZE = 20
        self.BORDER_WIDTH = 2

        self.WIDTH = self.WINDOW_WIDTH // self.CELL_SIZE
        self.HEIGHT = self.WINDOW_HEIGHT // self.CELL_SIZE

        self.BG_COLOR = (0, 0, 0)
        self.GRID_COLOR = (40, 40, 40)
        self.APPLE_COLOR = (255, 0, 0)
        self.APPLE_OUTER_COLOR = (155, 0, 0)
        self.SNAKE_COLOR = (0, 255, 0)
        self.SNAKE_OUTER_COLOR = (0, 155, 0)

        self.FPS = 120

        self.apple_position = [random.randint(1, self.HEIGHT - 1), random.randint(0, self.WIDTH - 1)]

    def start(self, snake):
        pygame.init()
        self.FPS_CLOCK = pygame.time.Clock()
        self.DISPLAY = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Snake score: 0")

        self.DISPLAY.fill(self.BG_COLOR)
        self.draw_rect((0, 0), "snake")
        self.draw_rect((0, 20), "snake")

        move_ticker = snake.speed

        while snake.is_alive:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    snake.change_direction(event)

            if move_ticker == 0:
                move_ticker = snake.speed
                snake.move(self)

            else:
                move_ticker -= 1

            self.draw(snake)
            pygame.display.flip()
            self.FPS_CLOCK.tick(self.FPS)

    def generate_apple(self, snake):
        free_cells = []
        for i in range(self.HEIGHT):
            for j in range(self.WIDTH):
                if [i, j] not in snake.positions:
                    free_cells.append([i, j])

        self.apple_position = random.choice(free_cells)

    def draw_rect(self, pos, type_of_cell):
        pos_x, pos_y = pos
        color, outer_color = (0, 0, 0), (0, 0, 0)

        if type_of_cell == "nothing":
            color = self.BG_COLOR
            outer_color = self.GRID_COLOR
        elif type_of_cell == "snake":
            color = self.SNAKE_COLOR
            outer_color = self.SNAKE_OUTER_COLOR
        elif type_of_cell == "apple":
            color = self.APPLE_COLOR
            outer_color = self.APPLE_OUTER_COLOR

        pygame.draw.rect(self.DISPLAY, color, (pos_x, pos_y, self.CELL_SIZE, self.CELL_SIZE))
        pygame.draw.rect(self.DISPLAY, outer_color, (pos_x, pos_y, self.CELL_SIZE, self.CELL_SIZE), self.BORDER_WIDTH)

    def draw(self, snake):
        for i in range(self.HEIGHT):
            for j in range(self.WIDTH):
                if [i, j] in snake.positions:
                    self.draw_rect((j * self.CELL_SIZE, i * self.CELL_SIZE), "snake")
                elif [i, j] == self.apple_position:
                    self.draw_rect((j * self.CELL_SIZE, i * self.CELL_SIZE), "apple")
                else:
                    self.draw_rect((j * self.CELL_SIZE, i * self.CELL_SIZE), "nothing")


field = Field()
snake = Snake(field)

field.start(snake)
