# Dimensions
WIDTH = 600
HEIGHT = 600
ROWS = 30
SQUARE_SIZE = WIDTH // ROWS
GAP_SIZE = 1    # Gap between adjacent squares

# Colors
SCREEN_CLR = (15, 15, 15)
GRID_CLR = (20, 20, 20)
SNAKE_CLR = (50, 255, 50)
APPLE_CLR = (255, 255, 0)
HEAD_CLR = (0, 150, 0)

# Game Settings
FPS = 60
INITIAL_SNAKE_LENGTH = 4

# Variables used is BFS algorithm
n_nodes = ROWS * ROWS
grid = [[i, j] for i in range(ROWS) for j in range(ROWS)]


def get_neighbors(position):
    neighbors = [[position[0] + 1, position[1]],
                 [position[0] - 1, position[1]],
                 [position[0], position[1] + 1],
                 [position[0], position[1] - 1]]
    in_grid_neighbors = []
    for pos in neighbors:
        if pos in grid:
            in_grid_neighbors.append(pos)
    return in_grid_neighbors


#   Note here that each position is a tuple because python doesn't allow hashing lists
adjacency_dict = {tuple(pos): get_neighbors(pos) for pos in grid}
