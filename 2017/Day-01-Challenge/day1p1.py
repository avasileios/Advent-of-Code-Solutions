import os

def solve_captcha_puzzle(filepath):
    """
    Calculates the sum of all digits that match the next digit in the circular list.
    """
    try:
        # Robust path reading
        input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), filepath)
        with open(input_file, 'r') as f:
            # Read the digits as a string
            digits_str = f.read().strip()
    except FileNotFoundError:
        print(f"Error: Input file not found at '{filepath}'")
        return 0
    
    if not digits_str:
        return 0
        
    N = len(digits_str)
    captcha_sum = 0
    
    # Iterate through all digits in the list
    for i in range(N):
        current_digit = digits_str[i]
        
        # Calculate the index of the next digit (circularly)
        next_index = (i + 1) % N
        next_digit = digits_str[next_index]
        
        # Check for match
        if current_digit == next_digit:
            # Add the value of the matching digit to the sum
            captcha_sum += int(current_digit)
            
    return captcha_sum

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting captcha simulation using data from: {os.path.abspath(input_file)}\n")
    
    final_sum = solve_captcha_puzzle(input_file)
    
    print("\n" + "="*50)
    print("THE SOLUTION TO YOUR CAPTCHA (Sum of next matching digits):")
    print(f"SCORE: {final_sum}")
    print("="*50)