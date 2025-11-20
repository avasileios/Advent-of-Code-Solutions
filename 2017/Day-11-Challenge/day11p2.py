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

def calculate_hex_distance(q: int, r: int) -> int:
    """
    Calculates the minimum number of steps required to reach position (q, r).
    Distance = max(|q|, |r|, |s|) where s = -(q + r).
    """
    s = -(q + r)
    return max(abs(q), abs(r), abs(s))


def calculate_max_distance(path: list[str]) -> int:
    """
    Simulates the path movement and tracks the maximum distance ever achieved.
    """
    q, r = 0, 0 # Axial coordinates (starting at origin)
    max_steps_reached = 0
    
    # 1. Simulate movement step by step
    for move in path:
        if move in HEX_DELTAS:
            dq, dr = HEX_DELTAS[move]
            q += dq
            r += dr
            
            # 2. Calculate distance at the current position
            current_steps = calculate_hex_distance(q, r)
            
            # 3. Track maximum distance encountered
            max_steps_reached = max(max_steps_reached, current_steps)
            
    return max_steps_reached

def solve_hex_grid_puzzle(filepath):
    """Main function to orchestrate path simulation."""
    
    path_sequence = parse_path(filepath)
    max_steps = calculate_max_distance(path_sequence)
    
    return max_steps

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting hex grid pathfinding simulation (Part 2 - Max Distance) using data from: {os.path.abspath(input_file)}\n")
    
    final_steps = solve_hex_grid_puzzle(input_file)
    
    print("\n" + "="*50)
    print("MAXIMUM NUMBER OF STEPS (FURTHEST DISTANCE EVER REACHED):")
    print(f"SCORE: {final_steps}")
    print("="*50)