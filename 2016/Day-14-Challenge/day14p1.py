import hashlib
import os
from collections import defaultdict
import re

# --- Constants ---
SECRET_SALT = "cuanljph"
KEY_TARGET_COUNT = 64
LOOKUP_RANGE = 1000 # The next 1000 hashes to check for quintuplets

# Cache for computed MD5 hashes: {index: hex_hash_string}
HASH_CACHE = {}
# Cache for the first triplet character: {index: char | None}
TRIPLET_CACHE = {}
# Cache for quintuplet characters: {index: set_of_chars_with_quintuplet}
QUINTUPLET_CACHE = defaultdict(set)


def get_hash(index: int, salt: str) -> str:
    """
    Computes or retrieves the MD5 hash for a given index.
    """
    if index in HASH_CACHE:
        return HASH_CACHE[index]
        
    input_string = salt + str(index)
    hex_hash = hashlib.md5(input_string.encode('utf-8')).hexdigest()
    
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
    
    hex_hash = get_hash(index, salt)
    char = find_first_triplet_char(hex_hash)
    
    TRIPLET_CACHE[index] = char
    return char


def solve_one_time_pad():
    """
    Iteratively searches for the index that generates the 64th key.
    """
    key_count = 0
    index = 0
    
    print(f"Targeting {KEY_TARGET_COUNT} keys using salt '{SECRET_SALT}'.")
    
    while key_count < KEY_TARGET_COUNT:
        
        # 1. Check for Triplet (Key Condition 1)
        triplet_char = get_triplet_char(index, SECRET_SALT)
        
        if triplet_char is not None:
            
            # 2. Check Quintuplet Range (Key Condition 2)
            is_key = False
            
            # The range is [index + 1, index + 1000]
            for j in range(index + 1, index + LOOKUP_RANGE + 1):
                
                # Ensure hash j is calculated and quintuplets are cached
                hex_hash_j = get_hash(j, SECRET_SALT)
                check_for_quintuplets(j, hex_hash_j) # Caches the quintuplet chars
                
                if triplet_char in QUINTUPLET_CACHE[j]:
                    # Found the matching quintuplet! This index N is a key.
                    is_key = True
                    break
            
            if is_key:
                key_count += 1
                print(f"[KEY {key_count:02}] Index: {index} (Char: {triplet_char}). Hash: {get_hash(index, SECRET_SALT)}")
                
        # Optimization: We check future indexes (j) on demand, so we don't 
        # need to pre-cache hashes far in advance. We just continue incrementing N.
        index += 1
        
    # The loop terminates when the key count reaches 64, but the index reported 
    # should be the *last* index that produced a key, not the index that caused 
    # the loop to terminate (which is index + 1). We return index - 1.
    return index - 1

# --- Main Execution Block ---
if __name__ == "__main__":
    
    final_index = solve_one_time_pad()
    
    print("\n" + "="*50)
    print(f"INDEX THAT PRODUCES THE {KEY_TARGET_COUNT}TH ONE-TIME PAD KEY:")
    print(f"SCORE: {final_index}")
    print("="*50)