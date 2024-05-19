from random import choice, randrange

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTER_SCREEN = (SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)

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
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
SKORE = 0  # Счет игры, увеличивается когда съедается яблоко

pygame.display.set_caption(f"Змейка. Скорость игры: {SPEED}, счет: {SKORE}")

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """
    Класс GameObject инициализирует базовые атрибуты объекта,
    color (цвет). Также предоставляется
    свойство position для получения позиции объекта.
    """

    def __init__(self) -> None:
        self.position = CENTER_SCREEN
        self.body_color = None

    def draw(self, surface) -> None:
        """
        Абстрактный метод, который
        переопределяется в дочерних классах
        """
        pass

    @staticmethod
    def draw_segment(position, body_color):
        """
        Статический метод для отрисовки прямоугольника на заданной поверхности
        с заданными позицией и цветом.
        """
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс Apple, наследуется от класса GameObject"""

    def __init__(self, occupied_positions=CENTER_SCREEN):
        """иницилизация яблока"""
        self.body_color = APPLE_COLOR
        self.position = self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_positions):
        """устанавливает случайное положение яблока"""
        while True:
            self.position = (
                randrange(0, SCREEN_WIDTH, 20),
                randrange(0, SCREEN_HEIGHT, 20)
            )
            if self.position not in occupied_positions:
                return self.position

    def draw(self):
        """Отрисовывает яблоко на игровой поверхности"""
        self.draw_segment(self.position, self.body_color)


class Snake(GameObject):
    """Класс Snake, наследуется от класса GameObject"""

    def __init__(self):
        self.reset()
        self.body_color = SNAKE_COLOR
        self.direction = RIGHT
        self.next_direction = None

    def update_direction(self):
        """Обнавляет движение змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Описывает движения змейки на игровом поле"""
        head_x, head_y = self.get_head_position()
        d_x, d_y = self.direction
        new_position = (
            (head_x + d_x * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + d_y * GRID_SIZE) % SCREEN_HEIGHT
        )

        self.positions.insert(0, new_position)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self):
        """Отрисовывает змейку на игровой поверхности"""
        for position in self.positions:
            self.draw_segment(position, self.body_color)
        self.draw_segment(self.get_head_position(), self.body_color)
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает позицию головы змейки"""
        return self.positions[0]

    def reset(self):
        """Сбрасывае игру"""
        self.position = CENTER_SCREEN
        self.positions = [(self.position)]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.length = 1
        self.last = None


def handle_keys(game_object):
    """Функция обработки действий пользователя"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise SystemExit
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная логика игры"""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple(snake.positions)
    global SKORE
    global SPEED
    while True:
        handle_keys(snake)
        snake.update_direction()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
            SKORE += 1
            SPEED += 1
            pygame.display.set_caption(
                f"Змейка. Скорость игры: {SPEED}, счет: {SKORE}"
            )
        snake.draw()
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.randomize_position(snake.positions)
            SPEED = 10
            SKORE = 0
        snake.move()
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        clock.tick(SPEED)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
