import pygame
import random

pygame.init()

# Window
WIDTH = 640
HEIGHT = 480
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Daft Punk vs. Ghosts")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_PINK = (255, 240, 245)
SKY_BLUE = (0, 191, 255)
RED = (139, 0, 0)

clock = pygame.time.Clock()

# Load sprites
robot = pygame.image.load("robot.png")
coin = pygame.image.load("coin.png")
monster = pygame.image.load("monster.png")
bullet = pygame.Surface((5, 15))
bullet.fill(SKY_BLUE)

# Robot
robot_width = robot.get_width()
robot_height = robot.get_height()
robot_x = WIDTH // 2 - robot_width // 2
robot_y = HEIGHT - robot_height - 10
robot_speed = 10

# Objects
coins = []
monsters = []
bullets = []
bullet_speed = 10
bullet_cooldown = 300
last_bullet_time = pygame.time.get_ticks()

# Score and lives
score = 0
lives = 3
font = pygame.font.Font(None, 36)

def show_score_and_lives():
    score_text = font.render(f"Score: {score}", True, BLACK)
    lives_text = font.render(f"Lives: {lives}", True, BLACK)
    window.blit(score_text, (10, 10))
    window.blit(lives_text, (10, 40))

running = True
while running:
    window.fill(LIGHT_PINK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and robot_x > 0:
        robot_x -= robot_speed
    if keys[pygame.K_RIGHT] and robot_x < WIDTH - robot_width:
        robot_x += robot_speed
    if keys[pygame.K_SPACE]:
        current_time = pygame.time.get_ticks()
        if current_time - last_bullet_time > bullet_cooldown:
            bullets.append([robot_x + robot_width // 2 - 2, robot_y])
            last_bullet_time = current_time

     # Spawn coins and monsters
    if random.randint(1, 20) == 1:
        coins.append([random.randint(0, WIDTH - coin.get_width()), 0])
    if random.randint(1, 50) == 1:
        monsters.append([random.randint(0, WIDTH - monster.get_width()), 0])

    # Update positions of coins
    for c in coins[:]:
        c[1] += 5
        if c[1] > HEIGHT:
            coins.remove(c)
        elif (robot_x < c[0] < robot_x + robot_width or
              robot_x < c[0] + coin.get_width() < robot_x + robot_width) and \
             (robot_y < c[1] + coin.get_height() < robot_y + robot_height):
            coins.remove(c)
            score += 1

    # Update positions of monsters
    for m in monsters[:]:
        m[1] += 7
        if m[1] > HEIGHT:
            monsters.remove(m)
        elif (robot_x < m[0] < robot_x + robot_width or
              robot_x < m[0] + monster.get_width() < robot_x + robot_width) and \
             (robot_y < m[1] + monster.get_height() < robot_y + robot_height):
            monsters.remove(m)
            lives -= 1

    # Update bullets
    for b in bullets[:]:
        b[1] -= bullet_speed
        if b[1] < 0:
            bullets.remove(b)
        for m in monsters[:]:
            if (m[0] < b[0] < m[0] + monster.get_width() or
                m[0] < b[0] + 5 < m[0] + monster.get_width()) and \
               (m[1] < b[1] < m[1] + monster.get_height()):
                monsters.remove(m)
                bullets.remove(b)
                score += 2
                break

    # Draw everything
    window.blit(robot, (robot_x, robot_y))
    for c in coins:
        window.blit(coin, (c[0], c[1]))
    for m in monsters:
        window.blit(monster, (m[0], m[1]))
    for b in bullets:
        window.blit(bullet, (b[0], b[1]))
    show_score_and_lives()

    # Check for game over
    if lives <= 0:
        game_over_text = font.render("GAME OVER!", True, RED)
        window.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(2000)
        running = False

    pygame.display.flip()
    clock.tick(30)

pygame.quit()