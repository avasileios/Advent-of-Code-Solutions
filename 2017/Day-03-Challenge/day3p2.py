import os
from collections import defaultdict

# --- Constants ---
# Target value (puzzle input)
TARGET_VALUE = 312051

# Directions for checking the 8 neighbors (including diagonals)
NEIGHBORS = [
    (1, 0), (1, 1), (0, 1), (-1, 1),
    (-1, 0), (-1, -1), (0, -1), (1, -1)
]

def get_next_spiral_coordinates():
    """
    Generator that yields (x, y) coordinates in spiral order, starting at (0, 0).
    """
    x, y = 0, 0
    yield x, y # Square 1
    
    # Segment length increases every two turns (1, 1, 2, 2, 3, 3, ...)
    segment_length = 1 
    # Direction sequence: R, U, L, D (0, 1, 2, 3)
    direction = 0 
    
    while True:
        for _ in range(2): # Two segments per length (e.g., R and U)
            dx, dy = NEIGHBORS[direction * 2] # Map 0, 1, 2, 3 to actual R, U, L, D deltas
            
            for _ in range(segment_length):
                x += dx
                y += dy
                yield x, y
            
            direction = (direction + 1) % 4
        
        # Increase the segment length after two segments (R and U, then L and D)
        segment_length += 1

def solve_spiral_sum_puzzle():
    """
    Simulates the spiral memory sum until the target value is exceeded.
    """
    # Grid stores: {(x, y): value}
    grid = {}
    
    # Initialize the spiral coordinate generator
    coord_generator = get_next_spiral_coordinates()
    
    # --- Square 1: Base Case ---
    x, y = next(coord_generator)
    grid[(x, y)] = 1
    
    # --- Squares 2, 3, 4, ... ---
    
    # Map direction index (0, 1, 2, 3) to the correct (dx, dy)
    # 0=R, 1=U, 2=L, 3=D
    SPIRAL_DELTAS = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    
    # Reset spiral state for the main loop iteration
    x, y = 0, 0
    segment_length = 1
    direction_index = 0
    
    # Start checking from Square 2
    while True:
        
        for _ in range(2): # Two segments (R, U then L, D)
            dx, dy = SPIRAL_DELTAS[direction_index]
            
            for _ in range(segment_length):
                x += dx
                y += dy
                
                # Calculate the value for the new square (x, y)
                current_sum = 0
                
                # Sum the values of all 8 neighbors (including diagonals)
                for nx_offset, ny_offset in NEIGHBORS:
                    neighbor_pos = (x + nx_offset, y + ny_offset)
                    
                    if neighbor_pos in grid:
                        current_sum += grid[neighbor_pos]
                
                # Check termination condition
                if current_sum > TARGET_VALUE:
                    return current_sum # Found the first value larger than the input
                
                # Write the new value to the grid
                grid[(x, y)] = current_sum
                
            direction_index = (direction_index + 1) % 4
        
        segment_length += 1

# --- Main Execution Block ---
if __name__ == "__main__":
    
    print(f"Target Threshold: {TARGET_VALUE}")
    
    first_value = solve_spiral_sum_puzzle()
    
    print("\n" + "="*50)
    print("FIRST VALUE WRITTEN LARGER THAN THE PUZZLE INPUT:")
    print(f"SCORE: {first_value}")
    print("="*50)