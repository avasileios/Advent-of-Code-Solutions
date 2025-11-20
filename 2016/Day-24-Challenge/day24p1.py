import os
import re
from collections import deque
from itertools import permutations, combinations # FIXED: combinations added here

# Directions: (dR, dC) for Up, Down, Left, Right
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def parse_map(filepath):
    """
    Reads the map and finds the coordinates of all numbered points of interest (0, 1, 2, ...).
    
    Returns:
        tuple: (grid: list[str], pois: dict[int, tuple[int, int]], ROWS, COLS)
    """
    grid = []
    pois = {}
    
    try:
        # Robust path reading
        input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), filepath)
        with open(input_file, 'r') as f:
            for r, line in enumerate(f):
                clean_line = line.strip()
                if not clean_line: continue
                grid.append(clean_line)
                
                # Find Points of Interest (POIs)
                for c, char in enumerate(clean_line):
                    if char.isdigit():
                        pois[int(char)] = (r, c)

    except FileNotFoundError:
        print(f"Error: Map file not found at '{filepath}'")
        return None, None, 0, 0
    
    if not grid:
        return None, None, 0, 0
    
    ROWS = len(grid)
    COLS = len(grid[0])
    
    return grid, pois, ROWS, COLS

def bfs_shortest_distance(grid, start_pos, end_pos, ROWS, COLS):
    """
    Performs BFS to find the shortest path length between two points.
    """
    queue = deque([(start_pos, 0)]) # (r, c, distance)
    visited = {start_pos}
    
    while queue:
        (r, c), dist = queue.popleft()
        
        if (r, c) == end_pos:
            return dist
            
        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            next_pos = (nr, nc)
            
            # Check bounds and wall condition
            if 0 <= nr < ROWS and 0 <= nc < COLS and \
               grid[nr][nc] != '#' and next_pos not in visited:
                
                visited.add(next_pos)
                queue.append((next_pos, dist + 1))
                
    return float('inf') # Path unreachable

def build_distance_matrix(grid, pois, ROWS, COLS):
    """
    Calculates the shortest path distance between all pairs of POIs.
    
    Returns:
        dict: distance_matrix[(id1, id2)] = distance
    """
    poi_ids = sorted(pois.keys())
    distance_matrix = {}
    
    # We use combinations to ensure we only calculate each pair once (A->B is B->A)
    for id_a, id_b in combinations(poi_ids, 2):
        pos_a = pois[id_a]
        pos_b = pois[id_b]
        
        distance = bfs_shortest_distance(grid, pos_a, pos_b, ROWS, COLS)
        
        # Store bidirectional distance
        distance_matrix[(id_a, id_b)] = distance
        distance_matrix[(id_b, id_a)] = distance
        
    return distance_matrix

def solve_duct_puzzle(filepath):
    """
    Orchestrates the BFS and TSP solution to find the shortest route starting at 0 
    and visiting all others.
    """
    grid, pois, ROWS, COLS = parse_map(filepath)
    if grid is None or len(pois) < 2:
        print("Error: Invalid map or insufficient points of interest.")
        return 0

    # 1. Calculate all pairwise shortest distances
    distance_matrix = build_distance_matrix(grid, pois, ROWS, COLS)
    
    # 2. Setup for TSP
    poi_ids = sorted(pois.keys())
    start_node = 0
    # Destinations are all nodes EXCEPT 0
    destinations = [p for p in poi_ids if p != start_node]
    
    min_total_steps = float('inf')
    
    # 3. Generate all permutations of the destinations
    # We iterate over all paths that start at 0 and visit destinations 1..N
    for path_order in permutations(destinations):
        
        current_route = [start_node] + list(path_order)
        current_cost = 0
        
        # Calculate cost for the route
        for i in range(len(current_route) - 1):
            node_a = current_route[i]
            node_b = current_route[i+1]
            
            # Look up distance (key is sorted for robustness, though either order works here)
            # The matrix stores (small_id, large_id)
            cost = distance_matrix.get((node_a, node_b))
            
            if cost is None:
                # Fallback check (if matrix lookup failed)
                cost = distance_matrix.get((node_b, node_a), float('inf'))
                
            if cost == float('inf'):
                current_cost = float('inf') # Path invalid
                break
                
            current_cost += cost
        
        min_total_steps = min(min_total_steps, current_cost)

    return min_total_steps

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting HVAC duct search (TSP) using map from: {os.path.abspath(input_file)}\n")
    
    final_score = solve_duct_puzzle(input_file)
    
    print("\n" + "="*50)
    print("FEWEST NUMBER OF STEPS REQUIRED TO VISIT EVERY LOCATION:")
    print(f"SCORE: {final_score}")
    print("="*50)