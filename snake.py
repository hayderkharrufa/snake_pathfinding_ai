import pygame
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
        sz, gz = SQUARE_SIZE, GAP_SIZE

        if self.dir == [-1, 0]:
            if self.is_tail:
                pygame.draw.rect(self.surface, clr, (x * sz + gz, y * sz + gz, sz - 2*gz, sz - 2*gz))
            else:
                pygame.draw.rect(self.surface, clr, (x * sz + gz, y * sz + gz, sz, sz - 2*gz))

        if self.dir == [1, 0]:
            if self.is_tail:
                pygame.draw.rect(self.surface, clr, (x * sz + gz, y * sz + gz, sz - 2*gz, sz - 2*gz))
            else:
                pygame.draw.rect(self.surface, clr, (x * sz - gz, y * sz + gz, sz, sz - 2*gz))

        if self.dir == [0, 1]:
            if self.is_tail:
                pygame.draw.rect(self.surface, clr, (x * sz + gz, y * sz + gz, sz - 2*gz, sz - 2*gz))
            else:
                pygame.draw.rect(self.surface, clr, (x * sz + gz, y * sz - gz, sz - 2*gz, sz))

        if self.dir == [0, -1]:
            if self.is_tail:
                pygame.draw.rect(self.surface, clr, (x * sz + gz, y * sz + gz, sz - 2*gz, sz - 2*gz))
            else:
                pygame.draw.rect(self.surface, clr, (x * sz + gz, y * sz + gz, sz - 2*gz, sz))

        if self.is_apple:
            pygame.draw.rect(self.surface, clr, (x * sz + gz, y * sz + gz, sz - 2*gz, sz - 2*gz))

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

    def draw(self):
        self.apple.draw(APPLE_CLR)
        self.head.draw(HEAD_CLR)
        for sqr in self.squares[1:]:
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
        self.moves_without_eating += 1

    def add_square(self):
        self.squares[-1].is_tail = False
        tail = self.squares[-1]     # Tail Before Adding New Square

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
        self.squares[-1].is_tail = True     # Tail After Adding New Square
        self.score += 1

    def reset(self):
        self.__init__(self.surface)

    def hitting_self(self):
        for sqr in self.squares[1:]:
            if sqr.pos == self.head.pos:
                return True

    def apple_pos_blocked(self):
        for sqr in self.squares:
            if self.apple.pos == sqr.pos:
                return True

    def generate_apple(self):
        self.apple = Square([randrange(ROWS), randrange(ROWS)], self.surface, is_apple=True)
        if self.apple_pos_blocked():
            self.generate_apple()

    def eat_apple(self):
        if self.head.pos == self.apple.pos:
            self.generate_apple()
            self.moves_without_eating = 0
            return True

    def is_right_blocked(self):
        if self.head.dir == [1, 0]:
            x = self.head.pos[0] + 0
            y = self.head.pos[1] + 1
            for sqr in self.squares:
                if sqr.pos == [x, y] or y >= ROWS:
                    return 1
            return 0

        if self.head.dir == [-1, 0]:
            x = self.head.pos[0] + 0
            y = self.head.pos[1] - 1
            for sqr in self.squares:
                if sqr.pos == [x, y] or y <= -1:
                    return 1
            return 0

        if self.head.dir == [0, 1]:
            x = self.head.pos[0] - 1
            y = self.head.pos[1] + 0
            for sqr in self.squares:
                if sqr.pos == [x, y] or x <= -1:
                    return 1
            return 0

        if self.head.dir == [0, -1]:
            x = self.head.pos[0] + 1
            y = self.head.pos[1] + 0
            for sqr in self.squares:
                if sqr.pos == [x, y] or x >= ROWS:
                    return 1
            return 0

    def is_left_blocked(self):
        if self.head.dir == [1, 0]:
            x = self.head.pos[0] + 0
            y = self.head.pos[1] - 1
            for sqr in self.squares:
                if sqr.pos == [x, y] or y <= -1:
                    return 1
            return 0

        if self.head.dir == [-1, 0]:
            x = self.head.pos[0] + 0
            y = self.head.pos[1] + 1
            for sqr in self.squares:
                if sqr.pos == [x, y] or y >= ROWS:
                    return 1
            return 0

        if self.head.dir == [0, 1]:
            x = self.head.pos[0] + 1
            y = self.head.pos[1] + 0
            for sqr in self.squares:
                if sqr.pos == [x, y] or x >= ROWS:
                    return 1
            return 0

        if self.head.dir == [0, -1]:
            x = self.head.pos[0] - 1
            y = self.head.pos[1] + 0
            for sqr in self.squares:
                if sqr.pos == [x, y] or x <= -1:
                    return 1
            return 0

    def is_front_blocked(self):
        if self.head.dir == [1, 0]:
            x = self.head.pos[0] + 1
            y = self.head.pos[1] + 0
            for sqr in self.squares:
                if sqr.pos == [x, y] or x >= ROWS:
                    return 1
            return 0

        if self.head.dir == [-1, 0]:
            x = self.head.pos[0] - 1
            y = self.head.pos[1] + 0
            for sqr in self.squares:
                if sqr.pos == [x, y] or x <= -1:
                    return 1
            return 0

        if self.head.dir == [0, 1]:
            x = self.head.pos[0] + 0
            y = self.head.pos[1] + 1
            for sqr in self.squares:
                if sqr.pos == [x, y] or y >= ROWS:
                    return 1
            return 0

        if self.head.dir == [0, -1]:
            x = self.head.pos[0] + 0
            y = self.head.pos[1] - 1
            for sqr in self.squares:
                if sqr.pos == [x, y] or y <= -1:
                    return 1
            return 0

    def go_left(self):
        if self.head.dir == [1, 0]:
            self.dir = [0, -1]
            self.turns[self.head.pos[0], self.head.pos[1]] = self.dir
        elif self.head.dir == [-1, 0]:
            self.dir = [0, 1]
            self.turns[self.head.pos[0], self.head.pos[1]] = self.dir
        elif self.head.dir == [0, 1]:
            self.dir = [1, 0]
            self.turns[self.head.pos[0], self.head.pos[1]] = self.dir
        elif self.head.dir == [0, -1]:
            self.dir = [-1, 0]
            self.turns[self.head.pos[0], self.head.pos[1]] = self.dir

    def go_right(self):
        if self.head.dir == [1, 0]:
            self.dir = [0, 1]
            self.turns[self.head.pos[0], self.head.pos[1]] = self.dir
        elif self.head.dir == [-1, 0]:
            self.dir = [0, -1]
            self.turns[self.head.pos[0], self.head.pos[1]] = self.dir
        elif self.head.dir == [0, 1]:
            self.dir = [-1, 0]
            self.turns[self.head.pos[0], self.head.pos[1]] = self.dir
        elif self.head.dir == [0, -1]:
            self.dir = [1, 0]
            self.turns[self.head.pos[0], self.head.pos[1]] = self.dir

    def go_to(self, position):
        if self.head.pos[0] > position[0]:
            self.set_direction('left')
        if self.head.pos[0] < position[0]:
            self.set_direction('right')
        if self.head.pos[1] > position[1]:
            self.set_direction('up')
        if self.head.pos[1] < position[1]:
            self.set_direction('down')

    def is_position_free(self, position):
        for sqr in self.squares:
            if sqr.pos == position:
                return False
        return True

    def update(self):
        self.handle_events()

        # self.go_to(self.apple.pos)
        print(self.is_position_free([1, 1]))
        self.draw()
        self.move()

        if self.hitting_self() or self.head.hitting_wall():
            self.is_dead = True

        if self.eat_apple():
            self.add_square()
