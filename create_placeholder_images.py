import pygame
import os

# Initialize pygame
pygame.init()

# Create directory if it doesn't exist
os.makedirs('assets/images', exist_ok=True)

# Define image sizes
PLAYER_SIZE = (30, 30)
WALL_SIZE = (40, 40)
TOKEN_SIZE = (20, 20)
OBSTACLE_SIZE = (25, 25)
HEART_SIZE = (25, 25)

# Create player image (green square with eyes)
player_surface = pygame.Surface(PLAYER_SIZE, pygame.SRCALPHA)
pygame.draw.rect(player_surface, (0, 200, 0), (0, 0, PLAYER_SIZE[0], PLAYER_SIZE[1]))
# Add eyes
pygame.draw.circle(player_surface, (255, 255, 255), (10, 10), 5)
pygame.draw.circle(player_surface, (255, 255, 255), (20, 10), 5)
pygame.draw.circle(player_surface, (0, 0, 0), (10, 10), 2)
pygame.draw.circle(player_surface, (0, 0, 0), (20, 10), 2)
pygame.image.save(player_surface, 'assets/images/player.png')
print("Created player.png")

# Create wall image (blue brick pattern)
wall_surface = pygame.Surface(WALL_SIZE)
wall_surface.fill((50, 50, 150))  # Dark blue base
# Draw brick pattern
for y in range(0, WALL_SIZE[1], 10):
    offset = 0 if y % 20 == 0 else 10
    for x in range(offset, WALL_SIZE[0], 20):
        pygame.draw.rect(wall_surface, (80, 80, 180), (x, y, 10, 10))
pygame.draw.rect(wall_surface, (30, 30, 100), (0, 0, WALL_SIZE[0], WALL_SIZE[1]), 1)  # Border
pygame.image.save(wall_surface, 'assets/images/wall.png')
print("Created wall.png")

# Create token image (gold coin)
token_surface = pygame.Surface(TOKEN_SIZE, pygame.SRCALPHA)
pygame.draw.circle(token_surface, (255, 215, 0), (TOKEN_SIZE[0]//2, TOKEN_SIZE[1]//2), TOKEN_SIZE[0]//2)
pygame.draw.circle(token_surface, (200, 170, 0), (TOKEN_SIZE[0]//2, TOKEN_SIZE[1]//2), TOKEN_SIZE[0]//2 - 2)
pygame.image.save(token_surface, 'assets/images/token.png')
print("Created token.png")

# Create obstacle image (red spiky ball)
obstacle_surface = pygame.Surface(OBSTACLE_SIZE, pygame.SRCALPHA)
# Draw main circle
pygame.draw.circle(obstacle_surface, (200, 0, 0), (OBSTACLE_SIZE[0]//2, OBSTACLE_SIZE[1]//2), OBSTACLE_SIZE[0]//2)
# Draw spikes
for i in range(8):
    angle = i * 45
    x = OBSTACLE_SIZE[0]//2 + int(OBSTACLE_SIZE[0]//2 * 0.8 * pygame.math.Vector2(1, 0).rotate(angle).x)
    y = OBSTACLE_SIZE[1]//2 + int(OBSTACLE_SIZE[1]//2 * 0.8 * pygame.math.Vector2(1, 0).rotate(angle).y)
    pygame.draw.line(obstacle_surface, (255, 0, 0), 
                     (OBSTACLE_SIZE[0]//2, OBSTACLE_SIZE[1]//2), 
                     (x, y), 3)
pygame.image.save(obstacle_surface, 'assets/images/obstacle.png')
print("Created obstacle.png")

# Create heart image
heart_surface = pygame.Surface(HEART_SIZE, pygame.SRCALPHA)
# Draw a heart shape
heart_color = (255, 0, 0)  # Red heart
# Draw two circles for the top of the heart
radius = HEART_SIZE[0] // 4
pygame.draw.circle(heart_surface, heart_color, (radius, radius), radius)
pygame.draw.circle(heart_surface, heart_color, (HEART_SIZE[0] - radius, radius), radius)
# Draw a triangle for the bottom of the heart
points = [
    (0, radius),
    (HEART_SIZE[0] // 2, HEART_SIZE[1]),
    (HEART_SIZE[0], radius)
]
pygame.draw.polygon(heart_surface, heart_color, points)
pygame.image.save(heart_surface, 'assets/images/heart.png')
print("Created heart.png")

print("All placeholder images created successfully!")
