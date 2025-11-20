import hashlib
import os

# Your puzzle input
SECRET_KEY = "ffykfhsq"
TARGET_PREFIX = "00000"
PASSWORD_LENGTH = 8

def generate_password(secret_key: str, target_length: int) -> str:
    """
    Brute-forces indices starting at 0 to generate the 8-character password.
    """
    password = ""
    index = 0
    
    print("Starting password generation...")
    
    while len(password) < target_length:
        input_string = secret_key + str(index)
        
        # 1. Calculate MD5 hash
        hash_object = hashlib.md5(input_string.encode('utf-8'))
        hex_hash = hash_object.hexdigest()
        
        if hex_hash.startswith(TARGET_PREFIX):
            # 2. Found a matching hash! Extract the sixth character (index 5)
            next_char = hex_hash[5]
            password += next_char
            
            # Print status update
            print(f"[{len(password)}/{target_length}] Found character '{next_char}' at index {index} (Hash: {hex_hash})")

        # Increment and continue search
        index += 1
        
    return password

def solve_door_puzzle():
    """Main function to run the password search."""
    print(f"Door ID: {SECRET_KEY}")
    print(f"Target Hash Prefix: {TARGET_PREFIX}")
    
    final_password = generate_password(SECRET_KEY, PASSWORD_LENGTH)
    return final_password

# --- Main Execution Block ---
if __name__ == "__main__":
    
    final_score = solve_door_puzzle()
    
    print("\n" + "="*50)
    print(f"THE EIGHT-CHARACTER PASSWORD:")
    print(f"SCORE: {final_score}")
    print("="*50)