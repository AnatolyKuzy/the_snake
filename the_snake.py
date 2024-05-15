from random import choice, randrange

import pygame

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
pygame.display.set_caption("Змейка")

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """
    Класс GameObject инициализирует базовые атрибуты объекта,
    color (цвет). Также предоставляется
    свойство position для получения позиции объекта.
    """

    def __init__(self) -> None:
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self, surface) -> None:
        """
        Абстрактный метод, который
        переопределяется в дочерних классах
        """
        pass


class Apple(GameObject):
    """Класс Apple, наследуется от класса GameObject"""

    def __init__(self):
        """иницилизация яблока"""
        self.body_color = APPLE_COLOR
        self.position = self.randomize_position()

    def randomize_position(self):
        """устанавливает случайное положение яблока"""
        posit_x = randrange(0, SCREEN_WIDTH, 20)
        posit_y = randrange(0, SCREEN_HEIGHT, 20)
        self.position = posit_x, posit_y
        return (posit_x, posit_y)

    def draw(self):
        """Отрисовывает яблоко на игровой поверхности"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс Snake, наследуется от класса GameObject"""

    def __init__(self):
        self.position = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        self.positions = [(self.position)]
        self.body_color = SNAKE_COLOR
        self.direction = RIGHT
        self.speed = SPEED
        self.length = 1
        self.last = None
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
        new_head_x = (head_x + d_x * GRID_SIZE) % SCREEN_WIDTH
        new_head_y = (head_y + d_y * GRID_SIZE) % SCREEN_HEIGHT
        new_position = (new_head_x, new_head_y)

        if self.check_collision():
            self.reset()
            return

        self.positions.insert(0, new_position)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self):
        """Отрисовывает змейку на игровой поверхности"""
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает позицию головы змейки"""
        return self.positions[0]

    def reset(self):
        """Сбрасывае игру"""
        self.positions = [(self.position)]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.speed = SPEED
        self.length = GRID_SIZE
        self.last = None

    def check_collision(self):
        """
        Проверяет, не столкнулась ли змейка со своим телом.
        Возвращает True, если столкновение произошло, иначе False.
        """
        head_x, head_y = self.positions[0]
        if len(self.positions) == 1:
            return False
        for h_x, h_y in self.positions[2:]:
            if head_x == h_x and head_y == h_y:
                return True
        return False


def handle_keys(game_object):
    """Функция обработки действий пользователя"""
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
    """Основная логика игры"""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()
    while True:
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
        if snake.check_collision():
            snake.reset()
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        clock.tick(snake.speed)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
