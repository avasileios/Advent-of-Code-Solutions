import os
from collections import defaultdict
from typing import Set, Tuple, Dict, List

# --- Constants ---
NUM_BURSTS = 10000

# Direction Index Map (0=Up, 1=Right, 2=Down, 3=Left)
# Turning Right: (D + 1) % 4
# Turning Left: (D - 1) % 4
DIRECTIONS = [
    (0, -1), # 0: Up (North, -Y in array indexing)
    (1, 0),  # 1: Right (East, +X)
    (0, 1),  # 2: Down (South, +Y)
    (-1, 0)  # 3: Left (West, -X)
]

def parse_initial_grid(filepath) -> Set[Tuple[int, int]]:
    """
    Reads the initial map and extracts the coordinates of all infected nodes (#).
    The center of the grid is determined relative to the input size.
    
    Returns:
        set: {(x, y) coordinates of infected nodes}
    """
    infected_nodes = set()
    raw_grid = []
    
    try:
        # Robust path reading
        input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), filepath)
        with open(input_file, 'r') as f:
            raw_grid = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"Error: Map file not found at '{filepath}'")
        return infected_nodes
        
    if not raw_grid:
        return infected_nodes

    ROWS = len(raw_grid)
    # The center of the input map is (mid, mid)
    mid = ROWS // 2
    
    # We map the input grid onto an infinite (x, y) coordinate system, 
    # where the center of the map (mid, mid) maps to the origin (0, 0) for the simulation.
    
    for r in range(ROWS):
        for c in range(ROWS): # Assuming square grid
            if raw_grid[r][c] == '#':
                # Map array coordinates (r, c) to simulation coordinates (x, y)
                # x = c - mid
                # y = r - mid
                infected_nodes.add((c - mid, r - mid))
                
    return infected_nodes

def solve_sporifica_puzzle(filepath):
    """
    Simulates the virus carrier's movement and counts bursts that cause infection.
    """
    # 1. Initialize the state
    infected_nodes = parse_initial_grid(filepath)
    
    # Carrier starts at (0, 0) in the center of the grid
    x, y = 0, 0
    # Carrier starts facing Up (Index 0)
    direction_index = 0
    
    infection_bursts_count = 0
    
    # 2. Simulation Loop
    for burst in range(NUM_BURSTS):
        
        current_pos = (x, y)
        is_infected = current_pos in infected_nodes
        
        # --- Step 1: Turn ---
        if is_infected:
            # If infected, turn RIGHT (D + 1) % 4
            direction_index = (direction_index + 1) % 4
        else:
            # If clean, turn LEFT (D - 1) % 4
            direction_index = (direction_index + 3) % 4
            
        # --- Step 2: Infect/Clean ---
        if is_infected:
            # Infected -> Cleaned (Remove from set)
            infected_nodes.remove(current_pos)
        else:
            # Clean -> Infected (Add to set)
            infected_nodes.add(current_pos)
            infection_bursts_count += 1 # Count this burst!

        # --- Step 3: Move ---
        dx, dy = DIRECTIONS[direction_index]
        x += dx
        y += dy
        
    return infection_bursts_count

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting Sporifica Virus simulation for {NUM_BURSTS} bursts using data from: {os.path.abspath(input_file)}\n")
    
    final_count = solve_sporifica_puzzle(input_file)
    
    print("\n" + "="*50)
    print(f"TOTAL BURSTS THAT CAUSED A NODE TO BECOME INFECTED:")
    print(f"SCORE: {final_count}")
    print("="*50)