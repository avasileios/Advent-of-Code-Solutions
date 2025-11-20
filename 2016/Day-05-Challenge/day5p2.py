import hashlib
import os

# Your puzzle input
SECRET_KEY = "ffykfhsq"
TARGET_PREFIX = "00000"
PASSWORD_LENGTH = 8

def generate_password_part_two(secret_key: str, target_length: int) -> str:
    """
    Brute-forces indices starting at 0 to fill the password array based on 
    hash characters at indices 5 (position) and 6 (character).
    """
    # Initialize password array with placeholders
    password_array = ['_'] * target_length 
    index = 0
    chars_found = 0
    
    print(f"Starting password generation for {target_length} positions...")
    
    while chars_found < target_length:
        input_string = secret_key + str(index)
        
        # 1. Calculate MD5 hash
        hash_object = hashlib.md5(input_string.encode('utf-8'))
        hex_hash = hash_object.hexdigest()
        
        if hex_hash.startswith(TARGET_PREFIX):
            # Check length to ensure we can safely read indices 5 and 6
            if len(hex_hash) >= 7:
                
                position_char = hex_hash[5]
                value_char = hex_hash[6]
                
                # 2. Validate Position (index 5 must be a digit 0-7)
                if position_char.isdigit():
                    pos = int(position_char)
                    
                    if 0 <= pos < target_length:
                        # 3. Check if position is empty
                        if password_array[pos] == '_':
                            
                            # Insert the character
                            password_array[pos] = value_char
                            chars_found += 1
                            
                            # Print status update
                            print(f"[{chars_found}/{target_length}] Inserted '{value_char}' at position {pos}. Password: {''.join(password_array)}")

        # Increment and continue search
        index += 1
        
    return "".join(password_array)

def solve_door_puzzle():
    """Main function to run the password search for Part Two."""
    print(f"Door ID: {SECRET_KEY}")
    print(f"Target Hash Prefix: {TARGET_PREFIX}")
    
    final_password = generate_password_part_two(SECRET_KEY, PASSWORD_LENGTH)
    return final_password

# --- Main Execution Block ---
if __name__ == "__main__":
    
    final_score = solve_door_puzzle()
    
    print("\n" + "="*50)
    print(f"THE EIGHT-CHARACTER PASSWORD (Part Two):")
    print(f"SCORE: {final_score}")
    print("="*50)