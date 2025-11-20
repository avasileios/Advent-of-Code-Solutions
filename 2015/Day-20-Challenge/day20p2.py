import os
import math
import sys

# Set a large recursion limit for the sieve simulation
sys.setrecursionlimit(2000)

# Your puzzle input
TARGET_PRESENTS = 34000000

# Estimated upper bound for the house number. 
# CRITICAL FIX: Increasing the limit to ensure the solution is found.
MAX_HOUSES = 1200000 

# --- PART TWO CHANGES ---
PRESENTS_PER_ELF_FACTOR = 11
DELIVERY_LIMIT = 50 # Elves stop after 50 houses

def solve_present_delivery_puzzle():
    """
    Finds the lowest house number that receives at least TARGET_PRESENTS 
    using a Sieve-like algorithm, applying the 50-house limit and 11x factor.
    """
    
    # Initialize array to track the total presents delivered to each house.
    presents = [0] * MAX_HOUSES
    
    # 1. Sieve Simulation: Iterate through every Elf (1 to MAX_HOUSES - 1)
    for elf_num in range(1, MAX_HOUSES):
        
        # Calculate the base presents delivered by this specific elf
        presents_delivered = elf_num * PRESENTS_PER_ELF_FACTOR
        
        # 2. Iterate through every house (H) that the current Elf visits
        # We stop after 50 deliveries. House index is H = elf_num * delivery_count.
        
        # Start at the first house visited by this elf: house_num = elf_num * 1
        house_num = elf_num
        delivery_count = 1
        
        while house_num < MAX_HOUSES and delivery_count <= DELIVERY_LIMIT:
            
            # Add the presents delivered by this elf to the house total
            presents[house_num] += presents_delivered
            
            # Move to the next house visited by this elf
            delivery_count += 1
            house_num = elf_num * delivery_count

    # 3. Search for the lowest house number that meets the target
    for house_num in range(1, MAX_HOUSES):
        if presents[house_num] >= TARGET_PRESENTS:
            return house_num

    # If the required house number exceeds the estimate, raise a warning.
    print(f"Warning: Did not find solution within MAX_HOUSES={MAX_HOUSES}. The solution is likely just above this threshold.")
    return -1

# --- Main Execution Block ---
if __name__ == "__main__":
    
    print(f"Target Presents: {TARGET_PRESENTS}")
    print(f"Presents Factor: {PRESENTS_PER_ELF_FACTOR}x, Delivery Limit: {DELIVERY_LIMIT} houses.")
    print(f"Simulating up to house number {MAX_HOUSES} using Sieve method...")
    
    lowest_house_number = solve_present_delivery_puzzle()
    
    print("\n" + "="*50)
    print("PART TWO: LOWEST HOUSE NUMBER TO GET AT LEAST TARGET PRESENTS:")
    print(f"SCORE: {lowest_house_number}")
    print("="*50)