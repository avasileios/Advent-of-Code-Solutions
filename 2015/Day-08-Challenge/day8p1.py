import os

def count_memory_chars(s):
    """
    Count the actual memory characters in a string literal.
    The string s includes the surrounding quotes.
    """
    # Remove the outer quotes
    if len(s) < 2 or s[0] != '"' or s[-1] != '"':
        return 0
    
    inner = s[1:-1]
    memory_count = 0
    i = 0
    
    while i < len(inner):
        if inner[i] == '\\' and i + 1 < len(inner):
            next_char = inner[i + 1]
            if next_char == '\\' or next_char == '"':
                # Escape sequences \\ or \" represent 1 character
                memory_count += 1
                i += 2
            elif next_char == 'x' and i + 3 < len(inner):
                # Hex escape \xHH represents 1 character
                memory_count += 1
                i += 4
            else:
                # Not a valid escape, count as-is
                memory_count += 1
                i += 1
        else:
            # Regular character
            memory_count += 1
            i += 1
    
    return memory_count

def count_encoded_chars(s):
    """
    Count characters needed to encode a string literal.
    We need to add outer quotes and escape internal quotes and backslashes.
    """
    # Start with 2 for the new outer quotes
    encoded = 2
    
    # Each character in the original string
    for char in s:
        if char == '"' or char == '\\':
            # These need to be escaped, so they become 2 characters
            encoded += 2
        else:
            # Regular characters stay as 1
            encoded += 1
    
    return encoded

def solve_puzzle(filepath):
    """
    Solve both parts of the puzzle.
    """
    try:
        with open(filepath, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: Input file not found at '{filepath}'")
        return 0, 0
    
    total_code_chars = 0
    total_memory_chars = 0
    total_encoded_chars = 0
    
    for line in lines:
        code_chars = len(line)
        memory_chars = count_memory_chars(line)
        encoded_chars = count_encoded_chars(line)
        
        total_code_chars += code_chars
        total_memory_chars += memory_chars
        total_encoded_chars += encoded_chars
    
    part1 = total_code_chars - total_memory_chars
    part2 = total_encoded_chars - total_code_chars
    
    return part1, part2

# --- Main Execution ---
if __name__ == "__main__":
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Reading from: {os.path.abspath(input_file)}\n")
    
    # Test with the examples first
    test_cases = ['""', '"abc"', r'"aaa\"aaa"', r'"\x27"']
    print("Testing with examples:")
    for test in test_cases:
        code = len(test)
        memory = count_memory_chars(test)
        print(f"{test:20} → code: {code}, memory: {memory}")
    print()
    
    part1, part2 = solve_puzzle(input_file)
    
    print("="*50)
    print("PART 1: Code Chars - Memory Chars")
    print(f"Answer: {part1}")
    print("-"*50)
    #print("PART 2: Encoded Chars - Code Chars")
    #print(f"Part 2 Answer: {part2}")
    print("="*50)