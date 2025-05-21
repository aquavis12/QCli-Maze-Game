"""
UI elements for the Maze Runner game.
"""
import pygame
import os
import time

# Initialize pygame font
pygame.font.init()

# Define fonts
DEFAULT_FONT = pygame.font.SysFont('Arial', 36)
TITLE_FONT = pygame.font.SysFont('Arial', 48)
MESSAGE_FONT = pygame.font.SysFont('Arial', 24)
SCORE_FONT = pygame.font.SysFont('Arial', 42, bold=True)  # Larger, bold font for score

def load_image(filename, size=None):
    """Load an image and optionally resize it"""
    try:
        path = os.path.join('assets', 'images', filename)
        image = pygame.image.load(path)
        if size:
            image = pygame.transform.scale(image, size)
        return image
    except pygame.error as e:
        print(f"Could not load image {filename}: {e}")
        # Create a colored surface as a fallback
        surface = pygame.Surface(size or (32, 32))
        surface.fill((255, 0, 255))  # Magenta for missing textures
        return surface

class MessageSystem:
    """Handles displaying messages to the player"""
    def __init__(self):
        self.messages = []  # List of (message, color, duration, position, creation_time)
    
    def add_message(self, message, color=(255, 255, 255), duration=3.0, position='bottom'):
        """Add a message to be displayed"""
        self.messages.append((message, color, duration, position, time.time()))
    
    def update(self):
        """Update messages, removing expired ones"""
        current_time = time.time()
        self.messages = [msg for msg in self.messages 
                        if current_time - msg[4] < msg[2]]
    
    def draw(self, surface, screen_width, screen_height):
        """Draw all active messages"""
        # Group messages by position
        top_messages = []
        center_messages = []
        bottom_messages = []
        
        for msg, color, _, position, creation_time in self.messages:
            if position == 'top':
                top_messages.append((msg, color, creation_time))
            elif position == 'center':
                center_messages.append((msg, color, creation_time))
            else:  # Default to bottom
                bottom_messages.append((msg, color, creation_time))
        
        # Draw top messages
        y_offset = 100
        for msg, color, _ in top_messages:
            text = MESSAGE_FONT.render(msg, True, color)
            text_rect = text.get_rect(center=(screen_width // 2, y_offset))
            surface.blit(text, text_rect)
            y_offset += 30
        
        # Draw center messages
        y_offset = screen_height // 2 - len(center_messages) * 15
        for msg, color, _ in center_messages:
            text = MESSAGE_FONT.render(msg, True, color)
            text_rect = text.get_rect(center=(screen_width // 2, y_offset))
            surface.blit(text, text_rect)
            y_offset += 30
        
        # Draw bottom messages
        y_offset = screen_height - 100 - len(bottom_messages) * 30
        for msg, color, _ in bottom_messages:
            text = MESSAGE_FONT.render(msg, True, color)
            text_rect = text.get_rect(center=(screen_width // 2, y_offset))
            surface.blit(text, text_rect)
            y_offset += 30
    
    def add_level_complete_message(self):
        """Add a level complete message"""
        self.add_message("Level Complete!", (0, 255, 0), 5.0, 'center')
        self.add_message("Press N for next level", (255, 255, 255), 5.0, 'center')
    
    def add_game_over_message(self):
        """Add a game over message"""
        self.add_message("Game Over!", (255, 0, 0), 5.0, 'center')
        self.add_message("Press R to restart", (255, 255, 255), 5.0, 'center')
    
    def add_final_score_message(self, score):
        """Add a final score message"""
        self.add_message(f"Final Score: {score}", (255, 215, 0), 5.0, 'center')  # Gold color
        
    def add_game_complete_message(self, score):
        """Add a game complete message"""
        self.add_message("Congratulations!", (0, 255, 0), 5.0, 'center')
        self.add_message("You completed all levels!", (0, 255, 0), 5.0, 'center')
        self.add_message(f"Final Score: {score}", (255, 215, 0), 5.0, 'center')
        self.add_message("Want to play again? Press R", (255, 255, 255), 5.0, 'center')

def initialize_ui():
    """Initialize UI elements"""
    message_system = MessageSystem()
    return message_system
