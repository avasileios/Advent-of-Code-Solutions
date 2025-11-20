import os

# --- Constants ---
# Keypad map (Row, Col) -> Button
KEYPAD = [
    ['1', '2', '3'],
    ['4', '5', '6'],
    ['7', '8', '9']
]
GRID_SIZE = 3 # 0 to 2

# Movement deltas: (dR, dC)
MOVE_DELTAS = {
    'U': (-1, 0),
    'D': (1, 0),
    'L': (0, -1),
    'R': (0, 1)
}

# Initial position is '5', which is Row 1, Column 1
START_POS = (1, 1)

def is_valid_pos(r, c):
    """Checks if the position (r, c) is within the 3x3 grid bounds."""
    return 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE

def solve_bathroom_code(filepath):
    """
    Simulates the movement across the keypad and determines the final code.
    """
    try:
        # Robust path reading
        input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), filepath)
        with open(input_file, 'r') as f:
            instructions = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"Error: Instructions file not found at '{filepath}'")
        return ""
    
    # Initial position
    current_r, current_c = START_POS
    bathroom_code = ""
    
    print(f"Starting simulation at button {KEYPAD[current_r][current_c]}")

    # Process each line of instructions (corresponds to one button press)
    for line_of_moves in instructions:
        
        for move in line_of_moves:
            if move not in MOVE_DELTAS:
                continue
                
            dr, dc = MOVE_DELTAS[move]
            next_r, next_c = current_r + dr, current_c + dc
            
            # Check boundaries: If the move is valid, update the position. 
            # If invalid, ignore the move (position remains current_r, current_c).
            if is_valid_pos(next_r, next_c):
                current_r, current_c = next_r, next_c
        
        # At the end of the line, press the button
        button = KEYPAD[current_r][current_c]
        bathroom_code += button
        
        # print(f"  Line finished on button: {button}")

    return bathroom_code

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = "input.txt" # Assuming input.txt is the standard file name
    
    final_code = solve_bathroom_code(input_file)
    
    print("\n" + "="*50)
    print("THE BATHROOM CODE:")
    print(f"SCORE: {final_code}")
    print("="*50)