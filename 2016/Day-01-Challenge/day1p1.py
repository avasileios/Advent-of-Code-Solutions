import os

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
    Simulates the movement path and calculates the final Manhattan distance 
    from the origin (0, 0).
    """
    try:
        # Robust path reading
        with open(directions_file, 'r') as f:
            # Read all content, clean up, and split by comma/space
            content = f.read().strip()
            # Split using regex to handle "R2, L3" or "R2,L3" or "R2 L3"
            instructions = re.split(r',\s*|\s+', content)
    except FileNotFoundError:
        print(f"Error: Directions file not found at '{directions_file}'")
        return 0
    
    # Initial State
    x, y = 0, 0
    current_direction = 0  # 0: North (as instructed)
    
    # --- Simulation Loop ---
    for instruction in instructions:
        if not instruction:
            continue
            
        turn_char = instruction[0]
        try:
            distance = int(instruction[1:])
        except ValueError:
            # print(f"Warning: Skipping invalid instruction: {instruction}")
            continue

        # 1. Update Direction (R or L)
        if turn_char == 'R':
            # Turn Right: (D + 1) % 4 (e.g., 0 (N) -> 1 (E))
            current_direction = (current_direction + 1) % 4
        elif turn_char == 'L':
            # Turn Left: (D - 1) % 4, or (D + 3) % 4
            current_direction = (current_direction + 3) % 4
        
        # 2. Update Position
        dx, dy = DIRECTION_DELTAS[current_direction]
        
        x += dx * distance
        y += dy * distance
        
    # 3. Calculate Manhattan Distance: |x| + |y|
    manhattan_distance = abs(x) + abs(y)
    
    return manhattan_distance

# --- Main Execution Block ---
if __name__ == "__main__":
    import re
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting Bunny HQ path simulation using instructions from: {os.path.abspath(input_file)}\n")
    
    final_score = solve_bunny_hq_puzzle(input_file)
    
    print("\n" + "="*50)
    print("SHORTEST PATH TO DESTINATION (MANHATTAN DISTANCE):")
    print(f"SCORE: {final_score}")
    print("="*50)