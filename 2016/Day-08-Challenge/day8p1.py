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
    Simulates the display operations and calculates the total number of lit pixels.
    """
    display = initialize_display(ROWS, COLS)
    
    try:
        # Robust path reading
        input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), filepath)
        with open(input_file, 'r') as f:
            instructions = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"Error: Instructions file not found at '{filepath}'")
        return 0
        
    # Regex to capture the instructions
    # rect AxB: rect (\d+)x(\d+)
    # rotate row y=A by B: rotate row y=(\d+) by (\d+)
    # rotate column x=A by B: rotate column x=(\d+) by (\d+)
    
    # We use separate patterns or check the starting word for robustness.
    
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
                    
                    # Pythonic rotation: row[offset:] + row[:offset]
                    # Since it shifts RIGHT by B, the new row starts at COLS - B % COLS
                    shift = B % COLS
                    
                    # Example: [1, 2, 3, 4] shifted right by 1 -> [4, 1, 2, 3]
                    # [4, 1, 2, 3] = [4] + [1, 2, 3]
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
                    
                    # Example: [1, 2, 3, 4] shifted down by 1 -> [4, 1, 2, 3]
                    # [4, 1, 2, 3] = [4] + [1, 2, 3]
                    new_col_array = col_array[ROWS - shift:] + col_array[:ROWS - shift]
                    
                    # Write the new column back to the display grid
                    for r in range(ROWS):
                        display[r][x] = new_col_array[r]
        
    # 4. Calculate the total number of lit pixels (sum of all 1s)
    total_lit_pixels = sum(sum(row) for row in display)
    
    # print("\nFinal Display State (Partial View):")
    # for r in range(ROWS):
    #     print("".join(['#' if c == 1 else '.' for c in display[r]]))

    return total_lit_pixels

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting display simulation ({ROWS}x{COLS}) using instructions from: {os.path.abspath(input_file)}\n")
    
    final_count = solve_display_puzzle(input_file)
    
    print("\n" + "="*50)
    print("TOTAL NUMBER OF PIXELS THAT SHOULD BE LIT:")
    print(f"SCORE: {final_count}")
    print("="*50)