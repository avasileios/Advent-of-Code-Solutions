import os
import math
import sys

# Set a large recursion limit for the sieve simulation
sys.setrecursionlimit(2000)

# Your puzzle input
TARGET_PRESENTS = 34000000

# Estimated upper bound for the house number. 
# Since the sum of divisors is roughly H*1.5 to H*3, H is roughly 
# TARGET / 30 to TARGET / 10. (3.4M / 10 = 340,000).
# We use a safety margin to 800,000.
MAX_HOUSES = 800000 

PRESENTS_PER_ELF = 10

def solve_present_delivery_puzzle():
    """
    Finds the lowest house number that receives at least TARGET_PRESENTS 
    using a Sieve-like algorithm.
    """
    
    # Initialize array to track the total presents delivered to each house.
    # Array indices represent house numbers (1 to MAX_HOUSES). Index 0 is ignored.
    presents = [0] * MAX_HOUSES
    
    # 1. Sieve Simulation: Iterate through every Elf (1 to MAX_HOUSES - 1)
    for elf_num in range(1, MAX_HOUSES):
        
        presents_delivered = elf_num * PRESENTS_PER_ELF
        
        # 2. Iterate through every house (H) that the current Elf visits
        # H starts at the elf_num and increases by steps of elf_num (i.e., multiples)
        for house_num in range(elf_num, MAX_HOUSES, elf_num):
            
            # Add the presents delivered by this elf to the house total
            presents[house_num] += presents_delivered

    # 3. Search for the lowest house number that meets the target
    for house_num in range(1, MAX_HOUSES):
        if presents[house_num] >= TARGET_PRESENTS:
            return house_num

    # If the required house number exceeds the estimate, raise a warning.
    print(f"Warning: Did not find solution within MAX_HOUSES={MAX_HOUSES}. Increase the limit.")
    return -1

# --- Main Execution Block ---
if __name__ == "__main__":
    
    print(f"Target Presents: {TARGET_PRESENTS}")
    print(f"Simulating up to house number {MAX_HOUSES} using Sieve method...")
    
    lowest_house_number = solve_present_delivery_puzzle()
    
    print("\n" + "="*50)
    print("LOWEST HOUSE NUMBER TO GET AT LEAST TARGET PRESENTS:")
    print(f"SCORE: {lowest_house_number}")
    print("="*50)