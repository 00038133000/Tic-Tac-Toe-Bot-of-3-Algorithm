import pygame
import sys
import subprocess
import datetime
import os
import time
import psutil

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 300, 300
LINE_WIDTH = 5
WHITE = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS

# Colors for X and O
X_COLOR = (255, 0, 0)
O_COLOR = (0, 0, 255)

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minimax AI")
screen.fill(WHITE)

# Initialize the board
board = [['' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

# Font
font = pygame.font.Font(None, 36)

# Folder to save images
IMAGE_FOLDER = "images/minimax_results"

# Create the folder if it doesn't exist
if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER)
    
# Function to save game result to a text file and image
def save_result(result):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    with open("minimax_results.txt", "a") as file:
        # Write the result message
        file.write(f"{timestamp}: {result} (Image: {os.path.join(IMAGE_FOLDER, f'{timestamp}.png')})\n")
        
        # Save the image to the folder
        pygame.image.save(screen, os.path.join(IMAGE_FOLDER, f"{timestamp}.png"))

# Function to save game result to a text file and image
def save_time_memory(time_taken, memory_taken):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    with open("minimax_time_memory.txt", "a") as file:
        # Write the result message and time taken
        file.write(f"{timestamp}: {time_taken:.3f} seconds, {memory_taken:.3f} kb\n")

# Back to main menu
def run_game():
    subprocess.Popen(["python", "main.py"])  # Open the selected AI file

# Function to draw the grid
def draw_grid():
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE), LINE_WIDTH)
    for i in range(1, BOARD_COLS):
        pygame.draw.line(screen, LINE_COLOR, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

# Function to draw the X's and O's
def draw_markers():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 'X':
                pygame.draw.line(screen, X_COLOR, (col * SQUARE_SIZE, row * SQUARE_SIZE),
                                 ((col + 1) * SQUARE_SIZE, (row + 1) * SQUARE_SIZE), LINE_WIDTH)
                pygame.draw.line(screen, X_COLOR, ((col + 1) * SQUARE_SIZE, row * SQUARE_SIZE),
                                 (col * SQUARE_SIZE, (row + 1) * SQUARE_SIZE), LINE_WIDTH)
            elif board[row][col] == 'O':
                pygame.draw.circle(screen, O_COLOR, (int(col * SQUARE_SIZE + SQUARE_SIZE / 2),
                                 int(row * SQUARE_SIZE + SQUARE_SIZE / 2)), SQUARE_SIZE // 2 - LINE_WIDTH // 2, LINE_WIDTH)

# Function to check for a winner
def check_winner():
    # Check rows
    for row in range(BOARD_ROWS):
        if board[row][0] == board[row][1] == board[row][2] != '':
            return board[row][0]

    # Check columns
    for col in range(BOARD_COLS):
        if board[0][col] == board[1][col] == board[2][col] != '':
            return board[0][col]

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != '':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != '':
        return board[0][2]

    # Check for tie
    if all(board[row][col] != '' for row in range(BOARD_ROWS) for col in range(BOARD_COLS)):
        return 'Tie'

    return None

# Function to evaluate the game state
def evaluate():
    winner = check_winner()
    if winner == 'X':
        return -1
    elif winner == 'O':
        return 1
    elif winner == 'Tie':
        return 0

# Minimax algorithm
def minimax(depth, is_maximizing):
    score = evaluate()

    # Base cases
    if score != None:
        return score

    if is_maximizing:
        best_score = float('-inf')
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == '':
                    board[row][col] = 'O'
                    score = minimax(depth + 1, False)
                    board[row][col] = ''
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == '':
                    board[row][col] = 'X'
                    score = minimax(depth + 1, True)
                    board[row][col] = ''
                    best_score = min(score, best_score)
        return best_score

# Main game loop
running = True
turn = 'X'
player_move_time = 0  # Variable to store the time of the player's move

while running:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if turn == 'X':
                # Player's turn
                mouseX, mouseY = event.pos
                clicked_row = mouseY // SQUARE_SIZE
                clicked_col = mouseX // SQUARE_SIZE

                if board[clicked_row][clicked_col] == '':
                    board[clicked_row][clicked_col] = 'X'
                    turn = 'O'
                    player_move_time = current_time  # Store the time of the player's move

    # Check for winner after player's move
    winner = check_winner()
    if winner:
        message = ""
        if winner == 'Tie':
            message = "It's a Tie!"
        else:
            message = f"{winner} wins!"
        
        # Save result to text file
        save_result(message)
        
        # Fill the screen with black
        screen.fill((0, 0, 0))

        # Draw the grid and markers one last time before delay
        draw_grid()
        draw_markers()
        
        # Render the text background
        text_surface = font.render(message, True, (255, 255, 255))  # White text
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        text_background_rect = text_rect.inflate(10, 10)  # Inflate the text rectangle to create background padding
        pygame.draw.rect(screen, (0, 0, 0), text_background_rect)  # Draw the background rectangle
        screen.blit(text_surface, text_rect)
        
        pygame.display.update()

        pygame.time.delay(5000)  # Delay before quitting
        pygame.quit()
        
        run_game()
                
    # Introduce delay after player's move
    if turn == 'O' and current_time - player_move_time >= 500:
        
        # Computer's turn using minimax algorithm
        start_time = time.time()  
        
        # Measure memory before the minimax call
        before_memory = psutil.Process().memory_info().rss
        
        best_score = float('-inf')
        best_move = None
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == '':
                    board[row][col] = 'O'
                    score = minimax(0, False)
                    board[row][col] = ''
                    if score > best_score:
                        best_score = score
                        best_move = (row, col)
        if best_move:
            board[best_move[0]][best_move[1]] = 'O'
            turn = 'X'
        
        # Measure memory after the minimax call
        after_memory = psutil.Process().memory_info().rss
        memory_usage = after_memory - before_memory
        minimax_memory = memory_usage / 1024  # Convert to kilobytes
        
        end_time = time.time()  # End timing
        minimax_time = end_time - start_time  # Calculate the time taken
        
        # Save result to text file
        save_time_memory(minimax_time, minimax_memory)
    
    # Clear the screen
    screen.fill(WHITE)
    
    # Draw the grid
    draw_grid()
    
    # Draw X's and O's
    draw_markers()

    # Update the display
    pygame.display.update()