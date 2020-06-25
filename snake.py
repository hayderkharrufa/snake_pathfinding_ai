import pygame
import copy
from settings import *
from random import randrange


class Square:
    def __init__(self, pos, surface, is_apple=False):
        self.pos = pos
        self.surface = surface
        self.is_apple = is_apple
        self.is_tail = False
        self.dir = [-1, 0]      # [x, y] Direction

        if self.is_apple:
            self.dir = [0, 0]

    def draw(self, clr=SNAKE_CLR):
        x, y = self.pos[0], self.pos[1]
        ss, gs = SQUARE_SIZE, GAP_SIZE

        if self.dir == [-1, 0]:
            if self.is_tail:
                pygame.draw.rect(self.surface, clr, (x * ss + gs, y * ss + gs, ss - 2*gs, ss - 2*gs))
            else:
                pygame.draw.rect(self.surface, clr, (x * ss + gs, y * ss + gs, ss, ss - 2*gs))

        if self.dir == [1, 0]:
            if self.is_tail:
                pygame.draw.rect(self.surface, clr, (x * ss + gs, y * ss + gs, ss - 2*gs, ss - 2*gs))
            else:
                pygame.draw.rect(self.surface, clr, (x * ss - gs, y * ss + gs, ss, ss - 2*gs))

        if self.dir == [0, 1]:
            if self.is_tail:
                pygame.draw.rect(self.surface, clr, (x * ss + gs, y * ss + gs, ss - 2*gs, ss - 2*gs))
            else:
                pygame.draw.rect(self.surface, clr, (x * ss + gs, y * ss - gs, ss - 2*gs, ss))

        if self.dir == [0, -1]:
            if self.is_tail:
                pygame.draw.rect(self.surface, clr, (x * ss + gs, y * ss + gs, ss - 2*gs, ss - 2*gs))
            else:
                pygame.draw.rect(self.surface, clr, (x * ss + gs, y * ss + gs, ss - 2*gs, ss))

        if self.is_apple:
            pygame.draw.rect(self.surface, clr, (x * ss + gs, y * ss + gs, ss - 2*gs, ss - 2*gs))

    def move(self, direction):
        self.dir = direction
        self.pos[0] += self.dir[0]
        self.pos[1] += self.dir[1]

    def hitting_wall(self):
        if (self.pos[0] <= -1) or (self.pos[0] >= ROWS) or (self.pos[1] <= -1) or (self.pos[1] >= ROWS):
            return True
        else:
            return False


class Snake:
    def __init__(self, surface):
        self.surface = surface
        self.is_dead = False
        self.squares_start_pos = [[ROWS // 2 + i, ROWS // 2] for i in range(INITIAL_SNAKE_LENGTH)]
        self.turns = {}
        self.dir = [-1, 0]
        self.score = 0
        self.moves_without_eating = 0
        self.apple = Square([randrange(ROWS), randrange(ROWS)], self.surface, is_apple=True)

        self.squares = []
        for pos in self.squares_start_pos:
            self.squares.append(Square(pos, self.surface))

        self.head = self.squares[0]
        self.tail = self.squares[-1]
        self.tail.is_tail = True

        self.path = []
        self.fake_snake = False

    def draw(self):
        self.apple.draw(APPLE_CLR)
        self.head.draw(HEAD_CLR)
        for sqr in self.squares[1:]:
            if self.fake_snake:
                sqr.draw((255, 0, 0))
            else:
                sqr.draw()

    def set_direction(self, direction):
        if direction == 'left':
            if not self.dir == [1, 0]:
                self.dir = [-1, 0]
                self.turns[self.head.pos[0], self.head.pos[1]] = self.dir
        if direction == "right":
            if not self.dir == [-1, 0]:
                self.dir = [1, 0]
                self.turns[self.head.pos[0], self.head.pos[1]] = self.dir
        if direction == "up":
            if not self.dir == [0, 1]:
                self.dir = [0, -1]
                self.turns[self.head.pos[0], self.head.pos[1]] = self.dir
        if direction == "down":
            if not self.dir == [0, -1]:
                self.dir = [0, 1]
                self.turns[self.head.pos[0], self.head.pos[1]] = self.dir

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for _ in keys:
                if keys[pygame.K_LEFT]:
                    self.set_direction('left')

                elif keys[pygame.K_RIGHT]:
                    self.set_direction('right')

                elif keys[pygame.K_UP]:
                    self.set_direction('up')

                elif keys[pygame.K_DOWN]:
                    self.set_direction('down')

    def move(self):
        for j, sqr in enumerate(self.squares):
            p = (sqr.pos[0], sqr.pos[1])
            if p in self.turns:
                turn = self.turns[p]
                sqr.move([turn[0], turn[1]])
                if j == len(self.squares) - 1:
                    self.turns.pop(p)
            else:
                sqr.move(sqr.dir)

    def add_square(self):
        self.squares[-1].is_tail = False
        tail = self.squares[-1]     # Tail before adding new square

        direction = tail.dir
        if direction == [1, 0]:
            self.squares.append(Square([tail.pos[0] - 1, tail.pos[1]], self.surface))
        if direction == [-1, 0]:
            self.squares.append(Square([tail.pos[0] + 1, tail.pos[1]], self.surface))
        if direction == [0, 1]:
            self.squares.append(Square([tail.pos[0], tail.pos[1] - 1], self.surface))
        if direction == [0, -1]:
            self.squares.append(Square([tail.pos[0], tail.pos[1] + 1], self.surface))

        self.squares[-1].dir = direction
        self.squares[-1].is_tail = True     # Tail after adding new square
        self.score += 1

    def reset(self):
        self.__init__(self.surface)

    def hitting_self(self):
        for sqr in self.squares[1:]:
            if sqr.pos == self.head.pos:
                return True

    def generate_apple(self):
        self.apple = Square([randrange(ROWS), randrange(ROWS)], self.surface, is_apple=True)
        if not self.is_position_free(self.apple.pos):
            self.generate_apple()

    def eating_apple(self):
        if self.head.pos == self.apple.pos and not self.fake_snake:
            self.generate_apple()
            self.moves_without_eating = 0
            return True

    def go_to(self, position):  # Set head direction to target position
        if self.head.pos[0] - 1 == position[0]:
            self.set_direction('left')
        if self.head.pos[0] + 1 == position[0]:
            self.set_direction('right')
        if self.head.pos[1] - 1 == position[1]:
            self.set_direction('up')
        if self.head.pos[1] + 1 == position[1]:
            self.set_direction('down')
        if self.head.pos == position:
            print('EQUALS')
            self.set_direction('stop')

    def is_position_free(self, position):
        if position[0] >= ROWS or position[0] < 0 or position[1] >= ROWS or position[1] < 0:
            return False
        for sqr in self.squares:
            if sqr.pos == position:
                return False
        return True

    # Breadth First Search Algorithm
    def bfs(self, s, e):    # Find shortest path between (start_position, end_position)
        q = []  # Queue
        visited = {tuple(pos): False for pos in grid}

        q.append(s)
        visited[s] = True
        prev = {tuple(pos): None for pos in grid}   # The is used to find the parent node of each node to create a path

        while q:    # While the queue is not empty
            node = q.pop(0)
            neighbors = adjacency_dict[node]
            for next_node in neighbors:
                if self.is_position_free(next_node) and not visited[tuple(next_node)]:
                    q.append(tuple(next_node))
                    visited[tuple(next_node)] = True
                    prev[tuple(next_node)] = node

        path = list()
        p_node = e  # Starting from end, we will find the parent node of each node

        start_node_found = False
        while not start_node_found:
            if prev[p_node] is None:
                return []
            p_node = prev[p_node]
            if p_node == s:
                path.append(e)
                return path
            path.insert(0, p_node)

        return []   # Path not available

    def create_virtual_snake(self):
        v_snake = Snake(self.surface)
        for i in range(len(self.squares) - len(v_snake.squares)):
            v_snake.add_square()

        for i, sqr in enumerate(v_snake.squares):
            sqr.pos = copy.deepcopy(self.squares[i].pos)
            sqr.dir = copy.deepcopy(self.squares[i].dir)

        v_snake.dir = copy.deepcopy(self.dir)
        v_snake.turns = copy.deepcopy(self.turns)
        v_snake.apple.pos = copy.deepcopy(self.apple.pos)
        v_snake.apple.is_apple = True
        v_snake.fake_snake = True

        return v_snake

    def get_path_to_tail(self):
        path_end_point = copy.deepcopy(self.squares[-1].pos)
        self.squares.pop(-1)
        path = self.bfs(tuple(self.head.pos), tuple(path_end_point))
        self.add_square()
        return path

    def get_valid_head_neighbors(self):
        valid_neighbors = []
        neighbors = get_neighbors(tuple(self.head.pos))
        for n in neighbors:
            if self.is_position_free(n):
                valid_neighbors.append(n)
        return valid_neighbors

    def set_path(self):
        v_snake = self.create_virtual_snake()

        # Let the virtual snake check if path to apple is available
        path_1 = self.bfs(tuple(self.head.pos), tuple(self.apple.pos))
        path_2 = []

        if path_1:
            for pos in path_1:
                v_snake.go_to(pos)
                v_snake.move()

            v_snake.add_square()    # Because it will eat an apple
            path_2 = v_snake.get_path_to_tail()

        # v_snake.draw()

        if path_2:
            return path_1

        if (not path_1) or (not path_2):
            print('follow tail')
            return self.get_path_to_tail()

        print('wander')
        path = []
        neighbors = get_neighbors(self.head.pos)
        for n in neighbors:
            if self.is_position_free(n):
                path.append(n)

    def update(self):
        self.handle_events()

        self.path = self.set_path()
        if self.path:
            self.go_to(self.path[0])

        self.draw()
        self.move()

        if self.hitting_self() or self.head.hitting_wall():
            self.is_dead = True

        if self.eating_apple():
            self.add_square()
