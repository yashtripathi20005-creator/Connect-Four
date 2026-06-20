"""
Connect Four - Board Class
Manages the game board state, piece placement, and win detection.
"""

class Board:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.board = []
        self.reset()
    
    def reset(self):
        """Reset the board to empty state."""
        self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
    
    def drop_piece(self, col, player_id):
        """
        Drop a piece in the specified column.
        Returns the row where the piece landed, or None if column is full.
        """
        if col < 0 or col >= self.cols:
            return None
        
        # Find the lowest empty row in the column
        for row in range(self.rows - 1, -1, -1):
            if self.board[row][col] == 0:
                self.board[row][col] = player_id
                return row
        
        return None  # Column is full
    
    def check_win(self, row, col, player_id):
        """
        Check if the last move resulted in a win.
        Checks all four directions: horizontal, vertical, diagonal (both ways).
        """
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return False
        
        # Check horizontal
        if self._check_direction(row, col, player_id, 0, 1) + self._check_direction(row, col, player_id, 0, -1) >= 3:
            return True
        
        # Check vertical
        if self._check_direction(row, col, player_id, 1, 0) + self._check_direction(row, col, player_id, -1, 0) >= 3:
            return True
        
        # Check diagonal (down-right / up-left)
        if self._check_direction(row, col, player_id, 1, 1) + self._check_direction(row, col, player_id, -1, -1) >= 3:
            return True
        
        # Check diagonal (down-left / up-right)
        if self._check_direction(row, col, player_id, 1, -1) + self._check_direction(row, col, player_id, -1, 1) >= 3:
            return True
        
        return False
    
    def _check_direction(self, row, col, player_id, row_dir, col_dir):
        """
        Count consecutive pieces in a specific direction.
        """
        count = 0
        r, c = row + row_dir, col + col_dir
        
        while 0 <= r < self.rows and 0 <= c < self.cols and self.board[r][c] == player_id:
            count += 1
            r += row_dir
            c += col_dir
        
        return count
    
    def is_full(self):
        """Check if the board is full."""
        return all(self.board[0][col] != 0 for col in range(self.cols))
    
    def get_valid_moves(self):
        """Return a list of columns that are not full."""
        return [col for col in range(self.cols) if self.board[0][col] == 0]
