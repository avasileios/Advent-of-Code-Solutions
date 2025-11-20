import os
import math
import hashlib

# --- Constants ---
LIST_SIZE = 256
NUM_ROUNDS = 64
SUFFIX_LENGTHS = [17, 31, 73, 47, 23]

def preprocess_input(input_str: str) -> list[int]:
    """
    Converts the input string to ASCII codes and appends the fixed suffix.
    """
    # 1. Convert characters to ASCII codes (bytes)
    # Ensure any trailing/leading whitespace is removed before conversion
    lengths = [ord(char) for char in input_str.strip()]
    
    # 2. Append the fixed suffix
    lengths.extend(SUFFIX_LENGTHS)
    
    return lengths

def run_knot_tying_round(list_of_marks: list[int], lengths: list[int], current_position: int, skip_size: int) -> tuple[int, int]:
    """
    Performs a single round of the knot tying simulation.
    
    Returns:
        tuple: (new_current_position, new_skip_size)
    """
    N = LIST_SIZE
    
    for length in lengths:
        
        # --- A. Identify the sublist to reverse ---
        sublist_values = []
        for i in range(length):
            index = (current_position + i) % N
            sublist_values.append(list_of_marks[index])
            
        sublist_values.reverse()
        
        # --- B. Replace the reversed sublist back into the main list ---
        for i in range(length):
            index = (current_position + i) % N
            list_of_marks[index] = sublist_values[i]
            
        # --- C. Move the current position ---
        current_position = (current_position + length + skip_size) % N
        
        # --- D. Increase the skip size ---
        skip_size += 1
        
    return current_position, skip_size

def calculate_dense_hash(sparse_hash: list[int]) -> list[int]:
    """
    Reduces the 256-element sparse hash to a 16-element dense hash using bitwise XOR.
    """
    DENSE_HASH_BLOCK_SIZE = 16
    dense_hash = []
    
    # Iterate through the sparse hash in blocks of 16
    for i in range(0, LIST_SIZE, DENSE_HASH_BLOCK_SIZE):
        block = sparse_hash[i : i + DENSE_HASH_BLOCK_SIZE]
        
        # Calculate the XOR sum of the block (0 ^ e1 ^ e2 ^ ...)
        xor_sum = 0
        for element in block:
            xor_sum ^= element
            
        dense_hash.append(xor_sum)
        
    return dense_hash

def to_hex_string(dense_hash: list[int]) -> str:
    """
    Converts the 16-element dense hash into a 32-character hexadecimal string.
    """
    hex_parts = []
    for num in dense_hash:
        # Convert to hex, ensuring two digits (leading zero)
        hex_parts.append(f'{num:02x}')
        
    return "".join(hex_parts)


def solve_full_knot_hash(filepath: str):
    """
    Orchestrates the entire Knot Hash calculation process.
    """
    try:
        input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), filepath)
        with open(input_file, 'r') as f:
            # Read the input string (which may contain commas or just text)
            input_str = f.read().strip()
    except FileNotFoundError:
        print(f"Error: Input file not found at '{filepath}'")
        return ""
        
    # 1. Preprocessing
    lengths = preprocess_input(input_str)
    
    # 2. Sparse Hash Generation (64 Rounds)
    list_of_marks = list(range(LIST_SIZE))
    current_position = 0
    skip_size = 0
    
    print(f"Starting {NUM_ROUNDS} rounds of knot tying...")
    
    for _ in range(NUM_ROUNDS):
        current_position, skip_size = run_knot_tying_round(list_of_marks, lengths, current_position, skip_size)
        
    sparse_hash = list_of_marks
    
    # 3. Dense Hash Calculation
    dense_hash = calculate_dense_hash(sparse_hash)
    
    # 4. Hexadecimal Output
    final_hash = to_hex_string(dense_hash)
    
    return final_hash

# --- Main Execution Block ---
if __name__ == "__main__":
    
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting full Knot Hash analysis using data from: {os.path.abspath(input_file)}\n")
    
    final_hash = solve_full_knot_hash("input.txt")
    
    print("\n" + "="*50)
    print("THE KNOT HASH OF THE PUZZLE INPUT:")
    print(f"SCORE: {final_hash}")
    print("="*50)