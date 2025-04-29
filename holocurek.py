import pygame
import random
import math
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Roguelike Gacha Game")

# Dialog box dimensions
DIALOG_WIDTH, DIALOG_HEIGHT = 600, 350

# Clock and FPS
clock = pygame.time.Clock()
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BROWN = (139, 69, 19)
GRAY = (169, 169, 169)

# Load sounds
level_up_sound = pygame.mixer.Sound(os.path.join("assets", "level_up.wav"))

# Player settings
player_size = 40
player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
player_speed = 5
player_health = 100
player_shield = 0
max_shield = 0
shield_active = False
sword_damage = 50
fist_damage = sword_damage // 2
attack_radius = 50
swinging = False
swing_angle = 0
swing_direction = 1
has_sword = False
player_direction = "right"

# Player level and experience
player_level = 0
current_exp = 0
exp_to_next_level = 100
level_up_pending = False

# Enemy settings
enemy_size = 30
enemy_health = 50
enemy_exp_drop = 25
enemies = []
enemy_spawn_rate = 30

# Gacha items
items = ["Sword", "Shield", "Bow", "Fireball"]
inventory = []

# Coins
coins = 0

# Fonts
font = pygame.font.Font(None, 36)

# Game loop flag
running = True

# --- Skill Choice Additions Start ---
skill_choices = ["Skill 1", "Skill 2", "Skill 3"]
skill_descriptions = [
    "Increases attack power.",
    "Grants temporary invincibility.",
    "Heals some HP."
]
selected_skill_index = 0
# --- Skill Choice Additions End ---

# Functions
def spawn_enemy():
    x = random.randint(0, SCREEN_WIDTH - enemy_size)
    y = random.randint(0, SCREEN_HEIGHT - enemy_size)
    enemies.append([x, y, enemy_health])

def draw_player():
    pygame.draw.rect(screen, BLUE, (*player_pos, player_size, player_size))
    if has_sword:
        sword_length = 50
        sword_width = 5
        center_x = player_pos[0] + player_size // 2
        center_y = player_pos[1] + player_size // 2

        angle_rad = math.radians(swing_angle)
        if player_direction == "right":
            sword_x = center_x + sword_length * math.cos(angle_rad)
            sword_y = center_y + sword_length * math.sin(angle_rad)
        elif player_direction == "left":
            sword_x = center_x - sword_length * math.cos(angle_rad)
            sword_y = center_y - sword_length * math.sin(angle_rad)
        elif player_direction == "up":
            sword_x = center_x - sword_length * math.sin(angle_rad)
            sword_y = center_y - sword_length * math.cos(angle_rad)
        elif player_direction == "down":
            sword_x = center_x + sword_length * math.sin(angle_rad)
            sword_y = center_y + sword_length * math.cos(angle_rad)

        pygame.draw.line(screen, BROWN, (center_x, center_y), (sword_x, sword_y), sword_width)
        return (center_x, center_y, sword_x, sword_y)
    return None

def draw_enemies():
    for enemy in enemies:
        pygame.draw.rect(screen, RED, (*enemy[:2], enemy_size, enemy_size))
        health_ratio = enemy[2] / enemy_health
        pygame.draw.rect(screen, GREEN, (enemy[0], enemy[1] - 10, int(enemy_size * health_ratio), 5))

def move_player(keys):
    global player_direction
    if keys[pygame.K_w] and player_pos[1] > 0:
        player_pos[1] -= player_speed
        player_direction = "up"
    if keys[pygame.K_s] and player_pos[1] < SCREEN_HEIGHT - player_size:
        player_pos[1] += player_speed
        player_direction = "down"
    if keys[pygame.K_a] and player_pos[0] > 0:
        player_pos[0] -= player_speed
        player_direction = "left"
    if keys[pygame.K_d] and player_pos[0] < SCREEN_WIDTH - player_size:
        player_pos[0] += player_speed
        player_direction = "right"

def gacha_pull():
    global has_sword, player_shield, max_shield, shield_active, coins
    if coins >= 10:
        coins -= 10
        item = random.choice(items)
        inventory.append(item)

        if item == "Sword":
            has_sword = True
        elif item == "Shield":
            player_shield += 50
            max_shield += 50
            shield_active = True
        return f"You pulled: {item}"
    elif coins == 0:
        return "You don’t have any coins to gacha!"
    else:
        return "You don’t have enough coins!"

def check_collision():
    global player_health, player_shield, max_shield, shield_active
    if level_up_pending:
        return
    player_rect = pygame.Rect(*player_pos, player_size, player_size)
    for enemy in enemies:
        enemy_rect = pygame.Rect(*enemy[:2], enemy_size, enemy_size)
        if player_rect.colliderect(enemy_rect):
            if player_shield > 0:
                damage_absorbed = min(player_shield, 1)
                player_shield -= damage_absorbed
                if player_shield <= 0:
                    shield_active = False
                    max_shield = 0
            else:
                player_health -= 1

def gain_exp(amount):
    global current_exp, player_level, exp_to_next_level, player_health, level_up_pending
    current_exp += amount
    while current_exp >= exp_to_next_level:
        current_exp -= exp_to_next_level
        player_level += 1
        exp_to_next_level = int(exp_to_next_level * 1.5)
        player_health += 10
        level_up_sound.play()
        level_up_pending = True

def check_sword_collision(sword_coords):
    global enemies, coins
    if not sword_coords:
        return
    center_x, center_y, sword_x, sword_y = sword_coords
    sword_rect = pygame.Rect(min(center_x, sword_x), min(center_y, sword_y), abs(sword_x - center_x), abs(sword_y - center_y))
    updated_enemies = []
    for enemy in enemies:
        enemy_rect = pygame.Rect(*enemy[:2], enemy_size, enemy_size)
        if sword_rect.colliderect(enemy_rect):
            enemy[2] -= sword_damage
            if enemy[2] <= 0:
                coins += random.choices([0, 1, 2], weights=[60, 30, 10])[0]
                gain_exp(enemy_exp_drop)
            else:
                updated_enemies.append(enemy)
        else:
            updated_enemies.append(enemy)
    enemies = updated_enemies

def punch():
    global enemies, coins
    punch_rect = pygame.Rect(player_pos[0] - attack_radius, player_pos[1] - attack_radius, player_size + 2 * attack_radius, player_size + attack_radius * 2)
    updated_enemies = []
    for enemy in enemies:
        enemy_rect = pygame.Rect(*enemy[:2], enemy_size, enemy_size)
        if punch_rect.colliderect(enemy_rect):
            enemy[2] -= fist_damage
            if enemy[2] <= 0:
                coins += random.choices([0, 1, 2], weights=[60, 30, 10])[0]
                gain_exp(enemy_exp_drop)
            else:
                updated_enemies.append(enemy)
        else:
            updated_enemies.append(enemy)
    enemies = updated_enemies

def swing_sword():
    global swinging, swing_angle, swing_direction
    if not has_sword:
        return
    swinging = True
    swing_angle = -90
    swing_direction = 1

def update_swing():
    global swinging, swing_angle
    if swinging:
        swing_angle += 10 * swing_direction
        if swing_angle > 90:
            swinging = False
            swing_angle = 0

def draw_health_bar():
    bar_width = 200
    bar_height = 20
    health_ratio = player_health / 100

    pygame.draw.rect(screen, RED, (10, 50, bar_width, bar_height))
    pygame.draw.rect(screen, GREEN, (10, 50, int(bar_width * health_ratio), bar_height))

    if shield_active:
        shield_ratio = player_shield / max_shield
        pygame.draw.rect(screen, BLUE, (10, 75, bar_width, bar_height // 2))
        pygame.draw.rect(screen, WHITE, (10, 75, int(bar_width * shield_ratio), bar_height // 2))

def draw_coin_count():
    coin_text = font.render(f"Coins: {coins}", True, BLACK)
    screen.blit(coin_text, (10, 110))

def draw_level_and_exp():
    level_text = font.render(f"Level: {player_level}", True, BLACK)
    exp_text = font.render(f"EXP: {current_exp}/{exp_to_next_level}", True, BLACK)
    screen.blit(level_text, (10, 140))
    screen.blit(exp_text, (10, 170))

def draw_level_up_dialog():
    dialog_surface = pygame.Surface((DIALOG_WIDTH, DIALOG_HEIGHT))
    dialog_surface.fill(WHITE)
    pygame.draw.rect(dialog_surface, BLACK, (0, 0, DIALOG_WIDTH, DIALOG_HEIGHT), 5)
    text = font.render("Level Up! Press ENTER", True, BLACK)
    text_rect = text.get_rect(center=(DIALOG_WIDTH // 2, DIALOG_HEIGHT // 2))
    dialog_surface.blit(text, text_rect)
    screen.blit(dialog_surface, (SCREEN_WIDTH // 2 - DIALOG_WIDTH // 2, SCREEN_HEIGHT // 2 - DIALOG_HEIGHT // 2))

# --- Skill Choice Additions Start ---
def draw_skill_choices():
    draw_level_up_dialog()
    for i, skill in enumerate(skill_choices):
        color = RED if i == selected_skill_index else BLACK
        skill_text = font.render(skill, True, color)
        desc_text = font.render(skill_descriptions[i], True, color)
        x = SCREEN_WIDTH // 2 - DIALOG_WIDTH // 2 + 20
        y = SCREEN_HEIGHT // 2 - DIALOG_HEIGHT // 2 + 60 + i * 40
        screen.blit(skill_text, (x, y))
        screen.blit(desc_text, (x + 150, y))

def apply_skill(index):
    global sword_damage, player_health, player_shield, shield_active, max_shield
    if index == 0:
        sword_damage += 10
    elif index == 1:
        player_shield += 100
        max_shield += 100
        shield_active = True
    elif index == 2:
        player_health = min(100, player_health + 30)
# --- Skill Choice Additions End ---

# Main game loop
frame_count = 0
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if not level_up_pending:
                if event.key == pygame.K_g:
                    result = gacha_pull()
                    print(result)
                if event.key == pygame.K_SPACE:
                    if has_sword:
                        swing_sword()
                    else:
                        punch()
            # --- Skill Choice Additions Start ---
            if level_up_pending:
                if event.key == pygame.K_LEFT:
                    selected_skill_index = (selected_skill_index - 1) % len(skill_choices)
                elif event.key == pygame.K_RIGHT:
                    selected_skill_index = (selected_skill_index + 1) % len(skill_choices)
                elif event.key == pygame.K_RETURN:
                    apply_skill(selected_skill_index)
                    level_up_pending = False
                    selected_skill_index = 0
            # --- Skill Choice Additions End ---

    if not level_up_pending:
        keys = pygame.key.get_pressed()
        move_player(keys)
        update_swing()
        frame_count += 1
        if frame_count % enemy_spawn_rate == 0:
            spawn_enemy()
        check_collision()

    sword_coords = draw_player()
    draw_enemies()
    draw_health_bar()
    draw_coin_count()
    draw_level_and_exp()

    if swinging and not level_up_pending:
        check_sword_collision(sword_coords)

    inventory_text = font.render(f"Inventory: {', '.join(inventory[-3:])}", True, BLACK)
    screen.blit(inventory_text, (10, 10))

    # --- Skill Choice Additions Start ---
    if level_up_pending:
        draw_skill_choices()
    # --- Skill Choice Additions End ---

    pygame.display.flip()
    clock.tick(FPS)

    if player_health <= 0:
        print("Game Over")
        running = False

pygame.quit()
