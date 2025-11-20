import os
import hashlib
import math
import sys
from collections import defaultdict

# --- Constants ---
LIST_SIZE = 256
NUM_ROUNDS = 64
SUFFIX_LENGTHS = [17, 31, 73, 47, 23]

# Your puzzle input
PUZZLE_KEY = "hfdlxzhv"

def run_knot_tying_round(list_of_marks: list[int], lengths: list[int], current_position: int, skip_size: int) -> tuple[int, int]:
    """
    Performs a single round of the knot tying simulation.
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
        
        xor_sum = 0
        for element in block:
            xor_sum ^= element
            
        dense_hash.append(xor_sum)
        
    return dense_hash

def get_knot_hash(input_str: str) -> str:
    """
    Computes the final 32-character hexadecimal Knot Hash.
    """
    # 1. Preprocessing (ASCII + Suffix)
    lengths = [ord(char) for char in input_str.strip()]
    lengths.extend(SUFFIX_LENGTHS)
    
    # 2. Sparse Hash Generation (64 Rounds)
    list_of_marks = list(range(LIST_SIZE))
    current_position = 0
    skip_size = 0
    
    for _ in range(NUM_ROUNDS):
        current_position, skip_size = run_knot_tying_round(list_of_marks, lengths, current_position, skip_size)
        
    # 3. Dense Hash Calculation
    dense_hash = calculate_dense_hash(list_of_marks)
    
    # 4. Hexadecimal Output
    hex_parts = []
    for num in dense_hash:
        hex_parts.append(f'{num:02x}')
        
    return "".join(hex_parts)

def hex_to_binary(hex_hash: str) -> str:
    """
    Converts the 32-char hex hash into a 128-bit binary string.
    """
    binary_string = ""
    for char in hex_hash:
        # Convert hex digit to 4-bit binary, zero-padded
        binary_string += bin(int(char, 16))[2:].zfill(4)
    return binary_string

def solve_defragmenter_puzzle():
    """
    Calculates the Knot Hash for 128 rows and counts the total number of 'used' squares.
    """
    total_used_squares = 0
    
    print(f"Starting defragmentation analysis for key: {PUZZLE_KEY}")
    print(f"Calculating 128 Knot Hashes (Rows 0 to 127).")

    # Iterate through all 128 rows
    for row_num in range(128):
        
        # 1. Generate the hash input string (key-row_num)
        hash_input_string = f"{PUZZLE_KEY}-{row_num}"
        
        # 2. Compute the full 32-char hex Knot Hash
        hex_hash = get_knot_hash(hash_input_string)
        
        # 3. Convert the hash to a 128-bit binary string
        binary_row = hex_to_binary(hex_hash)
        
        # 4. Count the set bits ('1's) for this row (used squares)
        used_in_row = binary_row.count('1')
        total_used_squares += used_in_row
        
    return total_used_squares

# --- Main Execution Block ---
if __name__ == "__main__":
    
    final_count = solve_defragmenter_puzzle()
    
    print("\n" + "="*50)
    print("TOTAL NUMBER OF USED SQUARES ACROSS THE 128X128 GRID:")
    print(f"SCORE: {final_count}")
    print("="*50)