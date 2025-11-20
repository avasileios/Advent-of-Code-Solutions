import os

# --- Constants for Part Two ---
# Keypad map: None represents an empty space (no button)
KEYPAD = [
    [None, None, '1', None, None],  # Row 0
    [None, '2', '3', '4', None],    # Row 1
    ['5', '6', '7', '8', '9'],      # Row 2
    [None, 'A', 'B', 'C', None],    # Row 3
    [None, None, 'D', None, None]   # Row 4
]
ROWS = len(KEYPAD)
COLS = len(KEYPAD[0])

# Movement deltas: (dR, dC)
MOVE_DELTAS = {
    'U': (-1, 0),
    'D': (1, 0),
    'L': (0, -1),
    'R': (0, 1)
}

# Initial position is '5', which is Row 2, Column 0
START_POS = (2, 0) # (R, C) for button '5'

def is_valid_pos(r, c):
    """Checks if the position (r, c) is within the 5x5 grid bounds."""
    return 0 <= r < ROWS and 0 <= c < COLS

def is_button_at_pos(r, c):
    """Checks if there is a button at the given valid position."""
    return KEYPAD[r][c] is not None

def solve_bathroom_code(filepath):
    """
    Simulates the movement across the non-standard keypad and determines the final code.
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
            
            # Check validity: 
            # 1. Must be within the 5x5 grid bounds.
            # 2. Must land on an actual button (not None).
            if is_valid_pos(next_r, next_c) and is_button_at_pos(next_r, next_c):
                # Move is valid
                current_r, current_c = next_r, next_c
            # Else: Ignore the move (position remains the same)
        
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
    print("PART TWO: THE CORRECT BATHROOM CODE:")
    print(f"SCORE: {final_code}")
    print("="*50)