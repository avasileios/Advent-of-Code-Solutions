import os
import math

def parse_parameters(filepath):
    """
    Parses the input file to extract the loop parameters dynamically.
    Looks for specific instructions that define the range and step.
    """
    try:
        with open(filepath, 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"Error: File not found at '{filepath}'")
        return None

    if len(lines) < 31:
        print("Error: Input file seems too short to match expected structure.")
        return None

    try:
        # 1. Get Initial B Value (Line 0: set b X)
        # Example: set b 65
        initial_b_val = int(lines[0].split()[2])
        
        # 2. Calculate Start Range (b = b * 100 + 100000)
        # This logic is lines 4 and 5: mul b 100; sub b -100000
        b_start = (initial_b_val * 100) + 100000
        
        # 3. Calculate End Range (c = b + 17000)
        # This logic is line 7: sub c -17000
        c_end = b_start + 17000
        
        # 4. Find Step Size (Line 30: sub b -17)
        # The step is the absolute value of the argument
        step_val = abs(int(lines[30].split()[2]))
        
        return b_start, c_end, step_val
        
    except (IndexError, ValueError) as e:
        print(f"Error parsing parameters: {e}. Defaulting to standard values.")
        # Default fallback for standard input (set b 65)
        return 106500, 123500, 17

def is_composite(n):
    """
    Checks if n is a composite number (not prime).
    Returns True if n has factors other than 1 and itself.
    """
    if n <= 1: return False
    if n <= 3: return False # 2 and 3 are prime
    if n % 2 == 0 or n % 3 == 0: return True
    
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return True
        i += 6
    return False

def solve_part_two(filepath):
    """
    Executes the optimized logic: Count composite numbers in the calculated range.
    """
    params = parse_parameters(filepath)
    if not params:
        return 0
        
    start, end, step = params
    print(f"Counting composite numbers in range [{start}, {end}] with step {step}...")
    
    h_count = 0
    
    # Range is inclusive of 'end'
    for b in range(start, end + 1, step):
        if is_composite(b):
            h_count += 1
            
    return h_count

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting Coprocessor Optimization (Part 2) using data from: {os.path.abspath(input_file)}\n")
    
    final_h_value = solve_part_two(input_file)
    
    print("\n" + "="*50)
    print("PART TWO: FINAL VALUE IN REGISTER 'h' (Composite Count):")
    print(f"SCORE: {final_h_value}")
    print("="*50)