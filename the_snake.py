import sys
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

    def draw(self, screen):
        """Метотд отрисовки объекта. Которое переопределяется в подклассах"""
        def draw(self, surface):
            pass


class Apple(GameObject):
    """Класс для представления яблока."""

    def __init__(self, body_color=APPLE_COLOR):
        """Инициализация яблока"""

        self.body_color = body_color
        self.randomize_position()

    def randomize_position(self):
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self, surface):
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    
    def __init__(self):
            super().__init__()
            self.length = 1
            self.positions = GRID_SIZE  # Начальная позиция - центр экрана
            self.direction = RIGHT  # Змейка изначально движется вправо
            self.next_direction = None  # Следующее направление движения, по умолчанию None
            self.body_color = SNAKE_COLOR  # Цвет змейки (зеленый по умолчанию)

    def update_direction(self, new_direction):
        # Обновление направления движения змейки
        self.next_direction = new_direction

    def move(self, surface):
        # Получение текущей головной позиции
        head_position = self.get_head_position()
        """Вычисления позиции новой головы"""
        dx, dy = 0, 0

        # Обновление позиции змейки
        self.direction = None
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)
        head_x, head_y = self.positions[0]

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)


    def handle_keys(cls, GameObject):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and GameObject.direction != DOWN:
                    GameObject.next_direction = UP
                elif event.key == pygame.K_DOWN and GameObject.direction != UP:
                    GameObject.next_direction = DOWN
                elif event.key == pygame.K_LEFT and GameObject.direction != RIGHT:
                    GameObject.next_direction = LEFT
                elif event.key == pygame.K_RIGHT and GameObject.direction != LEFT:
                    GameObject.next_direction = RIGHT


        def update_direction(self):
            if self.next_direction:
                self.direction = self.next_direction
                self.next_direction = None


    def draw(self, surface):
        for position in self.positions[:-1]:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


    def get_head_position(self):
        # Возвращает позицию головы змейки
        return self.positions[0]

    def reset(self):
        # Сброс змейки в начальное состояние
        self.length = 1
        self.positions = GRID_SIZE
        self.direction = RIGHT
        self.next_direction = None

def main():
    # Тут нужно создать экземпляры классов.
    game = GameObject()
    snake = Snake()
    apple = Apple()



    while True:
        clock.tick(SPEED)

        # Тут опишите основную логику игры.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            screen.fill(BOARD_BACKGROUND_COLOR)
            pygame.display.flip()


if __name__ == '__main__':
    main()


# # Метод draw класса Snake
# def draw(self, surface):
#     for position in self.positions[:-1]:
#         rect = (
#             pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
#         )
#         pygame.draw.rect(surface, self.body_color, rect)
#         pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

#     # Отрисовка головы змейки
#     head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(surface, self.body_color, head_rect)
#     pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

#     # Затирание последнего сегмента
#     if self.last:
#         last_rect = pygame.Rect(
#             (self.last[0], self.last[1]),
#             (GRID_SIZE, GRID_SIZE)
#         )
#         pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

# # Функция обработки действий пользователя.
# def handle_keys(game_object):
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             raise SystemExit
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_UP and game_object.direction != DOWN:
#                 game_object.next_direction = UP
#             elif event.key == pygame.K_DOWN and game_object.direction != UP:
#                 game_object.next_direction = DOWN
#             elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
#                 game_object.next_direction = LEFT
#             elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
#                 game_object.next_direction = RIGHT


# # Метод обновления направления после нажатия на кнопку.
# def update_direction(self):
#     if self.next_direction:
#         self.direction = self.next_direction
#         self.next_direction = None
