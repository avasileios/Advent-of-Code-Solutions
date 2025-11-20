import os
from collections import Counter
import re

def generate_checksum(encrypted_name: str) -> str:
    """
    Generates the correct checksum (five most common letters, ties broken alphabetically).
    """
    # 1. Strip dashes to get only the letters
    name_letters = encrypted_name.replace('-', '')
    
    # 2. Count frequencies
    frequencies = Counter(name_letters)
    
    # 3. Apply custom sorting key for tie-breaking
    # The key prioritizes:
    # 1. Count (descending: -count)
    # 2. Letter (ascending: letter)
    
    sorted_items = sorted(
        frequencies.items(),
        key=lambda item: (-item[1], item[0])
    )
    
    # 4. Extract the top 5 letters and join to form the checksum
    checksum = "".join([item[0] for item in sorted_items[:5]])
    
    return checksum

def solve_room_puzzle(filepath):
    """
    Reads the room list, validates each room, and sums the sector IDs of all real rooms.
    """
    sum_of_sector_ids = 0
    
    try:
        # Robust path reading
        input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), filepath)
        with open(input_file, 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"Error: Instructions file not found at '{filepath}'")
        return 0
        
    # Regex to capture: encrypted_name, sector_id, checksum
    # Example: aaaaa-bbb-z-y-x-123[abxyz]
    pattern = re.compile(r'([\w-]+)-(\d+)\[(\w{5})\]')
    
    for line in lines:
        match = pattern.match(line)
        if not match:
            continue
            
        encrypted_name = match.group(1) # aaaaa-bbb-z-y-x
        sector_id = int(match.group(2)) # 123
        given_checksum = match.group(3)  # abxyz
        
        # 1. Generate the expected checksum
        expected_checksum = generate_checksum(encrypted_name)
        
        # 2. Check for validation (Is it a real room?)
        if expected_checksum == given_checksum:
            sum_of_sector_ids += sector_id
            # print(f"[REAL] {encrypted_name} {sector_id} -> Checksum: {expected_checksum}")
        # else:
            # print(f"[DECOY] {encrypted_name} -> Expected: {expected_checksum}, Given: {given_checksum}")
            
    return sum_of_sector_ids

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting room decryption and validation using data from: {os.path.abspath(input_file)}\n")
    
    final_sum = solve_room_puzzle(input_file)
    
    print("\n" + "="*50)
    print("SUM OF THE SECTOR IDS OF ALL REAL ROOMS:")
    print(f"SCORE: {final_sum}")
    print("="*50)