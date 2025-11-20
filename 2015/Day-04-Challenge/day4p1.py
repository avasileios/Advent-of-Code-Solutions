import hashlib
import os

# Your secret puzzle input
SECRET_KEY = "iwrupvqb"
TARGET_PREFIX = "00000"

def mine_advent_coin(secret_key: str, target_prefix: str) -> int:
    """
    Finds the lowest positive integer that, when combined with the secret key, 
    results in an MD5 hash starting with the target prefix.
    """
    
    # Start searching from the lowest positive number (1)
    number = 1
    
    # The search space is unknown, so we loop indefinitely until the condition is met.
    while True:
        # 1. Combine the key and the number
        input_string = secret_key + str(number)
        
        # 2. Calculate the MD5 hash
        # hashlib.md5 expects bytes as input, so we encode the string.
        hash_object = hashlib.md5(input_string.encode('utf-8'))
        
        # 3. Get the hexadecimal representation
        hex_hash = hash_object.hexdigest()
        
        # 4. Check the prefix condition
        if hex_hash.startswith(target_prefix):
            return number
        
        # 5. Increment and continue the search
        number += 1

def solve_advent_coin_puzzle():
    """Main function to run the mining simulation."""
    print(f"Secret Key: {SECRET_KEY}")
    print(f"Target Hash Prefix: {TARGET_PREFIX}")
    print("Starting brute-force search...")
    
    # Run the mining function
    lowest_number = mine_advent_coin(SECRET_KEY, TARGET_PREFIX)
    
    return lowest_number

# --- Main Execution Block ---
if __name__ == "__main__":
    
    final_score = solve_advent_coin_puzzle()
    
    print("\n" + "="*50)
    print("LOWEST POSITIVE NUMBER PRODUCING 5 ZEROES:")
    print(f"SCORE: {final_score}")
    print("="*50)