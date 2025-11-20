import os
import hashlib
from collections import deque

# --- Constants ---
PASSCODE = "pgflpeqp" # Your puzzle input
GRID_SIZE = 4 # 0 to 3
GOAL_POS = (GRID_SIZE - 1, GRID_SIZE - 1)

# Movement definitions: (R, C) delta, Path Character, Hash Index
MOVES = [
    ((-1, 0), 'U', 0), # Up: (dr, dc), char, hash_index
    ((1, 0), 'D', 1),  # Down
    ((0, -1), 'L', 2), # Left
    ((0, 1), 'R', 3)   # Right
]
# Doors are open if the hash char is one of these:
OPEN_CHARS = {'b', 'c', 'd', 'e', 'f'}

def get_hash_doors(passcode: str, path: str) -> str:
    """
    Generates the MD5 hash of (passcode + path) and returns the first four hex characters.
    """
    s = (passcode + path).encode('utf-8')
    return hashlib.md5(s).hexdigest()[:4]

def is_valid_position(r, c):
    """Checks if the position (r, c) is within the 4x4 grid bounds."""
    return 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE

def solve_vault_puzzle_longest(passcode: str):
    """
    Performs DFS (using a stack) to find the longest path string from (0, 0) to (3, 3).
    """
    start_r, start_c = 0, 0
    
    # Stack stores: (r, c, path_string)
    stack = [(start_r, start_c, "")]
    
    max_path_length = 0
    
    while stack:
        r, c, path = stack.pop() # LIFO (DFS behavior)
        
        # Check for Goal
        if (r, c) == GOAL_POS:
            # Reached the vault. This path length is a candidate for the longest path.
            max_path_length = max(max_path_length, len(path))
            continue # CONTINUE SEARCHING to find longer paths
            
        # Optimization: Prune paths that are clearly too long (optional safety)
        if len(path) >= 5000:
            continue
            
        # 1. Get open doors based on the current path
        door_chars = get_hash_doors(passcode, path)
        
        # 2. Iterate through possible moves (U, D, L, R)
        for i, (delta, move_char, hash_index) in enumerate(MOVES):
            dr, dc = delta
            
            # Check door status
            if door_chars[hash_index] in OPEN_CHARS:
                # Door is open. Calculate next position.
                nr, nc = r + dr, c + dc
                
                # Check 3. Boundary Condition
                if is_valid_position(nr, nc):
                    next_path = path + move_char
                    
                    # Push the new state onto the stack
                    stack.append((nr, nc, next_path))
                    
    return max_path_length

# --- Main Execution Block ---
if __name__ == "__main__":
    
    print(f"Starting Vault Path Finder for passcode: {PASSCODE}")
    print(f"Start: (1, 1), Goal: (4, 4)")
    
    longest_path_length = solve_vault_puzzle_longest(PASSCODE)
    
    print("\n" + "="*50)
    print("LENGTH OF THE LONGEST PATH TO REACH THE VAULT:")
    print(f"SCORE: {longest_path_length}")
    print("="*50)