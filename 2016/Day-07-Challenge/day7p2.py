import os
import re
from itertools import combinations

def parse_ip_parts(ip_address: str) -> tuple[list[str], list[str]]:
    """
    Splits the IP address into supernet (outside brackets) and hypernet (inside brackets) parts.
    (Used by both Part 1 and Part 2)
    """
    # Regex to capture hypernet sequences: [xxx]
    hypernet_pattern = r'\[([a-z]+)\]'
    
    # Extract hypernets
    hypernets = re.findall(hypernet_pattern, ip_address)
    
    # Extract supernets by splitting the string using the hypernets as delimiters
    supernets = re.split(hypernet_pattern, ip_address)
    
    # Supernets are in the even positions (index 0, 2, 4...)
    supernet_parts = [supernets[i] for i in range(0, len(supernets), 2) if supernets[i]]
    
    return supernet_parts, hypernets

# --- Part 1 Logic (Retained for completeness) ---

def has_abba(s: str) -> bool:
    """Checks if a string contains the ABBA pattern (xyyx where x != y)."""
    N = len(s)
    if N < 4: return False
    for i in range(N - 3):
        if s[i] == s[i+3] and s[i+1] == s[i+2] and s[i] != s[i+1]:
            return True
    return False

def supports_tls(ip_address: str) -> bool:
    """Checks if an IP supports TLS: ABBA in any supernet AND NO ABBA in any hypernet."""
    supernets, hypernets = parse_ip_parts(ip_address)
    for hypernet in hypernets:
        if has_abba(hypernet): return False
    for supernet in supernets:
        if has_abba(supernet): return True
    return False

# --- Part 2 Logic: SSL (ABA/BAB) ---

def find_abas(s: str) -> set[tuple[str, str]]:
    """
    Finds all unique ABA patterns (xyx where x != y) in a string.
    Returns a set of (x, y) tuples.
    """
    abas = set()
    N = len(s)
    if N < 3:
        return abas
        
    for i in range(N - 2):
        # Check for ABA pattern: s[i] = s[i+2]
        if s[i] == s[i+2]:
            x = s[i]
            y = s[i+1]
            # Check for x != y
            if x != y:
                abas.add((x, y))
                
    return abas

def supports_ssl(ip_address: str) -> bool:
    """
    Checks if an IP supports SSL: ABA in supernet AND corresponding BAB in hypernet.
    """
    supernets, hypernets = parse_ip_parts(ip_address)
    
    all_abas = set()
    
    # 1. Find all unique ABA patterns in all supernet sequences
    for supernet in supernets:
        all_abas.update(find_abas(supernet))
        
    if not all_abas:
        return False # No ABA found, impossible to support SSL

    # 2. Check if the corresponding BAB exists in any hypernet sequence
    for x, y in all_abas:
        # Corresponding BAB pattern is yxy
        bab_pattern = y + x + y
        
        # Check all hypernets for the BAB pattern
        for hypernet in hypernets:
            if bab_pattern in hypernet:
                # Found a matching ABA/BAB pair
                return True
                
    return False

def solve_ssl_puzzle(filepath):
    """
    Reads the list of IP addresses and counts how many support SSL.
    """
    supporting_ips_count = 0
    
    try:
        # Robust path reading
        input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), filepath)
        with open(input_file, 'r') as f:
            ip_addresses = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"Error: IP address file not found at '{filepath}'")
        return 0
        
    for ip in ip_addresses:
        if supports_ssl(ip):
            supporting_ips_count += 1
            
    return supporting_ips_count

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting SSL support analysis (Part 2) using data from: {os.path.abspath(input_file)}\n")
    
    final_count = solve_ssl_puzzle(input_file)
    
    print("\n" + "="*50)
    print("PART TWO: TOTAL NUMBER OF IPs THAT SUPPORT SSL:")
    print(f"SCORE: {final_count}")
    print("="*50)