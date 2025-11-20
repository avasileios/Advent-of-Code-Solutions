import os
from typing import List

# --- Constants ---
STEPS = 363
TOTAL_VALUES = 50000000 # 50 million insertions + initial 0
TOTAL_INSERTIONS = TOTAL_VALUES - 1

def solve_spinlock_puzzle_p2(steps: int):
    """
    Simulates the spinlock process for 50 million insertions without building 
    the list, tracking only the value at index 1.
    """
    
    # 1. Initialization
    current_position: int = 0
    # The value after 0 starts at 0 (meaning the buffer is [0])
    value_after_zero: int = 0 
    
    # Simulation Loop: Insert values 1 up to 50,000,000
    for value_to_insert in range(1, TOTAL_VALUES):
        buffer_length = value_to_insert # Length increases by 1 each step (starts at 1)
        
        # 2a. Calculate insertion position (index where the value lands)
        # Landed index (index of element before insertion) is (CP + STEPS) % L
        landed_index = (current_position + steps) % buffer_length
        
        # Insertion index: inserts AT index (landed_index + 1)
        insertion_index = landed_index + 1
        
        # 2b. Check if the insertion happens immediately after index 0
        if insertion_index == 1:
            # If the new value is inserted at index 1, it becomes the value after 0
            value_after_zero = value_to_insert
            
        # 2c. Update the current position
        # The new current position is the index of the inserted value.
        current_position = insertion_index

        # Optional progress indicator
        if value_to_insert % 1000000 == 0:
            print(f"Processed {value_to_insert // 1000000}M insertions. Current value after 0: {value_after_zero}")
            
    return value_after_zero

# --- Main Execution Block ---
if __name__ == "__main__":
    # The puzzle input (STEPS) is hardcoded.
    
    final_value = solve_spinlock_puzzle_p2(STEPS)
    
    print("\n" + "="*50)
    print(f"PART TWO: THE VALUE AFTER 0 WHEN {TOTAL_VALUES} ELEMENTS ARE INSERTED:")
    print(f"SCORE: {final_value}")
    print("="*50)