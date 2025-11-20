import os

# --- Constants ---
INITIAL_STATE = "11011110011011101"
DISK_LENGTH = 35651584 # Updated for Part Two

def generate_dragon_data(initial_a: str, target_length: int) -> str:
    """
    Generates the Dragon Curve data string until its length reaches 
    or exceeds the target_length.
    """
    a = initial_a
    
    while len(a) < target_length:
        # 1. Make a copy of "a" (b)
        b = a
        
        # 2. Reverse "b"
        b_rev = b[::-1]
        
        # 3. Inverse "b" (0->1, 1->0)
        # Use str.translate for highly efficient character replacement
        b_inv_rev = b_rev.translate(str.maketrans('01', '10'))
        
        # 4. New data = a + "0" + b_inv_rev
        a = a + "0" + b_inv_rev
        
    # Return the data truncated to the exact disk length
    return a[:target_length]

def calculate_checksum(data: str) -> str:
    """
    Calculates the checksum iteratively until an odd length is achieved.
    """
    current_checksum = data
    
    while len(current_checksum) % 2 == 0:
        
        next_checksum_list = []
        N = len(current_checksum)
        
        # Process in non-overlapping pairs (i, i+1)
        for i in range(0, N, 2):
            char1 = current_checksum[i]
            char2 = current_checksum[i+1]
            
            # If the two characters match (00 or 11), the next checksum char is 1.
            if char1 == char2:
                next_checksum_list.append('1')
            # If the characters do not match (01 or 10), the next checksum char is 0.
            else:
                next_checksum_list.append('0')
                
        current_checksum = "".join(next_checksum_list)
        
    return current_checksum

def solve_dragon_checksum_puzzle():
    """
    Orchestrates the data generation and final checksum calculation.
    """
    print(f"Initial State: {INITIAL_STATE}")
    print(f"Target Disk Length: {DISK_LENGTH}")
    
    # 1. Generate the data string
    data_string = generate_dragon_data(INITIAL_STATE, DISK_LENGTH)
    
    print(f"Generated Data Length: {len(data_string)}")
    
    # 2. Calculate the checksum
    final_checksum = calculate_checksum(data_string)
    
    return final_checksum

# --- Main Execution Block ---
if __name__ == "__main__":
    
    final_score = solve_dragon_checksum_puzzle()
    
    print("\n" + "="*50)
    print("PART TWO: THE CORRECT CHECKSUM FOR DISK LENGTH 35651584:")
    print(f"SCORE: {final_score}")
    print("="*50)