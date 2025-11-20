import os
from collections import defaultdict

def parse_components(filepath):
    """
    Reads the component list and builds an adjacency map.
    Returns:
        components: A list of tuples (port1, port2, id).
        adjacency: A dict mapping a port number to a list of (other_port, component_id).
    """
    adjacency = defaultdict(list)
    components_list = []
    
    try:
        # Robust path reading
        input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), filepath)
        with open(input_file, 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"Error: Input file not found at '{filepath}'")
        return [], {}

    for i, line in enumerate(lines):
        try:
            a, b = map(int, line.split('/'))
            # Store the component with a unique ID (i)
            components_list.append((a, b, i))
            
            # Add to adjacency map for both ports
            adjacency[a].append((b, i))
            adjacency[b].append((a, i))
        except ValueError:
            continue
            
    return components_list, adjacency

def find_strongest_bridge(adjacency):
    """
    Performs DFS to find the bridge with the highest strength.
    """
    max_strength = 0
    
    # Stack stores: (current_port, current_strength, set_of_used_component_ids)
    # We start at port 0, strength 0, and no components used.
    stack = [(0, 0, set())]
    
    while stack:
        current_port, current_strength, used = stack.pop()
        
        # Update global max if this path is stronger
        if current_strength > max_strength:
            max_strength = current_strength
        
        # Try to extend the bridge
        # Look at all components connected to the current port
        if current_port in adjacency:
            for next_port, comp_id in adjacency[current_port]:
                if comp_id not in used:
                    # Calculate strength of this component (current_port + next_port)
                    component_strength = current_port + next_port
                    
                    # Create new used set
                    new_used = used.copy()
                    new_used.add(comp_id)
                    
                    # Add next state to stack
                    stack.append((next_port, current_strength + component_strength, new_used))
                    
    return max_strength

def solve_bridge_puzzle(filepath):
    """
    Main solver function.
    """
    _, adjacency = parse_components(filepath)
    
    if not adjacency:
        return 0
        
    print(f"Components loaded. Starting search for strongest bridge...")
    strength = find_strongest_bridge(adjacency)
    
    return strength

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction
    input_file = "input.txt"
    
    print(f"Starting Magnetic Bridge Builder analysis using data from: {os.path.abspath(input_file)}\n")
    
    final_strength = solve_bridge_puzzle(input_file)
    
    print("\n" + "="*50)
    print("STRENGTH OF THE STRONGEST BRIDGE:")
    print(f"SCORE: {final_strength}")
    print("="*50)