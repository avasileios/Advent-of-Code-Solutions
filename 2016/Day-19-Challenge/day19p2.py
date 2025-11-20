import os
import math

# Your puzzle input
NUM_ELVES = 3014603

def find_winning_elf_p2(N: int) -> int:
    """
    Finds the winning Elf when stealing from the Elf directly across the circle.
    Uses the three-case modular arithmetic pattern related to powers of three.
    
    The winning position is 1-indexed.
    """
    if N <= 0:
        return 0
        
    # 1. Find the largest power of three (3^k) such that 3^k <= N.
    power_of_three = 1
    while power_of_three * 3 <= N:
        power_of_three *= 3
    
    # power_of_three now holds 3^k.
    
    # 2. Calculate the remainder (r = N - 3^k)
    r = N - power_of_three
    
    # 3. Apply the pattern based on the segment (r vs. 3^k)
    
    # Case 1: 3^k < N <= 2 * 3^k (r is in the range [1, 3^k])
    if r <= power_of_three:
        # Winner position is simply the remainder r
        winner_position = r
    
    # Case 2: N > 2 * 3^k (r is in the range (3^k, 2 * 3^k])
    else:
        # The winner is derived from the excess amount above 2 * 3^k, 
        # multiplied by 2, plus the start of the next range.
        # Simplified formula: 2 * (N - 2 * 3^k)
        winner_position = 2 * (r - power_of_three)
        
    return winner_position
    
def solve_white_elephant_puzzle():
    """Main function to run the calculation."""
    
    print(f"Total number of Elves: {NUM_ELVES}")
    
    # Use the specific logic for this Part 2 puzzle
    winning_elf = find_winning_elf_p2(NUM_ELVES)
    
    return winning_elf

# --- Main Execution Block ---
if __name__ == "__main__":
    
    final_score = solve_white_elephant_puzzle()
    
    print("\n" + "="*50)
    print("PART TWO: THE ELF WHO GETS ALL THE PRESENTS (Stealing Across):")
    print(f"SCORE: {final_score}")
    print("="*50)