import pygame
import numpy as np
import random

# Constants
WIDTH, HEIGHT = 800, 500
CELL_SIZE = 2
GRID_WIDTH, GRID_HEIGHT = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE
FPS = 10000

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Cell types
EMPTY = 0
PREY = 1
PREDATOR = 2

# Rules
PREY_BREED_TIME = 8
PREDATOR_BREED_TIME = 9
PREDATOR_STARVE_TIME = 12


class Cell:
    def __init__(self, cell_type):
        self.cell_type = cell_type
        self.breed_time = 0
        self.starve_time = 0


def initialize_grid():
    count_of_preys = 0
    count_of_predators = 0
    grid = np.zeros((GRID_WIDTH, GRID_HEIGHT), dtype=Cell)
    for i in range(GRID_WIDTH):
        for j in range(GRID_HEIGHT):
            cell_type = random.choice([PREDATOR, PREY, EMPTY])
            if cell_type == PREY:
                count_of_preys += 1
            elif cell_type == PREDATOR:
                count_of_predators += 1
            if count_of_predators < 2300 and count_of_preys < 3000:
                cell_type = random.choice([PREDATOR, PREY, EMPTY])
            elif count_of_predators > 2300 and count_of_preys < 3000:
                cell_type = random.choice([PREY, EMPTY])
            elif count_of_predators < 2300 and count_of_preys > 3000:
                cell_type = EMPTY
            else:
                cell_type = EMPTY
            grid[i, j] = Cell(cell_type)
    return grid


def update_grid(grid):
    new_grid = np.zeros((GRID_WIDTH, GRID_HEIGHT), dtype=Cell)

    for i in range(GRID_WIDTH):
        for j in range(GRID_HEIGHT):
            current_cell = grid[i, j]

            if current_cell.cell_type == PREY:
                new_grid[i, j] = update_prey(current_cell, i, j, grid)
            elif current_cell.cell_type == PREDATOR:
                new_grid[i, j] = update_predator(current_cell, i, j, grid)
            else:
                new_grid[i, j] = update_empty(current_cell, i, j, grid)

    return new_grid


def update_prey(cell, x, y, grid):
    # Prey moves randomly
    new_x, new_y = get_random_neighbor(x, y)
    if grid[new_x, new_y].cell_type == EMPTY:
        grid[new_x, new_y].cell_type = PREY
        grid[x, y].cell_type = EMPTY

    # Prey breeds
    cell.breed_time += 1
    if cell.breed_time >= PREY_BREED_TIME:
        new_x, new_y = get_random_neighbor(x, y)
        grid[new_x, new_y].cell_type = PREY
        cell.breed_time = 0

    return cell


def update_predator(cell, x, y, grid):
    # Predator eats
    new_x, new_y = get_random_neighbor(x, y)
    if grid[new_x, new_y].cell_type == PREY:
        grid[new_x, new_y].cell_type = EMPTY
        cell.starve_time = 0
    # Predator breeds
    cell.breed_time += 1
    if cell.breed_time >= PREDATOR_BREED_TIME:
        new_x, new_y = get_random_neighbor(x, y)
        grid[new_x, new_y].cell_type = PREDATOR
        cell.breed_time = 0

    new_x, new_y = get_random_neighbor(x, y)
    # Predator moves to an empty cell
    if grid[new_x, new_y].cell_type == EMPTY:
        grid[new_x, new_y].cell_type = PREDATOR
        grid[x, y].cell_type = EMPTY

    # Predator starves
    cell.starve_time += 1
    if cell.starve_time >= PREDATOR_STARVE_TIME:
        grid[x, y].cell_type = EMPTY

    return cell


def update_empty(cell, x, y, grid):
    # Empty cell does nothing
    return cell


def get_random_neighbor(x, y):
    new_x = (x + random.choice([-1, 1])) % GRID_WIDTH
    new_y = (y + random.choice([-1, 1])) % GRID_HEIGHT
    return new_x, new_y


def draw_grid(screen, grid):
    screen.fill(WHITE)

    for i in range(GRID_WIDTH):
        for j in range(GRID_HEIGHT):
            cell = grid[i, j]
            color = BLACK

            if cell.cell_type == PREY:
                color = GREEN
            elif cell.cell_type == PREDATOR:
                color = RED

            pygame.draw.rect(screen, color, (i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    pygame.display.flip()


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Predator-Prey CA Model")

    clock = pygame.time.Clock()

    grid = initialize_grid()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        grid = update_grid(grid)
        draw_grid(screen, grid)

        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
