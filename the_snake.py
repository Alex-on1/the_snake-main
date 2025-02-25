from random import choice, randint

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
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self):
        # Позиция объекта по центру
        self.position = (SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)
        # Цвет тела объекта, будет определен в дочерних классах
        self.body_color = None

    def draw(self):
        """
        Метод отрисовки объекта,
        должен быть переопределен в дочерних классах.
        """
        pass


class Apple(GameObject):
    """Класс для яблок, которые змейка может съесть."""

    def __init__(self, snake_positions=(0, 0)):
        super().__init__()
        self.snake_positions = snake_positions
        self.body_color = APPLE_COLOR  # Устанавливаем цвет яблока
        self.randomize_position(snake_positions)  # Генерируем позицию яблока

    def randomize_position(self, snake_positions):
        """
        Случайно устанавливает позицию яблока,
        чтобы оно не пересекалось со змеёй.
        """
        while True:
            self.position = [
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
            ]
            # Проверка, что яблоко не накладывается на змею
            if self.position not in snake_positions:
                break  # Яблоко размещено в допустимой позиции

    def draw(self):
        """Отрисовывает яблока на экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE)
                           )  # Создается прямоугольник для яблока
        pygame.draw.rect(screen, self.body_color, rect)  # Рисует яблоко
        pygame.draw.rect(screen, BORDER_COLOR, rect,
                         1)  # Рисует границу яблока


class Snake(GameObject):
    """Класс для змейки."""

    def __init__(self):
        super().__init__()
        self.body_color = SNAKE_COLOR  # Устанавливаем цвет змейки
        # Изначальная позиция головы змейки
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        # Начальное направление движения
        self.direction = choice((RIGHT, LEFT, UP, DOWN))
        self.next_direction = None  # Следующее направление
        self.length = 1  # Длина змейки

    def update_direction(self):
        """Обновляет направление движения змейки, если оно изменилось."""
        if self.next_direction:
            # Обновляем текущее направление
            self.direction = self.next_direction
            self.next_direction = None  # Сбрасываем следующее направление

    def move(self):
        """Двигает змею в текущем направлении."""
        self.update_direction()  # Обновляем направление перед движением
        new_position = [
            self.positions[0][0] + GRID_SIZE * self.direction[0],
            self.positions[0][1] + GRID_SIZE * self.direction[1]
        ]

        # Обработка столкновения со стенами
        if new_position[0] < 0:
            # Перемещение в противоположную сторону
            new_position[0] = SCREEN_WIDTH - GRID_SIZE
        elif new_position[0] >= SCREEN_WIDTH:
            new_position[0] = 0  # Установка на начало поля
        if new_position[1] < 0:
            # Перемещение в противоположную сторону
            new_position[1] = SCREEN_HEIGHT - GRID_SIZE
        elif new_position[1] >= SCREEN_HEIGHT:
            new_position[1] = 0  # Установка на начало поля

        # Вставляем новую позицию головы
        self.positions.insert(0, new_position)
        # Если длина змейки превышает заданную
        if len(self.positions) > self.length:
            self.positions.pop(-1)  # Удаляем последний сегмент змейки

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def draw(self):
        """Отрисовывает змею на экране."""
        for position in self.positions:
            # Создание прямоугольника для сегмента
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)  # Рисуем сегмент
            # Рисуем границу сегмента
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def reset(self):
        """Сбрасывает изменения позиции змейки в случае столкновения собой."""
        if self.get_head_position() in self.positions[1:]:
            # Устанавливаем начальную позицию
            self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
            # Случайное направление
            self.direction = choice((RIGHT, LEFT, UP, DOWN))
            self.length = 1  # Сбрасываем длину


def handle_keys(snake):
    """Обрабатывает нажатия клавиш для управления змейкой."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit  # Закрытие игры при выходе
        elif event.type == pygame.KEYDOWN:  # Если нажата клавиша
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP  # Изменение направления
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def main():
    """Основная функция игры."""
    pygame.init()  # Инициализация Pygame
    snake = Snake()  # Создание змейки
    apple = Apple(snake.positions)  # Передаем позиции змеи при создании яблока

    while True:
        clock.tick(SPEED)  # Добавление вызова tick для управления скоростью
        screen.fill(BOARD_BACKGROUND_COLOR)  # Отрисовка фона
        apple.draw()  # Отрисовка яблока
        handle_keys(snake)  # Обработка нажатий клавиш
        snake.move()  # Движение змейки
        snake.draw()  # Отрисовка змейки
        snake.reset()  # Сброс состояния, если змейка столкнулась с собой

        # Проверка на поедание яблока
        if snake.get_head_position() == apple.position:
            snake.length += 1  # Увеличиваем длину змейки
            # Генерируем новую позицию яблока
            apple.randomize_position(snake.positions)

        pygame.display.update()  # Обновление дисплея


if __name__ == '__main__':
    main()  # Запуск основной функции, если файл исполняется непосредственно
