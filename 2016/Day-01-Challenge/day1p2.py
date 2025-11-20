import os
import re

# Direction Index Map: 0=N, 1=E, 2=S, 3=W (Clockwise order)
# Turning Right (R) is (D + 1) % 4
# Turning Left (L) is (D + 3) % 4
DIRECTION_DELTAS = [
    (0, 1),   # 0: North (+Y)
    (1, 0),   # 1: East (+X)
    (0, -1),  # 2: South (-Y)
    (-1, 0)   # 3: West (-X)
]

def solve_bunny_hq_puzzle(directions_file):
    """
    Simulates the movement path block-by-block and calculates the Manhattan distance 
    to the first location visited twice.
    """
    try:
        # Robust path reading
        with open(directions_file, 'r') as f:
            content = f.read().strip()
            # Split using regex to handle "R2, L3" or "R2,L3" or "R2 L3"
            instructions = re.split(r',\s*|\s+', content)
    except FileNotFoundError:
        print(f"Error: Directions file not found at '{directions_file}'")
        return 0
    
    # Initial State
    x, y = 0, 0
    current_direction = 0  # 0: North (as instructed)
    
    # Set to track all visited coordinates (x, y)
    visited = set([(x, y)])
    
    # Target location found during the simulation
    first_repeated_location = None
    
    # --- Simulation Loop ---
    for instruction in instructions:
        if not instruction or first_repeated_location:
            break
            
        turn_char = instruction[0]
        try:
            distance = int(instruction[1:])
        except ValueError:
            continue

        # 1. Update Direction (R or L)
        if turn_char == 'R':
            current_direction = (current_direction + 1) % 4
        elif turn_char == 'L':
            current_direction = (current_direction + 3) % 4
        
        # 2. Move ONE BLOCK AT A TIME to check for repeats
        dx, dy = DIRECTION_DELTAS[current_direction]
        
        for _ in range(distance):
            x += dx
            y += dy
            
            current_pos = (x, y)
            
            if current_pos in visited:
                # Found the first location visited twice!
                first_repeated_location = current_pos
                break # Exit the inner loop (distance traveled)
            
            visited.add(current_pos) # Add every step to visited set
        
        if first_repeated_location:
            break # Exit the outer loop (instructions)

    # 3. Calculate Manhattan Distance to the repeated location
    if first_repeated_location:
        rep_x, rep_y = first_repeated_location
        manhattan_distance = abs(rep_x) + abs(rep_y)
        return manhattan_distance
    else:
        # If no location was visited twice
        print("Warning: No location was visited twice by the end of instructions.")
        return 0

# --- Main Execution Block ---
if __name__ == "__main__":
    import re
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting Bunny HQ path simulation (Part Two - First Repeat) using instructions from: {os.path.abspath(input_file)}\n")
    
    final_score = solve_bunny_hq_puzzle(input_file)
    
    print("\n" + "="*50)
    print("PART TWO: SHORTEST PATH TO FIRST LOCATION VISITED TWICE:")
    print(f"SCORE: {final_score}")
    print("="*50)