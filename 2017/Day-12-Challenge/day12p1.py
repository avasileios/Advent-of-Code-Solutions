import os
import re
from collections import deque, defaultdict

# The target program ID for the connected group
START_NODE = 0

def parse_pipes(filepath) -> defaultdict[int, set[int]]:
    """
    Reads the pipe configuration and builds an adjacency list (graph).
    
    Returns:
        defaultdict: {program_id: {neighbor_id, ...}}
    """
    graph = defaultdict(set)
    
    try:
        # Robust path reading
        input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), filepath)
        with open(input_file, 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"Error: Pipe file not found at '{filepath}'")
        return graph

    # Regex to capture: PROGRAM_ID <-> NEIGHBOR1, NEIGHBOR2, ...
    pattern = re.compile(r'(\d+)\s+<->\s+(.*)')

    for line in lines:
        match = pattern.match(line)
        if not match:
            continue
            
        source_id = int(match.group(1))
        targets_str = match.group(2)
        
        # Parse comma-separated target IDs
        targets = [int(t.strip()) for t in targets_str.split(',') if t.strip()]
        
        for target_id in targets:
            # Pipes are bidirectional
            graph[source_id].add(target_id)
            graph[target_id].add(source_id)
            
    return graph

def find_group_size(graph: defaultdict[int, set[int]], start_node: int) -> int:
    """
    Performs BFS starting at start_node to find the size of the connected component.
    """
    if start_node not in graph:
        # If program 0 is not in the graph (i.e., input is empty or only references other nodes)
        return 0
        
    queue = deque([start_node])
    visited = {start_node}
    
    while queue:
        current_node = queue.popleft()
        
        # Check all direct neighbors
        for neighbor in graph[current_node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                
    return len(visited)

def solve_pipe_puzzle(filepath):
    """
    Loads the graph and solves for the size of the group containing START_NODE.
    """
    graph = parse_pipes(filepath)
    if not graph:
        return 0
        
    group_size = find_group_size(graph, START_NODE)
    
    return group_size

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting pipe network analysis for group containing Program ID {START_NODE} using data from: {os.path.abspath(input_file)}\n")
    
    final_size = solve_pipe_puzzle(input_file)
    
    print("\n" + "="*50)
    print(f"TOTAL NUMBER OF PROGRAMS IN THE GROUP CONTAINING PROGRAM ID {START_NODE}:")
    print(f"SCORE: {final_size}")
    print("="*50)