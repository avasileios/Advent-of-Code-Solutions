import os

# Your puzzle input
INITIAL_SEQUENCE = "3113322113"
NUM_ITERATIONS = 50 # Updated from 40 to 50

def look_and_say(sequence: str) -> str:
    """
    Generates the next sequence based on the look-and-say rule.
    """
    if not sequence:
        return ""

    next_sequence = []
    i = 0
    N = len(sequence)

    while i < N:
        current_digit = sequence[i]
        count = 1
        
        # Count the length of the current run
        j = i + 1
        while j < N and sequence[j] == current_digit:
            count += 1
            j += 1
        
        # Append the count and the digit
        next_sequence.append(str(count))
        next_sequence.append(current_digit)
        
        # Move the starting index to the end of the just-counted run
        i = j
        
    return "".join(next_sequence)

def solve_look_and_say():
    """
    Applies the look-and-say process 50 times and returns the length of the result.
    """
    current_sequence = INITIAL_SEQUENCE
    
    print(f"Initial Length: {len(current_sequence)}")
    
    for i in range(1, NUM_ITERATIONS + 1):
        current_sequence = look_and_say(current_sequence)
        
        # Optional check to see growth rate
        if i % 5 == 0 or i == NUM_ITERATIONS:
             print(f"After iteration {i:02}: Length = {len(current_sequence)}")
        
    return len(current_sequence)

# --- Main Execution Block ---
if __name__ == "__main__":
    
    final_length = solve_look_and_say()
    
    print("\n" + "="*50)
    print(f"LENGTH OF THE RESULT AFTER {NUM_ITERATIONS} ITERATIONS:")
    print(f"SCORE: {final_length}")
    print("="*50)