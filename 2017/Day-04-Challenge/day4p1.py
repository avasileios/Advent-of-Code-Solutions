import os

def is_valid_passphrase(passphrase: str) -> bool:
    """
    Checks if a passphrase contains no duplicate words.
    """
    # 1. Split the passphrase into words
    words = passphrase.split()
    
    # 2. Check uniqueness by comparing list length to set size
    # If len(set(words)) == len(words), all words are unique.
    return len(set(words)) == len(words)

def solve_passphrase_puzzle(filepath):
    """
    Reads the list of passphrases and counts how many are valid.
    """
    valid_count = 0
    
    try:
        # Robust path reading
        input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), filepath)
        with open(input_file, 'r') as f:
            passphrases = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"Error: Passphrase file not found at '{filepath}'")
        return 0
        
    if not passphrases:
        print("No passphrases found in the input file.")
        return 0
        
    for phrase in passphrases:
        if is_valid_passphrase(phrase):
            valid_count += 1
            
    return valid_count

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting passphrase validation using data from: {os.path.abspath(input_file)}\n")
    
    final_count = solve_passphrase_puzzle(input_file)
    
    print("\n" + "="*50)
    print("TOTAL NUMBER OF VALID PASSPHRASES:")
    print(f"SCORE: {final_count}")
    print("="*50)