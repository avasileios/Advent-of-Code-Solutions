import os

# --- Constants ---
# Total number of rows to simulate (including the starting row)
TOTAL_ROWS = 40
TRAP = '^'
SAFE = '.'

# --- Rule Logic Mapping ---
# We use a set of patterns that result in a TRAP (^)
# Key: (L, C, R) where True = Trap (^), False = Safe (.)
TRAP_PATTERNS = {
    (True, True, False),    # L^C & !R
    (False, True, True),    # !L & C^R
    (True, False, False),   # L & !C & !R
    (False, False, True)    # !L & !C & R
}

def load_initial_row(filepath):
    """
    Reads the starting row configuration from the file.
    """
    try:
        # Robust path reading
        input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), filepath)
        with open(input_file, 'r') as f:
            # Assume the entire content is the single starting row string
            initial_row = f.read().strip()
    except FileNotFoundError:
        print(f"Error: Input file not found at '{filepath}'")
        return None
        
    return initial_row

def is_trap(left: bool, center: bool, right: bool) -> bool:
    """
    Determines if the new tile is a trap based on the three tiles above it.
    """
    return (left, center, right) in TRAP_PATTERNS

def simulate_trap_rows(initial_row: str):
    """
    Simulates the trap generation process for TOTAL_ROWS and counts safe tiles.
    """
    current_row = initial_row
    total_safe_tiles = current_row.count(SAFE)
    ROW_WIDTH = len(current_row)
    
    # We iterate for TOTAL_ROWS - 1 additional rows
    for r in range(1, TOTAL_ROWS):
        next_row_list = []
        
        # Determine the type of the new tile for each position (c)
        for c in range(ROW_WIDTH):
            
            # 1. Determine the L, C, R inputs from the current row
            
            # Center (C): Always current_row[c]
            center_char = current_row[c]
            
            # Left (L): current_row[c-1]. If off edge (c=0), assume SAFE ('.').
            if c == 0:
                left_char = SAFE
            else:
                left_char = current_row[c - 1]
                
            # Right (R): current_row[c+1]. If off edge (c=ROW_WIDTH-1), assume SAFE ('.').
            if c == ROW_WIDTH - 1:
                right_char = SAFE
            else:
                right_char = current_row[c + 1]

            # 2. Convert characters to Boolean for rule check (True=Trap, False=Safe)
            left_is_trap = (left_char == TRAP)
            center_is_trap = (center_char == TRAP)
            right_is_trap = (right_char == TRAP)
            
            # 3. Apply the rule
            is_new_trap = is_trap(left_is_trap, center_is_trap, right_is_trap)
            
            # 4. Store the result
            new_tile = TRAP if is_new_trap else SAFE
            next_row_list.append(new_tile)
            
        # Update state for the next iteration
        current_row = "".join(next_row_list)
        total_safe_tiles += current_row.count(SAFE)

    return total_safe_tiles

def solve_trap_puzzle(filepath):
    """Main function to orchestrate the simulation."""
    
    initial_row = load_initial_row(filepath)
    if initial_row is None:
        return 0
        
    print(f"Starting simulation from initial row (Length: {len(initial_row)})")
    print(f"Simulating a total of {TOTAL_ROWS} rows.")
    
    final_count = simulate_trap_rows(initial_row)
    
    return final_count

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting trap generation analysis using data from: {os.path.abspath(input_file)}\n")
    
    final_score = solve_trap_puzzle(input_file)
    
    print("\n" + "="*50)
    print(f"TOTAL NUMBER OF SAFE TILES IN {TOTAL_ROWS} ROWS:")
    print(f"SCORE: {final_score}")
    print("="*50)