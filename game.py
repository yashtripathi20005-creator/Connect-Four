"""
Connect Four - Game Logic and Main Loop
Handles the game state, player turns, win checking, and the main game loop.
"""

import pygame
import sys
from board import Board
from player import Player

class Game:
    def __init__(self):
        pygame.init()
        
        # Constants
        self.WINDOW_WIDTH = 700
        self.WINDOW_HEIGHT = 600
        self.BOARD_ROWS = 6
        self.BOARD_COLS = 7
        self.CELL_SIZE = 80
        self.RADIUS = int(self.CELL_SIZE / 2 - 5)
        
        # Colors
        self.BLUE = (0, 0, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.YELLOW = (255, 255, 0)
        self.WHITE = (255, 255, 255)
        self.GRAY = (128, 128, 128)
        self.GREEN = (0, 255, 0)
        
        # Initialize screen
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Connect Four")
        
        # Font
        self.font = pygame.font.SysFont("Arial", 24)
        self.big_font = pygame.font.SysFont("Arial", 48)
        
        # Game objects
        self.board = Board(self.BOARD_ROWS, self.BOARD_COLS)
        self.player1 = Player("Player 1", self.RED)
        self.player2 = Player("Player 2", self.YELLOW)
        self.current_player = self.player1
        
        # Game state
        self.game_over = False
        self.winner = None
        self.turn_counter = 0
        
        # UI
        self.reset_button = pygame.Rect(250, 530, 200, 50)
        
    def draw_board(self):
        """Draw the game board and pieces."""
        # Draw background
        self.screen.fill(self.BLACK)
        
        # Draw board
        for row in range(self.BOARD_ROWS):
            for col in range(self.BOARD_COLS):
                # Calculate position
                x = col * self.CELL_SIZE + self.CELL_SIZE // 2 + 10
                y = row * self.CELL_SIZE + self.CELL_SIZE // 2 + 10
                
                # Draw cell background (blue circle)
                pygame.draw.circle(self.screen, self.BLUE, (x, y), self.RADIUS)
                
                # Draw piece if occupied
                if self.board.board[row][col] != 0:
                    color = self.RED if self.board.board[row][col] == 1 else self.YELLOW
                    pygame.draw.circle(self.screen, color, (x, y), self.RADIUS - 2)
                else:
                    # Draw empty cell (black circle)
                    pygame.draw.circle(self.screen, self.BLACK, (x, y), self.RADIUS - 2)
        
        # Draw current player indicator
        indicator_text = f"{self.current_player.name}'s Turn"
        if self.game_over:
            if self.winner:
                indicator_text = f"{self.winner.name} Wins!"
            else:
                indicator_text = "It's a Draw!"
        
        text_surface = self.big_font.render(indicator_text, True, self.WHITE)
        text_rect = text_surface.get_rect(center=(self.WINDOW_WIDTH // 2, 510))
        self.screen.blit(text_surface, text_rect)
        
        # Draw reset button
        pygame.draw.rect(self.screen, self.GREEN, self.reset_button)
        reset_text = self.font.render("New Game", True, self.BLACK)
        reset_rect = reset_text.get_rect(center=self.reset_button.center)
        self.screen.blit(reset_text, reset_rect)
        
        pygame.display.update()
    
    def get_column_from_mouse(self, pos):
        """Get the column index from mouse position."""
        x, y = pos
        if y > 10 + self.BOARD_ROWS * self.CELL_SIZE:
            return None
        col = (x - 10) // self.CELL_SIZE
        if 0 <= col < self.BOARD_COLS:
            return col
        return None
    
    def handle_click(self, pos):
        """Handle mouse click events."""
        if self.game_over:
            # Check if reset button clicked
            if self.reset_button.collidepoint(pos):
                self.reset_game()
            return
        
        col = self.get_column_from_mouse(pos)
        if col is not None:
            row = self.board.drop_piece(col, self.current_player.id)
            if row is not None:
                self.turn_counter += 1
                
                # Check for win
                if self.board.check_win(row, col, self.current_player.id):
                    self.game_over = True
                    self.winner = self.current_player
                # Check for draw
                elif self.turn_counter >= self.BOARD_ROWS * self.BOARD_COLS:
                    self.game_over = True
                    self.winner = None
                else:
                    # Switch player
                    self.current_player = self.player2 if self.current_player == self.player1 else self.player1
    
    def reset_game(self):
        """Reset the game to initial state."""
        self.board.reset()
        self.current_player = self.player1
        self.game_over = False
        self.winner = None
        self.turn_counter = 0
    
    def run(self):
        """Main game loop."""
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
            
            self.draw_board()
            clock.tick(60)
        
        pygame.quit()
        sys.exit()
