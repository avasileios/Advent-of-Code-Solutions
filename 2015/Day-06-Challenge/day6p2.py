import os
import re

GRID_SIZE = 1000

def initialize_grid(size):
    """Initializes a square grid of the given size to all 0s (brightness 0)."""
    # Grid now stores brightness levels (integers >= 0)
    return [[0 for _ in range(size)] for _ in range(size)]

def solve_light_puzzle(filepath):
    """
    Simulates the light grid based on Santa's instructions and calculates 
    the total brightness of all lights (Part 2).
    """
    grid = initialize_grid(GRID_SIZE)
    
    try:
        # Robust path reading
        with open(filepath, 'r') as f:
            instructions = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"Error: Instructions file not found at '{filepath}'")
        return 0
    
    # Regex to parse the instruction line: action x1,y1 through x2,y2
    pattern = re.compile(r'(turn on|turn off|toggle)\s+(\d+),(\d+)\s+through\s+(\d+),(\d+)')
    
    for instruction in instructions:
        match = pattern.match(instruction)
        if not match:
            # print(f"Warning: Skipping malformed instruction: {instruction}")
            continue

        action = match.group(1)
        # Coordinates (x1, y1) and (x2, y2)
        # Collect the four groups into a single iterable (tuple) and map int() over it.
        try:
            x1, y1, x2, y2 = map(int, (match.group(2), match.group(3), match.group(4), match.group(5)))
        except ValueError:
            continue # Skip if coordinates are invalid

        # Determine the inclusive boundaries (ensuring min/max order)
        start_x, end_x = min(x1, x2), max(x1, x2)
        start_y, end_y = min(y1, y2), max(y1, y2)
        
        # 3. Apply the action to the rectangular range
        for r in range(start_y, end_y + 1):
            for c in range(start_x, end_x + 1):
                
                # Check boundaries explicitly
                if r < 0 or r >= GRID_SIZE or c < 0 or c >= GRID_SIZE:
                    continue 

                # Apply new brightness rules
                if action == 'turn on':
                    grid[r][c] += 1
                elif action == 'turn off':
                    # Decrease brightness, minimum 0
                    grid[r][c] = max(0, grid[r][c] - 1)
                elif action == 'toggle':
                    # Increase brightness by 2
                    grid[r][c] += 2
                    
    # 4. Calculate the total brightness (sum of all brightness values)
    total_brightness = sum(sum(row) for row in grid)
    
    return total_brightness

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting light grid simulation (Part Two - Brightness) using instructions from: {os.path.abspath(input_file)}\n")
    
    final_count = solve_light_puzzle(input_file)
    
    print("\n" + "="*50)
    print("PART TWO: TOTAL BRIGHTNESS OF ALL LIGHTS COMBINED:")
    print(f"SCORE: {final_count}")
    print("="*50)