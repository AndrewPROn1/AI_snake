import random
import math


def column(arr):
    n = Matrix(len(arr), 1)
    for i in range(len(arr)):
        n.matrix[i][0] = arr[i]

    return n


def sigmoid(x):
    return 1 / (1 + math.e ** (-x))


class Matrix:
    rows: int
    cols: int
    matrix: [[float]]

    def __init__(self, *args, **kwargs):
        if "data" in kwargs:
            self.rows = len(kwargs["data"])
            self.cols = len(kwargs["data"][0])
            self.matrix = kwargs["data"].copy()
            return
        self.rows = args[0]
        self.cols = args[1]
        self.matrix = [[0 for _ in range(self.cols)] for __ in range(self.rows)]

    def from_array(self, arr):
        for i in range(self.rows):
            for j in range(self.cols):
                self.matrix[i][j] = arr[i * self.cols + j]

    def to_array(self):
        arr = []
        for i in range(self.rows):
            for j in range(self.cols):
                arr.append(self.matrix[i][j])

        return arr

    def output(self):
        for i in range(self.rows):
            print(*self.matrix[i], sep=' ')

    def __mul__(self, other):
        if isinstance(other, Matrix):
            if self.rows == other.rows and self.cols == other.cols:
                newMatrix = Matrix(self.rows, self.cols)
                for i in range(self.rows):
                    for j in range(self.cols):
                        newMatrix.matrix[i][j] = self.matrix[i][j] * other.matrix[i][j]

                return newMatrix
            return

        for i in range(self.rows):
            for j in range(self.cols):
                self.matrix[i][j] *= other

    def randomize(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.matrix[i][j] = random.uniform(-1, 1)

    def __add__(self, other):
        if isinstance(other, Matrix):
            if self.rows == other.rows and self.cols == other.cols:
                newMatrix = Matrix(self.rows, self.cols)
                for i in range(self.rows):
                    for j in range(self.cols):
                        newMatrix.matrix[i][j] = self.matrix[i][j] + other.matrix[i][j]

                return newMatrix
            return

        for i in range(self.rows):
            for j in range(self.cols):
                self.matrix[i][j] += other

    def __sub__(self, other):
        if isinstance(other, Matrix):
            if self.rows == other.rows and self.cols == other.cols:
                newMatrix = Matrix(self.rows, self.cols)
                for i in range(self.rows):
                    for j in range(self.cols):
                        newMatrix.matrix[i][j] = self.matrix[i][j] - other.matrix[i][j]

                return newMatrix
            return

        for i in range(self.rows):
            for j in range(self.cols):
                self.matrix[i][j] -= other

    def dot(self, n):
        res = Matrix(self.rows, n.cols)

        if self.cols == n.rows:
            for i in range(self.rows):
                for j in range(n.cols):
                    su = 0
                    for k in range(self.cols):
                        su += self.matrix[i][k] * n.matrix[k][j]

                    res.matrix[i][j] = su

        return res

    def add_bias(self):
        n = Matrix(self.rows + 1, 1)
        for i in range(self.rows):
            n.matrix[i][0] = self.matrix[i][0]
        n.matrix[self.rows][0] = 1

        return n

    def activate(self):
        n = Matrix(self.rows, self.cols)
        for i in range(self.rows):
            for j in range(self.cols):
                n.matrix[i][j] = sigmoid(self.matrix[i][j])

        return n

    def sigmoid_derived(self):
        n = Matrix(self.rows, self.cols)
        for i in range(self.rows):
            for j in range(self.cols):
                n.matrix[i][j] = self.matrix[i][j] * (1 - self.matrix[i][j])

        return n

    def remove_bottom_layer(self):
        n = Matrix(self.rows - 1, self.cols)
        for i in range(n.rows):
            for j in range(self.cols):
                n.matrix[i][j] = self.matrix[i][j]

        return n

    def transpose(self):
        n = Matrix(self.cols, self.rows)
        for i in range(self.rows):
            for j in range(self.cols):
                n.matrix[j][i] = self.matrix[i][j]

        return n

    def mutate(self, mutations_rate):
        for i in range(self.rows):
            for j in range(self.cols):
                rand = random.random()
                if rand < mutations_rate:
                    self.matrix[i][j] += random.gauss() / 5

                    if self.matrix[i][j] > 1:
                        self.matrix[i][j] = 1
                    if self.matrix[i][j] < -1:
                        self.matrix[i][j] = -1

    def crossover(self, partner):
        child = Matrix(self.rows, self.cols)

        rand_r = random.randint(0, self.rows - 1)
        rand_c = random.randint(0, self.cols - 1)

        for i in range(self.rows):
            for j in range(self.cols):
                if i < rand_r or (i == rand_r and j <= rand_c):
                    child.matrix[i][j] = self.matrix[i][j]
                else:
                    child.matrix[i][j] = partner.matrix[i][j]

        return child

    def clone(self):
        clone = Matrix(self.rows, self.cols)

        for i in range(self.rows):
            for j in range(self.cols):
                clone.matrix[i][j] = self.matrix[i][j]

        return clone
