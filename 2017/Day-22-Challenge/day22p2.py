import os
from collections import defaultdict
from typing import Set, Tuple, Dict, List

# --- Constants ---
# CRITICAL CHANGE: Increased bursts for Part 2
NUM_BURSTS = 10000000 

# State mapping (Numerical ID)
STATE_CLEAN = 0
STATE_WEAKENED = 1
STATE_INFECTED = 2
STATE_FLAGGED = 3

# Direction Index Map (0=Up, 1=Right, 2=Down, 3=Left)
DIRECTIONS = [
    (0, -1), # 0: Up (North, -Y)
    (1, 0),  # 1: Right (East, +X)
    (0, 1),  # 2: Down (South, +Y)
    (-1, 0)  # 3: Left (West, -X)
]

def parse_initial_grid(filepath) -> Dict[Tuple[int, int], int]:
    """
    Reads the initial map and extracts the coordinates of all infected nodes (#).
    Stores them as { (x, y): STATE_INFECTED }. All others are STATE_CLEAN (0).
    """
    grid_state = {}
    raw_grid = []
    
    try:
        # Robust path reading
        input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), filepath)
        with open(input_file, 'r') as f:
            raw_grid = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"Error: Map file not found at '{filepath}'")
        return grid_state
        
    if not raw_grid:
        return grid_state

    ROWS = len(raw_grid)
    mid = ROWS // 2
    
    # Map array coordinates (r, c) to simulation coordinates (x, y)
    for r in range(ROWS):
        for c in range(ROWS):
            if raw_grid[r][c] == '#':
                # Initial infected nodes start in the INFECTED state (2)
                grid_state[(c - mid, r - mid)] = STATE_INFECTED
                
    return grid_state

def solve_sporifica_puzzle(filepath):
    """
    Simulates the Evolved Virus carrier's movement and counts bursts that cause infection.
    """
    # 1. Initialize the state
    # grid_state: { (x, y): state_id } -> If key is missing, state is CLEAN (0).
    grid_state = parse_initial_grid(filepath)
    
    # Carrier starts at (0, 0) in the center of the grid
    x, y = 0, 0
    # Carrier starts facing Up (Index 0)
    direction_index = 0
    
    infection_bursts_count = 0
    
    # 2. Simulation Loop
    for burst in range(NUM_BURSTS):
        
        current_pos = (x, y)
        # Current state: Get from dictionary, default to CLEAN (0)
        current_state = grid_state.get(current_pos, STATE_CLEAN)
        
        # --- Step 1: Turn based on Current State ---
        if current_state == STATE_CLEAN:
            # Clean (0): Turn LEFT (D - 1) % 4
            direction_index = (direction_index + 3) % 4
        elif current_state == STATE_WEAKENED:
            # Weakened (1): NO turn (Straight)
            pass
        elif current_state == STATE_INFECTED:
            # Infected (2): Turn RIGHT (D + 1) % 4
            direction_index = (direction_index + 1) % 4
        elif current_state == STATE_FLAGGED:
            # Flagged (3): REVERSE (180 degrees) (D + 2) % 4
            direction_index = (direction_index + 2) % 4
            
        # --- Step 2: Modify State ---
        
        next_state = (current_state + 1) % 4 # Cycle: 0->1->2->3->0
        
        if next_state == STATE_INFECTED:
            # Count this burst if the transition resulted in a new infection
            infection_bursts_count += 1 
            
        # Update the grid state dictionary
        if next_state == STATE_CLEAN:
            # Clean state is the default, so we remove the entry to save memory
            if current_pos in grid_state:
                del grid_state[current_pos]
        else:
            # Weakened, Infected, or Flagged states are stored
            grid_state[current_pos] = next_state

        # --- Step 3: Move ---
        dx, dy = DIRECTIONS[direction_index]
        x += dx
        y += dy
        
    return infection_bursts_count

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting Evolved Virus simulation for {NUM_BURSTS} bursts (Part 2) using data from: {os.path.abspath(input_file)}\n")
    
    final_count = solve_sporifica_puzzle(input_file)
    
    print("\n" + "="*50)
    print("PART TWO: TOTAL BURSTS THAT CAUSED A NODE TO BECOME INFECTED:")
    print(f"SCORE: {final_count}")
    print("="*50)