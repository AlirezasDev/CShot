import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CShot")
clock = pygame.time.Clock()

# Dark Theme Colors
BG_COLOR1 = (30, 30, 30)
BG_COLOR2 = (10, 10, 10)
P1_COLOR = (0, 191, 255)
P2_COLOR = (255, 140, 0)
TEXT_BG = (50, 50, 50, 180)
SHADOW_COLOR = (20, 20, 20, 100)
TEXT_COLOR = (220, 220, 220)
TIME_BONUS_COLOR = (0, 200, 0)
ARROW_BONUS_COLOR = (255, 255, 0)

# Fonts
font = pygame.font.SysFont("Arial", 16, bold=True)
bonus_font = pygame.font.SysFont("Arial", 12, bold=True)
winner_font = pygame.font.SysFont("Arial", 24, bold=True)


class GameObject:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visible = True

    def draw(self, screen):
        pass

    def is_hit(self, shot_x, shot_y):
        pass
