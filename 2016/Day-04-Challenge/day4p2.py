import os
from collections import Counter
import re

# --- Constants ---
# Search term often used in these types of puzzles for the final room
SEARCH_TERM = "northpole object storage" 

def generate_checksum(encrypted_name: str) -> str:
    """
    Generates the correct checksum (five most common letters, ties broken alphabetically).
    (Logic preserved from Part 1)
    """
    # 1. Strip dashes to get only the letters
    name_letters = encrypted_name.replace('-', '')
    
    # 2. Count frequencies
    frequencies = Counter(name_letters)
    
    # 3. Apply custom sorting key for tie-breaking
    # The key prioritizes: 1. Count (descending: -count); 2. Letter (ascending: letter)
    sorted_items = sorted(
        frequencies.items(),
        key=lambda item: (-item[1], item[0])
    )
    
    # 4. Extract the top 5 letters and join to form the checksum
    checksum = "".join([item[0] for item in sorted_items[:5]])
    
    return checksum

def decrypt_name(encrypted_name: str, sector_id: int) -> str:
    """
    Decrypts a room name by rotating each letter forward by the sector ID.
    Dashes are converted to spaces.
    """
    decrypted_name = []
    shift = sector_id % 26 # The effective shift wraps around the alphabet (26 letters)
    
    for char in encrypted_name:
        if char == '-':
            decrypted_name.append(' ')
        elif 'a' <= char <= 'z':
            # 1. Get the 0-indexed position (0 for 'a', 25 for 'z')
            base = ord('a')
            old_pos = ord(char) - base
            
            # 2. Apply the shift and wrap (modulo 26)
            new_pos = (old_pos + shift) % 26
            
            # 3. Convert back to character
            new_char = chr(base + new_pos)
            decrypted_name.append(new_char)
        else:
            # Should not happen in valid input
            decrypted_name.append(char)
            
    return "".join(decrypted_name)

def solve_room_puzzle(filepath):
    """
    Reads the room list, validates real rooms, decrypts them, and searches for the target room.
    """
    sum_of_sector_ids_p1 = 0
    target_room_id = None
    
    try:
        # Robust path reading
        input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), filepath)
        with open(input_file, 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"Error: Instructions file not found at '{filepath}'")
        return 0, None
        
    pattern = re.compile(r'([\w-]+)-(\d+)\[(\w{5})\]')
    
    for line in lines:
        match = pattern.match(line)
        if not match:
            continue
            
        encrypted_name = match.group(1)
        sector_id = int(match.group(2))
        given_checksum = match.group(3)
        
        # 1. Validation Check (Part 1 Logic)
        expected_checksum = generate_checksum(encrypted_name)
        
        if expected_checksum == given_checksum:
            sum_of_sector_ids_p1 += sector_id # Keep track of P1 score
            
            # 2. Decryption and Search (Part 2 Logic)
            decrypted_name = decrypt_name(encrypted_name, sector_id)
            
            # Check if the decrypted name contains the expected storage description
            if SEARCH_TERM in decrypted_name:
                target_room_id = sector_id
                # print(f"[FOUND] Room: {decrypted_name}, ID: {sector_id}")
            
    return sum_of_sector_ids_p1, target_room_id

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting room decryption and search (Part 2) using data from: {os.path.abspath(input_file)}\n")
    
    sum_p1, sector_id_p2 = solve_room_puzzle(input_file)
    
    print("\n" + "="*50)
    print("PART 1: SUM OF THE SECTOR IDS OF ALL REAL ROOMS:")
    print(f"SCORE: {sum_p1}")
    print("-" * 50)
    print("PART 2: SECTOR ID OF THE NORTH POLE OBJECTS ROOM:")
    print(f"SCORE: {sector_id_p2}")
    print("="*50)