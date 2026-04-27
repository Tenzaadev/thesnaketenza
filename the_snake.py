from random import choice, randint

import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class Game:
    """Класс Game управляет игровым процессом."""

    def __init__(self):
        self.snake = Snake()
        self.apple = Apple(self.snake)
        self.score = 0
        self.game_over = False

    def process_events(self):
        """Обрабатывает события клавиатуры."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.snake.change_direction(UP)
                elif event.key == pygame.K_DOWN:
                    self.snake.change_direction(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.snake.change_direction(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.snake.change_direction(RIGHT)
                elif event.key == pygame.K_ESCAPE:
                    return False
        return True

    def update(self):
        """Обновляет состояние игры."""
        if self.game_over:
            return

        self.snake.move()

        if self.snake.check_collision():
            self.game_over = True

        if self.snake.get_head_position() == self.apple.position:
            self.snake.length += 1
            self.score += 1
            self.apple.randomize_position(self.snake)

    def draw(self):
        """Отрисовывает игровое поле."""
        screen.fill(BOARD_BACKGROUND_COLOR)

        self.apple.draw()
        self.snake.draw()

        self.draw_score()

        pygame.display.flip()

    def draw_score(self):
        """Отрисовывает счет."""
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Счет: {self.score}", True, BORDER_COLOR)
        screen.blit(score_text, (10, 10))

    def reset(self):
        """Сбрасывает игру."""
        self.snake = Snake()
        self.apple = Apple(self.snake)
        self.score = 0
        self.game_over = False


class Snake:
    """Кlasse Snake управляет змейкой."""

    def __init__(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.length = 1
        self.score = 0

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def change_direction(self, new_direction):
        """Изменяет направление движения змейки."""
        if (new_direction[0] + self.direction[0] != 0 or
                new_direction[1] + self.direction[1] != 0):
            self.direction = new_direction

    def move(self):
        """Перемещает змейку на одну клетку."""
        head_x, head_y = self.positions[0]
        dir_x, dir_y = self.direction
        new_head = ((head_x + dir_x) % GRID_WIDTH,
                    (head_y + dir_y) % GRID_HEIGHT)

        self.positions.insert(0, new_head)

        if self.length < len(self.positions):
            self.positions.pop()

    def check_collision(self):
        """Проверяет столкновение змейки с самой собой."""
        head = self.positions[0]
        return head in self.positions[1:]

    def draw(self):
        """Отрисовывает змейку."""
        for position in self.positions:
            rect = (position[0] * GRID_SIZE,
                    position[1] * GRID_SIZE,
                    GRID_SIZE,
                    GRID_SIZE)
            pygame.draw.rect(screen, SNAKE_COLOR, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple:
    """Класс Apple управляет яблоком."""

    def __init__(self, snake):
        self.position = (0, 0)
        self.snake = snake
        self.randomize_position(snake)

    def randomize_position(self, snake):
        """Генерирует случайную позицию для яблока."""
        while True:
            self.position = (randint(0, GRID_WIDTH - 1),
                             randint(0, GRID_HEIGHT - 1))
            if self.position not in snake.positions:
                break

    def draw(self):
        """Отрисовывает яблоко."""
        rect = (self.position[0] * GRID_SIZE,
                self.position[1] * GRID_SIZE,
                GRID_SIZE,
                GRID_SIZE)
        pygame.draw.rect(screen, APPLE_COLOR, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


def main():
    """Главная функция игры."""
    game = Game()

    running = True
    while running:
        running = game.process_events()
        game.update()
        game.draw()
        clock.tick(SPEED)

    pygame.quit()


if __name__ == "__main__":
    main()