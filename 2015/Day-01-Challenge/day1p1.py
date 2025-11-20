import os

def solve_floor_puzzle(directions_file):
    """
    Calculates the final floor number by counting the difference between 
    opening '(' and closing ')' parentheses.
    """
    try:
        # Robust path reading
        with open(directions_file, 'r') as f:
            instructions = f.read().strip()
    except FileNotFoundError:
        print(f"Error: Instructions file not found at '{directions_file}'")
        return 0
    
    if not instructions:
        return 0
        
    # Count the two types of movements
    up_moves = instructions.count('(')
    down_moves = instructions.count(')')
    
    final_floor = up_moves - down_moves
    
    return final_floor

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting floor calculation using instructions from: {os.path.abspath(input_file)}\n")
    
    final_floor = solve_floor_puzzle(input_file)
    
    print("\n" + "="*50)
    print("FINAL FLOOR NUMBER:")
    print(f"SCORE: {final_floor}")
    print("="*50)