import os

def is_valid_passphrase(passphrase: str, check_anagrams: bool) -> bool:
    """
    Checks if a passphrase contains no duplicate words (Part 1) or no anagrams (Part 2).
    """
    # 1. Split the passphrase into words
    words = passphrase.split()
    
    if check_anagrams:
        # Part 2: Check for anagrams
        
        # Create a canonical representation (fingerprint) for each word 
        # by sorting its letters.
        canonical_words = []
        for word in words:
            # Sort the letters and join them back into a string (e.g., "ecdab" -> "abcde")
            canonical_words.append("".join(sorted(word)))
        
        # Check uniqueness of the canonical forms
        return len(set(canonical_words)) == len(words)
        
    else:
        # Part 1: Check for exact duplicate words
        return len(set(words)) == len(words)

def solve_passphrase_puzzle(filepath):
    """
    Reads the list of passphrases and counts how many are valid for Part 1 
    and Part 2.
    """
    valid_count_p1 = 0
    valid_count_p2 = 0
    
    try:
        # Robust path reading
        input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), filepath)
        with open(input_file, 'r') as f:
            passphrases = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"Error: Passphrase file not found at '{filepath}'")
        return 0, 0
        
    if not passphrases:
        print("No passphrases found in the input file.")
        return 0, 0
        
    for phrase in passphrases:
        # Check Part 1 rule (no duplicate words)
        if is_valid_passphrase(phrase, check_anagrams=False):
            valid_count_p1 += 1
            
        # Check Part 2 rule (no anagrams)
        if is_valid_passphrase(phrase, check_anagrams=True):
            valid_count_p2 += 1
            
    return valid_count_p1, valid_count_p2

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting passphrase validation (Part 2 - Anagrams) using data from: {os.path.abspath(input_file)}\n")
    
    count_p1, count_p2 = solve_passphrase_puzzle(input_file)
    
    print("\n" + "="*50)
    print("PART 1: TOTAL NUMBER OF VALID PASSPHRASES (No Duplicate Words):")
    print(f"SCORE: {count_p1}")
    print("-" * 50)
    print("PART 2: TOTAL NUMBER OF VALID PASSPHRASES (No Anagrams):")
    print(f"SCORE: {count_p2}")
    print("="*50)