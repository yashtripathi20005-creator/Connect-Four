"""
Connect Four - Player Class
Represents a player in the game with a name and color.
"""

class Player:
    def __init__(self, name, color, player_id=None):
        self.name = name
        self.color = color
        self.id = player_id
    
    def __str__(self):
        return self.name
