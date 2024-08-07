import pygame
import csv
from neuralNet import *


def load_snake(snake_num):
    load = Snake()

    file_snake = open(f"data/Snake{snake_num}.csv", "r")
    r = csv.reader(file_snake)

    d = dict()
    i = 0
    keys = []
    for row in r:
        if i == 0:
            for k in row:
                keys.append(k)
        else:
            j = 0
            for v in row:
                d[keys[j]] = eval(v)
                j += 1

        i += 1

    load.brain.file_to_net(d)


class Snake:
    def __init__(self):
        self.speed = 20
        self.positions = [[2, 2], [2, 1], [2, 0]]
        self.directions = {
            "up": (-1, 0),
            "down": (1, 0),
            "right": (0, 1),
            "left": (0, -1),
        }
        self.direction = "right"
        self.is_alive = True

        self.time_to_live = 200
        self.life_time = 0
        self.fitness = 0

        self.vision = [0] * 24
        self.decision = []

        self.brain = NeuralNet(24, 18, 4)

    def mutate(self, mutate_rate):
        self.brain.mutate(mutate_rate)

    def calculate_fitness(self):
        if len(self.positions) < 10:
            self.fitness = int(self.life_time * self.life_time * (2 ** len(self.positions)))
        else:
            self.fitness = self.life_time * self.life_time
            self.fitness *= 2 ** 10
            self.fitness *= (len(self.positions) - 9)

    def crossover(self, partner):
        child = Snake()
        child.brain = self.brain.crossover(partner.brain)
        return child

    def clone(self):
        n = Snake()
        n.brain = self.brain
        n.is_alive = True
        return n

    def move(self, field):
        prev_pos = self.positions[0].copy()

        self.positions[0][0] += self.directions[self.direction][0]
        self.positions[0][1] += self.directions[self.direction][1]

        status = self.check(field)

        if status == "dead":
            self.positions[0] = prev_pos
            return

        self.life_time += 1
        self.time_to_live -= 1

        if self.time_to_live < 0:
            self.is_alive = False
            return

        for i in range(1, len(self.positions)):
            self.positions[i], prev_pos = prev_pos.copy(), self.positions[i]

        if status == "apple":
            self.positions.append(prev_pos.copy())
            field.generate_apple(self)
            self.time_to_live += 100
            pygame.display.set_caption(f"Snake score: {len(self.positions) - 3}")

    def look(self, field):
        self.vision = [0] * 24
        dirs = ["up", "up-right", "right", "down-right", "down", "down-left", "left", "up-left"]

        border = self.get_border(field)
        for i in range(8):
            self.vision[i] = border[dirs[i]]

        body = self.get_body(field)
        for i in range(8):
            self.vision[8 + i] = body[dirs[i]]

        apple = self.get_apple(field)
        for i in range(8):
            self.vision[16 + i] = apple[dirs[i]]

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
        if event.key == pygame.K_RIGHT and self.positions[0][0] != self.positions[1][0]:
            self.direction = "right"
        if event.key == pygame.K_LEFT and self.positions[0][0] != self.positions[1][0]:
            self.direction = "left"
        if event.key == pygame.K_UP and self.positions[0][1] != self.positions[1][1]:
            self.direction = "up"
        if event.key == pygame.K_DOWN and self.positions[0][1] != self.positions[1][1]:
            self.direction = "down"

    def change_direction_by_ai(self):
        self.decision = self.brain.output(self.vision)

        ma = max(self.decision)
        max_index = 0
        for i in range(len(self.decision)):
            if ma == self.decision[i]:
                max_index = i

        if max_index == 0:
            self.direction = "up"
        elif max_index == 1:
            self.direction = "left"
        elif max_index == 2:
            self.direction = "down"
        else:
            self.direction = "right"

    def get_border(self, field):
        return {"up": 1 / (self.positions[0][0] + 1),
                "up-right": 1 / (min(self.positions[0][0], field.WIDTH - 1 - self.positions[0][1]) + 1),
                "left": 1 / (self.positions[0][1] + 1),
                "up-left": 1 / (min(self.positions[0]) + 1),
                "down": 1 / (field.HEIGHT - 1 - self.positions[0][0] + 1),
                "down-right": 1 / (
                        min(field.HEIGHT - 1 - self.positions[0][0], field.WIDTH - 1 - self.positions[0][1]) + 1),
                "down-left": 1 / (min(field.HEIGHT - 1 - self.positions[0][0], self.positions[0][1]) + 1),
                "right": 1 / (field.WIDTH - 1 - self.positions[0][1] + 1)
                }

    def get_body(self, field):
        directions = {"left": -1,
                      "up-left": -1,
                      "right": -1,
                      "up-right": -1,
                      "up": -1,
                      "down-left": -1,
                      "down": -1,
                      "down-right": -1
                      }

        for i in range(self.positions[0][1] - 1, -1, -1):
            if [self.positions[0][0], i] in self.positions:
                directions["left"] = 1 / (self.positions[0][1] - i)
                break

        for i in range(self.positions[0][1] + 1, field.WIDTH):
            if [self.positions[0][0], i] in self.positions:
                directions["right"] = 1 / (i - self.positions[0][1])
                break

        for i in range(self.positions[0][0] + 1, field.HEIGHT):
            if [i, self.positions[0][1]] in self.positions:
                directions["down"] = 1 / (i - self.positions[0][0])
                break

        for i in range(self.positions[0][0] - 1, -1, -1):
            if [i, self.positions[0][1]] in self.positions:
                directions["up"] = 1 / (self.positions[0][0] - i)
                break

        for i in range(1, min(self.positions[0]) + 1):
            if [self.positions[0][0] - i, self.positions[0][1] - i] in self.positions:
                directions["up-left"] = 1 / i
                break

        for i in range(1, min(self.positions[0][0], field.WIDTH - 1 - self.positions[0][1]) + 1):
            if [self.positions[0][0] - i, self.positions[0][1] + i] in self.positions:
                directions["up-right"] = 1 / i
                break

        for i in range(1, min(field.HEIGHT - 1 - self.positions[0][0], field.WIDTH - 1 - self.positions[0][1]) + 1):
            if [self.positions[0][0] + i, self.positions[0][1] + i] in self.positions:
                directions["down-right"] = 1 / i
                break

        for i in range(1, min(field.HEIGHT - 1 - self.positions[0][0], self.positions[0][1]) + 1):
            if [self.positions[0][0] + i, self.positions[0][1] - i] in self.positions:
                directions["down-left"] = 1 / i
                break

        return directions

    def get_apple(self, field):
        directions = {"left": 0,
                      "up-left": 0,
                      "right": 0,
                      "up-right": 0,
                      "up": 0,
                      "down-left": 0,
                      "down": 0,
                      "down-right": 0
                      }

        if self.positions[0][1] == field.apple_position[1] and self.positions[0][0] >= field.apple_position[0]:
            directions["up"] = 1
        if sum(self.positions[0]) == sum(field.apple_position) and self.positions[0][0] >= field.apple_position[0]:
            directions["up-right"] = 1
        if self.positions[0][0] == field.apple_position[0] and self.positions[0][1] <= field.apple_position[1]:
            directions["right"] = 1
        if field.apple_position[0] - self.positions[0][0] == field.apple_position[1] - self.positions[0][1] and \
                self.positions[0][0] <= field.apple_position[0]:
            directions["down-right"] = 1
        if self.positions[0][1] == field.apple_position[1] and self.positions[0][0] <= field.apple_position[0]:
            directions["down"] = 1
        if sum(self.positions[0]) == sum(field.apple_position) and self.positions[0][0] <= field.apple_position[0]:
            directions["down-left"] = 1
        if self.positions[0][0] == field.apple_position[0] and self.positions[0][1] >= field.apple_position[1]:
            directions["left"] = 1
        if field.apple_position[0] - self.positions[0][0] == field.apple_position[1] - self.positions[0][1] and \
                self.positions[0][0] >= field.apple_position[0]:
            directions["up-left"] = 1

        return directions

    def save_snake(self, snake_num, score, pop_id):
        snake_stats = {"Top Score": score, "Population ID": pop_id}

        file_stats = open(f"data/SnakeStats{snake_num}.csv", "w")

        w = csv.DictWriter(file_stats, snake_stats.keys())
        w.writeheader()
        w.writerow(snake_stats)
        file_stats.close()

        snake_info = self.brain.net_to_file()

        file_snake = open(f"data/Snake{snake_num}.csv", "w")

        w = csv.DictWriter(file_snake, snake_info.keys())
        w.writeheader()
        w.writerow(snake_info)
        file_snake.close()
