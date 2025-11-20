import hashlib
import os
from collections import defaultdict
import re

# --- Constants ---
SECRET_SALT = "cuanljph"
KEY_TARGET_COUNT = 64
LOOKUP_RANGE = 1000 # The next 1000 hashes to check for quintuplets
STRETCH_COUNT = 2016 # NEW: Total extra hashings (2016)

# Cache for computed MD5 hashes: {index: hex_hash_string}
# NOTE: The cache now stores the *stretched* hash.
HASH_CACHE = {} 
# Cache for the first triplet character: {index: char | None}
TRIPLET_CACHE = {}
# Cache for quintuplet characters: {index: set_of_chars_with_quintuplet}
QUINTUPLET_CACHE = defaultdict(set)


def get_stretched_hash(index: int, salt: str) -> str:
    """
    Computes or retrieves the MD5 hash for a given index, applying 2016 extra MD5 calls.
    """
    if index in HASH_CACHE:
        return HASH_CACHE[index]
        
    # Start with the initial hash (MD5 of salt + index)
    hash_input = (salt + str(index)).encode('utf-8')
    hex_hash = hashlib.md5(hash_input).hexdigest()
    
    # Apply 2016 additional hashings (key stretching)
    for _ in range(STRETCH_COUNT):
        # The input for the next hash is the hex string of the previous hash
        hex_hash = hashlib.md5(hex_hash.encode('utf-8')).hexdigest()
    
    HASH_CACHE[index] = hex_hash
    return hex_hash

def find_first_triplet_char(hex_hash: str) -> str | None:
    """
    Finds the character of the first triplet (XXX) in a hash.
    """
    for i in range(len(hex_hash) - 2):
        if hex_hash[i] == hex_hash[i+1] == hex_hash[i+2]:
            return hex_hash[i]
    return None

def check_for_quintuplets(index: int, hex_hash: str):
    """
    Scans the hash for all quintuplets (CCCCC) and caches the results.
    """
    if index in QUINTUPLET_CACHE:
        return # Already processed

    # Regex to find any character repeated 5 times
    pattern = r'([0-9a-f])\1{4}' 
    
    for match in re.finditer(pattern, hex_hash):
        char = match.group(1)
        QUINTUPLET_CACHE[index].add(char)


def get_triplet_char(index: int, salt: str) -> str | None:
    """
    Retrieves or computes the first triplet character for a given index.
    """
    if index in TRIPLET_CACHE:
        return TRIPLET_CACHE[index]
    
    hex_hash = get_stretched_hash(index, salt)
    char = find_first_triplet_char(hex_hash)
    
    TRIPLET_CACHE[index] = char
    return char


def solve_one_time_pad():
    """
    Iteratively searches for the index that generates the 64th key.
    """
    key_count = 0
    index = 0
    
    print(f"Targeting {KEY_TARGET_COUNT} keys using salt '{SECRET_SALT}' with {STRETCH_COUNT} stretching steps.")
    
    while key_count < KEY_TARGET_COUNT:
        
        # 1. Check for Triplet (Key Condition 1)
        triplet_char = get_triplet_char(index, SECRET_SALT)
        
        if triplet_char is not None:
            
            # 2. Check Quintuplet Range (Key Condition 2)
            is_key = False
            
            # Pre-calculate/check quintuplets for the full range required by this index
            for j in range(index + 1, index + LOOKUP_RANGE + 1):
                # Ensure hash j is calculated and quintuplets are cached
                hex_hash_j = get_stretched_hash(j, SECRET_SALT)
                check_for_quintuplets(j, hex_hash_j)
                
            # Now, check the cache for the required quintuplet character
            for j in range(index + 1, index + LOOKUP_RANGE + 1):
                if triplet_char in QUINTUPLET_CACHE[j]:
                    # Found the matching quintuplet! This index N is a key.
                    is_key = True
                    break
            
            if is_key:
                key_count += 1
                print(f"[KEY {key_count:02}] Index: {index} (Char: {triplet_char}). Hash: {get_stretched_hash(index, SECRET_SALT)}")
                
        index += 1
        
    # The loop terminates when the key count reaches 64. 
    # We return index - 1 (since index was incremented after finding the last key).
    return index - 1

# --- Main Execution Block ---
if __name__ == "__main__":
    
    final_index = solve_one_time_pad()
    
    print("\n" + "="*50)
    print(f"INDEX THAT PRODUCES THE {KEY_TARGET_COUNT}TH ONE-TIME PAD KEY (STRETCHED):")
    print(f"SCORE: {final_index}")
    print("="*50)