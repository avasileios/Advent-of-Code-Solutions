import os
from collections import deque

# --- Constants ---
GRID_SIZE = 100
NUM_STEPS = 100
ON = 1
OFF = 0

# Define the coordinates of the four corners
CORNERS = [
    (0, 0),                        # Top-Left
    (0, GRID_SIZE - 1),            # Top-Right
    (GRID_SIZE - 1, 0),            # Bottom-Left
    (GRID_SIZE - 1, GRID_SIZE - 1) # Bottom-Right
]

def load_initial_grid(filepath):
    """
    Reads the initial configuration (#=on, .=off) into a 2D list of integers 
    and forces the four corners to ON state.
    """
    grid = []
    try:
        # Robust path reading
        with open(filepath, 'r') as f:
            for line in f:
                clean_line = line.strip()
                if clean_line:
                    # Convert '#' to 1 (ON) and '.' to 0 (OFF)
                    row = [ON if char == '#' else OFF for char in clean_line]
                    if len(row) != GRID_SIZE:
                        print(f"Warning: Row length {len(row)} does not match expected size {GRID_SIZE}. Aborting.")
                        return None
                    grid.append(row)
    except FileNotFoundError:
        print(f"Error: Input file not found at '{filepath}'")
        return None
        
    if len(grid) != GRID_SIZE:
        print(f"Warning: Grid height {len(grid)} does not match expected size {GRID_SIZE}. Aborting.")
        return None
    
    # Enforce the "stuck on" rule for the initial state
    for r, c in CORNERS:
        grid[r][c] = ON
        
    return grid

def count_on_neighbors(grid, r, c, size):
    """
    Counts the number of 'on' neighbors (including diagonals) for the cell at (r, c).
    Missing neighbors outside the grid count as 'off'.
    """
    on_neighbors = 0
    
    # Iterate over all 8 neighbors (dr, dc): [-1, 0, 1] for both row and col delta
    for dr in range(-1, 2):
        for dc in range(-1, 2):
            # Skip the center cell itself
            if dr == 0 and dc == 0:
                continue
                
            nr, nc = r + dr, c + dc
            
            # Check bounds: If the neighbor is outside the grid, it counts as 'off' (0)
            if 0 <= nr < size and 0 <= nc < size:
                # Add the current state of the neighbor
                on_neighbors += grid[nr][nc]
                
    return on_neighbors

def simulate_animation(initial_grid):
    """
    Simulates the light grid animation for NUM_STEPS steps, keeping the 
    four corners permanently ON.
    """
    size = GRID_SIZE
    current_grid = initial_grid
    
    for step in range(1, NUM_STEPS + 1):
        # Create a new grid for the next state (simultaneous update)
        next_grid = [[OFF for _ in range(size)] for _ in range(size)]
        
        for r in range(size):
            for c in range(size):
                current_state = current_grid[r][c]
                
                # IMPORTANT: If the cell is a corner, it stays ON, 
                # so skip the standard rules.
                if (r, c) in CORNERS:
                    next_grid[r][c] = ON
                    continue 

                # Apply standard rules to non-corner lights
                on_neighbors = count_on_neighbors(current_grid, r, c, size)
                
                if current_state == ON:
                    # Rule 1: ON stays ON if 2 or 3 neighbors are on, turns OFF otherwise.
                    if on_neighbors == 2 or on_neighbors == 3:
                        next_grid[r][c] = ON
                    else:
                        next_grid[r][c] = OFF
                
                elif current_state == OFF:
                    # Rule 2: OFF turns ON if exactly 3 neighbors are on, stays OFF otherwise.
                    if on_neighbors == 3:
                        next_grid[r][c] = ON
                    else:
                        next_grid[r][c] = OFF
                        
        # Update the grid for the next step (Current grid is now the fully calculated next_grid)
        current_grid = next_grid

    # Calculate the total number of lights on
    total_lights_on = sum(sum(row) for row in current_grid)
    
    return total_lights_on

def solve_light_animation_puzzle(filepath):
    """Main function to run the puzzle."""
    
    initial_grid = load_initial_grid(filepath)
    if initial_grid is None:
        return 0

    print(f"Grid Size: {GRID_SIZE}x{GRID_SIZE}. Simulating {NUM_STEPS} steps.")
    print("WARNING: Four corner lights are enforced ON.")
    
    final_count = simulate_animation(initial_grid)
    
    return final_count

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting light animation simulation (Part 2 - Stuck Corners) using data from: {os.path.abspath(input_file)}\n")
    
    final_score = solve_light_animation_puzzle(input_file)
    
    print("\n" + "="*50)
    print(f"PART TWO: TOTAL NUMBER OF LIGHTS ON AFTER {NUM_STEPS} STEPS (Stuck Corners):")
    print(f"SCORE: {final_score}")
    print("="*50)