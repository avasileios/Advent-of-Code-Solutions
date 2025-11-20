import os
import re

# --- Constants ---
ROWS = 6
COLS = 50
ON = 1
OFF = 0

def initialize_display(rows, cols):
    """Initializes the display grid to all 0s (off)."""
    return [[OFF for _ in range(cols)] for _ in range(rows)]

def solve_display_puzzle(filepath):
    """
    Simulates the display operations. Returns the final display grid state.
    """
    display = initialize_display(ROWS, COLS)
    
    try:
        # Robust path reading
        input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), filepath)
        with open(input_file, 'r') as f:
            instructions = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"Error: Instructions file not found at '{filepath}'")
        return None
        
    # Regex to capture the instructions
    # rect AxB: rect (\d+)x(\d+)
    # rotate row y=A by B: rotate row y=(\d+) by (\d+)
    # rotate column x=A by B: rotate column x=(\d+) by (\d+)
    
    for instruction in instructions:
        parts = instruction.split()
        
        if not parts:
            continue
            
        operation = parts[0]
        
        if operation == 'rect':
            # rect AxB -> parts[1] is AxB
            try:
                A, B = map(int, parts[1].split('x'))
            except ValueError:
                continue

            # Turn on pixels in a rectangle (B tall x A wide)
            for r in range(B):
                for c in range(A):
                    if 0 <= r < ROWS and 0 <= c < COLS:
                        display[r][c] = ON
        
        elif operation == 'rotate':
            op_type = parts[1] # row or column
            
            if op_type == 'row':
                # rotate row y=A by B -> parts[2] is y=A, parts[4] is B
                try:
                    y = int(parts[2].split('=')[1])
                    B = int(parts[4])
                except (ValueError, IndexError):
                    continue

                if 0 <= y < ROWS:
                    # Perform array rotation: row y by B steps right
                    row_array = display[y]
                    shift = B % COLS
                    
                    # Pythonic rotation: [4, 1, 2, 3] = [4] + [1, 2, 3]
                    display[y] = row_array[COLS - shift:] + row_array[:COLS - shift]
                    
            elif op_type == 'column':
                # rotate column x=A by B -> parts[2] is x=A, parts[4] is B
                try:
                    x = int(parts[2].split('=')[1])
                    B = int(parts[4])
                except (ValueError, IndexError):
                    continue
                
                if 0 <= x < COLS:
                    # Extract column into a 1D array
                    col_array = [display[r][x] for r in range(ROWS)]
                    
                    # Perform rotation: column x by B steps DOWN
                    shift = B % ROWS
                    
                    # Pythonic rotation
                    new_col_array = col_array[ROWS - shift:] + col_array[:ROWS - shift]
                    
                    # Write the new column back to the display grid
                    for r in range(ROWS):
                        display[r][x] = new_col_array[r]
        
    return display

def render_display(display):
    """Converts the display grid into a readable string format."""
    output = []
    for r in range(ROWS):
        output.append("".join(['#' if c == ON else '.' for c in display[r]]))
    return "\n".join(output)


# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting display simulation ({ROWS}x{COLS}) for visual output.\n")
    
    final_display = solve_display_puzzle(input_file)
    
    if final_display is not None:
        # Calculate Part 1 score as well (total lit pixels)
        total_lit = sum(sum(row) for row in final_display)
        
        print("-" * 50)
        print(f"Part 1: Total Lit Pixels: {total_lit}")
        print("---")
        
        final_code_output = render_display(final_display)
        
        print("Final Code Display (Read vertically in 5x6 blocks):")
        print("==================================================")
        print(final_code_output)
        print("==================================================")