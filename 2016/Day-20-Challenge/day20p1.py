import os
import re
from typing import List, Tuple

# The maximum possible IP address (2^32 - 1)
MAX_IP = 4294967295 

def parse_ranges(filepath) -> List[Tuple[int, int]]:
    """
    Reads the blacklist and parses inclusive ranges (start, end).
    """
    ranges = []
    try:
        # Robust path reading
        input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), filepath)
        with open(input_file, 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"Error: Blacklist file not found at '{filepath}'")
        return []

    for line in lines:
        try:
            start, end = map(int, line.split('-'))
            ranges.append((start, end))
        except ValueError:
            continue
            
    return ranges

def merge_ranges(ranges: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """
    Sorts the ranges and merges all overlapping and contiguous ranges.
    """
    if not ranges:
        return []

    # 1. Sort by the start value
    ranges.sort(key=lambda x: x[0])

    merged = []
    current_start, current_end = ranges[0]

    # 2. Iterate and merge
    for next_start, next_end in ranges[1:]:
        # If the next range overlaps or is contiguous (end + 1 == next_start)
        if next_start <= current_end + 1:
            # Merge: Extend the current end if the next end is larger
            current_end = max(current_end, next_end)
        else:
            # No overlap/contiguity: finalize the current merged range and start a new one
            merged.append((current_start, current_end))
            current_start, current_end = next_start, next_end

    # 3. Add the last merged range
    merged.append((current_start, current_end))

    return merged

def solve_ip_unblocker(filepath: str) -> int:
    """
    Finds the lowest-valued IP address that is not blocked.
    """
    ranges = parse_ranges(filepath)
    if not ranges:
        # If the blacklist is empty, the lowest IP (0) is allowed.
        return 0

    merged_blacklist = merge_ranges(ranges)

    # 1. Start searching from the lowest possible IP (0)
    current_ip = 0

    # 2. Iterate through the merged blacklist
    for start, end in merged_blacklist:
        
        # Check 1: Gap found before the current blocked range?
        # If the start of the blocked range is greater than the current IP, 
        # then current_ip is the first allowed address.
        if start > current_ip:
            return current_ip
        
        # Check 2: If the current IP is blocked, jump past the blocked range.
        # This handles the case where current_ip is inside or equal to the blocked range start.
        # We jump to the address immediately following the end of the blocked range.
        current_ip = end + 1

        # Safety check against exceeding the maximum IP limit
        if current_ip > MAX_IP:
            return -1 # Should not happen if a solution exists
            
    # 3. If the loop completes, the lowest unblocked IP is the number immediately 
    # following the end of the last merged range.
    return current_ip

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting IP unblocker analysis (Max IP: {MAX_IP}) using data from: {os.path.abspath(input_file)}\n")
    
    lowest_unblocked_ip = solve_ip_unblocker(input_file)
    
    print("\n" + "="*50)
    print("LOWEST-VALUED IP ADDRESS THAT IS NOT BLOCKED:")
    print(f"SCORE: {lowest_unblocked_ip}")
    print("="*50)