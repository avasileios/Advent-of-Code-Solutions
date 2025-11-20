import os

# --- Configuration: REPLACE THESE WITH YOUR TARGET COORDINATES ---
# Target coordinates for the final code
TARGET_ROW = 2978
TARGET_COL = 3083
# ----------------------------------------------------------------

# --- Generation Constants ---
START_CODE = 20151125
MULTIPLIER = 252533
DIVISOR = 33554393

def coordinate_to_index(R: int, C: int) -> int:
    """
    Calculates the sequence index (k) of the code at the given 1-indexed (R, C) position.
    The formula uses the sum of preceding full diagonals plus the offset within the current diagonal.
    """
    # Total cells in previous full diagonals (D-1 diagonals)
    # where D = R + C - 1
    D_prev_sum = (R + C - 2) * (R + C - 1) // 2
    
    # Add the offset within the current diagonal, which is the column index C
    k = D_prev_sum + C
    
    return k

def generate_code(index: int) -> int:
    """
    Generates the code at the given sequence index k using the iterative formula.
    """
    current_code = START_CODE
    
    # We need to run the formula k - 1 times.
    num_iterations = index - 1
    
    if num_iterations <= 0:
        return START_CODE
        
    for _ in range(num_iterations):
        current_code = (current_code * MULTIPLIER) % DIVISOR
        
    return current_code

def solve_weather_machine_puzzle():
    """
    Orchestrates the coordinate to index mapping and code generation.
    """
    
    if TARGET_ROW <= 0 or TARGET_COL <= 0:
        print("ERROR: Target Row and Column must be positive integers.")
        return 0
        
    # 1. Map Coordinates to Sequence Index (k)
    sequence_index = coordinate_to_index(TARGET_ROW, TARGET_COL)
    print(f"Target: Row {TARGET_ROW}, Column {TARGET_COL} is the {sequence_index}-th code in the sequence.")
    
    # 2. Generate Code at Index k
    final_code = generate_code(sequence_index)
    
    return final_code

# --- Main Execution Block ---
if __name__ == "__main__":
    
    final_code = solve_weather_machine_puzzle()
    
    print("\n" + "="*50)
    print("CODE TO GIVE THE MACHINE (Row {}, Col {}):".format(TARGET_ROW, TARGET_COL))
    print(f"SCORE: {final_code}")
    print("="*50)