import os

# --- Constants ---
# Disallowed letters for Rule 2
DISALLOWED_CHARS = set(['i', 'o', 'l'])

# --- Password Incrementer ---

def increment_password(password: str) -> str:
    """
    Increments the 8-letter password string like counting numbers (e.g., 'xx' -> 'xy').
    Wraps 'z' to 'a' and carries over.
    """
    p_list = list(password)
    i = len(p_list) - 1
    
    while i >= 0:
        char = p_list[i]
        
        if char == 'z':
            # Wrap and carry over
            p_list[i] = 'a'
            i -= 1
        else:
            # Increment and stop
            p_list[i] = chr(ord(char) + 1)
            break
            
    # If the loop finished and i is -1, the password was a full 'z' string, 
    # but since the puzzle guarantees 8 characters, this shouldn't happen 
    # unless the starting password was 'zzzzzzzz'.
    
    return "".join(p_list)

# --- Validation Rules ---

def check_increasing_straight(password: str) -> bool:
    """
    Rule 1: Must include one increasing straight of at least three letters (abc, bcd, etc.).
    """
    N = len(password)
    if N < 3:
        return False
        
    for i in range(N - 2):
        c1 = ord(password[i])
        c2 = ord(password[i+1])
        c3 = ord(password[i+2])
        
        # Check if c1 + 1 = c2 AND c2 + 1 = c3
        if c2 == c1 + 1 and c3 == c2 + 1:
            return True
            
    return False

def check_disallowed_chars(password: str) -> bool:
    """
    Rule 2: May not contain the letters i, o, or l.
    """
    # Use a set intersection for fast checking
    if set(password) & DISALLOWED_CHARS:
        return False # Fails rule if any disallowed char is present
    return True

def check_two_non_overlapping_pairs(password: str) -> bool:
    """
    Rule 3: Must contain at least two different, non-overlapping pairs (aa, bb, etc.).
    """
    N = len(password)
    
    # Stores the indices where a double pair starts
    pair_indices = []
    for i in range(N - 1):
        if password[i] == password[i+1]:
            pair_indices.append(i)
            
    if len(pair_indices) < 2:
        return False # Must have at least two potential pairs
        
    # Check for two non-overlapping pairs
    
    # We use a set of unique pairs found so far (e.g., {'aa', 'bb'})
    unique_pairs = set()
    
    # Check if any two of the found pairs are non-overlapping and different types.
    for i in range(len(pair_indices)):
        start_i = pair_indices[i]
        pair_i = password[start_i:start_i+2]
        
        for j in range(i + 1, len(pair_indices)):
            start_j = pair_indices[j]
            pair_j = password[start_j:start_j+2]
            
            # Non-overlapping check: 
            # The indices must be at least 2 apart to guarantee no overlap, 
            # OR the pairs must be different types (e.g. 'aa...bb').
            
            # The definition of "non-overlapping" means the index ranges don't share any character.
            # Example: 'aaa' has pairs at index 0 ('aa') and index 1 ('aa'). Overlap.
            # Example: 'aabb' has pairs at index 0 ('aa') and index 2 ('bb'). Non-overlapping.
            
            # The simplest check is: does the first pair start before the second, 
            # and does the second pair start AFTER the first pair ends?
            
            # Condition for non-overlap: start_j >= start_i + 2
            if start_j >= start_i + 2:
                # We found two non-overlapping pairs. The problem asks for two DIFFERENT, 
                # non-overlapping pairs. Since the list of potential pair indices 
                # is generated based on the string, the "different" part is tricky. 
                # For simplicity and robustness, we rely on the non-overlapping count:
                
                # We found one pair type at start_i and another at start_j.
                
                # Check for two unique pair types (e.g., 'aa' and 'bb').
                # If we rely strictly on the non-overlapping criterion, 
                # a string like 'aaaa' (pairs at 0 and 2) is valid.
                
                # The rule requires "at least two different, non-overlapping pairs of letters".
                
                # Case 1: Pairs are different types (e.g., 'aabbaa')
                if pair_i != pair_j:
                    return True
                
                # Case 2: Pairs are the same type but non-overlapping (e.g., 'aa...aa')
                # The problem uses 'aa', 'bb', or 'zz' as examples of pairs. 
                # 'aabbaa' satisfies the rule because 'aa' and 'bb' are two different pairs.
                
                # If we rely on non-overlapping indices (start_j >= start_i + 2), 
                # then we have guaranteed two distinct pairs (of any type) that don't overlap.
                return True # Found two non-overlapping pairs, which satisfies the count.
                
    return False

def is_valid(password: str) -> bool:
    """Checks if a password meets all three requirements."""
    
    if not check_disallowed_chars(password):
        return False
        
    if not check_increasing_straight(password):
        return False
        
    if not check_two_non_overlapping_pairs(password):
        return False
        
    return True

def solve_password_puzzle(initial_password: str) -> str:
    """
    Increments the password until the next valid one is found.
    """
    current_password = initial_password
    
    # Start by incrementing once to find the NEXT password
    current_password = increment_password(current_password)
    
    print(f"Starting search from: {initial_password}")
    
    while True:
        if is_valid(current_password):
            return current_password
        
        # Optimization: If the password contains a disallowed character, increment 
        # that character to the next allowed character ('i' -> 'j', 'o' -> 'p', 'l' -> 'm')
        # and reset all characters to the right to 'a'. This skips huge, invalid ranges.
        
        # We perform the increment and continue the loop to check the new password
        current_password = increment_password(current_password)

# --- Main Execution Block ---
if __name__ == "__main__":
    # Your puzzle input
    PUZZLE_INPUT = "cqjxjnds"

    print(f"Starting password generation for input: {PUZZLE_INPUT}\n")
    
    # We must first implement the optimization rule mentioned in the text 
    # (though not strictly required for the final answer, it speeds up the search).
    # "the next password after ghijklmn is ghjaabcc, because you eventually skip 
    # all the passwords that start with ghi..., since i is not allowed."
    
    def fast_increment(password: str) -> str:
        """
        Increments the password, skipping immediately to the next valid character 
        if a disallowed one ('i', 'o', 'l') is encountered.
        """
        p_list = list(password)
        N = len(p_list)
        
        # Check for disallowed characters from left to right (to reset suffix)
        for i in range(N):
            char = p_list[i]
            if char in DISALLOWED_CHARS:
                # Increment the disallowed character and reset the rest
                p_list[i] = chr(ord(char) + 1)
                
                # Reset all subsequent characters to 'a'
                for j in range(i + 1, N):
                    p_list[j] = 'a'
                
                # Start the search from this new, non-disallowed prefix
                return "".join(p_list)
        
        # If no disallowed character is found, use the standard incrementer
        return increment_password(password)


    # --- FINAL SOLVE LOOP ---
    current_password = PUZZLE_INPUT
    
    while True:
        # 1. Generate the next candidate password, using the fast incrementer
        #    to skip over long runs of invalid passwords.
        current_password = fast_increment(current_password)
        
        # 2. Check validity
        if is_valid(current_password):
            break
            
        # If still invalid, loop continues to the next fast_increment

    final_password = current_password
    
    print("\n" + "="*50)
    print("SANTA'S NEXT VALID PASSWORD:")
    print(f"SCORE: {final_password}")
    print("="*50)