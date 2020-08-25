import pygame
from settings import *
from random import choice

cols, rows = WIDTH // TILE, HEIGHT // TILE

pygame.init()
sc = pygame.display.set_mode(RES)
clock = pygame.time.Clock()


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = {
            'TOP': True,
            'BOTTOM': True,
            'RIGHT': True,
            'LEFT': True,
        }
        self.visited = False

    def draw(self):
        x, y = self.x * TILE, self.y * TILE
        if self.visited:
            pygame.draw.rect(sc, visited_cell_color, (x, y, TILE, TILE))

        if self.walls['TOP']:
            pygame.draw.line(sc, cell_line_color, (x, y), (x + TILE, y), 3)
        if self.walls['BOTTOM']:
            pygame.draw.line(sc, cell_line_color, (x, y + TILE), (x + TILE, y + TILE), 3)
        if self.walls['LEFT']:
            pygame.draw.line(sc, cell_line_color, (x, y), (x, y + TILE), 3)
        if self.walls['RIGHT']:
            pygame.draw.line(sc, cell_line_color, (x + TILE, y), (x + TILE, y + TILE), 3)

    def draw_current_cell(self):
        x, y = self.x * TILE, self.y * TILE
        pygame.draw.rect(sc, current_cell_color, (x, y, TILE, TILE))

    @staticmethod
    def check_cell(x, y):
        """по индексам клетки в двумерном массиве находим ее координаты в одномерном массиве
            i + j *cols"""
        find_index = lambda x, y: x + y * cols
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False
        return grid_cells[find_index(x, y)]

    def get_random_neighbors(self):
        neighbors = []
        top = self.check_cell(self.x, self.y - 1)
        right = self.check_cell(self.x + 1, self.y)
        left = self.check_cell(self.x - 1, self.y)
        bottom = self.check_cell(self.x, self.y + 1)
        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if left and not left.visited:
            neighbors.append(left)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        return choice(neighbors) if neighbors else False


def restart(grid_cell):
    """помечаем все клетки как не посещеные
       таким образом лабиринт перезапускается
     """
    global current_cell
    for cell in grid_cells:
        cell.visited = False
        cell.walls['TOP'] = True
        cell.walls['BOTTOM'] = True
        cell.walls['RIGHT'] = True
        cell.walls['LEFT'] = True
    current_cell = grid_cells[0]


def remove_walls(current, next):
    dx = current.x - next.x
    if dx == 1:
        current.walls['LEFT'] = False
        next.walls['RIGHT'] = False
    elif dx == -1:
        current.walls['RIGHT'] = False
        next.walls['LEFT'] = False

    dy = current.y - next.y
    if dy == 1:
        current.walls['TOP'] = False
        next.walls['BOTTOM'] = False
    elif dy == -1:
        current.walls['BOTTOM'] = False
        next.walls['TOP'] = False


grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]
current_cell = grid_cells[0]
stack = []

colors, color = [], 40

while True:
    sc.fill(background_color)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart(grid_cells)

    [cell.draw() for cell in grid_cells]

    current_cell.visited = True
    current_cell.draw_current_cell()

    [pygame.draw.rect(sc, colors[i], (cell.x * TILE + 5, cell.y * TILE + 5, TILE - 10, TILE - 10)) for
     i, cell in enumerate(stack)]

    next_cell = current_cell.get_random_neighbors()
    if next_cell:
        next_cell.visited = True
        stack.append((current_cell))
        colors.append((min(color, 255), 10, 100))
        remove_walls(current_cell, next_cell)
        color += 10
        current_cell = next_cell
    elif stack:
        current_cell = stack.pop()
    pygame.display.flip()
    clock.tick(FPS)
