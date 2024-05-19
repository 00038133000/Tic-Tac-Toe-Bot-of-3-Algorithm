import pygame
import sys
import subprocess

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Menu")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Fonts
font = pygame.font.SysFont(None, 36)

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

def main_menu():
    while True:
        screen.fill(WHITE)
        draw_text("Select AI to Play Against", font, BLACK, WIDTH // 2, HEIGHT // 4)
        
        # Buttons
        button_width, button_height = 200, 50
        button_x, button_y = WIDTH // 2 - button_width // 2, HEIGHT // 2 - button_height
        
        # Define button rects
        minimax_button = pygame.Rect(button_x, button_y, button_width, button_height)
        ab_pruning_button = pygame.Rect(button_x, button_y + 75, button_width, button_height)
        mcts_button = pygame.Rect(button_x, button_y + 150, button_width, button_height)
        
        # Draw button outlines
        pygame.draw.rect(screen, BLACK, minimax_button, 2)
        pygame.draw.rect(screen, BLACK, ab_pruning_button, 2)
        pygame.draw.rect(screen, BLACK, mcts_button, 2)
        
        # Draw button text
        draw_text("Minimax AI", font, BLACK, minimax_button.centerx, minimax_button.centery)
        draw_text("A-B Pruning AI", font, BLACK, ab_pruning_button.centerx, ab_pruning_button.centery)
        draw_text("MCTS AI", font, BLACK, mcts_button.centerx, mcts_button.centery)
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if minimax_button.collidepoint(mouse_pos):
                    return "minimax.py"
                elif ab_pruning_button.collidepoint(mouse_pos):
                    return "alphabeta.py"
                elif mcts_button.collidepoint(mouse_pos):
                    return "mcts.py"
        
        pygame.display.update()

def run_game(ai_file):
    print("Starting game against", ai_file[:-3], "AI")
    subprocess.Popen(["python", ai_file])  # Open the selected AI file

# Main loop
if __name__ == "__main__":
    ai_file = main_menu()
    run_game(ai_file)
