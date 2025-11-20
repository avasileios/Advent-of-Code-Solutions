import os
import re
from typing import List, Dict, Tuple

# Structure to hold parsed node data
NodeData = Dict[str, any]

def parse_node_data(filepath) -> List[NodeData]:
    """
    Reads the df output and extracts data for each node, excluding header lines.
    
    The expected format per line is:
    /dev/grid/node-x<X>-y<Y>   <Size>T   <Used>T   <Avail>T   <Use>%
    """
    nodes = []
    
    # Regex to capture the node coordinates and the three key numeric values (Size, Used, Avail).
    # We ignore the first few header lines.
    pattern = re.compile(
        r'/dev/grid/node-x(\d+)-y(\d+)\s+'  # Group 1: X, Group 2: Y
        r'(\d+)T\s+'                       # Group 3: Size
        r'(\d+)T\s+'                       # Group 4: Used
        r'(\d+)T'                          # Group 5: Avail
    )
    
    try:
        # Robust path reading
        input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), filepath)
        with open(input_file, 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"Error: Disk usage file not found at '{filepath}'")
        return []

    # Skip header lines (usually 2 lines)
    data_lines = lines[2:]
    
    for line in data_lines:
        match = pattern.match(line)
        if match:
            x = int(match.group(1))
            y = int(match.group(2))
            # Note: Size is not strictly needed for this problem, but we parse it.
            # Used and Avail are the critical metrics.
            size = int(match.group(3))
            used = int(match.group(4))
            avail = int(match.group(5))
            
            nodes.append({
                'id': (x, y),
                'used': used,
                'avail': avail
            })
            
    return nodes

def solve_viability_puzzle(filepath: str) -> int:
    """
    Counts the number of viable pairs (A, B) based on the three viability rules.
    """
    nodes = parse_node_data(filepath)
    if not nodes:
        print("No node data parsed.")
        return 0
        
    viable_pairs_count = 0
    N = len(nodes)
    
    # Brute-force: Check every possible pair (A, B)
    
    # Outer loop: Node A (the sender)
    for i in range(N):
        node_A = nodes[i]
        used_A = node_A['used']
        
        # Rule 1: Node A is not empty (Used > 0)
        if used_A == 0:
            continue
            
        # Inner loop: Node B (the receiver)
        for j in range(N):
            node_B = nodes[j]
            
            # Rule 2: Nodes A and B are not the same (A != B)
            if i == j:
                continue
                
            avail_B = node_B['avail']
            
            # Rule 3: Data on Node A (Used_A) would fit on Node B (Avail_B)
            if used_A <= avail_B:
                viable_pairs_count += 1
                
    return viable_pairs_count

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting viability check using disk usage data from: {os.path.abspath(input_file)}\n")
    
    final_count = solve_viability_puzzle(input_file)
    
    print("\n" + "="*50)
    print("TOTAL NUMBER OF VIABLE PAIRS OF NODES:")
    print(f"SCORE: {final_count}")
    print("="*50)