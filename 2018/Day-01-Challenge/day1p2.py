from pathlib import Path
import sys
import itertools

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

def solve_day1_part2(raw_input: str) -> int:
    """
    Finds the first frequency that is reached twice.
    The list of changes repeats indefinitely.
    """
    changes = []
    # Parse input first
    for line in raw_input.strip().split('\n'):
        line = line.strip()
        if not line:
            continue
        try:
            changes.append(int(line))
        except ValueError:
            continue
            
    if not changes:
        return 0
        
    current_frequency = 0
    seen_frequencies = {0}
    
    # Cycle through the changes indefinitely
    print(f"Searching for duplicate frequency with {len(changes)} changes in the loop...")
    
    # itertools.cycle repeats the list [a, b, c] -> a, b, c, a, b, c, ...
    for i, change in enumerate(itertools.cycle(changes)):
        current_frequency += change
        
        if current_frequency in seen_frequencies:
            print(f"Duplicate found after {i+1} steps.")
            return current_frequency
        
        seen_frequencies.add(current_frequency)
        
    return 0 # Should not be reached given the problem statement

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
    # 1. Example input from the prompt for verification (Expected 3 for P1, 2 for P2)
    EXAMPLE_RAW_INPUT = """
+1
-2
+3
+1
"""
    
    print("--- Running Example Input for Verification ---")
    example_result_p1 = solve_day1_part1(EXAMPLE_RAW_INPUT)
    print(f"Part 1 Example (Expected 3): {example_result_p1}")
    
    example_result_p2 = solve_day1_part2(EXAMPLE_RAW_INPUT)
    print(f"Part 2 Example (Expected 2): {example_result_p2}")
    print("----------------------------------------------------------\n")

    # 2. Run with your actual puzzle input from the file
    ACTUAL_RAW_INPUT = load_input()
    
    if ACTUAL_RAW_INPUT:
        print("--- Running Actual Puzzle Input ---")
        
        actual_result_p1 = solve_day1_part1(ACTUAL_RAW_INPUT)
        print(f"PART ONE: RESULTING FREQUENCY: {actual_result_p1}")
        
        print("-" * 30)
        
        actual_result_p2 = solve_day1_part2(ACTUAL_RAW_INPUT)
        print(f"PART TWO: FIRST FREQUENCY REACHED TWICE: {actual_result_p2}")
        print("="*50)
    else:
        print("Could not run actual puzzle: Input data is missing.")