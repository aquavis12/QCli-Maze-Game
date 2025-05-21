import pygame
import sys
import os
import random
import math
from levels import LEVELS
from ui_elements import initialize_ui, load_image

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 40
PLAYER_SIZE = 30
TOKEN_SIZE = 20
OBSTACLE_SIZE = 25
HEART_SIZE = 25
PLAYER_SPEED = 5

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GOLD = (255, 215, 0)
LIGHT_BLUE = (100, 149, 237)  # For buttons

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Q Maze Runner")
clock = pygame.time.Clock()

# Initialize UI elements
message_system = initialize_ui()

# Load images
try:
    # Try to load images
    player_img = load_image('player.png', (PLAYER_SIZE, PLAYER_SIZE))
    wall_img = load_image('wall.png', (TILE_SIZE, TILE_SIZE))
    token_img = load_image('token.png', (TOKEN_SIZE, TOKEN_SIZE))
    obstacle_img = load_image('obstacle.png', (OBSTACLE_SIZE, OBSTACLE_SIZE))
    heart_img = load_image('heart.png', (HEART_SIZE, HEART_SIZE))
    
    # Set flag for using images
    use_images = True
except Exception as e:
    print(f"Error loading images: {e}")
    use_images = False

# Create fonts for title screen
try:
    title_font = pygame.font.SysFont('Arial', 72, bold=True)
    button_font = pygame.font.SysFont('Arial', 36)
except:
    title_font = pygame.font.Font(None, 72)
    button_font = pygame.font.Font(None, 36)

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)
        self.color = GREEN
        self.velocity_x = 0
        self.velocity_y = 0
        self.speed = PLAYER_SPEED
        self.score = 0
        self.lives = 3  # Player starts with 3 lives
        self.invulnerable = False
        self.invulnerable_timer = 0
        self.invulnerable_duration = 1.5  # seconds
        self.previous_lives = 3  # To track life changes
    
    def update(self, walls, obstacles):
        # Store the current position to revert if collision occurs
        original_x = self.rect.x
        original_y = self.rect.y
        
        # Move the player
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        
        # Check for collisions with walls
        collision = False
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                collision = True
                break
        
        # If collision occurred, revert to original position
        if collision:
            self.rect.x = original_x
            self.rect.y = original_y
        
        # Store previous lives to detect changes
        self.previous_lives = self.lives
        
        # Check for collisions with obstacles
        if not self.invulnerable:
            for obstacle in obstacles:
                if self.rect.colliderect(obstacle.rect):
                    self.lives -= 1
                    self.invulnerable = True
                    self.invulnerable_timer = pygame.time.get_ticks()
                    # Show message
                    message_system.add_message("Ouch! Hit by an obstacle!", RED)
                    break
        else:
            # Check if invulnerability period is over
            current_time = pygame.time.get_ticks()
            if current_time - self.invulnerable_timer > self.invulnerable_duration * 1000:
                self.invulnerable = False
    
    def draw(self, surface):
        if use_images:
            # Flash when invulnerable
            if self.invulnerable and pygame.time.get_ticks() % 300 < 150:
                # Create a semi-transparent white overlay
                overlay = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE), pygame.SRCALPHA)
                overlay.fill((255, 255, 255, 128))
                surface.blit(player_img, self.rect)
                surface.blit(overlay, self.rect)
            else:
                surface.blit(player_img, self.rect)
        else:
            if self.invulnerable and pygame.time.get_ticks() % 300 < 150:
                pygame.draw.rect(surface, WHITE, self.rect)
            else:
                pygame.draw.rect(surface, self.color, self.rect)
    
    def draw_lives(self, surface):
        """Draw heart icons representing player lives"""
        if use_images:
            for i in range(self.lives):
                x_pos = SCREEN_WIDTH - 40 - (i * (HEART_SIZE + 5))  # Position from right to left
                y_pos = 15  # Align with score height
                surface.blit(heart_img, (x_pos, y_pos))
        else:
            # Fallback to drawing simple hearts
            for i in range(self.lives):
                x_pos = SCREEN_WIDTH - 40 - (i * 30)
                y_pos = 15
                # Draw a simple heart shape
                pygame.draw.polygon(surface, RED, [
                    (x_pos + 15, y_pos + 5),
                    (x_pos + 5, y_pos + 15),
                    (x_pos + 15, y_pos + 25),
                    (x_pos + 25, y_pos + 15),
                ])
    
    def has_lost_life(self):
        """Returns True if player just lost a life"""
        return self.lives < self.previous_lives

class Wall:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = BLUE
    
    def draw(self, surface):
        if use_images:
            surface.blit(wall_img, self.rect)
        else:
            pygame.draw.rect(surface, self.color, self.rect)

class Token:
    def __init__(self, x, y):
        # Center the token in the tile
        center_x = x + (TILE_SIZE - TOKEN_SIZE) // 2
        center_y = y + (TILE_SIZE - TOKEN_SIZE) // 2
        self.rect = pygame.Rect(center_x, center_y, TOKEN_SIZE, TOKEN_SIZE)
        self.color = GOLD
    
    def draw(self, surface):
        if use_images:
            surface.blit(token_img, self.rect)
        else:
            pygame.draw.rect(surface, self.color, self.rect)

class MovingObstacle:
    def __init__(self, x, y, speed=2):
        # Center the obstacle in the tile
        center_x = x + (TILE_SIZE - OBSTACLE_SIZE) // 2
        center_y = y + (TILE_SIZE - OBSTACLE_SIZE) // 2
        self.rect = pygame.Rect(center_x, center_y, OBSTACLE_SIZE, OBSTACLE_SIZE)
        self.color = RED
        self.speed = speed
        self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        self.move_timer = 0
        self.move_delay = 30  # milliseconds between movement updates
    
    def update(self, walls):
        # Only move every few milliseconds to control speed
        current_time = pygame.time.get_ticks()
        if current_time - self.move_timer < self.move_delay:
            return
        
        self.move_timer = current_time
        
        # Store original position
        original_x = self.rect.x
        original_y = self.rect.y
        
        # Move in current direction
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed
        
        # Check for collisions with walls or screen boundaries
        collision = False
        if (self.rect.left < 0 or self.rect.right > SCREEN_WIDTH or 
            self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT):
            collision = True
        
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                collision = True
                break
        
        # If collision, revert position and change direction
        if collision:
            self.rect.x = original_x
            self.rect.y = original_y
            
            # Choose a new direction (not the same as current)
            possible_directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            possible_directions.remove(self.direction)
            opposite_dir = (-self.direction[0], -self.direction[1])
            if opposite_dir in possible_directions:
                possible_directions.remove(opposite_dir)  # Avoid going back and forth
            
            if possible_directions:
                self.direction = random.choice(possible_directions)
            else:
                self.direction = opposite_dir  # If no other options, go back
    
    def draw(self, surface):
        if use_images:
            surface.blit(obstacle_img, self.rect)
        else:
            pygame.draw.rect(surface, self.color, self.rect)

class Button:
    def __init__(self, x, y, width, height, text, color=LIGHT_BLUE, hover_color=BLUE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        self.text_color = WHITE
        self.font = button_font
        
    def draw(self, surface):
        # Draw button rectangle
        pygame.draw.rect(surface, self.current_color, self.rect)
        pygame.draw.rect(surface, WHITE, self.rect, 2)  # White border
        
        # Draw text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
        
    def is_hovered(self, pos):
        return self.rect.collidepoint(pos)
        
    def update(self, mouse_pos):
        if self.is_hovered(mouse_pos):
            self.current_color = self.hover_color
        else:
            self.current_color = self.color

def load_level(level_data):
    """Load a level from the level data"""
    maze = level_data["maze"]
    
    # Create game elements
    walls = []
    tokens = []
    player = None
    empty_spaces = []
    obstacle_spawn_points = []
    
    # Get wall color if specified
    wall_color = level_data.get("wall_color", BLUE)
    
    # Process the maze layout
    for row in range(len(maze)):
        for col in range(len(maze[0])):
            x = col * TILE_SIZE
            y = row * TILE_SIZE
            
            if maze[row][col] == 0:  # Empty path
                empty_spaces.append((col, row))
            elif maze[row][col] == 1:  # Wall
                wall = Wall(x, y, TILE_SIZE, TILE_SIZE)
                wall.color = wall_color  # Set custom wall color
                walls.append(wall)
            elif maze[row][col] == 2:  # Player starting position
                player = Player(x + (TILE_SIZE - PLAYER_SIZE) // 2, 
                               y + (TILE_SIZE - PLAYER_SIZE) // 2)
                empty_spaces.append((col, row))  # Player position is also an empty space
            elif maze[row][col] == 3:  # Token
                tokens.append(Token(x, y))
                empty_spaces.append((col, row))
            elif maze[row][col] == 4:  # Obstacle spawn point
                obstacle_spawn_points.append((x, y))
                empty_spaces.append((col, row))
    
    # If no player was defined in the maze, create one at a default position
    if player is None:
        player = Player(TILE_SIZE + (TILE_SIZE - PLAYER_SIZE) // 2, 
                       TILE_SIZE + (TILE_SIZE - PLAYER_SIZE) // 2)
    
    # Create obstacles based on level settings
    obstacles = []
    obstacle_count = level_data.get("obstacle_count", 0)
    obstacle_speed = level_data.get("obstacle_speed", 2)
    
    # If we have spawn points, use them; otherwise use random empty spaces
    if obstacle_spawn_points and obstacle_count > 0:
        # Use defined spawn points first
        for i in range(min(obstacle_count, len(obstacle_spawn_points))):
            x, y = obstacle_spawn_points[i]
            obstacles.append(MovingObstacle(x, y, obstacle_speed))
        
        # If we need more obstacles than spawn points, use random empty spaces
        if obstacle_count > len(obstacle_spawn_points):
            for i in range(obstacle_count - len(obstacle_spawn_points)):
                if empty_spaces:
                    col, row = random.choice(empty_spaces)
                    x, y = col * TILE_SIZE, row * TILE_SIZE
                    obstacles.append(MovingObstacle(x, y, obstacle_speed))
    elif obstacle_count > 0:
        # No spawn points defined, use random empty spaces
        for i in range(obstacle_count):
            if empty_spaces:
                col, row = random.choice(empty_spaces)
                x, y = col * TILE_SIZE, row * TILE_SIZE
                obstacles.append(MovingObstacle(x, y, obstacle_speed))
    
    return {
        "walls": walls,
        "player": player,
        "tokens": tokens,
        "obstacles": obstacles,
        "empty_spaces": empty_spaces,
        "name": level_data.get("name", "Unnamed Level"),
        "description": level_data.get("description", "")
    }

def show_title_screen():
    """Show the title screen with start button"""
    # Create start button
    button_width = 200
    button_height = 60
    start_button = Button(
        SCREEN_WIDTH // 2 - button_width // 2,
        SCREEN_HEIGHT // 2 + 50,
        button_width,
        button_height,
        "Start Game"
    )
    
    title_running = True
    while title_running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_button.is_hovered(mouse_pos):
                    title_running = False  # Exit title screen and start game
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Enter key also starts the game
                    title_running = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        
        # Update button hover states
        mouse_pos = pygame.mouse.get_pos()
        start_button.update(mouse_pos)
        
        # Draw title screen
        screen.fill(BLACK)
        
        # Draw title
        title_text = title_font.render("Q Maze Runner", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(title_text, title_rect)
        
        # Draw start button
        start_button.draw(screen)
        
        # Draw instructions
        instructions = button_font.render("Press ENTER to start or ESC to quit", True, WHITE)
        instructions_rect = instructions.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        screen.blit(instructions, instructions_rect)
        
        # Update display
        pygame.display.flip()
        clock.tick(60)

# Initialize game state
current_level_index = 0
level_data = load_level(LEVELS[current_level_index])
walls = level_data["walls"]
player = level_data["player"]
tokens = level_data["tokens"]
obstacles = level_data["obstacles"]
empty_spaces = level_data["empty_spaces"]
level_name = level_data["name"]
level_description = level_data["description"]

# Game state
game_over = False
level_complete = False

def next_level():
    """Load the next level"""
    global current_level_index, level_data, walls, player, tokens
    global obstacles, empty_spaces, level_name, level_description, level_complete
    
    current_level_index += 1
    if current_level_index < len(LEVELS):
        level_data = load_level(LEVELS[current_level_index])
        walls = level_data["walls"]
        player = level_data["player"]
        tokens = level_data["tokens"]
        obstacles = level_data["obstacles"]
        empty_spaces = level_data["empty_spaces"]
        level_name = level_data["name"]
        level_description = level_data["description"]
        level_complete = False
        return True
    else:
        # No more levels, game is complete
        return False

# Show title screen first
show_title_screen()

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Handle key presses
        if event.type == pygame.KEYDOWN:
            if not game_over and not level_complete:
                if event.key == pygame.K_LEFT:
                    player.velocity_x = -player.speed
                elif event.key == pygame.K_RIGHT:
                    player.velocity_x = player.speed
                elif event.key == pygame.K_UP:
                    player.velocity_y = -player.speed
                elif event.key == pygame.K_DOWN:
                    player.velocity_y = player.speed
            
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_r and game_over:
                # Reset the game to first level
                current_level_index = -1
                player.score = 0  # Reset score
                player.lives = 3  # Reset lives
                if next_level():
                    game_over = False
            elif event.key == pygame.K_n and level_complete:
                # Manual level advancement (now mostly unused due to auto-advancement)
                if not next_level():
                    # No more levels, game is complete
                    game_over = True
                    message_system.add_game_complete_message(player.score)
        
        # Handle key releases
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and player.velocity_x < 0:
                player.velocity_x = 0
            elif event.key == pygame.K_RIGHT and player.velocity_x > 0:
                player.velocity_x = 0
            elif event.key == pygame.K_UP and player.velocity_y < 0:
                player.velocity_y = 0
            elif event.key == pygame.K_DOWN and player.velocity_y > 0:
                player.velocity_y = 0
    
    # Update game state if not game over or level complete
    if not game_over and not level_complete:
        # Update player
        player.update(walls, obstacles)
        
        # Update obstacles
        for obstacle in obstacles:
            obstacle.update(walls)
        
        # Check for token collection
        tokens_to_remove = []
        for token in tokens:
            if player.rect.colliderect(token.rect):
                tokens_to_remove.append(token)
                player.score += 10
        
        # Remove collected tokens
        for token in tokens_to_remove:
            tokens.remove(token)
        
        # Check if player lost all lives
        if player.lives <= 0:
            game_over = True
            message_system.add_game_over_message()
            message_system.add_final_score_message(player.score)
        
        # Check if all tokens are collected
        if not tokens:
            # Add bonus points for completing the level
            player.score += 10
            message_system.add_message(f"Level Complete! +10 points", GREEN, 2.0, 'center')
            
            # Show level complete message briefly before automatically advancing
            level_complete = True
            pygame.display.flip()  # Update display to show the message
            pygame.time.delay(2000)  # Wait 2 seconds
            
            # Automatically advance to next level
            if not next_level():
                # No more levels, game is complete
                game_over = True
                message_system.add_game_complete_message(player.score)
            else:
                level_complete = False  # Continue to the next level
    
    # Update message system
    message_system.update()
    
    # Draw everything
    screen.fill(BLACK)
    
    # Draw walls
    for wall in walls:
        wall.draw(screen)
    
    # Draw tokens
    for token in tokens:
        token.draw(screen)
    
    # Draw obstacles
    for obstacle in obstacles:
        obstacle.draw(screen)
    
    # Draw player
    player.draw(screen)
    
    # Draw UI elements
    from ui_elements import DEFAULT_FONT, TITLE_FONT, SCORE_FONT, MESSAGE_FONT
    
    # Draw score with a more prominent display
    score_text = SCORE_FONT.render(f"Score: {player.score}", True, WHITE)
    # Add a semi-transparent background for better readability
    score_bg = pygame.Surface((score_text.get_width() + 20, score_text.get_height() + 10))
    score_bg.set_alpha(128)  # Semi-transparent
    score_bg.fill((0, 0, 0))  # Black background
    screen.blit(score_bg, (10, 10))
    screen.blit(score_text, (20, 15))  # Offset slightly for padding
    
    # Draw level info
    level_text = DEFAULT_FONT.render(f"Level {current_level_index + 1}: {level_name}", True, WHITE)
    screen.blit(level_text, (SCREEN_WIDTH // 2 - level_text.get_width() // 2, 15))  # Center level text
    
    # Draw hearts for lives
    player.draw_lives(screen)
    
    # Visual effect when losing a life
    if player.has_lost_life():
        # Flash the screen red briefly
        flash = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        flash.fill(RED)
        flash.set_alpha(100)  # Semi-transparent
        screen.blit(flash, (0, 0))
        
        # Add a message
        message_system.add_message("Life lost!", RED, 1.5, 'center')
    
    # Draw level description
    desc_text = MESSAGE_FONT.render(level_description, True, WHITE)
    screen.blit(desc_text, (SCREEN_WIDTH - 300, 50))
    
    # Draw messages
    message_system.draw(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
    
    # Draw game over message if game is over
    if game_over:
        # Draw a semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(150)  # Semi-transparent
        overlay.fill((0, 0, 0))  # Black
        screen.blit(overlay, (0, 0))
        
        # Draw game over or game complete message
        if current_level_index >= len(LEVELS):
            game_complete_text = TITLE_FONT.render("All Levels Complete!", True, GREEN)
            game_complete_rect = game_complete_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
            screen.blit(game_complete_text, game_complete_rect)
            
            score_text = DEFAULT_FONT.render(f"Final Score: {player.score}", True, GOLD)
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(score_text, score_rect)
            
            restart_text = DEFAULT_FONT.render("Want to play again? Press R", True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
            screen.blit(restart_text, restart_rect)
        else:
            game_over_text = TITLE_FONT.render("GAME OVER", True, RED)
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
            screen.blit(game_over_text, game_over_rect)
            
            score_text = DEFAULT_FONT.render(f"Final Score: {player.score}", True, GOLD)
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(score_text, score_rect)
            
            restart_text = DEFAULT_FONT.render("Press R to Restart", True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            screen.blit(restart_text, restart_rect)
    
    # Draw level complete message if level is complete (now rarely shown due to auto-advancement)
    if level_complete:
        level_complete_text = TITLE_FONT.render("LEVEL COMPLETE", True, GREEN)
        level_complete_rect = level_complete_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(level_complete_text, level_complete_rect)
    
    # Draw controls hint
    controls_text = MESSAGE_FONT.render("Controls: Arrow Keys to move | ESC: Quit", True, WHITE)
    screen.blit(controls_text, (10, SCREEN_HEIGHT - 30))
    
    # Update the display
    pygame.display.flip()
    
    # Cap the frame rate
    clock.tick(60)

# Quit pygame
pygame.quit()
sys.exit()
