import os
import re
from itertools import permutations
import math

def parse_distances(filepath):
    """
    Reads the distances and builds a graph dictionary:
    graph[Location_A][Location_B] = distance
    Also collects the set of all unique locations.
    """
    graph = {}
    locations = set()
    
    try:
        # Robust path reading
        with open(filepath, 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"Error: Instructions file not found at '{filepath}'")
        return None, None
    
    # Regex to capture: Location A to Location B = Distance
    pattern = re.compile(r'(\w+)\s+to\s+(\w+)\s+=\s+(\d+)')
    
    for line in lines:
        match = pattern.match(line)
        if not match:
            continue
            
        loc_a, loc_b, dist_str = match.groups()
        distance = int(dist_str)
        
        # Add locations to the set
        locations.add(loc_a)
        locations.add(loc_b)
        
        # Initialize graph entries if they don't exist
        graph.setdefault(loc_a, {})
        graph.setdefault(loc_b, {})
        
        # Distances are bidirectional
        graph[loc_a][loc_b] = distance
        graph[loc_b][loc_a] = distance
        
    return graph, sorted(list(locations))

def calculate_route_distance(route, graph):
    """
    Calculates the total distance for a given route (list of locations).
    """
    total_distance = 0
    
    # Iterate over pairs of adjacent locations
    for i in range(len(route) - 1):
        loc_a = route[i]
        loc_b = route[i+1]
        
        # Check if the path exists (it should, as the graph is complete)
        if loc_b in graph[loc_a]:
            total_distance += graph[loc_a][loc_b]
        else:
            # Should not happen with valid input, but acts as a safety measure
            return float('inf') 
            
    return total_distance

def solve_shortest_longest_route(filepath):
    """
    Finds both the shortest and longest distances required to visit every location exactly once.
    """
    graph, locations = parse_distances(filepath)
    
    if not graph or not locations:
        print("Error: Could not parse graph or find locations.")
        return 0, 0
        
    min_distance = float('inf')
    max_distance = 0 # Initialize to 0 for maximization
    
    print(f"Total locations to visit: {len(locations)} ({locations})")
    print(f"Total routes to check: {math.factorial(len(locations))}")
    
    # 1. Generate all possible routes (permutations)
    all_routes = permutations(locations)
    
    # 2. Check the distance for each route
    for route in all_routes:
        distance = calculate_route_distance(route, graph)
        
        if distance != float('inf'):
            min_distance = min(min_distance, distance)
            max_distance = max(max_distance, distance)
            
    return min_distance, max_distance

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting route analysis using data from: {os.path.abspath(input_file)}\n")
    
    shortest, longest = solve_shortest_longest_route(input_file)
    
    print("\n" + "="*50)
    print("PART 1: DISTANCE OF THE SHORTEST ROUTE:")
    print(f"SCORE: {shortest}")
    print("-" * 50)
    print("PART 2: DISTANCE OF THE LONGEST ROUTE:")
    print(f"SCORE: {longest}")
    print("="*50)