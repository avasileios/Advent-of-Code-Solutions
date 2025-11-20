import os
import math

# Your puzzle input
NUM_ELVES = 3014603

def find_winning_elf(N: int) -> int:
    """
    Finds the winning Elf in the Josephus-style circle game using the mathematical pattern.
    
    Winner = 2 * (N - 2^k) + 1
    where 2^k is the largest power of two less than or equal to N.
    """
    if N <= 0:
        return 0
        
    # 1. Find k (the exponent)
    # k = floor(log2(N))
    k = N.bit_length() - 1
    
    # 2. Calculate the largest power of two, 2^k
    largest_power_of_two = 1 << k
    
    # 3. Apply the formula
    winner_position = 2 * (N - largest_power_of_two) + 1
    
    return winner_position

def solve_white_elephant_puzzle():
    """Main function to run the calculation."""
    
    print(f"Total number of Elves: {NUM_ELVES}")
    
    winning_elf = find_winning_elf(NUM_ELVES)
    
    return winning_elf

# --- Main Execution Block ---
if __name__ == "__main__":
    
    final_score = solve_white_elephant_puzzle()
    
    print("\n" + "="*50)
    print("THE ELF WHO GETS ALL THE PRESENTS:")
    print(f"SCORE: {final_score}")
    print("="*50)