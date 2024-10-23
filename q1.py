import random
from collections import defaultdict
import itertools

class MENACE:
    def __init__(self, initial_beads=4):
        # Initialize the matchboxes (states) with beads (moves)
        self.boxes = defaultdict(lambda: self.create_initial_beads(initial_beads))
        self.moves_history = []  # Store moves for current game
        self.states_history = []  # Store states for current game
        self.initial_beads = initial_beads
        
    def create_initial_beads(self, count):
        """Create initial bead distribution for empty positions"""
        return {i: count for i in range(9)}  # 9 possible positions
        
    def get_state_key(self, board):
        """Convert board to unique string key, accounting for symmetries"""
        def rotate_board(b):
            return [b[6], b[3], b[0], b[7], b[4], b[1], b[8], b[5], b[2]]
            
        def mirror_board(b):
            return [b[2], b[1], b[0], b[5], b[4], b[3], b[8], b[7], b[6]]
        
        # Generate all symmetrical positions
        states = []
        current = board[:]
        
        # Add rotations
        for _ in range(4):
            states.append(current[:])
            states.append(mirror_board(current))
            current = rotate_board(current)
            
        # Return the lexicographically smallest representation
        return min(''.join(str(x) for x in s) for s in states)
        
    def get_move(self, board):
        """Choose a move based on current board state"""
        # Get canonical state representation
        state = self.get_state_key(board)
        
        # Get available moves
        available_moves = [i for i, x in enumerate(board) if x == 0]
        if not available_moves:
            return None
            
        # Get beads for current state
        beads = self.boxes[state]
        valid_beads = {pos: count for pos, count in beads.items() 
                      if pos in available_moves and count > 0}
        
        if not valid_beads:
            # If no beads for valid moves, add some
            for pos in available_moves:
                beads[pos] = self.initial_beads
            valid_beads = {pos: self.initial_beads for pos in available_moves}
            
        # Choose move based on bead counts
        total_beads = sum(valid_beads.values())
        choice = random.randrange(total_beads)
        
        # Find selected move
        current_count = 0
        for pos, count in valid_beads.items():
            current_count += count
            if choice < current_count:
                # Store state and move for learning
                self.states_history.append(state)
                self.moves_history.append(pos)
                return pos
                
    def reward(self, result):
        """Update bead counts based on game result"""
        if not self.moves_history:
            return
            
        # Reward scheme
        if result == 1:  # Win
            reward = 3  # Add 3 beads
        elif result == 0:  # Draw
            reward = 1  # Add 1 bead
        else:  # Loss
            reward = -1  # Remove 1 bead
            
        # Update bead counts for each move made
        for state, move in zip(self.states_history, self.moves_history):
            self.boxes[state][move] = max(0, self.boxes[state][move] + reward)
            
        # Clear history
        self.moves_history = []
        self.states_history = []

def play_game(menace, opponent_func):
    """Play a game between MENACE and an opponent"""
    board = [0] * 9
    
    def check_winner(b):
        # Check rows, columns, and diagonals
        wins = [(0,1,2), (3,4,5), (6,7,8),  # rows
               (0,3,6), (1,4,7), (2,5,8),   # columns
               (0,4,8), (2,4,6)]            # diagonals
               
        for i,j,k in wins:
            if b[i] == b[j] == b[k] != 0:
                return b[i]
        if 0 not in b:
            return 0  # Draw
        return None
    
    # Play game
    current_player = 1
    while True:
        if current_player == 1:
            move = menace.get_move(board)
        else:
            move = opponent_func(board)
            
        if move is None:
            return 0  # Draw
            
        board[move] = current_player
        winner = check_winner(board)
        
        if winner is not None:
            if winner == 1:
                menace.reward(1)  # MENACE won
            elif winner == -1:
                menace.reward(-1)  # MENACE lost
            else:
                menace.reward(0)  # Draw
            return winner
            
        current_player = -current_player

def random_opponent(board):
    """Simple opponent that makes random valid moves"""
    moves = [i for i, x in enumerate(board) if x == 0]
    return random.choice(moves) if moves else None

# Training example
if __name__ == "__main__":
    menace = MENACE(initial_beads=4)
    results = {"wins": 0, "losses": 0, "draws": 0}
    
    # Train for 1000 games
    for i in range(1000):
        result = play_game(menace, random_opponent)
        if result == 1:
            results["wins"] += 1
        elif result == -1:
            results["losses"] += 1
        else:
            results["draws"] += 1
            
        if (i + 1) % 100 == 0:
            print(f"After {i+1} games:")
            print(f"Wins: {results['wins']}")
            print(f"Losses: {results['losses']}")
            print(f"Draws: {results['draws']}")
            print("---")