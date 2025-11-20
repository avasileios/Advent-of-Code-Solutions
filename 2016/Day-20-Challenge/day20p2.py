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
    (Part 1) Finds the lowest-valued IP address that is not blocked.
    """
    ranges = parse_ranges(filepath)
    if not ranges:
        return 0

    merged_blacklist = merge_ranges(ranges)

    current_ip = 0

    for start, end in merged_blacklist:
        
        # Check 1: Gap found before the current blocked range?
        if start > current_ip:
            return current_ip
        
        # Check 2: If the current IP is blocked, jump past the blocked range.
        current_ip = end + 1

        if current_ip > MAX_IP:
            return -1
            
    return current_ip

def solve_allowed_count(filepath: str) -> int:
    """
    (Part 2) Finds the total count of IP addresses that are not blocked.
    """
    ranges = parse_ranges(filepath)
    if not ranges:
        # If blacklist is empty, all IPs are allowed (MAX_IP + 1)
        return MAX_IP + 1

    merged_blacklist = merge_ranges(ranges)

    total_allowed = 0
    current_ip = 0

    # 1. Iterate through the merged blocked ranges
    for start, end in merged_blacklist:
        
        # Calculate the size of the gap before this blocked range
        if start > current_ip:
            # The gap is [current_ip, start - 1]
            gap_size = start - current_ip
            total_allowed += gap_size
        
        # Update current_ip to the address immediately following the blocked range
        # We cap this update at MAX_IP + 1 to stay within the overall boundary.
        current_ip = end + 1
        
        # Stop early if we have processed all possible IPs
        if current_ip > MAX_IP:
            break
            
    # 2. Check the final gap (from the end of the last blocked range to MAX_IP)
    if current_ip <= MAX_IP:
        # The final gap is [current_ip, MAX_IP]
        final_gap_size = MAX_IP - current_ip + 1
        total_allowed += final_gap_size

    return total_allowed

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting IP unblocker analysis (Max IP: {MAX_IP}) using data from: {os.path.abspath(input_file)}\n")
    
    lowest_unblocked_ip = solve_ip_unblocker(input_file)
    total_allowed_ips = solve_allowed_count(input_file)
    
    print("\n" + "="*50)
    print("PART 1: LOWEST-VALUED IP ADDRESS THAT IS NOT BLOCKED:")
    print(f"SCORE: {lowest_unblocked_ip}")
    print("-" * 50)
    print("PART 2: TOTAL NUMBER OF IP ADDRESSES THAT ARE ALLOWED:")
    print(f"SCORE: {total_allowed_ips}")
    print("="*50)