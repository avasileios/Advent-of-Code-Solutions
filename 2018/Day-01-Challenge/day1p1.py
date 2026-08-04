from pathlib import Path
import sys

def solve_day1_part1(raw_input: str) -> int:
    """
    Calculates the resulting frequency after applying all changes.
    Starting frequency is 0.
    """
    current_frequency = 0
    
    # Split input into lines
    lines = raw_input.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        try:
            # Python's int() automatically handles the explicit "+" sign (e.g., int("+5") -> 5)
            change = int(line)
            current_frequency += change
        except ValueError:
            print(f"Warning: Could not parse line '{line}'. Skipping.")
            
    return current_frequency

def load_input():
    """
    Loads the puzzle input from the input.txt file.
    """
    input_file = Path(__file__).parent / "input.txt"
    try:
        with open(input_file, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: Input file not found at {input_file}")
        return ""

# --- Main Execution ---

if __name__ == "__main__":
    # 1. Example input from the prompt for verification (Expected 3)
    EXAMPLE_RAW_INPUT = """
+1
-2
+3
+1
"""
    
    print("--- Running Example Input for Verification (Expected 3) ---")
    example_result = solve_day1_part1(EXAMPLE_RAW_INPUT)
    print(f"Example Result: {example_result}\n")
    print("----------------------------------------------------------\n")

    # 2. Run with your actual puzzle input from the file
    ACTUAL_RAW_INPUT = load_input()
    
    if ACTUAL_RAW_INPUT:
        print("--- Running Actual Puzzle Input ---")
        actual_result = solve_day1_part1(ACTUAL_RAW_INPUT)
        
        print("\n" + "="*50)
        print("PART ONE: RESULTING FREQUENCY:")
        print(f"FREQUENCY: {actual_result}")
        print("="*50)
    else:
        print("Could not run actual puzzle: Input data is missing.")