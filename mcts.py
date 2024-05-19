import pygame
import random
import math
import sys
import subprocess
import datetime
import os
import time
import psutil

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

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MCTS AI")
screen.fill(WHITE)
font = pygame.font.Font(None, 36)

# Folder to save images
IMAGE_FOLDER = "images/mcts_results"

# Create the folder if it doesn't exist
if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER)
    
class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0

def select(node):
    while node.children:
        node = max(node.children, key=uct)
    return node

def expand(node):
    actions = get_legal_actions(node.state)
    for action in actions:
        new_state = apply_action(node.state, action)
        new_node = Node(new_state, parent=node)
        node.children.append(new_node)
    return random.choice(node.children)

def simulate(node):
    state = node.state
    while not is_terminal(state):
        action = random.choice(get_legal_actions(state))
        state = apply_action(state, action)
    return evaluate(state)

def backpropagate(node, result):
    while node:
        node.visits += 1
        node.wins += result
        node = node.parent

def uct(node):
    if node.visits == 0:
        return float("inf")
    return (node.wins / node.visits) + math.sqrt(2 * math.log(node.parent.visits) / node.visits)

def get_legal_actions(state):
    actions = []
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if state[row][col] == '':
                actions.append((row, col))
    return actions

def apply_action(state, action):
    row, col = action
    new_state = [row[:] for row in state]
    new_state[row][col] = 'X' if sum(row.count('X') for row in state) <= sum(row.count('O') for row in state) else 'O'
    return new_state

def is_terminal(state):
    return check_winner(state) is not None or all(state[row][col] != '' for row in range(BOARD_ROWS) for col in range(BOARD_COLS))

def check_winner(state):
    for row in range(BOARD_ROWS):
        if state[row][0] == state[row][1] == state[row][2] != '':
            return state[row][0]

    for col in range(BOARD_COLS):
        if state[0][col] == state[1][col] == state[2][col] != '':
            return state[0][col]

    if state[0][0] == state[1][1] == state[2][2] != '':
        return state[0][0]
    if state[0][2] == state[1][1] == state[2][0] != '':
        return state[0][2]

    if all(state[row][col] != '' for row in range(BOARD_ROWS) for col in range(BOARD_COLS)):
        return 'Tie'

    return None

def evaluate(state):
    winner = check_winner(state)
    if winner == 'X':
        return -1
    elif winner == 'O':
        return 1
    elif winner == 'Tie':
        return 0

def draw_grid():
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE), LINE_WIDTH)
    for i in range(1, BOARD_COLS):
        pygame.draw.line(screen, LINE_COLOR, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

def draw_markers(board):
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

# Function to save game result to a text file and image
def save_result(result):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    with open("mcts_results.txt", "a") as file:
        # Write the result message
        file.write(f"{timestamp}: {result} (Image: {os.path.join(IMAGE_FOLDER, f'{timestamp}.png')})\n")
        
        # Save the image to the folder
        pygame.image.save(screen, os.path.join(IMAGE_FOLDER, f"{timestamp}.png"))

# Function to save game result to a text file and image
def save_time_memory(time_taken, memory_taken):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    with open("mcts_time_memory.txt", "a") as file:
        # Write the result message and time taken
        file.write(f"{timestamp}: {time_taken:.3f} seconds, {memory_taken:.3f} kb\n")

# Back to main menu
def run_game():
    subprocess.Popen(["python", "main.py"])  # Open the selected AI file

def main(iterations=500):
    board = [['' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    current_node = Node(board)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and not is_terminal(current_node.state):
                pos = pygame.mouse.get_pos()
                col = pos[0] // SQUARE_SIZE
                row = pos[1] // SQUARE_SIZE
                if current_node.state[row][col] == '':
                    current_node.state[row][col] = 'X'
                    
                    if not is_terminal(current_node.state):
                        # Computer's turn using mcts algorithm
                        start_time = time.perf_counter()  
                        
                        # Measure memory before the MCTS call
                        process = psutil.Process()
                        before_memory = process.memory_info().rss
                    
                        for _ in range(iterations):  # Perform iterations
                            if not current_node.children:
                                new_node = expand(current_node)
                            else:
                                new_node = select(current_node)
                            result = simulate(new_node)
                            backpropagate(new_node, result)
                            
                        current_node = max(current_node.children, key=lambda n: n.visits)
                    
                        # Measure memory after the MCTS call
                        after_memory = process.memory_info().rss
                        
                        memory_usage = after_memory - before_memory
                        mcts_memory = memory_usage / 1024  # Convert to kilobytes
                        
                        end_time = time.perf_counter() 
                        mcts_time = end_time - start_time
                        
                        save_time_memory(mcts_time, mcts_memory)


        screen.fill(WHITE)
        draw_grid()
        draw_markers(current_node.state)
        pygame.display.flip()

        # Check for winner after player's move
        winner = check_winner(current_node.state)
        if winner:
            message = ""
            if winner == 'Tie':
                message = "It's a Tie!"
            else:
                message = f"{winner} wins!"

            save_result(message)
            
            # Fill the screen with black
            screen.fill((0, 0, 0))

            # Draw the grid and markers one last time before delay
            draw_grid()
            draw_markers(current_node.state)

            # Render the text background
            text_surface = font.render(message, True, (255, 255, 255))  # White text
            text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            text_background_rect = text_rect.inflate(10, 10)  # Inflate the text rectangle to create background padding
            pygame.draw.rect(screen, (0, 0, 0), text_background_rect)  # Draw the background rectangle
            screen.blit(text_surface, text_rect)
            pygame.display.flip()
            pygame.time.delay(5000)  # Delay before quitting
            pygame.quit()
            
            run_game()


if __name__ == "__main__":
    main(iterations=500)
