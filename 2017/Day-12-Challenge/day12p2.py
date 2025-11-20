import os
import re
from collections import deque, defaultdict
from typing import Set, Dict, Tuple

# The target program ID for the connected group (for Part 1 reference)
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
    (Part 1 Logic) Performs BFS starting at start_node to find the size of the connected component.
    """
    if start_node not in graph:
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


def find_total_groups(graph: defaultdict[int, set[int]]) -> int:
    """
    (Part 2 Logic) Iterates through all nodes and counts the total number of 
    disjoint connected components (groups).
    """
    if not graph:
        return 0
        
    visited_globally = set()
    total_groups = 0
    
    # Iterate through every single program ID in the graph keys
    all_programs = sorted(graph.keys())
    
    for program_id in all_programs:
        if program_id not in visited_globally:
            # Found the root of a new, unvisited group
            total_groups += 1
            
            # Start BFS to find all members of this new group
            queue = deque([program_id])
            visited_globally.add(program_id)
            
            while queue:
                current_node = queue.popleft()
                
                for neighbor in graph[current_node]:
                    if neighbor not in visited_globally:
                        visited_globally.add(neighbor)
                        queue.append(neighbor)
                        
    return total_groups


def solve_pipe_puzzle(filepath):
    """
    Loads the graph and solves for the size of Group 0 (P1) and the total number of groups (P2).
    """
    graph = parse_pipes(filepath)
    if not graph:
        return 0, 0
        
    group_size_p1 = find_group_size(graph, START_NODE)
    total_groups_p2 = find_total_groups(graph)
    
    return group_size_p1, total_groups_p2

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting pipe network analysis using data from: {os.path.abspath(input_file)}\n")
    
    size_p1, count_p2 = solve_pipe_puzzle(input_file)
    
    print("\n" + "="*50)
    print(f"PART 1: SIZE OF THE GROUP CONTAINING PROGRAM ID {START_NODE}:")
    print(f"SCORE: {size_p1}")
    print("-" * 50)
    print("PART 2: TOTAL NUMBER OF GROUPS:")
    print(f"SCORE: {count_p2}")
    print("="*50)