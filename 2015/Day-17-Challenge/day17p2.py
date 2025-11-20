import os

# The total amount of eggnog to store
TARGET_LITERS = 150

def parse_containers(filepath):
    """
    Reads container capacities from the file, one per line.
    
    Returns:
        list: A list of integer container capacities.
    """
    containers = []
    
    try:
        # Robust path reading
        with open(filepath, 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"Error: Container file not found at '{filepath}'")
        return []
    
    for line in lines:
        try:
            containers.append(int(line))
        except ValueError:
            print(f"Warning: Skipping non-integer line: {line}")
            continue
            
    return containers

def solve_container_combinations(filepath):
    """
    Uses recursive DFS to find:
    1. The total number of combinations that sum exactly to TARGET_LITERS (P1).
    2. The number of combinations that use the minimum number of containers (P2).
    """
    containers = parse_containers(filepath)
    if not containers:
        print("No container data loaded.")
        return 0, 0

    N = len(containers)
    
    # --- CRITICAL OPTIMIZATION: Sort containers. ---
    # Sorting allows DFS to find the minimum number of containers (min_containers) 
    # much faster, enabling aggressive pruning of subsequent branches.
    containers.sort(reverse=True) 
    
    # Part 1: Total count of all valid combinations
    total_combinations_p1 = 0
    
    # Part 2: Tracking for the minimum number of containers
    min_containers = float('inf')
    count_of_min_containers_p2 = 0

    def find_combinations(index, current_sum, containers_used):
        nonlocal total_combinations_p1, min_containers, count_of_min_containers_p2
        
        # Optimization 1: Prune if already using too many containers
        if containers_used > min_containers:
            return
            
        # Optimization 2: Prune if the remaining sum is impossible to reach (Target exceeded)
        if current_sum > TARGET_LITERS:
            return
        
        # Base Case 1: Target reached
        if current_sum == TARGET_LITERS:
            total_combinations_p1 += 1
            
            # --- Part 2 Logic: Update Minimums ---
            if containers_used < min_containers:
                # Found a NEW minimum container count
                min_containers = containers_used
                count_of_min_containers_p2 = 1
            elif containers_used == min_containers:
                # Found another way to achieve the current minimum
                count_of_min_containers_p2 += 1
            
            return
            
        # Base Case 2: End of list reached
        if index == N:
            return

        # Recursive Step: Iterate through the remaining containers starting from 'index'
        for i in range(index, N):
            
            # Action: Include the container at index i
            # Pass i + 1 to prevent reuse of the same physical container
            find_combinations(i + 1, 
                              current_sum + containers[i], 
                              containers_used + 1)

    # Start the DFS: index 0, sum 0, 0 containers used
    find_combinations(0, 0, 0)
    
    return total_combinations_p1, count_of_min_containers_p2

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting eggnog combination analysis for {TARGET_LITERS} liters using data from: {os.path.abspath(input_file)}\n")
    
    total_combinations, min_ways = solve_container_combinations(input_file)
    
    print("\n" + "="*50)
    print(f"PART 1: TOTAL NUMBER OF COMBINATIONS THAT FIT EXACTLY {TARGET_LITERS} LITERS:")
    print(f"SCORE: {total_combinations}")
    print("-" * 50)
    print(f"PART 2: NUMBER OF WAYS TO ACHIEVE THE MINIMUM CONTAINER COUNT:")
    print(f"SCORE: {min_ways}")
    print("="*50)