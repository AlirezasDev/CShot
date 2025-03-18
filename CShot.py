import pygame
import sys
import random

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

class Player:
    def __init__(self, name):
        self.name = name
        self.arrows = 10
        self.time = 100
        self.score = 0
        self.pointer_x = random.randint(50, WIDTH - 50)
        self.pointer_y = random.randint(50, HEIGHT - 50)
        self.shots = []
        self.last_shot_x = None
        self.last_shot_y = None
        self.active = True
        self.speed = 5

    def shoot(self):
        if self.arrows > 0 and self.time > 0:
            self.arrows -= 1
            self.shots.append((self.pointer_x, self.pointer_y))
            return True
        return False

    def update_time(self, dt):
        if self.active:
            self.time -= dt
            if self.time <= 0:
                self.time = 0
                self.active = False

    def move_pointer(self, keys, player_num, width, height):
        if not self.active:
            return
        if player_num == 1:
            if keys[pygame.K_LEFT]:
                self.pointer_x -= self.speed
            if keys[pygame.K_RIGHT]:
                self.pointer_x += self.speed
            if keys[pygame.K_UP]:
                self.pointer_y -= self.speed
            if keys[pygame.K_DOWN]:
                self.pointer_y += self.speed
        elif player_num == 2:
            if keys[pygame.K_a]:
                self.pointer_x -= self.speed
            if keys[pygame.K_d]:
                self.pointer_x += self.speed
            if keys[pygame.K_w]:
                self.pointer_y -= self.speed
            if keys[pygame.K_s]:
                self.pointer_y += self.speed
        self.pointer_x = max(0, min(self.pointer_x, width))
        self.pointer_y = max(0, min(self.pointer_y, height))

    def clear_shots(self):
        self.shots = []
        self.last_shot_x = None
        self.last_shot_y = None

    def calculate_points(self, shot_x, shot_y):
        if self.last_shot_x is None or self.last_shot_y is None:
            points = 1
        else:
            distance = ((self.last_shot_x - shot_x) ** 2 + (self.last_shot_y - shot_y) ** 2) ** 0.5
            if distance < 20:
                points = 5
            elif distance < 50:
                points = 4
            elif distance < 100:
                points = 3
            elif distance < 200:
                points = 2
            else:
                points = 1
        self.last_shot_x = shot_x
        self.last_shot_y = shot_y
        return points


class Target(GameObject):
    def __init__(self, x, y, radius=20):
        super().__init__(x, y)
        self.radius = radius
        self.color = (200, 0, 0)

    def draw(self, screen):
        if self.visible:
            pygame.draw.circle(screen, (150, 150, 150), (int(self.x), int(self.y)), self.radius + 5)
            pygame.draw.circle(screen, (100, 0, 0), (int(self.x), int(self.y)), self.radius + 2)
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def is_hit(self, shot_x, shot_y):
        distance = ((self.x - shot_x) ** 2 + (self.y - shot_y) ** 2) ** 0.5
        return distance <= self.radius


class BonusItem(Target):
    def __init__(self, x, y, bonus_type="time", value=5):
        super().__init__(x, y, radius=15)
        self.bonus_type = bonus_type
        self.value = value
        self.lifetime = 300
        self.color = TIME_BONUS_COLOR if bonus_type == "time" else ARROW_BONUS_COLOR

    def update(self, dt):
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.visible = False

    def apply_bonus(self, player):
        if self.bonus_type == "time":
            player.time += self.value
        elif self.bonus_type == "arrows":
            player.arrows += self.value

    def draw(self, screen):
        if self.visible:
            pygame.draw.circle(screen, (150, 150, 150), (int(self.x), int(self.y)), self.radius + 5)
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
            label = bonus_font.render("T" if self.bonus_type == "time" else "A", True, TEXT_COLOR)
            label_rect = label.get_rect(center=(self.x + self.radius + 10, self.y))
            screen.blit(label, label_rect)