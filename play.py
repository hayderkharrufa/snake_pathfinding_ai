from snake import *
from os import environ


def draw_screen(surface):
    surface.fill(SCREEN_CLR)


def draw_grid(surface):
    x = 0
    y = 0
    for r in range(ROWS):
        x = x + SQUARE_SIZE
        y = y + SQUARE_SIZE
        pygame.draw.line(surface, GRID_CLR, (x, 0), (x, HEIGHT))
        pygame.draw.line(surface, GRID_CLR, (0, y), (WIDTH, y))


def play():
    pygame.init()
    environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.display.set_caption("Snake Game")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    snake = Snake(screen)

    mainloop = True
    while mainloop:
        draw_screen(screen)
        draw_grid(screen)

        snake.update()

        if snake.is_dead:
            snake.reset()

        clock.tick(FPS)
        pygame.display.update()


if __name__ == '__main__':
    play()
