import pygame
import random
import sys
import mysql.connector
from mysql.connector import Error

# Database connection details
HOST = "db4free.net"
DATABASE = "pythonfinal33"
USER = "af3311"
PASSWORD = "School33103311!"


def insert_user(username):
    # Open user.txt and check if it is empty
    with open("user.txt", "r") as file:
        if file.readlines():
            print("user.txt is not empty. No user added to the database.")
            return
    
    # Proceed with database insertion if user.txt is empty
    try:
        connection = mysql.connector.connect(
            host=HOST,
            database=DATABASE,
            user=USER,
            password=PASSWORD
        )
        if connection.is_connected():
            cursor = connection.cursor()
            insert_query = """INSERT INTO user (userName) VALUES (%s)"""
            cursor.execute(insert_query, (username,))
            connection.commit()
            print("User inserted successfully")
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 768
PLAYER_SIZE = 64
ENEMY_SIZE = 64
BULLET_SIZE = 32
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (170, 170, 170)
DARK_GRAY = (100, 100, 100)
PLAYER_SPEED = 7
BULLET_SPEED = 10
ENEMY_SPEED = 4
ENEMY_BULLET_SPEED = 6
SPAWN_ENEMY_EVENT = pygame.USEREVENT + 1
SHOOT_ENEMY_BULLET_EVENT = pygame.USEREVENT + 2

# Load images
background = pygame.image.load("spacebackground2.jpg")
player_img = pygame.image.load("player.png")
player2_img = pygame.image.load("player2.png")
enemy_img = pygame.image.load("enemy.png")
bullet_img = pygame.image.load("bullet.png")
enemy_bullet_img = pygame.image.load("enemy_bullet.png")
ENEMY_BULLET_SIZE = 52

# Scale images to the appropriate size
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
player_img = pygame.transform.scale(player_img, (PLAYER_SIZE, PLAYER_SIZE))
player2_img = pygame.transform.scale(player2_img, (PLAYER_SIZE, PLAYER_SIZE))
enemy_img = pygame.transform.scale(enemy_img, (ENEMY_SIZE, ENEMY_SIZE))
bullet_img = pygame.transform.scale(bullet_img, (BULLET_SIZE, BULLET_SIZE))
enemy_bullet_img = pygame.transform.scale(enemy_bullet_img, (ENEMY_BULLET_SIZE, ENEMY_BULLET_SIZE))

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Top-Down Shooter")

# Font setup
font = pygame.font.Font(None, 36)

# Enemy class
class Enemy:
    def __init__(self, x, y):
        self.rect = enemy_img.get_rect(topleft=(x, y))
        self.speed = ENEMY_SPEED

    def move_towards_player(self, player_rect):
        # Simplified movement towards player
        if self.rect.centerx < player_rect.centerx:
            self.rect.x += self.speed
        elif self.rect.centerx > player_rect.centerx:
            self.rect.x -= self.speed
        if self.rect.centery < player_rect.centery:
            self.rect.y += self.speed
        elif self.rect.centery > player_rect.centery:
            self.rect.y -= self.speed

# Enemy bullet class
class EnemyBullet:
    def __init__(self, x, y, direction):
        self.rect = enemy_bullet_img.get_rect(center=(x, y))
        self.direction = direction

    def move(self):
        self.rect.move_ip(self.direction[0] * ENEMY_BULLET_SPEED, self.direction[1] * ENEMY_BULLET_SPEED)

# Spawn enemy function
def spawn_enemy():
    x_pos = random.randint(0, SCREEN_WIDTH - ENEMY_SIZE)
    enemy = Enemy(x_pos, -2 * ENEMY_SIZE)
    enemies.append(enemy)

# Shoot enemy bullet function
def shoot_enemy_bullet():
    if enemies:
        enemy = random.choice(enemies)
        direction = ((player_rect.centerx - enemy.rect.centerx), (player_rect.centery - enemy.rect.centery))
        magnitude = (direction[0]**2 + direction[1]**2) ** 0.5
        direction = (direction[0] / magnitude, direction[1] / magnitude)
        enemy_bullet = EnemyBullet(enemy.rect.centerx, enemy.rect.centery, direction)
        enemy_bullets.append(enemy_bullet)

# Display Game Over screen
def game_over_screen():
    screen.fill(BLACK)
    game_over_text = font.render("GAME OVER", True, WHITE)
    restart_text = font.render("Press 'R' to Restart or 'Q' to Quit", True, WHITE)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

def game_over_screen_single_player():
    # Fill the screen with black
    screen.fill(BLACK)
    
    # Render game over text
    game_over_text = font.render("GAME OVER", True, WHITE)
    restart_text = font.render("Press 'R' to Restart or 'Q' to Quit", True, WHITE)
    
    # Display the game over text and restart instructions
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
    
    # Fetch top scores
    top_scores = get_top_scores()
    
    # Render and display top scores
    score_y_position = SCREEN_HEIGHT // 2 + 100  # Start below the restart instructions
    for idx, (user_name, score) in enumerate(top_scores):
        score_text = font.render(f"{idx + 1}. {user_name}: {score}", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, score_y_position + idx * 30))
    
    # Update the display
    pygame.display.flip()

    # Wait for user input
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

# Display Level Up message
def level_up_message(level):
    popup_width, popup_height = 300, 150
    popup_x = (SCREEN_WIDTH - popup_width) // 2
    popup_y = (SCREEN_HEIGHT - popup_height) // 2

    font = pygame.font.Font(None, 54)
    level_up_text = font.render(f"Level {level}", True, BLACK)
    pygame.draw.rect(screen, WHITE, (popup_x, popup_y, popup_width, popup_height))
    screen.blit(level_up_text, (popup_x + (popup_width - level_up_text.get_width()) // 2, popup_y + (popup_height - level_up_text.get_height()) // 2))
    pygame.display.flip()
    pygame.time.delay(2000)  # Display the pop-up for 2 seconds


#function to draw buttons to be used inside the home screen functions
def draw_button(screen, text, rect, color):
    pygame.draw.rect(screen, color, rect)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

# function to display home screen for user
def show_home_screen():
    screen.fill(BLACK)
    title_text = font.render("Top-Down Shooter", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - 150))

    # Button dimensions and positions
    button_width = 300
    button_height = 70
    single_player_rect = pygame.Rect((SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2), (button_width, button_height))
    multiplayer_rect = pygame.Rect((SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2 + 100), (button_width, button_height))
    add_user_rect = pygame.Rect((SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2 + 200), (button_width, button_height))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if single_player_rect.collidepoint(event.pos):
                    return "single"
                elif multiplayer_rect.collidepoint(event.pos):
                    return "multi"
                elif add_user_rect.collidepoint(event.pos):
                    username = input("Enter your username: ")
                    insert_user(username)

        # Draw buttons
        draw_button(screen, "Single Player", single_player_rect, DARK_GRAY if single_player_rect.collidepoint(pygame.mouse.get_pos()) else LIGHT_GRAY)
        draw_button(screen, "Multiplayer", multiplayer_rect, DARK_GRAY if multiplayer_rect.collidepoint(pygame.mouse.get_pos()) else LIGHT_GRAY)
       # draw_button(screen, "Add User", add_user_rect, DARK_GRAY if add_user_rect.collidepoint(pygame.mouse.get_pos()) else LIGHT_GRAY)

        pygame.display.flip()

# Game loop
def get_user_id_from_db(username):
    try:
        connection = mysql.connector.connect(
            host=HOST,
            database=DATABASE,
            user=USER,
            password=PASSWORD
        )
        if connection.is_connected():
            cursor = connection.cursor()
            select_query = "SELECT id FROM user WHERE userName=%s"
            cursor.execute(select_query, (username,))
            result = cursor.fetchall()  # Fetch all results
            
            if result:
                return result[0][0]
            else:
                return None
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            

def insert_score_into_leaderboard(user_id, score):
    try:
        connection = mysql.connector.connect(
            host=HOST,
            database=DATABASE,
            user=USER,
            password=PASSWORD
        )
        if connection.is_connected():
            cursor = connection.cursor()
            insert_query = "INSERT INTO leaderboard (userid, score) VALUES (%s, %s)"
            cursor.execute(insert_query, (user_id, score))
            connection.commit()
            print("Score inserted into leaderboard successfully")
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
def get_top_scores():
    try:
        connection = mysql.connector.connect(
            host=HOST,
            database=DATABASE,
            user=USER,
            password=PASSWORD
        )
        if connection.is_connected():
            cursor = connection.cursor()
            query = """
                SELECT u.userName, l.score
                FROM leaderboard l
                INNER JOIN user u ON u.id = l.userID
                ORDER BY l.score DESC
                LIMIT 3;
            """
            cursor.execute(query)
            results = cursor.fetchall()
            
            top_scores = []
            for row in results:
                top_scores.append((row[0], row[1]))  # (userName, score)
                
            return top_scores
    except Error as e:
        print("Error while connecting to MySQL", e)
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Example usage:
top_scores = get_top_scores()
for userName, score in top_scores:
    print(f"Username: {userName}, Score: {score}")
def main_game():
    global bullets, enemies, enemy_bullets, player_rect, score, level
    player_rect = player_img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 2 * PLAYER_SIZE))
    bullets = []
    enemies = []
    enemy_bullets = []
    score = 0
    level = 1

    clock = pygame.time.Clock()
    running = True

    # Spawn enemy timer
    pygame.time.set_timer(SPAWN_ENEMY_EVENT, 1000)
    pygame.time.set_timer(SHOOT_ENEMY_BULLET_EVENT, 1500)

    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == SPAWN_ENEMY_EVENT:
                spawn_enemy()
            elif event.type == SHOOT_ENEMY_BULLET_EVENT:
                shoot_enemy_bullet()

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_rect.left > 0:
            player_rect.move_ip(-PLAYER_SPEED, 0)
        if keys[pygame.K_RIGHT] and player_rect.right < SCREEN_WIDTH:
            player_rect.move_ip(PLAYER_SPEED, 0)
        if keys[pygame.K_SPACE]:
            bullet_rect = bullet_img.get_rect(midbottom=player_rect.midtop)
            bullets.append(bullet_rect)

        # Bullet movement
        for bullet in bullets[:]:
            bullet.move_ip(0, -BULLET_SPEED)
            if bullet.bottom < 0:
                bullets.remove(bullet)

        # Enemy movement towards player
        for enemy in enemies:
            enemy.move_towards_player(player_rect)
            if enemy.rect.colliderect(player_rect):
                running = False  # Game over if enemy collides with player

        # Enemy bullet movement
        for enemy_bullet in enemy_bullets[:]:
            enemy_bullet.move()
            if enemy_bullet.rect.colliderect(player_rect):
                running = False  # Game over if enemy bullet hits player
            if enemy_bullet.rect.top > SCREEN_HEIGHT:
                enemy_bullets.remove(enemy_bullet)

        # Collision detection between bullets and enemies
        enemies_to_remove = []
        bullets_to_remove = []
        for bullet in bullets:
            for enemy in enemies:
                if bullet.colliderect(enemy.rect):
                    bullets_to_remove.append(bullet)
                    enemies_to_remove.append(enemy)
                    score += 1

        # Remove collided bullets and enemies
        for bullet in bullets_to_remove:
            if bullet in bullets:
                bullets.remove(bullet)
        for enemy in enemies_to_remove:
            if enemy in enemies:
                enemies.remove(enemy)

        # Increase difficulty for level 2
        if score >= 20 and level == 1:
            level = 2
            level_up_message(level)
            pygame.time.set_timer(SPAWN_ENEMY_EVENT, 500)  # Increase spawn rate

        if score >= 80 and level == 2:
            level = 3
            level_up_message(level)
            pygame.time.set_timer(SPAWN_ENEMY_EVENT, 375)  # Increase spawn rate

        if score >= 150 and level == 3:
            level = 4
            level_up_message(level)
            pygame.time.set_timer(SPAWN_ENEMY_EVENT, 250)  # Increase spawn rate

        if score >= 250 and level == 4:
            level = 5
            level_up_message(level)
            pygame.time.set_timer(SPAWN_ENEMY_EVENT, 125)  # Increase spawn rate

        if score >= 400 and level == 5:
            level = 6
            level_up_message(level)
            pygame.time.set_timer(SPAWN_ENEMY_EVENT, 75)  # Increase spawn rate

        # Drawing
        screen.blit(background, (0, 0))
        screen.blit(player_img, player_rect.topleft)
        for bullet in bullets:
            screen.blit(bullet_img, bullet.topleft)
        for enemy in enemies:
            screen.blit(enemy_img, enemy.rect.topleft)
        for enemy_bullet in enemy_bullets:
            screen.blit(enemy_bullet_img, enemy_bullet.rect.topleft)

        # Display score and level
        score_text = font.render(f"Score: {score}", True, WHITE)
        level_text = font.render(f"Level: {level}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (10, 50))

        # Update display
        pygame.display.flip()
        clock.tick(60)

    # Read the personal best score and update the leaderboard if the current score is higher
    try:
        with open("personalbestscore.txt", "r") as file:
            personal_best = int(file.readline().strip())
    except (FileNotFoundError, ValueError):
        personal_best = 0

    if score > personal_best:
        with open("personalbestscore.txt", "w") as file:
            file.write(str(score))

        # Get the username from user.txt and update the leaderboard
        with open("user.txt", "r") as file:
            username = file.readline().strip()
            if username:
                user_id = get_user_id_from_db(username) #maybe change out of time necessity 
                if user_id:
                    insert_score_into_leaderboard(user_id, score)
                else:
                    print("User not found in database.")

    # Display Game Over screen
    game_over_screen_single_player()
    
def main_multiplayer():
    global bullets, enemies, enemy_bullets, player_rect, player2_rect, score, level
    player_rect = player_img.get_rect(center=(2 * SCREEN_WIDTH // 3, SCREEN_HEIGHT - 2 * PLAYER_SIZE))
    player2_rect = player2_img.get_rect(center=(SCREEN_WIDTH // 3, SCREEN_HEIGHT - 2 * PLAYER_SIZE))
    bullets = []
    bullets2 = []
    enemies = []
    enemy_bullets = []
    score = 0
    level = 1

    clock = pygame.time.Clock()
    running = True

    # Spawn enemy timer
    pygame.time.set_timer(SPAWN_ENEMY_EVENT, 1000)
    pygame.time.set_timer(SHOOT_ENEMY_BULLET_EVENT, 1500)

    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == SPAWN_ENEMY_EVENT:
                spawn_enemy()
            elif event.type == SHOOT_ENEMY_BULLET_EVENT:
                shoot_enemy_bullet()

        # Player movement
        keys = pygame.key.get_pressed()
        # Player 1 controls (Arrow keys)
        if keys[pygame.K_LEFT] and player_rect.left > 0:
            player_rect.move_ip(-PLAYER_SPEED, 0)
        if keys[pygame.K_RIGHT] and player_rect.right < SCREEN_WIDTH:
            player_rect.move_ip(PLAYER_SPEED, 0)
        if keys[pygame.K_SPACE]:
            bullet_rect = bullet_img.get_rect(midbottom=player_rect.midtop)
            bullets.append(bullet_rect)
        
        # Player 2 controls (WASD keys)
        if keys[pygame.K_a] and player2_rect.left > 0:
            player2_rect.move_ip(-PLAYER_SPEED, 0)
        if keys[pygame.K_d] and player2_rect.right < SCREEN_WIDTH:
            player2_rect.move_ip(PLAYER_SPEED, 0)
        if keys[pygame.K_LSHIFT]:
            bullet2_rect = bullet_img.get_rect(midbottom=player2_rect.midtop)
            bullets2.append(bullet2_rect)

        # Bullet movement
        for bullet in bullets[:]:
            bullet.move_ip(0, -BULLET_SPEED)
            if bullet.bottom < 0:
                bullets.remove(bullet)
        
        for bullet in bullets2[:]:
            bullet.move_ip(0, -BULLET_SPEED)
            if bullet.bottom < 0:
                bullets2.remove(bullet)

        # Enemy movement towards players
        for enemy in enemies:
            if enemy.rect.colliderect(player_rect) or enemy.rect.colliderect(player2_rect):
                running = False  # Game over if enemy collides with any player
            elif abs(enemy.rect.centerx - player_rect.centerx) + abs(enemy.rect.centery - player_rect.centery) < \
                    abs(enemy.rect.centerx - player2_rect.centerx) + abs(enemy.rect.centery - player2_rect.centery):
                enemy.move_towards_player(player_rect)
            else:
                enemy.move_towards_player(player2_rect)

        # Enemy bullet movement
        for enemy_bullet in enemy_bullets[:]:
            enemy_bullet.move()
            if enemy_bullet.rect.colliderect(player_rect) or enemy_bullet.rect.colliderect(player2_rect):
                running = False  # Game over if enemy bullet hits any player
            if enemy_bullet.rect.top > SCREEN_HEIGHT:
                enemy_bullets.remove(enemy_bullet)

        # Collision detection between bullets and enemies
        enemies_to_remove = []
        bullets_to_remove = []
        bullets2_to_remove = []
        for bullet in bullets:
            for enemy in enemies:
                if bullet.colliderect(enemy.rect):
                    bullets_to_remove.append(bullet)
                    enemies_to_remove.append(enemy)
                    score += 1

        for bullet in bullets2:
            for enemy in enemies:
                if bullet.colliderect(enemy.rect):
                    bullets2_to_remove.append(bullet)
                    enemies_to_remove.append(enemy)
                    score += 1

        # Remove collided bullets and enemies
        for bullet in bullets_to_remove:
            if bullet in bullets:
                bullets.remove(bullet)
        for bullet in bullets2_to_remove:
            if bullet in bullets2:
                bullets2.remove(bullet)
        for enemy in enemies_to_remove:
            if enemy in enemies:
                enemies.remove(enemy)

        # Increase difficulty for level 2
        if score >= 20 and level == 1:
            level = 2
            level_up_message(level)
            pygame.time.set_timer(SPAWN_ENEMY_EVENT, 400)  # Increase spawn rate

        if score >= 80 and level == 2:
            level = 3
            level_up_message(level)
            pygame.time.set_timer(SPAWN_ENEMY_EVENT, 300)  # Increase spawn rate

        if score >= 150 and level == 3:
            level = 4
            level_up_message(level)
            pygame.time.set_timer(SPAWN_ENEMY_EVENT, 150)  # Increase spawn rate

        if score >= 250 and level == 4:
            level = 5
            level_up_message(level)
            pygame.time.set_timer(SPAWN_ENEMY_EVENT, 100)  # Increase spawn rate

        if score >= 400 and level == 5:
            level = 6
            level_up_message(level)
            pygame.time.set_timer(SPAWN_ENEMY_EVENT, 40)  # Increase spawn rate

        # Drawing
        screen.blit(background, (0, 0))
        screen.blit(player_img, player_rect.topleft)
        screen.blit(player2_img, player2_rect.topleft)
        for bullet in bullets:
            screen.blit(bullet_img, bullet.topleft)
        for bullet in bullets2:
            screen.blit(bullet_img, bullet.topleft)
        for enemy in enemies:
            screen.blit(enemy_img, enemy.rect.topleft)
        for enemy_bullet in enemy_bullets:
            screen.blit(enemy_bullet_img, enemy_bullet.rect.topleft)

        # Display score and level
        score_text = font.render(f"Score: {score}", True, WHITE)
        level_text = font.render(f"Level: {level}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (10, 50))

        # Update display
        pygame.display.flip()
        clock.tick(60)

    # Display Game Over screen
    game_over_screen()

# Main game loop
while True:
    mode = show_home_screen()  # Added home screen
    if mode == "single":
        main_game()  # Start single player game
    elif mode == "multi":
        main_multiplayer()  # Start multiplayer game
