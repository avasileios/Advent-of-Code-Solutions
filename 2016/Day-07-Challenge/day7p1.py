import os
import re

def parse_ip_parts(ip_address: str) -> tuple[list[str], list[str]]:
    """
    Splits the IP address into supernet (outside brackets) and hypernet (inside brackets) parts.
    """
    # Regex to capture hypernet sequences: [xxx]
    hypernet_pattern = r'\[([a-z]+)\]'
    
    # Extract hypernets
    hypernets = re.findall(hypernet_pattern, ip_address)
    
    # Extract supernets by splitting the string using the hypernets as delimiters
    supernets = re.split(hypernet_pattern, ip_address)
    
    # Note: re.split will return the segments that were between the matches. 
    # Example: abba[mnop]qrst -> [abba, mnop, qrst].
    # Since the hypernet sequences are guaranteed to be in the odd positions (index 1, 3, 5...),
    # the supernets are in the even positions (index 0, 2, 4...).
    
    supernet_parts = [supernets[i] for i in range(0, len(supernets), 2) if supernets[i]]
    
    return supernet_parts, hypernets

def has_abba(s: str) -> bool:
    """
    Checks if a string contains the ABBA pattern (xyyx where x != y).
    """
    N = len(s)
    if N < 4:
        return False
        
    for i in range(N - 3):
        # Check for xyyx pattern: s[i] = s[i+3] AND s[i+1] = s[i+2]
        if s[i] == s[i+3] and s[i+1] == s[i+2]:
            # Check for x != y
            if s[i] != s[i+1]:
                return True
                
    return False

def supports_tls(ip_address: str) -> bool:
    """
    Checks if an IP supports TLS: ABBA in any supernet AND NO ABBA in any hypernet.
    """
    supernets, hypernets = parse_ip_parts(ip_address)
    
    # Condition 1: Check for ABBA in hypernets (must FAIL)
    for hypernet in hypernets:
        if has_abba(hypernet):
            return False # Fails TLS requirement (ABBA found in brackets)
            
    # Condition 2: Check for ABBA in supernets (must PASS)
    for supernet in supernets:
        if has_abba(supernet):
            return True # Supports TLS (ABBA found outside brackets)
            
    return False # No ABBA found outside brackets

def solve_tls_puzzle(filepath):
    """
    Reads the list of IP addresses and counts how many support TLS.
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
        if supports_tls(ip):
            supporting_ips_count += 1
            
    return supporting_ips_count

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting TLS support analysis using data from: {os.path.abspath(input_file)}\n")
    
    final_count = solve_tls_puzzle(input_file)
    
    print("\n" + "="*50)
    print("TOTAL NUMBER OF IPs THAT SUPPORT TLS:")
    print(f"SCORE: {final_count}")
    print("="*50)