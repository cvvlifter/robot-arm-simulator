
# Инициализация import
import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Робот-манипулятор v0.1")
clock = pygame.time.Clock()

# Цвета
BG = (20, 20, 30)
BASE_COLOR = (200, 50, 50)
LINK1_COLOR = (100, 150, 255)
LINK2_COLOR = (100, 255, 150)

# Параметры манипулятора
base_pos = (WIDTH // 2, HEIGHT - 50)
link1_len = 150
link2_len = 120
angle1 = 45  # градусы
angle2 = 30  # градусы

# Главный цикл
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Очистка экрана
    screen.fill(BG)

    # Расчёт позиций звеньев (пока статично)
    import math
    rad1 = math.radians(angle1)
    joint1_x = base_pos[0] + link1_len * math.sin(rad1)
    joint1_y = base_pos[1] - link1_len * math.cos(rad1)

    rad2 = math.radians(angle1 + angle2)
    end_x = joint1_x + link2_len * math.sin(rad2)
    end_y = joint1_y - link2_len * math.cos(rad2)

    # Отрисовка
    pygame.draw.circle(screen, BASE_COLOR, base_pos, 15)  # база
    pygame.draw.line(screen, LINK1_COLOR, base_pos, (joint1_x, joint1_y), 8)  # звено 1
    pygame.draw.line(screen, LINK2_COLOR, (joint1_x, joint1_y), (end_x, end_y), 8)  # звено 2
    pygame.draw.circle(screen, (255, 220, 0), (end_x, end_y), 10)  # захват

    # Обновление экрана
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
