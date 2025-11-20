import os
import re
from itertools import permutations
import math

# Define the user's placeholder identity for Part Two
NEW_GUEST_NAME = "Me"

def parse_happiness_data(filepath):
    """
    Reads the input and builds a dictionary representing happiness changes:
    happiness[Person_A][Person_B] = change in happiness for A when next to B.
    Also collects the set of all unique people.
    
    This function is modified to support Part Two by allowing the injection of 
    a neutral guest.
    """
    happiness = {}
    people = set()
    
    try:
        # Robust path reading
        with open(filepath, 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"Error: Instructions file not found at '{filepath}'")
        return None, None
    
    # Regex to capture the full instruction line
    pattern = re.compile(
        r'(\w+)\s+would\s+(gain|lose)\s+(\d+)\s+happiness units by sitting next to\s+(\w+)\.'
    )
    
    for line in lines:
        match = pattern.match(line)
        if not match:
            continue
            
        person_a, direction, amount_str, person_b = match.groups()
        amount = int(amount_str)
        
        if direction == 'lose':
            amount = -amount
            
        # Add people to the set
        people.add(person_a)
        people.add(person_b)
        
        # Initialize dictionary entry for Person A
        if person_a not in happiness:
            happiness[person_a] = {}
            
        # Store the directed happiness change
        happiness[person_a][person_b] = amount
        
    # --- PART TWO MODIFICATION ---
    
    # 1. Add the new guest to the list of people
    people.add(NEW_GUEST_NAME)
    
    # 2. Add neutral scores (0) for all interactions involving the new guest
    
    # New guest's scores when sitting next to anyone else (outgoing)
    happiness[NEW_GUEST_NAME] = {p: 0 for p in people if p != NEW_GUEST_NAME}
    
    # Everyone else's scores when sitting next to the new guest (incoming)
    for person in people:
        if person != NEW_GUEST_NAME:
            happiness.setdefault(person, {})[NEW_GUEST_NAME] = 0
            
    return happiness, sorted(list(people))

def calculate_arrangement_happiness(arrangement, happiness_data):
    """
    Calculates the total happiness change for a circular arrangement.
    Each person contributes happiness based on BOTH their left and right neighbors.
    """
    N = len(arrangement)
    total_change = 0
    
    # Iterate through each person in the arrangement
    for i in range(N):
        current_person = arrangement[i]
        
        # Determine the left and right neighbors (circular check)
        left_neighbor = arrangement[(i - 1) % N]
        right_neighbor = arrangement[(i + 1) % N]
        
        # Contribution from Left Neighbor
        change_from_left = happiness_data[current_person][left_neighbor]
        total_change += change_from_left
        
        # Contribution from Right Neighbor
        change_from_right = happiness_data[current_person][right_neighbor]
        total_change += change_from_right
        
    return total_change

def solve_optimal_seating_puzzle(filepath):
    """
    Finds the maximum total happiness change for any circular seating arrangement.
    """
    happiness_data, people = parse_happiness_data(filepath)
    
    if not happiness_data or not people:
        print("Error: Could not parse happiness data or find people.")
        return 0
        
    max_happiness = float('-inf')
    
    print(f"Total guests (including {NEW_GUEST_NAME}): {len(people)} ({people})")
    print(f"Total arrangements to check: {math.factorial(len(people))}")
    
    # 1. Generate all possible linear arrangements (permutations)
    all_arrangements = permutations(people)
    
    # 2. Check the happiness for each arrangement
    for arrangement in all_arrangements:
        happiness_change = calculate_arrangement_happiness(arrangement, happiness_data)
        max_happiness = max(max_happiness, happiness_change)
        
    return max_happiness

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting optimal seating analysis (Part Two) using data from: {os.path.abspath(input_file)}\n")
    
    final_score = solve_optimal_seating_puzzle(input_file)
    
    print("\n" + "="*50)
    print("PART TWO: TOTAL CHANGE IN HAPPINESS (Including Me):")
    print(f"SCORE: {final_score}")
    print("="*50)