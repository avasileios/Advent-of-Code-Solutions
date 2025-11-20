import os
import hashlib
import math
import sys
from collections import deque # Added for Flood Fill (BFS)

# --- Constants ---
LIST_SIZE = 256
NUM_ROUNDS = 64
SUFFIX_LENGTHS = [17, 31, 73, 47, 23]
GRID_DIM = 128
USED = 1

# Your puzzle input
PUZZLE_KEY = "hfdlxzhv"

# Directions for adjacency check (Up, Down, Left, Right)
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)] 

# --- Knot Hash Functions (Retained) ---

def run_knot_tying_round(list_of_marks: list[int], lengths: list[int], current_position: int, skip_size: int) -> tuple[int, int]:
    """Performs a single round of the knot tying simulation."""
    N = LIST_SIZE
    
    for length in lengths:
        sublist_values = []
        for i in range(length):
            index = (current_position + i) % N
            sublist_values.append(list_of_marks[index])
            
        sublist_values.reverse()
        
        for i in range(length):
            index = (current_position + i) % N
            list_of_marks[index] = sublist_values[i]
            
        current_position = (current_position + length + skip_size) % N
        skip_size += 1
        
    return current_position, skip_size

def calculate_dense_hash(sparse_hash: list[int]) -> list[int]:
    """Reduces the 256-element sparse hash to a 16-element dense hash using bitwise XOR."""
    DENSE_HASH_BLOCK_SIZE = 16
    dense_hash = []
    
    for i in range(0, LIST_SIZE, DENSE_HASH_BLOCK_SIZE):
        block = sparse_hash[i : i + DENSE_HASH_BLOCK_SIZE]
        xor_sum = 0
        for element in block:
            xor_sum ^= element
            
        dense_hash.append(xor_sum)
        
    return dense_hash

def get_knot_hash(input_str: str) -> str:
    """Computes the final 32-character hexadecimal Knot Hash."""
    lengths = [ord(char) for char in input_str.strip()]
    lengths.extend(SUFFIX_LENGTHS)
    
    list_of_marks = list(range(LIST_SIZE))
    current_position = 0
    skip_size = 0
    
    for _ in range(NUM_ROUNDS):
        current_position, skip_size = run_knot_tying_round(list_of_marks, lengths, current_position, skip_size)
        
    dense_hash = calculate_dense_hash(list_of_marks)
    
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

# --- NEW: Region Counting Logic ---

def build_grid():
    """
    Generates the 128x128 grid from the Knot Hashes.
    
    Returns:
        list[list[int]]: The binary grid (1=used, 0=free).
    """
    grid = []
    for row_num in range(GRID_DIM):
        hash_input_string = f"{PUZZLE_KEY}-{row_num}"
        hex_hash = get_knot_hash(hash_input_string)
        binary_row = hex_to_binary(hex_hash)
        
        # Convert binary string row to list of integers
        grid.append([int(b) for b in binary_row])
        
    return grid

def flood_fill(grid, r, c, visited):
    """
    Performs BFS/Flood Fill to find all adjacent used squares belonging to 
    the current region, marking them as visited.
    """
    queue = deque([(r, c)])
    visited.add((r, c))
    
    while queue:
        cr, cc = queue.popleft()
        
        # Check 4 adjacent neighbors
        for dr, dc in DIRECTIONS:
            nr, nc = cr + dr, cc + dc
            next_pos = (nr, nc)
            
            if 0 <= nr < GRID_DIM and 0 <= nc < GRID_DIM:
                # Check if cell is used ('1') AND unvisited
                if grid[nr][nc] == USED and next_pos not in visited:
                    visited.add(next_pos)
                    queue.append(next_pos)
                    
def solve_defragmenter_puzzle():
    """
    Calculates the total number of used squares (P1) and the number of regions (P2).
    """
    # 1. Generate the grid (128x128)
    binary_grid = build_grid()
    
    total_used_squares = sum(sum(row) for row in binary_grid)
    
    # 2. Find total regions (Connected Components)
    region_count = 0
    visited = set()
    
    for r in range(GRID_DIM):
        for c in range(GRID_DIM):
            
            # Found the start of a new region?
            if binary_grid[r][c] == USED and (r, c) not in visited:
                region_count += 1
                # Flood fill to mark all connected used squares
                flood_fill(binary_grid, r, c, visited)
                
    return total_used_squares, region_count

# --- Main Execution Block ---
if __name__ == "__main__":
    
    print(f"Starting defragmentation analysis for key: {PUZZLE_KEY} ({GRID_DIM}x{GRID_DIM} grid)\n")
    
    count_p1, count_p2 = solve_defragmenter_puzzle()
    
    print("\n" + "="*50)
    print("PART 1: TOTAL NUMBER OF USED SQUARES:")
    print(f"SCORE: {count_p1}")
    print("-" * 50)
    print("PART 2: TOTAL NUMBER OF REGIONS:")
    print(f"SCORE: {count_p2}")
    print("="*50)