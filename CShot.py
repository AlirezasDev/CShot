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

def get_player_names(screen):
    title_font = pygame.font.SysFont("Arial", 48, bold=True)
    input_font = pygame.font.SysFont("Arial", 32, bold=True)
    button_font = pygame.font.SysFont("Arial", 24, bold=True)

    BG_COLOR1 = (30, 30, 30)
    BG_COLOR2 = (10, 10, 10)
    TEXT_COLOR = (220, 220, 220)
    SHADOW_COLOR = (20, 20, 20, 150)
    BOX_COLOR = (50, 50, 50, 200)
    BORDER_COLOR = (100, 100, 100)
    BUTTON_COLOR = (70, 70, 70)
    BUTTON_HOVER = (100, 100, 100)

    input_box1 = pygame.Rect(200, 250, 200, 50)
    input_box2 = pygame.Rect(450, 250, 200, 50)
    button_rect = pygame.Rect(350, 350, 100, 40)

    selected_box = 1
    text1 = ''
    text2 = ''
    clock = pygame.time.Clock()
    button_hover = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box1.collidepoint(event.pos):
                    selected_box = 1
                elif input_box2.collidepoint(event.pos):
                    selected_box = 2
                elif button_rect.collidepoint(event.pos) and text1 and text2:
                    return text1, text2
            if event.type == pygame.KEYDOWN:
                if selected_box == 1:
                    if event.key == pygame.K_BACKSPACE:
                        text1 = text1[:-1]
                    elif event.key == pygame.K_TAB:
                        selected_box = 2
                    elif event.key != pygame.K_RETURN:
                        text1 += event.unicode
                elif selected_box == 2:
                    if event.key == pygame.K_BACKSPACE:
                        text2 = text2[:-1]
                    elif event.key == pygame.K_TAB:
                        selected_box = 1
                    elif event.key != pygame.K_RETURN:
                        text2 += event.unicode
                if event.key == pygame.K_RETURN and text1 and text2:
                    return text1, text2

        mouse_pos = pygame.mouse.get_pos()
        button_hover = button_rect.collidepoint(mouse_pos)

        for y in range(screen.get_height()):
            r = BG_COLOR1[0] + (BG_COLOR2[0] - BG_COLOR1[0]) * y / screen.get_height()
            g = BG_COLOR1[1] + (BG_COLOR2[1] - BG_COLOR1[1]) * y / screen.get_height()
            b = BG_COLOR1[2] + (BG_COLOR2[2] - BG_COLOR1[2]) * y / screen.get_height()
            pygame.draw.line(screen, (r, g, b), (0, y), (screen.get_width(), y))

        title_text = title_font.render("Enter Player Names", True, TEXT_COLOR)
        shadow_text = title_font.render("Enter Player Names", True, SHADOW_COLOR)
        title_rect = title_text.get_rect(center=(WIDTH // 2, 150))
        screen.blit(shadow_text, title_rect.move(3, 3))
        screen.blit(title_text, title_rect)

        input_surface1 = input_font.render(text1, True, TEXT_COLOR)
        input_rect1 = input_surface1.get_rect(center=input_box1.center)
        pygame.draw.rect(screen, SHADOW_COLOR, input_box1.move(5, 5).inflate(10, 10), border_radius=15)
        pygame.draw.rect(screen, BOX_COLOR, input_box1, border_radius=10)
        pygame.draw.rect(screen, P1_COLOR if selected_box == 1 else BORDER_COLOR, input_box1, 2, border_radius=10)
        screen.blit(input_surface1, input_rect1)
        label1 = input_font.render("P1", True, P1_COLOR)
        screen.blit(label1, (input_box1.x - 40, input_box1.y + 10))

        input_surface2 = input_font.render(text2, True, TEXT_COLOR)
        input_rect2 = input_surface2.get_rect(center=input_box2.center)
        pygame.draw.rect(screen, SHADOW_COLOR, input_box2.move(5, 5).inflate(10, 10), border_radius=15)
        pygame.draw.rect(screen, BOX_COLOR, input_box2, border_radius=10)
        pygame.draw.rect(screen, P2_COLOR if selected_box == 2 else BORDER_COLOR, input_box2, 2, border_radius=10)
        screen.blit(input_surface2, input_rect2)
        label2 = input_font.render("P2", True, P2_COLOR)
        screen.blit(label2, (input_box2.right + 10, input_box2.y + 10))

        button_color = BUTTON_HOVER if button_hover else BUTTON_COLOR
        pygame.draw.rect(screen, SHADOW_COLOR, button_rect.move(3, 3), border_radius=10)
        pygame.draw.rect(screen, button_color, button_rect, border_radius=10)
        button_text = button_font.render("Start", True, TEXT_COLOR)
        button_text_rect = button_text.get_rect(center=button_rect.center)
        screen.blit(button_text, button_text_rect)

        pygame.display.flip()
        clock.tick(60)


# Initialize players and targets
player1_name, player2_name = get_player_names(screen)
player1 = Player(player1_name)
player2 = Player(player2_name)

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

        # Update time and check game over
        player1.update_time(dt)
        player2.update_time(dt)

        # Check win conditions
        if not player1.active and player2.active:
            game_over = True
            winner = player2.name
        elif player1.active and not player2.active:
            game_over = True
            winner = player1.name
        elif not player1.active and not player2.active:
            game_over = True
            if player1.score > player2.score:
                winner = player1.name
            elif player2.score > player1.score:
                winner = player2.name
            elif player1.arrows > player2.arrows:
                winner = player1.name
            elif player2.arrows > player1.arrows:
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

    pygame.display.flip()

pygame.quit()
sys.exit()