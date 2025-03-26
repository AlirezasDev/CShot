import pygame
import sys
import random
from Menu import p1, p2

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
        self.lifetime = 5
        self.color = TIME_BONUS_COLOR if bonus_type == "time" else ARROW_BONUS_COLOR

    def update(self, dt):
        self.lifetime -= dt
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

# Initialize players and targets
player1 = Player(p1.username)
player2 = Player(p2.username)

targets = [Target(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)) for _ in range(3)]
bonus_items = []

# Game loop
running = True
bonus_spawn_timer = 0
BONUS_SPAWN_INTERVAL = 300
game_over = False
fade_alpha = 0
next_bonus_is_arrow = True  # Start with arrow bonus

while running:
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if not game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and player1.active:
                    if player1.shoot():
                        shot_x, shot_y = player1.pointer_x, player1.pointer_y
                        for bonus in bonus_items[:]:
                            if bonus.is_hit(shot_x, shot_y):
                                bonus.apply_bonus(player1)
                                bonus_items.remove(bonus)
                                break
                        else:
                            for target in targets[:]:
                                if target.is_hit(shot_x, shot_y):
                                    points = player1.calculate_points(shot_x, shot_y)
                                    if len(player1.shots) == 1:
                                        points += 2
                                    player1.score += points
                                    player1.clear_shots()
                                    targets.remove(target)
                                    targets.append(
                                        Target(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)))
                                    break
                if event.key == pygame.K_SPACE and player2.active:
                    if player2.shoot():
                        shot_x, shot_y = player2.pointer_x, player2.pointer_y
                        for bonus in bonus_items[:]:
                            if bonus.is_hit(shot_x, shot_y):
                                bonus.apply_bonus(player2)
                                bonus_items.remove(bonus)
                                break
                        else:
                            for target in targets[:]:
                                if target.is_hit(shot_x, shot_y):
                                    points = player2.calculate_points(shot_x, shot_y)
                                    if len(player2.shots) == 1:
                                        points += 2
                                    player2.score += points
                                    player2.clear_shots()
                                    targets.remove(target)
                                    targets.append(
                                        Target(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)))
                                    break

    if not game_over:
        # Move pointers
        keys = pygame.key.get_pressed()
        player1.move_pointer(keys, 1, WIDTH, HEIGHT)
        player2.move_pointer(keys, 2, WIDTH, HEIGHT)

        # Update time (still affects active status, but not game end)
        player1.update_time(dt)
        player2.update_time(dt)

        # Check if both players are out of arrows or time
        if (player1.arrows <= 0 and player2.arrows <= 0) or (player1.time <= 0 and player2.time <= 0):
            game_over = True
            if player1.score > player2.score:
                winner = player1.name
            elif player2.score > player1.score:
                winner = player2.name
            else:
                winner = "Draw"

        for bonus in bonus_items[:]:
            bonus.update(dt)
            if not bonus.visible:
                bonus_items.remove(bonus)

        # Spawn bonus items alternately
        bonus_spawn_timer += 1
        if bonus_spawn_timer >= BONUS_SPAWN_INTERVAL:
            bonus_type = "arrows" if next_bonus_is_arrow else "time"
            bonus_items.append(
                BonusItem(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50), bonus_type, 5))
            next_bonus_is_arrow = not next_bonus_is_arrow  # Toggle for next spawn
            bonus_spawn_timer = 0

        # Draw dark gradient background
        for y in range(HEIGHT):
            r = BG_COLOR1[0] + (BG_COLOR2[0] - BG_COLOR1[0]) * y / HEIGHT
            g = BG_COLOR1[1] + (BG_COLOR2[1] - BG_COLOR1[1]) * y / HEIGHT
            b = BG_COLOR1[2] + (BG_COLOR2[2] - BG_COLOR1[2]) * y / HEIGHT
            pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))

        # Draw game elements
        for target in targets:
            target.draw(screen)
        for bonus in bonus_items:
            bonus.draw(screen)
        for shot_x, shot_y in player1.shots:
            pygame.draw.circle(screen, P1_COLOR, (int(shot_x), int(shot_y)), 5)
        for shot_x, shot_y in player2.shots:
            pygame.draw.circle(screen, P2_COLOR, (int(shot_x), int(shot_y)), 5)

        # Player 1 Info
        p1_info = font.render(f"{player1.name}: {player1.score} | Arrows: {player1.arrows} | Time: {int(player1.time)}",
                              True, P1_COLOR)
        p1_rect = pygame.Rect(10, 10, p1_info.get_width() + 20, p1_info.get_height() + 20)
        pygame.draw.rect(screen, SHADOW_COLOR, p1_rect.move(5, 5), border_radius=10)
        pygame.draw.rect(screen, TEXT_BG, p1_rect, border_radius=10)
        screen.blit(p1_info, (p1_rect.x + 10, p1_rect.y + 10))

        # Player 2 Info
        p2_info = font.render(f"{player2.name}: {player2.score} | Arrows: {player2.arrows} | Time: {int(player2.time)}",
                              True, P2_COLOR)
        p2_rect = pygame.Rect(WIDTH - p2_info.get_width() - 30, 10, p2_info.get_width() + 20, p2_info.get_height() + 20)
        pygame.draw.rect(screen, SHADOW_COLOR, p2_rect.move(5, 5), border_radius=10)
        pygame.draw.rect(screen, TEXT_BG, p2_rect, border_radius=10)
        screen.blit(p2_info, (p2_rect.x + 10, p2_rect.y + 10))

    # Draw game over screen
    if game_over:
        if fade_alpha < 200:
            fade_alpha += 10
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, fade_alpha))
        screen.blit(overlay, (0, 0))
        winner_text = winner_font.render(f"Game Over! Winner: {winner}", True, TEXT_COLOR)
        score_text = font.render(f"Scores - {player1.name}: {player1.score}, {player2.name}: {player2.score}", True,
                                 TEXT_COLOR)
        screen.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2 - 80))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 10))


    pygame.display.flip()

if winner == p1.username:
    p1.assign_point(player1.score, "W")
    p2.assign_point(player2.score, "L")
elif winner == p2.username:
    p1.assign_point(player1.score, "L")
    p2.assign_point(player2.score, "W")
else:
    p1.assign_point(player1.score, "D")
    p2.assign_point(player2.score, "D")

pygame.quit()
sys.exit()