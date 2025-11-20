import os
import re
import math

# Hexagonal coordinate mapping (q, r axes)
HEX_DELTAS = {
    'n':  (0, -1),
    'ne': (1, -1),
    'se': (1, 0),
    's':  (0, 1),
    'sw': (-1, 1),
    'nw': (-1, 0)
}

def parse_path(filepath):
    """
    Reads the comma-separated path sequence.
    """
    try:
        # Robust path reading
        input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), filepath)
        with open(input_file, 'r') as f:
            # Read single line, remove whitespace, and split by comma
            path_str = f.read().strip().replace(' ', '')
            path = path_str.split(',')
    except FileNotFoundError:
        print(f"Error: Path file not found at '{filepath}'")
        return []
    
    return [move for move in path if move]

def calculate_hex_distance(path: list[str]) -> int:
    """
    Simulates the path movement using axial coordinates (q, r) and calculates 
    the minimum number of steps required to reach the destination.
    """
    q, r = 0, 0 # Axial coordinates (starting at origin)
    
    # 1. Simulate movement and find final coordinates
    for move in path:
        if move in HEX_DELTAS:
            dq, dr = HEX_DELTAS[move]
            q += dq
            r += dr
            
    # 2. Calculate the distance (Manhattan distance on hex grid)
    # Distance = max(|q|, |r|, |s|) where s = -(q + r)
    
    s = -(q + r)
    
    min_steps = max(abs(q), abs(r), abs(s))
    
    return min_steps

def solve_hex_grid_puzzle(filepath):
    """Main function to orchestrate path simulation."""
    
    path = calculate_hex_distance(parse_path(filepath))
    
    return path

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting hex grid pathfinding simulation using data from: {os.path.abspath(input_file)}\n")
    
    final_steps = solve_hex_grid_puzzle(input_file)
    
    print("\n" + "="*50)
    print("FEWEST NUMBER OF STEPS REQUIRED TO REACH THE CHILD PROCESS:")
    print(f"SCORE: {final_steps}")
    print("="*50)