import os
import re
from typing import List, Dict, Tuple, Any

# Initial pattern (3x3)
INITIAL_PATTERN = ".#./..#/###"
NUM_ITERATIONS = 5

def parse_rules(filepath) -> Dict[str, str]:
    """
    Reads enhancement rules and stores them in a dict: {input_pattern: output_pattern}.
    """
    rules = {}
    
    try:
        input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), filepath)
        with open(input_file, 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"Error: Rules file not found at '{filepath}'")
        return {}
        
    for line in lines:
        try:
            input_pattern, output_pattern = line.split(' => ')
            rules[input_pattern.strip()] = output_pattern.strip()
        except ValueError:
            continue
            
    return rules

def rotate_and_flip(pattern: List[str]) -> List[List[str]]:
    """
    Generates all 8 possible rotations and flips (transformations) of a square pattern.
    
    Args:
        pattern (List[str]): Input pattern (e.g., ['.#.', '..#', '###']).
        
    Returns:
        List[List[str]]: A list of 8 unique transformed patterns (each pattern is a list of strings).
    """
    size = len(pattern)
    grid = [list(row) for row in pattern]
    
    def to_tuple(g):
        return tuple("".join(row) for row in g)

    transformed = set()
    current_grid = grid
    
    # R0, R90, R180, R270
    for _ in range(4):
        # Add current grid (0, 90, 180, 270 degree rotation)
        transformed.add(to_tuple(current_grid))
        
        # Add flip (horizontal)
        flipped_grid = [row[::-1] for row in current_grid]
        transformed.add(to_tuple(flipped_grid))
        
        # Rotate 90 degrees clockwise for the next iteration
        next_grid = [['' for _ in range(size)] for _ in range(size)]
        for r in range(size):
            for c in range(size):
                next_grid[c][size - 1 - r] = current_grid[r][c]
        current_grid = next_grid
        
    return [list("".join(t) for t in p) for p in transformed]


def build_lookup_cache(raw_rules: Dict[str, str]) -> Dict[str, str]:
    """
    Creates a comprehensive lookup table mapping ALL 8 transformed input patterns 
    to their single output pattern.
    """
    lookup_cache = {}
    
    for input_str, output_str in raw_rules.items():
        # Convert pattern string ('#./..') to list of strings (['#.', '..'])
        input_pattern = input_str.split('/')
        
        # Generate all 8 rotations/flips
        all_transforms = rotate_and_flip(input_pattern)
        
        # Map all transformed strings back to the same output
        for transformed_pattern in all_transforms:
            # Recreate the pattern string for the lookup key
            key = "/".join(transformed_pattern)
            lookup_cache[key] = output_str
            
    return lookup_cache

def enhance_grid(current_grid: List[str], lookup_cache: Dict[str, str]) -> List[str]:
    """
    Performs one step of image enhancement.
    """
    size = len(current_grid)
    
    # Determine block size S (2x2 or 3x3)
    if size % 2 == 0:
        block_size = 2
    elif size % 3 == 0:
        block_size = 3
    else:
        raise ValueError("Grid size not divisible by 2 or 3.")
        
    # New block size is S+1
    new_block_size = block_size + 1
    num_blocks_per_dim = size // block_size
    new_grid_size = num_blocks_per_dim * new_block_size
    
    # Initialize new grid structure (list of rows)
    new_grid = [[] for _ in range(new_grid_size)]
    
    # Iterate through blocks (by row index R and column index C of the blocks)
    for block_r in range(num_blocks_per_dim):
        for block_c in range(num_blocks_per_dim):
            
            # 1. Extract the S x S input block
            input_block = []
            for r in range(block_size):
                start_r = block_r * block_size + r
                start_c = block_c * block_size
                
                # Extract the row segment
                input_block.append(current_grid[start_r][start_c : start_c + block_size])
            
            # 2. Convert to lookup key
            lookup_key = "/".join(input_block)
            
            # 3. Find the enhanced output block (new_block_size x new_block_size)
            output_str = lookup_cache.get(lookup_key)
            if output_str is None:
                raise KeyError(f"No rule found for pattern: {lookup_key}")
                
            output_block = output_str.split('/')
            
            # 4. Reassemble the grid: insert the new block into the new grid rows
            for r in range(new_block_size):
                new_row_index = block_r * new_block_size + r
                
                # Append the new block's row segment to the corresponding new grid row
                new_grid[new_row_index].extend(list(output_block[r]))
                
    # 5. Join characters back into strings
    final_grid = ["".join(row) for row in new_grid]
    
    return final_grid

def count_lit_pixels(grid: List[str]) -> int:
    """Counts the total number of '#' pixels in the grid."""
    return sum(row.count('#') for row in grid)

def solve_image_puzzle(filepath):
    """
    Orchestrates the simulation for 5 iterations.
    """
    # 1. Build the lookup cache (including all rotations/flips)
    raw_rules = parse_rules(filepath)
    if not raw_rules:
        return 0
    
    lookup_cache = build_lookup_cache(raw_rules)
    
    # 2. Initialization
    current_grid = INITIAL_PATTERN.split('/')
    
    print(f"Initial size: {len(current_grid)}x{len(current_grid)}")
    print(f"Initial lit pixels: {count_lit_pixels(current_grid)}")
    
    # 3. Simulation Loop
    for iteration in range(1, NUM_ITERATIONS + 1):
        current_grid = enhance_grid(current_grid, lookup_cache)
        
        # print(f"Iteration {iteration}: Size {len(current_grid)}x{len(current_grid)}, Lit: {count_lit_pixels(current_grid)}")
        
    final_lit_count = count_lit_pixels(current_grid)
    
    return final_lit_count

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting image enhancement simulation for {NUM_ITERATIONS} iterations using data from: {os.path.abspath(input_file)}\n")
    
    final_score = solve_image_puzzle(input_file)
    
    print("\n" + "="*50)
    print(f"TOTAL PIXELS ON AFTER {NUM_ITERATIONS} ITERATIONS:")
    print(f"SCORE: {final_score}")
    print("="*50)