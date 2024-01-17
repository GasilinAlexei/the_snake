from random import randint

import pygame as pg

from typing import Optional, Tuple, List

# Инициализация pg:
pg.init()

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
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, body_color: Optional[Tuple[int, int, int]] = None):
        self.body_color: Optional[Tuple[int, int, int]] = body_color
        self.position: Tuple[int, int] = (
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2
        )

    def draw(self, surface):
        """Метотд отрисовки объекта. Которое переопределяется в подклассах."""
        pass


class Apple(GameObject):
    """Класс для представления яблока."""

    def __init__(self, snake, body_color: Tuple[int, int, int] = APPLE_COLOR):
        """Инициализация яблока."""
        super().__init__()
        self.snake = snake
        self.body_color: Tuple[int, int, int] = body_color
        self.randomize_position()

    def randomize_position(self):
        """Генерация случайной позиции для яблока в рамках игрового поля."""
        snake_positions: List[Tuple[int, int]] = [(x, y) for x, y in self.snake.positions]
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if self.position not in snake_positions:
                break

    def draw(self, surface: pg.Surface) -> None:
        """Метод draw класса Apple."""
        rect: pg.Rect = pg.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pg.draw.rect(surface, self.body_color, rect)
        pg.draw.rect(surface, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс для представления змейки."""

    def __init__(self):
        super().__init__()
        self.length: int = 1
        self.positions: List[Tuple[int, int]] = [(SCREEN_WIDTH // 2,
                                                  SCREEN_HEIGHT // 2)]
        self.direction: Tuple[int, int] = RIGHT
        self.next_direction: Optional[Tuple[int, int]] = None
        self.body_color: Tuple[int, int, int] = SNAKE_COLOR
        self.last: Optional[Tuple[int, int]] = None

    def update_direction(self):
        """Обновление направление движения."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Получение текущей головной позиции."""
        head_position: Tuple[int, int] = self.get_head_position()

        """Вычисления позиции новой головы."""
        dx, dy = self.direction
        new_head_x: int = (head_position[0] + dx * GRID_SIZE) % SCREEN_WIDTH
        new_head_y: int = (head_position[1] + dy * GRID_SIZE) % SCREEN_HEIGHT
        new_head_position: Tuple[int, int] = (new_head_x, new_head_y)

        """Проверка на столкновение с собой."""
        if new_head_position in self.positions[1:]:
            self.reset()

        """Обновление списка позиций."""
        self.positions.insert(0, new_head_position)
        if len(self.positions) > self.length + 1:
            self.positions.pop()

    def draw(self, surface: pg.Surface) -> None:
        """Метод draw класса Snake."""
        for position in self.positions[:-1]:
            rect = (
                pg.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pg.draw.rect(surface, self.body_color, rect)
            pg.draw.rect(surface, BORDER_COLOR, rect, 1)

        """Отрисовка головы змейки"""
        head_rect: pg.Rect = pg.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(surface, self.body_color, head_rect)
        pg.draw.rect(surface, BORDER_COLOR, head_rect, 1)

        """Затирание последнего сегмента"""
        if self.last:
            last_rect = pg.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pg.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """Сброс змейки в начальное состояние"""
        self.length: int = 1
        self.positions: List[Tuple[int, int]] = [(SCREEN_WIDTH // 2,
                                                  SCREEN_HEIGHT // 2)]
        self.direction: Tuple[int, int] = RIGHT
        self.next_direction: Optional[Tuple[int, int]] = None
        self.last: Optional[Tuple[int, int]] = None

    def get_head_position(self):
        """Возвращает позицию головы змейки"""
        return self.positions[0]


def handle_keys(game_object):
    """Управление стрелками"""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Экземпляры классов."""
    snake = Snake()
    apple = Apple(snake)
    running = True

    while running:
        clock.tick(SPEED)
        handle_keys(snake)

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

        pg.display.update()

    pg.quit()


if __name__ == '__main__':
    main()
