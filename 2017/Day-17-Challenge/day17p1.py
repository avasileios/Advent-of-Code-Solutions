import os
from typing import List

# --- Constants ---
STEPS = 363
TOTAL_INSERTIONS = 2017

def solve_spinlock_puzzle(steps: int):
    """
    Simulates the spinlock process for 2017 insertions to find the value 
    immediately following the last inserted value (2017).
    """
    
    # 1. Initialization
    circular_buffer: List[int] = [0]
    current_position: int = 0
    
    # 2. Simulation Loop: Insert values 1 up to 2017
    for value_to_insert in range(1, TOTAL_INSERTIONS + 1):
        buffer_length = len(circular_buffer)
        
        # 2a. Calculate the index of the position *AFTER* which the insertion should happen.
        # Landed index (index of element before insertion)
        landed_index = (current_position + steps) % buffer_length
        
        # Insertion index: inserts BEFORE this index. If landed on 0, inserts at 1.
        # Since Python insert(i, x) inserts x AT index i, and we insert AFTER landed_index, 
        # the insertion point is landed_index + 1.
        insertion_index = landed_index + 1
        
        # 2b. Insert the new value
        circular_buffer.insert(insertion_index, value_to_insert)
        
        # 2c. Update the current position
        # The new current position is the index of the inserted value.
        current_position = insertion_index

        # Optional: Print to check simulation against example
        # if value_to_insert < 10:
        #     print(f"Value {value_to_insert}: Current Pos {current_position}, Buffer: {circular_buffer}")
            
    # 3. Final Result: Find the index of 2017 and return the value after it.
    
    # The current position is the index of the last inserted value (2017)
    final_index = current_position
    
    # The value after 2017 is at index (final_index + 1) % final_length
    final_length = len(circular_buffer)
    value_after_2017 = circular_buffer[(final_index + 1) % final_length]
    
    return value_after_2017

# --- Main Execution Block ---
if __name__ == "__main__":
    # The puzzle input (STEPS) is hardcoded.
    
    final_value = solve_spinlock_puzzle(STEPS)
    
    print("\n" + "="*50)
    print("THE VALUE AFTER 2017 IN YOUR COMPLETED CIRCULAR BUFFER:")
    print(f"SCORE: {final_value}")
    print("="*50)