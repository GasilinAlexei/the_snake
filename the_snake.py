from random import randint

import pygame

# Инициализация PyGame:
pygame.init()

# Цвет
APPLE_COLLOR = (255, 0, 0)
SNAKE_COLLOR = (0, 255, 0)

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


# Тут опишите все классы игры.

class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, body_color=None):
        self.body_color = body_color
        self.position = (
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2
        )

    def draw(self, surface):
        """Метотд отрисовки объекта. Которое переопределяется в подклассах."""
        pass


class Apple(GameObject):
    """Класс для представления яблока."""

    def __init__(self, body_color=APPLE_COLOR):
        """Инициализация яблока."""
        super().__init__()
        self.body_color = body_color
        self.randomize_position()

    def randomize_position(self):
        """Генерация случайной позиции для яблока в рамках игрового поля."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self, surface):
        """Метод draw класса Apple."""
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс для представления змейки."""

    def __init__(self):
        super().__init__()
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2,
                           SCREEN_HEIGHT // 2)]  # Позиция в центре экрана
        self.direction = RIGHT  # Змейка изначально движется вправо
        self.next_direction = None  # Следующее движения, по умолчанию None
        self.body_color = SNAKE_COLOR  # Цвет змейки (зеленый по умолчанию)
        self.last = None
    #   self.game_over = False

    def update_direction(self):
        """Обновление направление движения."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Получение текущей головной позиции."""
        head_position = self.get_head_position()

        """Вычисления позиции новой головы."""
        dx, dy = self.direction
        new_head_x = (head_position[0] + dx * GRID_SIZE) % SCREEN_WIDTH
        new_head_y = (head_position[1] + dy * GRID_SIZE) % SCREEN_HEIGHT
        new_head_position = (new_head_x, new_head_y)

        """Проверка на столкновение с собой."""
        if new_head_position in self.positions[1:]:
            self.reset()

        """Обновление списка позиций."""
        self.positions.insert(0, new_head_position)
        if len(self.positions) > self.length + 1:
            self.positions.pop()

    def draw(self, surface):
        """Метод draw класса Snake."""
        for position in self.positions[:-1]:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

        """Отрисовка головы змейки"""
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

        """Затирание последнего сегмента"""
        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """Сброс змейки в начальное состояние"""
        self.length = 1  # Начальная длина змейка
        self.positions = [(SCREEN_WIDTH // 2,
                           SCREEN_HEIGHT // 2)]  # Позиция в центре экрана
        self.direction = RIGHT  # Движение змейки по умолчанию
        self.next_direction = None  # Следующее движения, по умолчанию None
        self.last = None

    def get_head_position(self):
        """Возвращает позицию головы змейки"""
        return self.positions[0]


def handle_keys(game_object):
    """Управление стрелками"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Экземпляры классов."""
    apple = Apple()
    snake = Snake()
    running = True

    while running:
        clock.tick(SPEED)
        handle_keys(snake)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Обновление направления движения змейки
        snake.update_direction()

        # Движение змейки
        snake.move()

        # Проверка съедания яблока
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        # Проверка столкновения с собой
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        # Отрисовка змейки и яблока
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)

        # Обновление экрана

        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
